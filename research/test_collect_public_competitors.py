import importlib.util
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock

spec = importlib.util.spec_from_file_location('collector', Path(__file__).with_name('collect_public_competitors.py'))
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
SID = '01a1e9d6-2518-71fa-9691-c7a2fec94e3d'


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.raw = b'An original test fixture.'
        self.record = {'submission_id': SID, 'sha256': sha256(self.raw).hexdigest(),
                       'source_url': f'https://make.fun/api/submissions/{SID}/artifact.txt?phase=dev',
                       'characters': len(self.raw), 'bytes': len(self.raw)}
        self.opener = MagicMock()
        self.reader = self.opener.open.return_value.__enter__.return_value.read
        self.reader.return_value = self.raw

    def test_refuses_offhost_and_url_traversal(self):
        for url in ('https://evil.example/api/submissions/x/artifact.txt',
                    f'https://make.fun/api/submissions/{SID}/../artifact.txt',
                    f'https://make.fun/api/submissions/{SID}/artifact.txt#fragment'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.artifact_url(url)

    def test_refuses_offhost_redirect(self):
        with self.assertRaises(ValueError):
            collector.SameHostRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.example/file')

    def test_refuses_filename_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            for field, value in [('submission_id', '../escape'), ('sha256', '../escape')]:
                record = dict(self.record, **{field: value})
                with self.subTest(field=field), self.assertRaises(ValueError):
                    collector.hydrate(record, Path(temp), self.opener)
            self.opener.open.assert_not_called()

    def test_bad_hash_never_reaches_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            self.reader.return_value = b'x' * len(self.raw)
            with self.assertRaises(ValueError):
                collector.hydrate(self.record, Path(temp), self.opener)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_download_is_bounded_and_rejects_oversize(self):
        with tempfile.TemporaryDirectory() as temp:
            self.reader.return_value = b'x' * 4001
            with self.assertRaises(ValueError):
                collector.hydrate(self.record, Path(temp), self.opener)
            self.reader.assert_called_once_with(4001)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_verified_cache_needs_no_network(self):
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            path = collector.hydrate(self.record, scratch, self.opener)
            self.assertEqual(path.parent, scratch)
            self.assertEqual(path.read_bytes(), self.raw)
            self.opener.reset_mock()
            self.assertEqual(collector.hydrate(self.record, scratch, self.opener), path)
            self.opener.open.assert_not_called()

    def test_refuses_cache_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            scratch = Path(temp)
            target = scratch / 'existing'
            target.write_bytes(self.raw)
            dest = scratch / f'{SID}-{self.record["sha256"][:12]}.txt'
            dest.symlink_to(target)
            with self.assertRaises(ValueError):
                collector.hydrate(self.record, scratch, self.opener)
            self.opener.open.assert_not_called()


if __name__ == '__main__':
    unittest.main()
