"""Freeze a fresh validation schedule and write the reviewers' anonymous texts."""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('finalists', nargs=3)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--texts', type=Path, required=True)
    args = parser.parse_args()
    research = Path(__file__).resolve().parent

    def read(name):
        return [json.loads(line) for line in (research / name).read_text().splitlines()]

    candidates = {row['id']: row['text'] for row in read('evaluation-pool-recovery.jsonl') if 'text' in row}
    public = read('heldout-public-second.jsonl')
    independent = read('heldout-fresh-independent.jsonl')
    earlier = {row['sha256'] for row in read('evaluation-pool.jsonl') if row.get('split') == 'development'}
    earlier.update(row['sha256'] for row in read('heldout-public-refresh.jsonl'))
    assert len(public) == 15 and len(independent) == 6
    assert len({row['sha256'] for row in public}) == len(public)
    assert all(row['sha256'] not in earlier for row in public)
    opponents = {row['id']: row['text'] for row in independent}
    for row in public:
        data = (args.artifacts / Path(row['artifact_path']).name).read_bytes()
        if sha256(data).hexdigest() != row['sha256']:
            raise ValueError(f"Public artifact hash mismatch for {row['id']}")
        opponents[row['id']] = data.decode('utf-8')
    assert len(set(args.finalists)) == 3
    texts = {**{id: candidates[id] for id in args.finalists}, **opponents}
    assert len(texts) == 24 and len(set(texts.values())) == 24
    rng = random.Random(1154652981)
    ids = list(texts)
    rng.shuffle(ids)
    book = {f'W{i:03d}': id for i, id in enumerate(ids, 1)}
    code = {id: alias for alias, id in book.items()}
    args.texts.write_text(''.join(json.dumps({'id': alias, 'text': texts[id]}, ensure_ascii=False) + '\n'
                                 for alias, id in book.items()))
    matchups = list(combinations(args.finalists, 2)) + [(a, b) for a in args.finalists for b in opponents]
    schedule = []
    for index, (a, b) in enumerate(matchups, 1):
        if rng.getrandbits(1):
            a, b = b, a
        comparison = f'fresh-{index:03d}'
        for replicate, (left, right) in enumerate(((a, b), (b, a)), 1):
            schedule.append({'pair_id': f'{comparison}-r{replicate}', 'comparison_id': comparison,
                             'a': code[left], 'b': code[right], 'split': 'fresh_held_out'})
    rng.shuffle(schedule)
    assert len(matchups) == 66 and len(schedule) == 132
    files = {'fresh-codebook.json': book, 'schedule-fresh.json': schedule,
             'schedule-fresh-reversed.json': [{**p, 'a': p['b'], 'b': p['a']} for p in schedule],
             'fresh-design.json': {'finalists': args.finalists, 'public_opponents': len(public),
                                   'independent_opponents': len(independent), 'matchups': len(matchups),
                                   'opinions': 2 * len(schedule), 'seed': 1154652981}}
    for name, data in files.items():
        (research / name).write_text(json.dumps(data, indent=2) + '\n')
    print(f'Froze {len(matchups)} unique matchups and {2 * len(schedule)} scheduled opinions')


if __name__ == '__main__':
    main()
