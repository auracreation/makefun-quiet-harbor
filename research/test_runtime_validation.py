from pathlib import Path
import tempfile
import unittest

import verify_runtime


class RuntimeValidationTests(unittest.TestCase):
    def test_unicode_code_points_and_identical_isolated_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            entry = Path(temp) / 'main.py'
            entry.write_text("import os\nfrom pathlib import Path\nPath(os.environ['MAKEFUN_OUTPUT_DIR'], 'entry.txt').write_text('é🌿', encoding='utf-8')\n")
            result = verify_runtime.verify(entry, 'é🌿'.encode(), runs=2)
            self.assertEqual(result['characters'], 2)
            self.assertEqual(result['runs'], 2)
            self.assertEqual(result['unique_hashes'], 1)

    def test_wrong_output_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            entry = Path(temp) / 'main.py'
            entry.write_text("import os\nfrom pathlib import Path\nPath(os.environ['MAKEFUN_OUTPUT_DIR'], 'entry.txt').write_text('different', encoding='utf-8')\n")
            with self.assertRaisesRegex(ValueError, 'selected text'):
                verify_runtime.verify(entry, b'chosen', runs=1)

    def test_empty_or_whitespace_selection_is_rejected(self):
        for text in (b'', b' \n', b'\xff'):
            with self.assertRaises(ValueError):
                verify_runtime.verify(Path('absent.py'), text, runs=1)


if __name__ == '__main__':
    unittest.main()
