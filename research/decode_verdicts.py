"""Check recorded anonymous verdicts against the frozen schedule and decode IDs."""

import argparse
import json
from pathlib import Path

from analyze import call_score


def decode(research, stage, side):
    suffix = '-reversed' if side == 'two' else ''
    schedule = json.loads((research / f'schedule-{stage}{suffix}.json').read_text())
    book = json.loads((research / f'{stage}-codebook.json').read_text())
    source = f'verdicts-{stage}-{side}-raw.jsonl'
    rows = [json.loads(line) for line in (research / source).read_text().splitlines()]
    keys = ['pair_id', 'a', 'b']
    if schedule and 'comparison_id' in schedule[0]:
        keys.append('comparison_id')
    if len(rows) != len(schedule) or len({row['pair_id'] for row in rows}) != len(schedule):
        raise ValueError(f'{source} has missing or duplicate verdicts')
    decoded = []
    for actual, expected in zip(rows, schedule):
        if any(actual[key] != expected[key] for key in keys):
            raise ValueError(f'{source} differs from the frozen schedule')
        call_score(actual['winner'], actual['margin'])
        if not actual.get('reason', '').strip():
            raise ValueError(f'{source} contains a verdict without a reason')
        decoded.append(dict(actual, raw_a=actual['a'], raw_b=actual['b'],
                            a=book[actual['a']], b=book[actual['b']], source_file=source))
    return decoded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['challenge', 'heldout', 'recovery', 'fresh'])
    args = parser.parse_args()
    research = Path(__file__).resolve().parent
    decoded = {side: decode(research, args.stage, side) for side in ('one', 'two')}
    for side, rows in decoded.items():
        (research / f'verdicts-{args.stage}-{side}.jsonl').write_text(
            ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    print(f'Validated and decoded {sum(map(len, decoded.values()))} opinions')


if __name__ == '__main__':
    main()
