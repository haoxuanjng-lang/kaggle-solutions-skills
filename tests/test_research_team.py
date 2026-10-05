"""Offline regression tests for real-case retrieval and research-role handoffs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "kaggle-solutions-skills" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import research_team as team


class ResearchTeamTests(unittest.TestCase):
    def test_all_cases_resolve_original_author_provenance(self):
        cases = team.scenarios()
        self.assertEqual({c["id"] for c in cases}, {"otto", "birdclef-2024", "rogii", "amex", "m5"})
        for case in cases:
            with self.subTest(case=case["id"]):
                plan = team.make_plan(case["id"])
                context = plan["tasks"][0]["context"]
                sources = {s["id"]: s for s in context["sources"]}
                self.assertEqual(plan["competition"]["slug"], case["competition"])
                self.assertEqual(plan["dispatch_status"], "not_dispatched")
                self.assertEqual(plan["execution_status"], "not_attempted")
                self.assertTrue(context["pattern_cards"])
                for source_id in case["source_ids"]:
                    source = sources[source_id]
                    self.assertEqual(source["competition"], case["competition"])
                    self.assertEqual(source["status"], "source_read")
                    self.assertEqual(source["reproduction_status"], "not_attempted")
                    self.assertTrue(source["url"].startswith("https://www.kaggle.com/"))
                    self.assertEqual(len(source["content_sha256"]), 64)
                for card in context["pattern_cards"]:
                    self.assertIn(case["competition"], card["competitions"])
                    for evidence in card["evidence"]:
                        self.assertIn(evidence["source_id"], sources)
                # OTTO metric is absent in the archive. Preserve the unknown.
                if case["id"] == "otto":
                    self.assertIsNone(plan["competition"]["metric"])

    def test_cli_plan_and_validate_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "research"
            command = [sys.executable, str(SCRIPTS / "research_team.py")]
            result = subprocess.run(command + ["plan", "--scenario", "birdclef-2024", "--output", str(output)], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)["dispatch_status"], "not_dispatched")
            checked = subprocess.run(command + ["validate", str(output)], cwd=root, capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
            self.assertEqual(len(list((output / "tasks").glob("*.json"))), 5)
            self.assertEqual(list((output / "outputs").iterdir()), [])

    def test_predecessor_dependencies_and_complete_result_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = team.make_plan("m5")
            team.save_plan(plan, tmp)
            self.assertEqual(plan["stages"][1], ["evidence", "validation"])
            self.assertEqual(plan["tasks"][3]["depends_on"], ["evidence", "validation"])
            # Packet creation cannot masquerade as completed role execution.
            self.assertFalse(team.validate_plan(tmp, results=True)["ok"])
            for task in plan["tasks"]:
                source = task["context"]["sources"][0]
                team.write_json(Path(tmp) / task["output"], {
                    "schema_version": 1, "role": task["role"], "status": "complete",
                    "findings": [{"statement": "Test fixture inference, no experiment executed", "claim_type": "maintainer_inference", "source_id": source["id"], "locator": source["locator"]}],
                    "unknowns": ["Target data unavailable"], "proposed_experiments": [],
                    "disagreements": [], "handoff": "Test fixture only",
                })
            self.assertTrue(team.validate_plan(tmp, results=True)["ok"])
            result_path = Path(tmp) / "outputs/reviewer.json"
            result = team.read_json(result_path)
            result["findings"][0]["claim_type"] = "locally_reproduced"
            team.write_json(result_path, result)
            checked = team.validate_plan(tmp, results=True)
            self.assertFalse(checked["ok"])
            self.assertTrue(any("lacks run record" in e for e in checked["errors"]))

    def test_provenance_tampering_and_dependency_cycles_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = team.make_plan("amex")
            team.save_plan(plan, tmp)
            plan["tasks"][0]["context"]["sources"][0]["status"] = "locally_reproduced"
            plan["tasks"][0]["depends_on"] = ["reviewer"]
            team.write_json(Path(tmp) / "plan.json", plan)
            for task in plan["tasks"]:
                team.write_json(Path(tmp) / "tasks" / f"{task['id']}.json", task)
            result = team.validate_plan(tmp)
            self.assertFalse(result["ok"])
            self.assertTrue(any("cyclic" in e for e in result["errors"]))
            self.assertTrue(any("provenance mismatch" in e for e in result["errors"]))

    def test_result_nontext_fields_cannot_masquerade_as_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = team.make_plan("otto")
            team.save_plan(plan, tmp)
            for task in plan["tasks"]:
                source = task["context"]["sources"][0]
                team.write_json(Path(tmp) / task["output"], {
                    "schema_version": 1, "role": task["role"], "status": "complete",
                    "findings": [{"statement": {"fabricated": True}, "claim_type": "maintainer_inference",
                                  "source_id": source["id"], "locator": ["not a locator"]}],
                    "unknowns": [], "proposed_experiments": [], "disagreements": [], "handoff": 42,
                })
            checked = team.validate_plan(tmp, results=True)
            self.assertFalse(checked["ok"])
            self.assertTrue(any("Finding fields must be non-empty strings" in e for e in checked["errors"]))
            self.assertTrue(any("handoff must be a non-empty string" in e for e in checked["errors"]))

    def test_workspace_overwrite_and_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = team.make_plan("rogii")
            team.save_plan(plan, tmp)
            with self.assertRaisesRegex(ValueError, "empty"):
                team.save_plan(plan, tmp)
            plan["tasks"][0]["output"] = "../outside.json"
            team.write_json(Path(tmp) / "plan.json", plan)
            result = team.validate_plan(tmp)
            self.assertFalse(result["ok"])
            self.assertTrue(any("escapes" in e for e in result["errors"]))

    def test_archive_identity_and_claim_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = team.make_plan("otto")
            team.save_plan(plan, tmp)
            archive = plan["tasks"][0]["context"]["archive_source"]
            self.assertIn(plan["upstream_commit"], archive["id"])
            self.assertEqual(archive["url"], f"{archive['upstream_repository']}/blob/{plan['upstream_commit']}/{archive['source_path']}")
            manifest = team.read_json(team.solutions.DATA / "manifest.json")
            self.assertEqual(archive["source_sha256"], manifest["source_sha256"])
            self.assertNotIn(archive["id"], {s["id"] for s in plan["tasks"][0]["context"]["sources"]})
            for task in plan["tasks"]:
                team.write_json(Path(tmp) / task["output"], {
                    "schema_version": 1, "role": task["role"], "status": "complete",
                    "findings": [{"statement": "The archive metric is unknown", "claim_type": "archive_metadata",
                                  "source_id": archive["id"], "locator": "competition.metric"}],
                    "unknowns": [], "proposed_experiments": [], "disagreements": [], "handoff": "Fixture only",
                })
            self.assertTrue(team.validate_plan(tmp, results=True)["ok"])
            path = Path(tmp) / "outputs/scout.json"
            original = team.read_json(path)
            mutations = [
                ({"claim_type": "author_report"}, "cannot support author"),
                ({"claim_type": "locally_reproduced", "run_record": "fixture.json"}, "cannot support author"),
                ({"source_id": plan["tasks"][0]["context"]["sources"][0]["id"]}, "requires the pinned archive"),
                ({"locator": "competition.official_current_status"}, "Unknown archive field locator"),
                ({"locator": "competition.nonexistent"}, "Unknown archive field locator"),
            ]
            for changes, message in mutations:
                with self.subTest(changes=changes):
                    result = json.loads(json.dumps(original))
                    result["findings"][0].update(changes)
                    team.write_json(path, result)
                    checked = team.validate_plan(tmp, results=True)
                    self.assertFalse(checked["ok"])
                    self.assertTrue(any(message in e for e in checked["errors"]), checked)
            original["findings"][0]["claim_type"] = "maintainer_inference"
            team.write_json(path, original)
            self.assertTrue(team.validate_plan(tmp, results=True)["ok"])
            # Changing both packet and plan cannot legitimize altered archive provenance.
            for task in plan["tasks"]:
                task["context"]["archive_source"]["upstream_commit"] = "0" * 40
                team.write_json(Path(tmp) / "tasks" / f"{task['id']}.json", task)
            team.write_json(Path(tmp) / "plan.json", plan)
            checked = team.validate_plan(tmp, results=True)
            self.assertFalse(checked["ok"])
            self.assertTrue(any("context differs" in e for e in checked["errors"]))

    def test_unknown_scenario_does_not_fabricate_competition(self):
        with self.assertRaisesRegex(ValueError, "Unknown scenario"):
            team.make_plan("made-up-live-competition")


if __name__ == "__main__":
    unittest.main()
