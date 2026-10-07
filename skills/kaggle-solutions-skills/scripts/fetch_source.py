# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Read source text into a local cache; never execute downloaded content."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


CONTENT_NORMALIZATION = "utf-8-lf"


def normalized_content_bytes(body):
    """Encode text after canonicalizing line endings, without other changes."""
    if not isinstance(body, str):
        raise TypeError("Source body must be text")
    return body.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def kaggle_token():
    token = os.environ.get("KAGGLE_API_TOKEN", "").strip()
    path = Path.home() / ".kaggle" / "access_token"
    if not token and path.is_file():
        token = path.read_text(encoding="utf-8").strip()
    if not token:
        raise ValueError("Kaggle web reads need an API token in KAGGLE_API_TOKEN or ~/.kaggle/access_token; legacy/OAuth-only credentials are not supported by this adapter.")
    return token


class KaggleReader:
    """Optional, version-sensitive Kaggle internal read API adapter."""
    def __enter__(self):
        import httpx
        self.client = httpx.Client(timeout=30, follow_redirects=False,
                                   headers={"Authorization": "Bearer " + kaggle_token()})
        response = self.client.get("https://www.kaggle.com")
        if response.status_code != 200:
            self.client.close()
            raise ValueError(f"Kaggle session seed returned HTTP {response.status_code}")
        self.xsrf = self.client.cookies.get("XSRF-TOKEN", "")
        if not self.xsrf:
            self.client.close()
            raise ValueError("Kaggle session did not supply XSRF; use browser/MCP/manual source export.")
        return self

    def __exit__(self, *args):
        self.client.close()

    def read(self, service, payload):
        # Only known read endpoints; no arbitrary service names from source text.
        allowed = {"discussions.DiscussionsService/GetForumTopicById",
                   "competitions.CompetitionService/GetCompetition",
                   "competitions.LeaderboardService/GetLeaderboard"}
        if service not in allowed:
            raise ValueError("Unsupported read endpoint")
        for attempt in range(3):
            response = self.client.post("https://www.kaggle.com/api/i/" + service,
                                        headers={"X-XSRF-TOKEN": self.xsrf}, json=payload)
            if response.status_code == 200:
                try:
                    value = response.json()
                except ValueError:
                    raise ValueError("Kaggle returned a non-JSON body; possible login/challenge page") from None
                if not isinstance(value, dict):
                    raise ValueError("Kaggle response schema changed")
                return value
            if response.status_code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise ValueError(f"Kaggle read returned HTTP {response.status_code}; response body not logged")
            time.sleep(2 ** attempt)
        raise ValueError("Read retries exhausted")


def extract_topic(data):
    topic = data.get("forumTopic") or {}
    writeup = topic.get("writeUp") or {}
    body = (writeup.get("message") or {}).get("rawMarkdown") or ""
    if not isinstance(body, str) or not body.strip():
        raise ValueError("Topic has no writeUp.message.rawMarkdown body; comments/title alone are not a retrieved solution. Try browser/MCP/manual export.")
    return body.strip(), {
        "title": writeup.get("title") or topic.get("name"),
        "author": topic.get("authorUserName") or topic.get("authorUserDisplayName"),
        "topic_id": topic.get("id"), "source_posted_at": topic.get("postDate"),
    }


def fetch_kaggle(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ("www.kaggle.com", "kaggle.com"):
        raise ValueError("Expected an HTTPS Kaggle URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Use the original-post URL without credentials/query/fragment; comment fragments require a separate browser/MCP read")
    topic_match = re.fullmatch(r"/(?:c|competitions)/([^/]+)/discussion/(\d+)/?", parsed.path)
    writeup_match = re.fullmatch(r"/(?:c|competitions)/([^/]+)/writeups/([^/]+)/?", parsed.path)
    if not topic_match and not writeup_match:
        raise ValueError("Supported sources: competition discussion/<id> or writeups/<slug>")
    with KaggleReader() as client:
        if topic_match:
            competition, topic_id = topic_match.groups()
            topic_id = int(topic_id)
        else:
            competition, slug = writeup_match.groups()
            info = client.read("competitions.CompetitionService/GetCompetition", {"competitionName": competition})
            competition_id = info.get("id") or (info.get("competition") or {}).get("id")
            if not competition_id:
                raise ValueError("Could not resolve competition ID")
            board = client.read("competitions.LeaderboardService/GetLeaderboard", {"competitionId": competition_id})
            topic_id = next((team.get("writeUpForumTopicId") for team in board.get("teams", [])
                             if (team.get("solutionWriteUpUrl") or "").rstrip("/").endswith("/" + slug)
                             and team.get("writeUpForumTopicId")), None)
            if not topic_id:
                raise ValueError("Writeup not present in this leaderboard response; not evidence that it was deleted. Use browser/MCP/manual export.")
        topic_data = client.read("discussions.DiscussionsService/GetForumTopicById",
                                 {"forumTopicId": topic_id, "includeComments": False})
        try:
            body, metadata = extract_topic(topic_data)
            metadata["content_format"] = "markdown"
        except ValueError:
            # Legacy forum posts need the public SDK messages API. Match the original
            # message ID explicitly; never substitute a highly voted comment.
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            messages = api.competition_list_topic_messages(competition, topic_id, page_size=1).messages or []
            topic = topic_data.get("forumTopic") or {}
            original = next((message for message in messages if message.id == topic.get("firstMessageId")), None)
            body = getattr(original, "content", "") if original is not None else ""
            if not isinstance(body, str) or not body.strip():
                raise ValueError("Original topic body unavailable; use browser/MCP/manual export.") from None
            metadata = {"title": topic.get("name"), "author": topic.get("authorUserName"),
                        "topic_id": topic_id, "source_posted_at": topic.get("postDate"),
                        "content_format": "html", "retrieval_method": "kaggle-sdk-original-message"}
    metadata.update(competition=competition)
    metadata.setdefault("retrieval_method", "kaggle-internal-read-api")
    return body, metadata


def fetch_github(url):
    import urllib.request
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "raw.githubusercontent.com":
        raise ValueError("Use raw.githubusercontent.com/<owner>/<repo>/<40-char-commit>/<path> for GitHub source text")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Use a pinned raw URL without credentials/query/fragment")
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 4 or not re.fullmatch(r"[0-9a-f]{40}", parts[2]):
        raise ValueError("GitHub source URLs must pin a 40-character commit SHA")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "kaggle-solutions-skills/0.1"}), timeout=30) as response:
        raw = response.read(5_000_001)
    if len(raw) > 5_000_000:
        raise ValueError("Source exceeds 5 MB text-cache limit; fetch selected files instead")
    body = raw.decode("utf-8")
    return body, {"title": "/".join(parts[3:]), "author": parts[0], "source_commit": parts[2],
                  "retrieval_method": "github-pinned-raw"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--cache", type=Path, default=Path("cache/sources"))
    args = parser.parse_args()
    metadata = {"url": args.url, "retrieved_at": utc_now(), "status": "unavailable", "evidence_level": "linked_unread"}
    cache_key = hashlib.sha256(args.url.encode()).hexdigest()[:20]
    args.cache.mkdir(parents=True, exist_ok=True)
    out = args.cache / cache_key
    try:
        hostname = urlparse(args.url).hostname
        body, details = fetch_kaggle(args.url) if hostname in ("www.kaggle.com", "kaggle.com") else fetch_github(args.url)
        if not body.strip():
            raise ValueError("Empty source text")
        cached_bytes = body.encode("utf-8")
        metadata.update(details, status="retrieved", evidence_level="source_retrieved_unreviewed",
                        content_sha256=hashlib.sha256(normalized_content_bytes(body)).hexdigest(),
                        content_normalization=CONTENT_NORMALIZATION,
                        cached_bytes_sha256=hashlib.sha256(cached_bytes).hexdigest(),
                        content_file=out.name + ".md")
        # Avoid platform newline translation (and CRCRLF corruption on Windows).
        out.with_suffix(".md").write_bytes(cached_bytes)
    except Exception as exc:
        # Do not print exception text from HTTP/auth libraries; it can contain headers.
        metadata["error"] = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        out.with_suffix(".json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(metadata, ensure_ascii=True))
        return 1
    out.with_suffix(".json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
