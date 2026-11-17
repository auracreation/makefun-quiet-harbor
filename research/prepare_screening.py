"""Freeze a balanced public-opponent screen and reserve untouched opponents."""

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random


def main():
    research = Path(__file__).resolve().parent
    read_rows = lambda name: [json.loads(line) for line in (research / name).read_text().splitlines() if line.strip()]
    candidates = read_rows('candidates.jsonl') + read_rows('candidates-additional.jsonl')
    assert len(candidates) == 120
    assert len({row['id'] for row in candidates}) == 120
    assert len({row['text'] for row in candidates}) == 120
    assert all(1 <= len(row['text']) <= 1000 and row['text'].strip() for row in candidates)
    competitors = [row for row in read_rows('competitors.jsonl') if row['snapshot'] == 'current']
    assert len({row['submission_id'] for row in competitors}) == len(competitors)
    dev_ranks = {1, 3, 5, 6, 8, 10}
    pool = [{'id': row['id'], 'text': row['text'], 'provenance': 'original candidate'} for row in candidates]
    development = []
    for row in competitors:
        identifier = 'PUB-' + hashlib.sha256(row['submission_id'].encode()).hexdigest()[:10]
        split = 'development' if row['rank'] in dev_ranks else 'held_out'
        pool.append({'id': identifier, 'artifact_path': row['artifact_path'], 'sha256': row['sha256'],
                     'source_url': row['source_url'], 'provenance': 'public competitor', 'split': split})
        if split == 'development':
            development.append(identifier)
    assert len(development) == 6
    (research / 'evaluation-pool.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in pool))
    rng = random.Random(1794922050)
    combinations = list(itertools.combinations(sorted(development), 2))
    for batch, group in [('a', candidates[:60]), ('b', candidates[60:])]:
        opponents = combinations * 4
        rng.shuffle(opponents)
        pairs = []
        for row, foes in zip(group, opponents):
            for foe in foes:
                a, b = row['id'], foe
                if rng.getrandbits(1):
                    a, b = b, a
                pairs.append({'pair_id': 'screen-%s-%03d' % (batch, len(pairs)+1), 'a': a, 'b': b, 'split': 'development'})
        rng.shuffle(pairs)
        counts = Counter(foe for foes in opponents for foe in foes)
        assert len(pairs) == 120 and set(counts.values()) == {20}
        for reverse in (False, True):
            schedule = [{**p, 'a': p['b'], 'b': p['a']} for p in pairs] if reverse else pairs
            suffix = '-reversed' if reverse else ''
            (research / ('schedule-screen-%s%s.json' % (batch, suffix))).write_text(json.dumps(schedule, indent=2) + '\n')
    print('120 original candidates; six balanced development competitors; %d reserved public opponents' % (len(competitors)-6))
    print('Two batches, each120 games; candidate two distinct public opponents; each development opponent20 games per batch')


if __name__ == '__main__':
    main()
