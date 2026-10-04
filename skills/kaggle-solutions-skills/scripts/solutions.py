# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
"""Versioned Kaggle solution archive, lexical retrieval and curated evidence cards."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen

SKILL = Path(__file__).resolve().parents[1]
DATA = SKILL / "assets" / "knowledge"
REPO = "faridrashidi/kaggle-solutions"
MODALITIES = ("tabular", "time-series", "vision", "text", "audio", "recommender", "simulation", "optimization", "unknown")
ALIASES = {
    "表格": "tabular", "信用风险": "default credit", "金融": "credit default",
    "时间序列": "forecasting time series", "时序": "forecasting time series",
    "销量": "sales forecasting", "预测": "prediction", "音频": "audio sound birdclef",
    "鸟鸣": "birdclef", "图像": "image vision", "医疗": "medical rsna hms",
    "医学影像": "rsna medical image", "文本": "text language writing",
    "推荐": "recommender recommendation", "智能体": "agent simulation lux",
    "仿真": "simulation", "伪标签": "pseudo labeling", "蒸馏": "distillation",
    "集成": "ensemble", "验证": "validation", "分组": "group",
    "检索": "retrieval", "排序": "ranking", "优化": "optimization search",
    "地质": "rogii geology", "钻井": "rogii wellbore", "分割": "segmentation",
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def dump_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(data=DATA):
    return [json.loads(line) for line in (data / "competitions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def slug_from_url(value):
    parsed = urlparse(value)
    match = re.fullmatch(r"/(?:c|competitions)/([a-zA-Z0-9_-]+)/?", parsed.path)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in ("www.kaggle.com", "kaggle.com") or not match:
        raise ValueError(f"Invalid competition URL: {value}")
    return match.group(1)


def as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in ("true", "false"):
        return value.lower() == "true"
    raise ValueError(f"Expected boolean or true/false string; got {value!r}")


def rank_int(value):
    text = str(value).strip()
    return int(text) if re.fullmatch(r"[1-9][0-9]*", text) else None


def modality_hints(title, description):
    text = (title + " " + description).lower()
    # These are retrieval hints, NOT labels supplied by the upstream archive.
    rules = {
        "audio": r"birdclef|audio|sound|speech|acoustic|song identification",
        "recommender": r"recommend|session-based|recommender|clicks.*carts",
        "simulation": r"lux ai|simulation|play the|playing|halite|hungry geese|kore 2022|kaggriculture|chess|connectx|connect x|agent.*game",
        "optimization": r"santa|traveling salesman|permutation|packing|scheduling|routing|optimization",
        "time-series": r"forecast|time series|time-series|sales prediction|ventilator|wellbore|geology",
        "vision": r"image|images|rsna|melanoma|segmentation|detection|vision|whale|satellite|microscopy|x-ray|ct scan|mri|cell tracking",
        "text": r"text|language|essay|writing|llm|bert|translation|discourse|feedback prize|question answering|sentiment|toxic|nli",
        "tabular": r"tabular|credit|default|fraud|house price|titanic|insurance|click-through|customer|playground series|student health|smartphone addiction",
    }
    return sorted(key for key, pattern in rules.items() if re.search(pattern, text)) or ["unknown"]


def normalize(raw, commit):
    import yaml
    obj = yaml.safe_load(raw)
    if not isinstance(obj, dict) or not isinstance(obj.get("competitions"), list) or not obj["competitions"]:
        raise ValueError("Upstream must have a non-empty competitions list")
    result, seen = [], set()
    for competition in obj["competitions"]:
        if not isinstance(competition, dict):
            raise ValueError("Competition record must be a mapping")
        for key in ("title", "desc", "link", "kind", "year", "metric", "done"):
            if key not in competition:
                raise ValueError(f"Upstream record missing {key}")
        slug = slug_from_url(str(competition["link"]))
        if slug in seen:
            raise ValueError(f"Duplicate competition slug: {slug}")
        seen.add(slug)
        solutions = competition.get("solutions") or []
        if not isinstance(solutions, list):
            raise ValueError(f"Invalid solutions list: {slug}")
        links = []
        for ordinal, solution in enumerate(solutions):
            if not isinstance(solution, dict) or not {"rank", "link", "kind"}.issubset(solution):
                raise ValueError(f"Malformed solution: {slug}")
            url = str(solution["link"]).strip()
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                raise ValueError(f"Malformed solution URL: {slug}")
            links.append({"id": digest(f"{slug}\0{url}\0{ordinal}".encode())[:20],
                          "rank_label": str(solution["rank"]), "rank": rank_int(solution["rank"]),
                          "url": url, "kind": str(solution["kind"]), "evidence_level": "linked_unread"})
        metric_raw = str(competition["metric"]).strip()
        result.append({"slug": slug, "title": str(competition["title"]).strip(),
                       "description": str(competition["desc"]).strip(), "kind": str(competition["kind"]),
                       "year": int(competition["year"]), "metric": metric_raw if metric_raw not in ("", "-") else None,
                       "metric_raw": metric_raw, "competition_url": f"https://www.kaggle.com/competitions/{slug}",
                       "archive_done": as_bool(competition["done"]), "prize": competition.get("prize"),
                       "team_count_raw": str(competition.get("team", "")),
                       "modality_hints": modality_hints(str(competition["title"]), str(competition["desc"])),
                       "modality_basis": "heuristic_title_description", "solutions": links,
                       "upstream_commit": commit, "upstream_number": str(competition.get("number", ""))})
    return sorted(result, key=lambda record: record["slug"])


def diff_rows(previous, current):
    old, new = {row["slug"]: row for row in previous}, {row["slug"]: row for row in current}
    def stable(row):
        return {key: value for key, value in row.items() if key != "upstream_commit"}
    return {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
            "changed": sorted(slug for slug in old.keys() & new.keys() if stable(old[slug]) != stable(new[slug]))}


def download(url):
    headers = {"User-Agent": "kaggle-solutions-skills/0.1"}
    api_host = urlparse(url).hostname == "api.github.com"
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if api_host and token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            raw = response.read(20_000_001)
    except HTTPError as exc:
        if not api_host or exc.code not in (403, 429):
            raise
        # Shared-IP anonymous limits are common. Reuse an authenticated gh
        # session without reading or logging its stored credentials.
        try:
            response = subprocess.run(["gh", "api", url], capture_output=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            raise ValueError("GitHub API rate-limited; authenticated gh is unavailable. Use refresh --source-dir with an existing checkout.") from None
        if response.returncode:
            raise ValueError("GitHub API rate-limited; authenticated gh fallback failed. Use refresh --source-dir or retry when quota resets.") from None
        raw = response.stdout
    if len(raw) > 20_000_000:
        raise ValueError("Upstream file exceeds 20 MB; inspect before extending importer")
    return raw


def upstream_snapshot(source_dir=None, ref="main"):
    if source_dir:
        source_dir = source_dir.resolve()
        commit = subprocess.check_output(["git", "-C", str(source_dir), "rev-parse", "HEAD"], text=True).strip()
        raw = subprocess.check_output(["git", "-C", str(source_dir), "show", f"{commit}:data/competitions.yml"])
        license_text = subprocess.check_output(["git", "-C", str(source_dir), "show", f"{commit}:LICENSE.md"])
        commit_time = subprocess.check_output(["git", "-C", str(source_dir), "show", "-s", "--format=%cI", commit], text=True).strip()
    else:
        if not re.fullmatch(r"[a-zA-Z0-9_.\-/]+", ref) or ".." in ref:
            raise ValueError("Invalid upstream ref")
        meta = json.loads(download(f"https://api.github.com/repos/{REPO}/commits/{ref}"))
        commit, commit_time = meta["sha"], meta["commit"]["committer"]["date"]
        raw = download(f"https://raw.githubusercontent.com/{REPO}/{commit}/data/competitions.yml")
        license_text = download(f"https://raw.githubusercontent.com/{REPO}/{commit}/LICENSE.md")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Upstream resolution did not produce a commit SHA")
    return raw, license_text, commit, commit_time


def refresh(data, source_dir=None, ref="main"):
    raw, license_text, commit, commit_time = upstream_snapshot(source_dir, ref)
    # All parsing/validation takes place before changing the live snapshot.
    rows = normalize(raw, commit)
    encoded = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()
    previous = read_rows(data) if (data / "competitions.jsonl").exists() else []
    change = diff_rows(previous, rows)
    previous_manifest = load_json(data / "manifest.json") if (data / "manifest.json").exists() else {}
    solutions = [item for row in rows for item in row["solutions"]]
    manifest = {"schema_version": 1, "upstream_repository": f"https://github.com/{REPO}",
                "upstream_commit": commit, "upstream_committed_at": commit_time, "retrieved_at": now(),
                "source_path": "data/competitions.yml", "source_sha256": digest(raw), "index_sha256": digest(encoded),
                "competition_count": len(rows), "solution_link_count": len(solutions),
                "unique_solution_url_count": len({item["url"] for item in solutions}),
                "competitions_without_solutions": sum(not row["solutions"] for row in rows),
                "source_status": "archive_metadata_only", "modality_status": "heuristic_hints_only"}
    delta = dict(change, previous_commit=previous_manifest.get("upstream_commit"), current_commit=commit)
    data.mkdir(parents=True, exist_ok=True)
    # Stage in the destination filesystem. Write manifest last; interrupted writes
    # are detected by validate via checksum rather than silently trusted.
    with tempfile.TemporaryDirectory(prefix=".refresh-", dir=data) as temp:
        staging = Path(temp)
        payloads = {"competitions.yml": raw, "competitions.jsonl": encoded,
                    "UPSTREAM-LICENSE.txt": license_text, "last-refresh.json": dump_json(delta).encode(),
                    "manifest.json": dump_json(manifest).encode()}
        for name, content in payloads.items():
            (staging / name).write_bytes(content)
        for name in payloads:
            (staging / name).replace(data / name)
    return {"manifest": manifest, "changes": delta}


def tokens(text):
    text = text.lower().replace("pseudo-label", "pseudo label")
    for term, replacement in ALIASES.items():
        text = text.replace(term, " " + replacement + " ")
    return re.findall(r"[a-z0-9]+", text)


def patterns(data=DATA):
    path = data / "patterns.json"
    return load_json(path) if path.exists() else []


def search(rows, query, cards):
    query_tokens = set(tokens(query))
    docs = []
    for row in rows:
        support = [card for card in cards if row["slug"] in card["competitions"]]
        # A method search matches only explicit curated cards; it does not infer
        # methods used by thousands of unread writeups from their competition titles.
        method_terms = " ".join(" ".join([card["title"], *card["tags"], card["decision"]]) for card in support)
        base = " ".join([row["slug"], row["title"], row["description"], row["metric"] or "", *row["modality_hints"]])
        docs.append(Counter(tokens(base + " " + base + " " + method_terms)))
    count = len(docs)
    if not count:
        return []
    df = Counter(token for doc in docs for token in doc)
    avg_length = sum(sum(doc.values()) for doc in docs) / count or 1
    results = []
    for row, doc in zip(rows, docs):
        score = 0.0
        matches = query_tokens & doc.keys()
        for token in matches:
            freq = doc[token]
            idf = math.log(1 + (count - df[token] + 0.5) / (df[token] + 0.5))
            score += idf * freq * 2.2 / (freq + 1.2 * (0.25 + 0.75 * sum(doc.values()) / avg_length))
        if query and not matches:
            continue
        if query.strip().lower() == row["slug"]:
            score += 100
        results.append(dict(row, retrieval_score=round(score, 4), matched_terms=sorted(matches),
                            matching_pattern_ids=[card["id"] for card in cards if row["slug"] in card["competitions"]
                                                  and query_tokens.intersection(tokens(" ".join([card["title"], *card["tags"], card["decision"]]))) ]))
    return sorted(results, key=lambda row: (-row["retrieval_score"], -row["year"], row["slug"]))


def select_links(row, top_rank=None, source_kind=None, limit=None):
    links = row["solutions"]
    if top_rank is not None:
        links = [link for link in links if link["rank"] is not None and link["rank"] <= top_rank]
    if source_kind:
        links = [link for link in links if link["kind"] == source_kind]
    # Dedup for display only; preserve all upstream link records on disk.
    unique = {}
    for link in links:
        unique.setdefault(link["url"], link)
    links = sorted(unique.values(), key=lambda link: (link["rank"] is None, link["rank"] or 0, link["url"]))
    return links[:limit] if limit is not None else links


def validate(data=DATA):
    errors = []
    manifest = load_json(data / "manifest.json")
    rows = read_rows(data)
    if digest((data / "competitions.jsonl").read_bytes()) != manifest["index_sha256"]:
        errors.append("Index checksum mismatch; refresh again")
    if digest((data / "competitions.yml").read_bytes()) != manifest["source_sha256"]:
        errors.append("Source checksum mismatch")
    if len(rows) != manifest["competition_count"] or len({row["slug"] for row in rows}) != len(rows):
        errors.append("Competition count/identity mismatch")
    if sum(len(row["solutions"]) for row in rows) != manifest["solution_link_count"]:
        errors.append("Solution count mismatch")
    # Check the normalized content, not just matching counts/checksums.
    rebuilt = normalize((data / "competitions.yml").read_bytes(), manifest["upstream_commit"])
    if rebuilt != rows:
        errors.append("Index differs from normalization of the pinned source")
    cards = patterns(data)
    source_path = data / "sources.json"
    sources = load_json(source_path) if source_path.exists() else []
    source_map = {source["id"]: source for source in sources}
    if len(source_map) != len(sources) or len({card["id"] for card in cards}) != len(cards):
        errors.append("Duplicate source/card IDs")
    known_slugs = {row["slug"] for row in rows}
    for source in sources:
        if source["status"] == "source_read" and (not re.fullmatch(r"[0-9a-f]{64}", source.get("content_sha256", ""))
                                                   or not source.get("read_at") or not source.get("locator")):
            errors.append(f"Incomplete read provenance: {source['id']}")
    for card in cards:
        for key in ("id", "title", "tags", "competitions", "decision", "applicability", "pitfalls", "minimal_experiment", "evidence"):
            if key not in card or not card[key]:
                errors.append(f"Missing card field {key}: {card.get('id')}")
        if not set(card["competitions"]).issubset(known_slugs):
            errors.append(f"Unknown competition in card: {card['id']}")
        for evidence in card["evidence"]:
            source = source_map.get(evidence.get("source_id"))
            if not source or source["status"] != "source_read":
                errors.append(f"Card uses unread/missing source: {card['id']}")
            if evidence.get("claim_type") not in ("author_report", "maintainer_inference", "locally_reproduced"):
                errors.append(f"Invalid claim_type: {card['id']}")
            if not evidence.get("locator") or not evidence.get("observation"):
                errors.append(f"Missing evidence locator/observation: {card['id']}")
            if evidence.get("claim_type") == "locally_reproduced" and not evidence.get("run_record"):
                errors.append(f"Reproduction lacks run record: {card['id']}")
    return {"ok": not errors, "errors": errors, "competitions": len(rows),
            "solution_links": manifest["solution_link_count"], "patterns": len(cards), "sources": len(sources)}


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("Must be positive")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA, help="Knowledge directory; place before subcommand")
    sub = parser.add_subparsers(dest="command", required=True)
    refresh_parser = sub.add_parser("refresh", help="Resolve upstream HEAD/ref and rebuild a pinned metadata index")
    refresh_parser.add_argument("--source-dir", type=Path)
    refresh_parser.add_argument("--ref", default="main")
    sub.add_parser("stats")
    sub.add_parser("validate")
    search_parser = sub.add_parser("search", help="Lexical retrieval over metadata and curated method cards")
    search_parser.add_argument("query", nargs="?", default="")
    search_parser.add_argument("--modality", choices=MODALITIES)
    search_parser.add_argument("--metric")
    search_parser.add_argument("--kind")
    search_parser.add_argument("--year-min", type=int)
    search_parser.add_argument("--year-max", type=int)
    search_parser.add_argument("--limit", type=positive, default=10)
    show_parser = sub.add_parser("show")
    show_parser.add_argument("competition")
    for command in (search_parser, show_parser):
        command.add_argument("--top-rank", type=positive)
        command.add_argument("--source-kind")
        command.add_argument("--solutions-limit", type=positive, default=5)
        command.add_argument("--json", action="store_true")
    card_parser = sub.add_parser("patterns")
    card_parser.add_argument("query", nargs="?", default="")
    card_parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "refresh":
            print(dump_json(refresh(args.data, args.source_dir, args.ref)))
            return 0
        if args.command == "validate":
            result = validate(args.data)
            print(dump_json(result))
            return 0 if result["ok"] else 1
        if args.command == "stats":
            manifest = load_json(args.data / "manifest.json")
            cards = patterns(args.data)
            source_records = load_json(args.data / "sources.json") if (args.data / "sources.json").exists() else []
            print(dump_json(dict(manifest, pattern_count=len(cards),
                                 read_source_count=sum(source["status"] == "source_read" for source in source_records),
                                 read_source_roles=dict(Counter(source["source_role"] for source in source_records if source["status"] == "source_read")))))
            return 0
        cards = patterns(args.data)
        if args.command == "patterns":
            terms = set(tokens(args.query))
            selected = [card for card in cards if not terms or terms.intersection(tokens(" ".join([card["title"], *card["tags"], card["decision"]])))]
            if args.json:
                print(dump_json(selected))
            else:
                for card in selected:
                    print(f"{card['id']} | {card['title']}\n  {card['decision']}\n  Example competitions: {', '.join(card['competitions'])}")
            return 0
        rows = read_rows(args.data)
        if args.command == "show":
            slug = slug_from_url(args.competition) if "://" in args.competition else args.competition.strip()
            selected = [row for row in rows if row["slug"] == slug]
            if not selected:
                raise ValueError(f"Competition not in this archive: {slug}; use live Kaggle discovery")
        else:
            filtered = [row for row in rows
                        if (not args.modality or args.modality in row["modality_hints"])
                        and (not args.metric or args.metric.lower() in (row["metric"] or "").lower())
                        and (not args.kind or args.kind.lower() == row["kind"].lower())
                        and (args.year_min is None or row["year"] >= args.year_min)
                        and (args.year_max is None or row["year"] <= args.year_max)]
            selected = search(filtered, args.query, cards)
        output = []
        for row in selected:
            links = select_links(row, args.top_rank, args.source_kind, args.solutions_limit)
            if args.command == "search" and (args.top_rank or args.source_kind) and not links:
                continue
            output.append(dict(row, solutions=links, archived_solution_link_count=len(row["solutions"])))
            if args.command == "search" and len(output) >= args.limit:
                break
        if args.json:
            print(dump_json({"archive": load_json(args.data / "manifest.json"), "results": output,
                             "retrieval": "BM25-style lexical ranking; modality hints are inferred; rank labels are archive claims; linked_unread is not source_read"}))
        else:
            for row in output:
                print(f"{row['slug']} | {row['title']} ({row['year']})\n  metric: {row['metric'] or 'unknown'} | modality hints: {', '.join(row['modality_hints'])}\n  {row['competition_url']}")
                for link in row["solutions"]:
                    print(f"  rank={link['rank_label']} kind={link['kind']} [linked_unread] {link['url']}")
            if not output:
                print("No matching archived records. Use live discovery or broader terms.")
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(dump_json({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
