"""Check a selected entry locally; this does not run make.fun's sealed grader."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def verify(entry, expected, runs=20):
    text = expected.decode('utf-8')
    if not text.strip() or not 1 <= len(text) <= 1000:
        raise ValueError('Selected text must contain 1..1000 code points and non-whitespace')
    if runs < 1:
        raise ValueError('At least one run required')
    entry = entry.resolve()
    source = entry.read_text(encoding='utf-8')
    compile(source, str(entry), 'exec')
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec', '__import__'):
            raise ValueError('Dynamic execution needs a separate manual dependency audit')
    if not imports <= {'os', 'pathlib'}:
        raise ValueError('Runtime imports exceed the minimal os/pathlib audit scope')
    hashes = []
    for _ in range(runs):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'output'
            output.mkdir()
            environment = os.environ.copy()
            environment['MAKEFUN_OUTPUT_DIR'] = str(output)
            process = subprocess.run([sys.executable, '-I', str(entry)], cwd=entry.parent,
                                     env=environment, capture_output=True, timeout=10)
            if process.returncode:
                raise ValueError('Entry execution failed: ' + process.stderr.decode('utf-8', errors='replace'))
            if process.stdout or process.stderr:
                raise ValueError('Entry produced unexpected stdout/stderr')
            if sorted(path.name for path in output.iterdir()) != ['entry.txt']:
                raise ValueError('Expected exactly output/entry.txt')
            data = (output / 'entry.txt').read_bytes()
            if data != expected:
                raise ValueError('Output differs from selected text')
            hashes.append(hashlib.sha256(data).hexdigest())
    if len(set(hashes)) != 1:
        raise ValueError('Output is not deterministic')
    return {'runs': runs, 'unique_hashes': len(set(hashes)), 'sha256': hashes[0],
            'characters': len(text), 'bytes': len(expected), 'encoding': 'UTF-8',
            'python': sys.version.split()[0], 'runtime_imports': sorted(imports),
            'limitations': 'Local macOS process test, not Linux sandbox or sealed judge; source still needs manual network audit'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entry', type=Path, required=True)
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.entry, args.expected.read_bytes(), runs=20)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
