# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'kaggle-solutions-skills'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


solutions = module('solutions', SKILL / 'scripts' / 'solutions.py')
fetch = module('fetch_source', SKILL / 'scripts' / 'fetch_source.py')
project = module('project', ROOT / 'scripts' / 'project.py')
COMMIT = 'a' * 40
FIXTURE = b'''competitions:
  - title: Future Sales Forecasting
    desc: Forecast sales
    link: https://www.kaggle.com/c/sales-example
    kind: Research
    year: "2024"
    metric: "-"
    done: "false"
    solutions:
      - {rank: "1", link: "https://example.com/author", kind: description}
      - {rank: "all solutions", link: "https://example.com/list", kind: kernel}
      - {rank: "1", link: "https://example.com/author", kind: code}
  - title: Sparse Example
    desc: Data
    link: https://www.kaggle.com/competitions/sparse-example
    kind: Featured
    year: "2023"
    metric: RMSE
    done: true
    solutions:
'''


class ArchiveBehavior(unittest.TestCase):
    def test_anonymous_github_limit_uses_authenticated_cli_without_token_export(self):
        error = HTTPError('https://api.github.com/repos/example/repo',403,'rate limit',{},None)
        response = subprocess.CompletedProcess(['gh'],0,b'{"sha":"example"}',b'')
        with patch.object(solutions,'urlopen',side_effect=error), patch.object(solutions.subprocess,'run',return_value=response) as api:
            self.assertEqual(response.stdout,solutions.download('https://api.github.com/repos/example/repo'))
            self.assertEqual(['gh','api','https://api.github.com/repos/example/repo'],api.call_args.args[0])

    def test_failed_github_limit_fallback_is_actionable(self):
        error = HTTPError('https://api.github.com/repos/example/repo',403,'rate limit',{},None)
        with patch.object(solutions,'urlopen',side_effect=error), patch.object(solutions.subprocess,'run',side_effect=FileNotFoundError):
            with self.assertRaisesRegex(ValueError,'source-dir'):
                solutions.download('https://api.github.com/repos/example/repo')

    def test_false_string_null_solutions_and_unknown_metric(self):
        rows = {row['slug']: row for row in solutions.normalize(FIXTURE, COMMIT)}
        self.assertFalse(rows['sales-example']['archive_done'])
        self.assertIsNone(rows['sales-example']['metric'])
        self.assertEqual([], rows['sparse-example']['solutions'])

    def test_preserve_original_links_and_nonnumeric_rank(self):
        row = solutions.normalize(FIXTURE, COMMIT)[0]
        self.assertEqual(3, len(row['solutions']))
        self.assertIsNone(row['solutions'][1]['rank'])
        self.assertEqual('all solutions', row['solutions'][1]['rank_label'])
        self.assertEqual(2, len(solutions.select_links(row)))
        self.assertEqual(1, len(solutions.select_links(row, top_rank=1)))
        self.assertEqual('code', solutions.select_links(row, source_kind='code')[0]['kind'])

    def test_duplicate_competition_or_bad_schema_is_not_silently_dropped(self):
        import yaml
        obj = yaml.safe_load(FIXTURE)
        obj['competitions'].append(obj['competitions'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            solutions.normalize(yaml.safe_dump(obj).encode(), COMMIT)
        with self.assertRaises(ValueError):
            solutions.normalize(b'competitions: []', COMMIT)
        with self.assertRaises(ValueError):
            solutions.as_bool('not-a-bool')

    def test_diff_detects_changes_without_commit_only_noise(self):
        rows = solutions.normalize(FIXTURE, COMMIT)
        changed = copy.deepcopy(rows)
        changed[0]['upstream_commit'] = 'b' * 40
        self.assertEqual([], solutions.diff_rows(rows, changed)['changed'])
        changed[0]['metric'] = 'WRMSSE'
        self.assertEqual(['sales-example'], solutions.diff_rows(rows, changed)['changed'])
        self.assertEqual(['sparse-example'], solutions.diff_rows(rows, changed[:1])['removed'])

    def test_refresh_keeps_curated_data_and_validates_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            curated = data / 'patterns.json'
            curated.write_text('[]\n', encoding='utf-8')
            with patch.object(solutions, 'upstream_snapshot', return_value=(FIXTURE, b'MIT test fixture', COMMIT, '2024-01-01')):
                result = solutions.refresh(data)
                self.assertEqual(2, result['manifest']['competition_count'])
                self.assertEqual(3, result['manifest']['solution_link_count'])
                self.assertEqual('[]\n', curated.read_text())
                self.assertTrue(solutions.validate(data)['ok'])
                self.assertEqual([], solutions.refresh(data)['changes']['changed'])
            index = data / 'competitions.jsonl'
            rows = solutions.read_rows(data)
            rows[0]['metric'] = 'wrong'
            index.write_text(''.join(json.dumps(row)+'\n' for row in rows),encoding='utf-8')
            self.assertFalse(solutions.validate(data)['ok'])

    def test_invalid_refresh_leaves_existing_snapshot_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            with patch.object(solutions, 'upstream_snapshot', return_value=(FIXTURE, b'MIT test fixture', COMMIT, '2024-01-01')):
                solutions.refresh(data)
            previous = {p.name:p.read_bytes() for p in data.iterdir()}
            with patch.object(solutions, 'upstream_snapshot', return_value=(b'competitions: []', b'license', COMMIT, '2024-01-01')):
                with self.assertRaises(ValueError):
                    solutions.refresh(data)
            self.assertEqual(previous, {p.name:p.read_bytes() for p in data.iterdir()})

    def test_local_import_uses_committed_yaml_not_dirty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / 'data').mkdir()
            (source / 'data' / 'competitions.yml').write_bytes(FIXTURE)
            (source / 'LICENSE.md').write_text('MIT test fixture')
            subprocess.run(['git','init',str(source)],capture_output=True,check=True)
            subprocess.run(['git','-C',str(source),'add','.'],capture_output=True,check=True)
            subprocess.run(['git','-C',str(source),'-c','user.name=Test','-c','user.email=test@example.com','commit','-m','fixture'],capture_output=True,check=True)
            committed = subprocess.check_output(['git','-C',str(source),'show','HEAD:data/competitions.yml'])
            (source / 'data' / 'competitions.yml').write_text('competitions: []')
            raw, _, commit, _ = solutions.upstream_snapshot(source)
            self.assertEqual(committed, raw)
            self.assertRegex(commit, r'^[0-9a-f]{40}$')


class RetrievalBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = solutions.read_rows()
        cls.cards = solutions.patterns()

    def test_exact_target_is_first(self):
        self.assertEqual('otto-recommender-system', solutions.search(self.rows,'otto-recommender-system',self.cards)[0]['slug'])

    def test_method_request_finds_evidence_backed_examples(self):
        found = solutions.search(self.rows,'pseudo labeling',self.cards)[:2]
        self.assertEqual({'birdclef-2024','feedback-prize-effectiveness'}, {row['slug'] for row in found})
        self.assertTrue(all(row['matching_pattern_ids'] for row in found))

    def test_chinese_distillation_query_maps_to_card(self):
        found = solutions.search(self.rows,'蒸馏',self.cards)
        self.assertEqual('feedback-prize-effectiveness',found[0]['slug'])
        self.assertIn('ensemble-distillation',found[0]['matching_pattern_ids'])

    def test_unknown_query_has_no_fabricated_hit(self):
        self.assertEqual([], solutions.search(self.rows,'zzzznonexistenttechniquezzzz',self.cards))

    def test_cli_filters_medical_search_to_vision_and_rank(self):
        response = subprocess.run([os.sys.executable,str(SKILL/'scripts'/'solutions.py'),'search','医学影像',
                                   '--modality','vision','--top-rank','3','--limit','3','--json'],capture_output=True,text=True,encoding='utf-8',check=True)
        results = json.loads(response.stdout)['results']
        self.assertTrue(results)
        self.assertTrue(all('vision' in row['modality_hints'] for row in results))
        self.assertTrue(all(link['rank']<=3 for row in results for link in row['solutions']))


class EvidenceAndDistribution(unittest.TestCase):
    def test_package_contains_exactly_the_portable_allowlist(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'skill.zip'
            result = project.package(output)
            self.assertTrue(result['crc_and_bytes_verified'])
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertEqual(len(project.skill_files()),len(names))
                self.assertIn(SKILL.name+'/LICENSE',names)
                self.assertTrue(all(name.startswith(SKILL.name+'/') for name in names))
    def test_missing_read_source_cannot_support_a_card(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            with patch.object(solutions,'upstream_snapshot',return_value=(FIXTURE,b'license',COMMIT,'2024-01-01')):
                solutions.refresh(data)
            card = copy.deepcopy(solutions.patterns()[0])
            card['competitions'] = ['sales-example']
            (data/'patterns.json').write_text(json.dumps([card]))
            self.assertTrue(any('unread/missing' in error for error in solutions.validate(data)['errors']))

    def test_reproduction_claim_requires_a_run_record(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            with patch.object(solutions,'upstream_snapshot',return_value=(FIXTURE,b'license',COMMIT,'2024-01-01')):
                solutions.refresh(data)
            card = copy.deepcopy(solutions.patterns()[0])
            card['competitions'] = ['sales-example']
            card['evidence'][0]['claim_type'] = 'locally_reproduced'
            (data/'patterns.json').write_text(json.dumps([card]))
            source = next(source for source in solutions.load_json(solutions.DATA/'sources.json') if source['id']==card['evidence'][0]['source_id'])
            (data/'sources.json').write_text(json.dumps([source]))
            self.assertTrue(any('run record' in error for error in solutions.validate(data)['errors']))

    def test_original_post_body_is_required(self):
        with self.assertRaises(ValueError):
            fetch.extract_topic({'forumTopic':{'name':'1st place','comments':[{'rawMarkdown':'nice work'}]}})
        body, metadata = fetch.extract_topic({'forumTopic':{'id':1,'writeUp':{'message':{'rawMarkdown':'Actual method'}}}})
        self.assertEqual('Actual method',body)
        self.assertEqual(1,metadata['topic_id'])

    def test_github_file_requires_immutable_commit(self):
        with self.assertRaisesRegex(ValueError,'pin'):
            fetch.fetch_github('https://raw.githubusercontent.com/owner/repo/main/README.md')

    def test_source_hash_separates_normalized_content_from_cached_bytes(self):
        lf = fetch.normalized_content_bytes('first\nsecond\n')
        self.assertEqual(lf, fetch.normalized_content_bytes('first\r\nsecond\r'))
        with tempfile.TemporaryDirectory() as directory:
            url = 'https://raw.githubusercontent.com/owner/repo/' + COMMIT + '/README.md'
            body = 'first\r\nsecond\r'
            with patch.object(fetch, 'fetch_github', return_value=(body, {'retrieval_method':'test'})), \
                 patch.object(os.sys, 'argv', ['fetch_source.py', url, '--cache', directory]):
                self.assertEqual(0, fetch.main())
            record = json.loads(next(Path(directory).glob('*.json')).read_text(encoding='utf-8'))
            cached = next(Path(directory).glob('*.md')).read_bytes()
            self.assertEqual(body.encode(), cached)
            self.assertEqual(hashlib.sha256(cached).hexdigest(), record['cached_bytes_sha256'])
            self.assertEqual(hashlib.sha256(lf).hexdigest(), record['content_sha256'])
            self.assertNotEqual(record['content_sha256'], record['cached_bytes_sha256'])
            self.assertEqual('utf-8-lf', record['content_normalization'])

    def test_install_contains_the_same_portable_knowledge_and_no_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skills' / SKILL.name
            result = project.install(destination)
            self.assertTrue(result['byte_verified'])
            installed = module('installed_solutions', destination / 'scripts' / 'solutions.py')
            self.assertTrue(installed.validate()['ok'])
            self.assertEqual(len(solutions.read_rows()),len(installed.read_rows()))
            self.assertFalse((destination / 'cache').exists())
            self.assertFalse((destination / 'sources').exists())
            self.assertEqual(result['files'],len(project.skill_files()))

    def test_unrelated_install_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            sentinel = destination / 'keep.txt'
            sentinel.write_text('User file')
            with self.assertRaisesRegex(ValueError,'Destination'):
                project.install(destination)
            self.assertEqual('User file',sentinel.read_text())


if __name__ == '__main__':
    unittest.main()
