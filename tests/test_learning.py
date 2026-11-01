import argparse
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = sorted(ROOT.glob('skills/*/scripts/learning.py'))
spec = importlib.util.spec_from_file_location('learning', SCRIPTS[0])
learning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(learning)


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'data' / 'one' / 'state.json'
        self.file = self.root / 'candidate.json'

    def run_command(self, command, **kw):
        defaults = dict(command=command, file=self.file, origin='auto', expected_revision=None,
                        kind=None, query=None, limit=20, include_retracted=False)
        defaults.update(kw)
        return learning.execute(self.path, argparse.Namespace(**defaults))

    def candidate(self, rid='case-one', task='task-one', confirmed=False):
        return dict(id=rid, kind='experience', title='contact', topic='product', rule='match light',
                    applicability=['glossy bottle'], unknowns=['causation'], related_ids=[], source_ids=[],
                    context=dict(task_id=task, model='unknown', settings={}, changes=['lighting'], observations=['visible seam']),
                    evidence=[dict(task_id=task, source='user_feedback' if confirmed else 'model_self_check',
                                   artifact_type='image', summary='looks better', outcome='improved', scope=['reflection'])])

    def save(self, data, **kw):
        self.file.write_text(json.dumps(data), encoding='utf-8')
        return self.run_command('record', **kw)

    def test_reads_and_disabled_auto_do_not_write(self):
        self.assertFalse(self.run_command('status')['enabled'])
        self.assertEqual(self.run_command('list'), [])
        self.assertFalse(self.save(self.candidate())['written'])
        self.assertFalse(self.path.parent.exists())

    def test_manual_record_allowed_while_off(self):
        self.save(self.candidate(), origin='manual')
        self.assertFalse(self.run_command('status')['enabled'])
        self.assertEqual(self.run_command('show', id='case-one')['status'], 'unconfirmed')

    def test_enable_disable_and_independent_stores(self):
        self.run_command('enable'); self.save(self.candidate())
        self.assertTrue(self.run_command('status')['enabled'])
        self.assertFalse(learning.load(self.root / 'data/two/state.json')['enabled'])
        self.run_command('disable')
        before = self.path.read_bytes()
        self.save(self.candidate('case-two'))
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(len(self.run_command('list')), 1)

    def test_dedup_does_not_grow_history(self):
        self.run_command('enable'); self.save(self.candidate())
        before = self.path.read_bytes()
        result = self.save(self.candidate('case-two'))
        self.assertEqual(result['reason'], 'duplicate')
        self.assertEqual(self.path.read_bytes(), before)

    def test_same_case_feedback_preserves_history_and_requires_revision(self):
        self.run_command('enable'); self.save(self.candidate())
        old = self.run_command('show', id='case-one')
        data = self.candidate(confirmed=True)
        data['evidence'].insert(0, self.candidate()['evidence'][0])
        with self.assertRaisesRegex(learning.Invalid, 'expected-revision'):
            self.save(data)
        self.save(data, expected_revision=old['revision'])
        current = self.run_command('show', id='case-one')
        self.assertEqual(current['status'], 'user_confirmed_effective')
        history = self.run_command('history', id='case-one')
        self.assertEqual(history[-1]['before'], old)
        self.assertEqual(len(current['evidence']), 2)

    def test_model_success_never_user_confirmation(self):
        data = self.candidate(); data['evidence'][0]['outcome'] = 'succeeded'
        self.save(data, origin='manual')
        self.assertEqual(self.run_command('show', id='case-one')['status'], 'unconfirmed')

    def test_prompt_cannot_validate_lip_sync(self):
        data = self.candidate(confirmed=True)
        data['evidence'][0].update(artifact_type='prompt', scope=['口型稳定'])
        with self.assertRaisesRegex(learning.Invalid, 'prompt alone'):
            self.save(data, origin='manual')

    def test_secret_rejected_before_store_write(self):
        data = self.candidate(); data['rule'] = 'sk-' + 'a' * 32
        with self.assertRaisesRegex(learning.Invalid, 'credentials'):
            self.save(data, origin='manual')
        self.assertFalse(self.path.exists())

    def test_retract_and_restore_preserve_history(self):
        self.save(self.candidate(), origin='manual')
        first = self.run_command('show', id='case-one')
        self.run_command('retract', id='case-one', reason='user correction')
        self.assertEqual(self.run_command('list'), [])
        self.run_command('restore', id='case-one', revision=first['revision'], reason='restore')
        self.assertEqual(len(self.run_command('list')), 1)
        self.assertEqual(len(self.run_command('history', id='case-one')), 3)

    def test_promotion_needs_independent_confirmed_tasks(self):
        self.run_command('enable'); self.save(self.candidate(confirmed=True))
        second = self.candidate('case-two', confirmed=True); second['rule'] = 'rebuild contact'
        self.save(second)
        strategy = self.candidate('strategy-one', confirmed=True)
        strategy.update(kind='strategy', source_ids=['case-one', 'case-two'])
        with self.assertRaisesRegex(learning.Invalid, 'two independent'):
            self.save(strategy)
        old = self.run_command('show', id='case-two')
        second['context']['task_id'] = 'task-two'; second['evidence'][0]['task_id'] = 'task-two'
        self.save(second, expected_revision=old['revision'])
        self.assertTrue(self.save(strategy)['written'])

    def test_unconfirmed_case_cannot_support_auto_strategy(self):
        self.run_command('enable'); self.save(self.candidate())
        data = self.candidate('strategy'); data.update(kind='strategy', source_ids=['case-one'])
        with self.assertRaisesRegex(learning.Invalid, 'user-confirmed'):
            self.save(data)

    def test_lock_blocks_concurrent_writer_without_overwriting(self):
        self.run_command('enable'); before = self.path.read_bytes()
        with learning.locked(self.path):
            with self.assertRaisesRegex(learning.Invalid, 'busy'):
                self.save(self.candidate())
        self.assertEqual(self.path.read_bytes(), before)

    def test_later_failure_downgrades_without_losing_positive_evidence(self):
        self.save(self.candidate(confirmed=True), origin='manual')
        old = self.run_command('show', id='case-one')
        data = self.candidate(confirmed=True)
        failure = copy.deepcopy(data['evidence'][0]); failure.update(summary='same issue returned', outcome='failed')
        data['evidence'].append(failure)
        self.save(data, origin='manual', expected_revision=old['revision'])
        current = self.run_command('show', id='case-one')
        self.assertEqual(current['status'], 'unconfirmed')
        self.assertEqual(len(current['evidence']), 2)

    def test_retracted_source_stops_strategy_retrieval(self):
        self.run_command('enable'); self.save(self.candidate(confirmed=True))
        second = self.candidate('case-two', 'task-two', True); second['rule'] = 'contact shadow'
        self.save(second)
        strategy = self.candidate('strategy-one', confirmed=True)
        strategy.update(kind='strategy', source_ids=['case-one', 'case-two'])
        self.save(strategy)
        self.assertEqual(len(self.run_command('list', kind='strategy')), 1)
        self.run_command('retract', id='case-one', reason='counterexample')
        self.assertEqual(self.run_command('list', kind='strategy'), [])
        self.assertEqual(len(self.run_command('history', id='strategy-one')), 1)

    def test_auto_cannot_reactivate_retracted_case(self):
        self.run_command('enable'); self.save(self.candidate())
        self.run_command('retract', id='case-one', reason='user correction')
        old = self.run_command('show', id='case-one')
        with self.assertRaisesRegex(learning.Invalid, 'cannot reactivate'):
            self.save(self.candidate(), expected_revision=old['revision'])

    def test_corrupt_state_is_not_silently_reset(self):
        self.path.parent.mkdir(parents=True); self.path.write_text('{oops', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.run_command('enable')
        self.assertEqual(self.path.read_text(), '{oops')

    def test_cli_and_config_for_all_packaged_skills(self):
        for script in SCRIPTS:
            config = learning.read(script.parent.parent / 'learning-config.json')
            for scope in config['scopes']:
                p = subprocess.run([sys.executable, '-X', 'utf8', str(script), '--data-root', str(self.root/'cli'),
                                    '--scope', scope, 'status'], capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(p.returncode, 0, p.stderr)
                self.assertFalse(json.loads(p.stdout)['enabled'])
            self.assertFalse((self.root/'cli').exists())


if __name__ == '__main__':
    unittest.main()
