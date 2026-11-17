"""Hydrate frozen public artifacts without changing research metadata.

From a clone: python3 research/collect_public_competitors.py --scratch /tmp/quiet-harbor-artifacts
Reads the frozen competitor provenance files beside this script. Only the
explicit scratch directory receives files; valid existing artifacts need no network.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

RESEARCH = Path(__file__).resolve().parent
ORIGIN = 'https://make.fun'
SUBMISSION_ID = r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}'


class SameHostRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        artifact_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def artifact_url(value):
    url = urljoin(ORIGIN, value)
    parsed = urlparse(url)
    if (parsed.scheme != 'https' or parsed.netloc != 'make.fun'
            or not re.fullmatch(rf'/api/submissions/{SUBMISSION_ID}/artifact\.txt', parsed.path)
            or parsed.query not in ('', 'phase=dev') or parsed.fragment or parsed.params):
        raise ValueError('Refusing non-public artifact URL')
    return url


def hydrate(record, scratch, opener):
    sid, expected = record['submission_id'], record['sha256']
    if not re.fullmatch(SUBMISSION_ID, sid) or not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('Invalid artifact filename components')
    url = artifact_url(record['source_url'])
    if urlparse(url).path != f'/api/submissions/{sid}/artifact.txt':
        raise ValueError('Artifact URL does not match submission ID')
    size, characters = record['bytes'], record['characters']
    if type(size) is not int or type(characters) is not int or not 1 <= size <= 4000 or not 1 <= characters <= 1000:
        raise ValueError('Invalid artifact length metadata')
    dest = scratch / f'{sid}-{expected[:12]}.txt'
    if dest.is_symlink():
        raise ValueError('Refusing artifact cache symlink')
    cached = dest.exists()
    if cached:
        with dest.open('rb') as source:
            raw = source.read(4001)
    else:
        with opener.open(Request(url, headers={'User-Agent': 'makefun-public-research/1'}), timeout=30) as response:
            raw = response.read(4001)
    if len(raw) > 4000 or len(raw) != size or sha256(raw).hexdigest() != expected:
        raise ValueError(f'Artifact size or SHA-256 mismatch: {sid}')
    text = raw.decode('utf-8')
    if len(text) > 1000 or len(text) != characters:
        raise ValueError(f'Artifact character count mismatch: {sid}')
    if not cached:
        with dest.open('xb') as target:
            target.write(raw)
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch', required=True, type=Path, help='Only directory used for artifact files')
    args = parser.parse_args()
    scratch = args.scratch.expanduser().resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    opener = build_opener(SameHostRedirect())
    seen = set()
    for name in ('competitors.jsonl', 'competitors-refresh.jsonl', 'heldout-public-second.jsonl'):
        with (RESEARCH / name).open() as source:
            for line in source:
                if line.strip():
                    record = json.loads(line)
                    hydrate(record, scratch, opener)
                    seen.add((record['submission_id'], record['sha256']))
    print(f'Verified {len(seen)} frozen public artifacts in {scratch}; metadata unchanged')


if __name__ == '__main__':
    main()
