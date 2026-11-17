"""Collapse repeated held-out opinions by unique matchup, not by presentation."""

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import random
import statistics

from analyze import call_score, percentile, wilson


def collapse(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['comparison_id']].append(row)
    games, rejected, diagnostics = [], [], defaultdict(list)
    for identifier, votes in groups.items():
        try:
            if len(votes) != 4:
                raise ValueError('Four opinions required per unique matchup')
            candidate_pairs = {tuple(sorted((v['a'], v['b']))) for v in votes}
            if len(candidate_pairs) != 1:
                raise ValueError('Inconsistent candidates within matchup')
            a, b = next(iter(candidate_pairs))
            if a == b:
                raise ValueError('Self-comparison')
            reviewers = defaultdict(list)
            for vote in votes:
                call_score(vote['winner'], vote['margin'])
                reviewers[vote['judge']].append(vote)
            if len(reviewers) != 2:
                raise ValueError('Two reviewers required')
            local_diagnostics = {}
            for judge, observations in reviewers.items():
                if len(observations) != 2 or {v['a'] for v in observations} != {a, b}:
                    raise ValueError('Each reviewer needs both orientations')
                winners = [v['a'] if v['winner'] == 'A' else v['b'] for v in observations]
                local_diagnostics[judge] = (winners[0] != winners[1], sum(v['winner'] == 'A' for v in observations))
            score = statistics.mean(call_score(v['winner'], v['margin']) if v['a'] == a
                                    else 1 - call_score(v['winner'], v['margin']) for v in votes)
            games.append((a, b, score))
            for judge, diagnostic in local_diagnostics.items():
                diagnostics[judge].append(diagnostic)
        except (KeyError, ValueError) as error:
            rejected.append({'comparison_id': identifier, 'reason': str(error)})
    bias = {judge: {'matchups': len(values),
                    'winner_changed_on_reversal': sum(v[0] for v in values),
                    'A_win_share': sum(v[1] for v in values) / (2 * len(values))}
            for judge, values in diagnostics.items()}
    return games, rejected, bias


def require_coverage(finalists, opponent_types, games):
    expected = {tuple(sorted((a, b))) for a in finalists for b in opponent_types}
    expected.update(tuple(sorted(pair)) for pair in combinations(finalists, 2))
    observed = Counter(tuple(sorted((a, b))) for a, b, _ in games)
    missing = expected - set(observed)
    unexpected = set(observed) - expected
    duplicate = [pair for pair, count in observed.items() if count != 1]
    if missing or unexpected or duplicate:
        raise ValueError('Incomplete or invalid heldout coverage: %d missing, %d unexpected, %d duplicate matchups' %
                         (len(missing), len(unexpected), len(duplicate)))
    return {'complete': True, 'expected_unique_matchups': len(expected), 'observed_unique_matchups': len(observed)}


def summarize(finalists, opponent_types, games, seed=1794922052):
    scores = {id: defaultdict(list) for id in finalists}
    direct = []
    for a, b, score in games:
        if a in finalists and b in finalists:
            direct.append({'a': a, 'b': b, 'score_a': score})
        elif a in finalists and b in opponent_types:
            scores[a][b].append(score)
        elif b in finalists and a in opponent_types:
            scores[b][a].append(1-score)
    rng = random.Random(seed)
    result = {}
    for id in finalists:
        per_opponent = {foe: statistics.mean(values) for foe, values in scores[id].items()}
        sections = {}
        for label in ['all_strong', 'public', 'independent']:
            values = [s for foe, s in per_opponent.items() if label == 'all_strong' or opponent_types[foe] == label]
            if not values:
                sections[label] = None
                continue
            wins = sum(s > .5000001 for s in values)
            losses = sum(s < .4999999 for s in values)
            ties = len(values)-wins-losses
            boot = [statistics.mean(rng.choices(values, k=len(values))) for _ in range(2000)]
            sections[label] = {'unique_opponents': len(values), 'wins': wins, 'ties': ties, 'losses': losses,
                               'observed_win_fraction_all_opponents': wins/len(values),
                               'decisive_win_fraction': wins/(wins+losses) if wins+losses else None,
                               'wilson_95_decisive_descriptive': wilson(wins, wins+losses),
                               'mean_margin_share': statistics.mean(values),
                               'mean_share_opponent_bootstrap_95_descriptive': [percentile(boot, .025), percentile(boot, .975)]}
        result[id] = {'by_source': sections, 'per_opponent_margin_share': per_opponent}
    return {'label': 'Held-out Codex proxy; not GLM or official performance',
            'unit': 'One unique candidate/opponent matchup averaged across two reviewers and both orders',
            'limitations': ['Two shared reviewer contexts; four presentations are not four independent trials.',
                            'Opponent-cluster bootstrap and Wilson intervals are descriptive, not calibrated GLM confidence.',
                            'This fixed challenging pool is not a random sample of future opponents.'],
            'finalists': result, 'head_to_head': direct, 'bootstrap_seed': seed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fresh', action='store_true', help='Analyze the second, fresh validation pool')
    args = parser.parse_args()
    research = Path(__file__).resolve().parent
    stage = 'fresh' if args.fresh else 'heldout'
    public_file = 'heldout-public-second.jsonl' if args.fresh else 'heldout-public-refresh.jsonl'
    baseline_file = 'heldout-fresh-independent.jsonl' if args.fresh else 'heldout-pool.jsonl'
    rows = [json.loads(line) for side in ['one', 'two']
            for line in (research / f'verdicts-{stage}-{side}.jsonl').read_text().splitlines()]
    games, rejected, diagnostics = collapse(rows)
    design = json.loads((research / f'{stage}-design.json').read_text())
    public = [json.loads(line) for line in (research / public_file).read_text().splitlines()]
    independent = [json.loads(line) for line in (research / baseline_file).read_text().splitlines()
                   if json.loads(line)['role'] == 'heldout_strong_baseline']
    opponent_types = {**{row['id']: 'public' for row in public}, **{row['id']: 'independent' for row in independent}}
    if rejected:
        raise ValueError('Rejected heldout comparisons: ' + json.dumps(rejected))
    coverage = require_coverage(design['finalists'], opponent_types, games)
    report = summarize(design['finalists'], opponent_types, games)
    report.update(unique_matchups=len(games), raw_opinions=len(rows), rejected=rejected, position_diagnostics=diagnostics, coverage=coverage)
    (research / f'{stage}-results.json').write_text(json.dumps(report, indent=2)+'\n')
    (research / f'{stage}-collapsed-games.json').write_text(json.dumps(games, indent=2)+'\n')
    print('%d unique heldout matchups; %d rejected; %d raw opinions' % (len(games), len(rejected), len(rows)))


if __name__ == '__main__':
    main()
