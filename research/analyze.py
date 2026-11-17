"""Analyze recorded agent opinions; never represents an official GLM score."""

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import random
import statistics


def call_score(winner, margin):
    if winner not in ('A', 'B') or type(margin) is not int or not 1 <= margin <= 5:
        raise ValueError('Expected winner A/B and integer margin 1..5')
    return .5 + (margin / 10 if winner == 'A' else -margin / 10)


def games_from(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['pair_id']].append(row)
    games, rejected = [], []
    for pair_id, votes in groups.items():
        try:
            if len(votes) != 2:
                raise ValueError('Game requires exactly two recorded opinions')
            first, second = votes
            if (first['a'], first['b']) != (second['b'], second['a']):
                raise ValueError('Presentation orders must be reversed')
            if first['judge'] == second['judge'] or first['a'] == first['b']:
                raise ValueError('Distinct reviewers and candidates required')
            score = (call_score(first['winner'], first['margin']) +
                     1 - call_score(second['winner'], second['margin'])) / 2
            games.append((first['a'], first['b'], score))
        except (KeyError, ValueError) as error:
            rejected.append({'pair_id': pair_id, 'reason': str(error)})
    return games, rejected


def probability(delta):
    return 1 / (1 + math.exp(-max(-40, min(40, delta))))


def fit(ids, games):
    """Ridge-regularized fractional Bradley–Terry, lambda=.25, zero prior."""
    theta = dict.fromkeys(ids, 0.)
    edges = defaultdict(list)
    for a, b, score in games:
        if a not in theta or b not in theta or a == b or not 0 <= score <= 1:
            raise ValueError('Unknown candidate or invalid score')
        edges[a].append((b, score))
        edges[b].append((a, 1 - score))
    for _ in range(500):
        change = 0.
        for a in ids:
            gradient, information = -.25 * theta[a], .25
            for b, score in edges[a]:
                p = probability(theta[a] - theta[b])
                gradient += score - p
                information += p * (1 - p)
            step = max(-1, min(1, gradient / information))
            theta[a] += step
            change = max(change, abs(step))
        if change < 1e-8:
            break
    return theta


def wilson(wins, trials):
    if not 0 <= wins <= trials:
        raise ValueError('Invalid binomial counts')
    if not trials:
        return 0, 1
    z = 1.959963984540054
    p = wins / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    radius = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return max(0, center - radius), min(1, center + radius)


def percentile(values, p):
    values = sorted(values)
    position = (len(values) - 1) * p
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def summarize(ids, rows, bootstrap=200, seed=1154652979):
    games, rejected = games_from(rows)
    if not games:
        raise ValueError('No complete reversed-order games')
    theta = fit(ids, games)
    active_ids = {candidate for a, b, _ in games for candidate in (a, b)}
    elo = dict.fromkeys(ids, 1500.)
    observations = defaultdict(list)
    opponents = defaultdict(set)
    for a, b, score in games:
        delta = 20 * (score - 1 / (1 + 10 ** ((elo[b] - elo[a]) / 400)))
        elo[a] += delta
        elo[b] -= delta
        observations[a].append(score)
        observations[b].append(1 - score)
        opponents[a].add(b)
        opponents[b].add(a)
    rng = random.Random(seed)
    draws = defaultdict(list)
    for _ in range(bootstrap):
        sample = fit(ids, rng.choices(games, k=len(games)))
        for candidate in ids:
            draws[candidate].append(sample[candidate])
    rankings = []
    for candidate in ids:
        scores = observations[candidate]
        wins = sum(s > .5 + 1e-10 for s in scores)
        losses = sum(s < .5 - 1e-10 for s in scores)
        decisive = wins + losses
        rankings.append({
            'id': candidate, 'bt_log_strength': theta[candidate],
            'bt_expected_share_vs_pool': statistics.mean(probability(theta[candidate] - theta[b]) for b in active_ids if b != candidate) if scores else None,
            'elo_exploratory': elo[candidate], 'games': len(scores),
            'unique_opponents': len(opponents[candidate]), 'wins': wins, 'losses': losses,
            'ties': len(scores) - decisive,
            'observed_decisive_win_rate': wins / decisive if decisive else None,
            'wilson_95_descriptive': wilson(wins, decisive),
            'bt_strength_bootstrap_95': [percentile(draws[candidate], .025), percentile(draws[candidate], .975)] if scores else None,
            'data_informed': bool(scores),
            'eliminated': False,
            'elimination_reason': 'Insufficient independent evidence for irreversible elimination',
        })
    rankings.sort(key=lambda row: row['bt_log_strength'], reverse=True)
    valid_votes = []
    rejected_ids = {row['pair_id'] for row in rejected}
    for row in rows:
        if row['pair_id'] in rejected_ids:
            continue
        try:
            call_score(row.get('winner'), row.get('margin'))
            valid_votes.append(row)
        except ValueError:
            pass
    by_judge = defaultdict(list)
    for row in valid_votes:
        by_judge[row['judge']].append(row['winner'] == 'A')
    return {
        'label': 'Codex agent proxy; not GLM, official practice, or final performance',
        'method': 'Fractional Bradley–Terry with L2=.25; two reversed opinions per game; Elo K=20 in recorded order',
        'limitations': [
            'Each reviewer supplies many judgments in one context; judgments are correlated.',
            'Different reviewers see reversed order: position and reviewer effects are confounded.',
            'Wilson and pair-cluster bootstrap intervals are descriptive, not calibrated GLM probability bounds.',
            'Bootstrap resamples pair games; sparse or disconnected samples are stabilized by the stated prior.',
            'Candidate selection uses development data; fresh held-out comparisons remain necessary.',
        ],
        'bootstrap': {'replicates': bootstrap, 'seed': seed, 'unit': 'complete pair game'},
        'external_api_cost_usd': 0, 'complete_games': len(games),
        'valid_opinions': len(valid_votes), 'rejected_games': rejected,
        'position_bias': {'overall_A_win_share': statistics.mean(r['winner'] == 'A' for r in valid_votes),
                          'by_reviewer_A_win_share': {k: statistics.mean(v) for k, v in by_judge.items()}},
        'rankings': rankings,
    }


def adaptive_pairs(report, count=40, round_id='adaptive'):
    candidates = report['rankings']
    allocated = defaultdict(int)
    pairs = []
    used = set()
    for _ in range(count):
        opportunities = []
        for i, a in enumerate(candidates):
            for b in candidates[i + 1:]:
                key = tuple(sorted((a['id'], b['id'])))
                if key in used:
                    continue
                coverage = max(a['games'] + allocated[a['id']], b['games'] + allocated[b['id']])
                uncertainty = sum((r.get('bt_strength_bootstrap_95') or [-1, 1])[1] -
                                  (r.get('bt_strength_bootstrap_95') or [-1, 1])[0] for r in (a, b))
                closeness = abs(a['bt_log_strength'] - b['bt_log_strength']) / (1 + uncertainty)
                opportunities.append(((coverage, allocated[a['id']] + allocated[b['id']], closeness), a, b, key))
        if not opportunities:
            break
        _, a, b, key = min(opportunities, key=lambda item: item[0])
        used.add(key)
        pairs.append({'pair_id': '%s-%03d' % (round_id, len(pairs) + 1), 'a': a['id'], 'b': b['id'], 'split': 'development'})
        allocated[a['id']] += 1
        allocated[b['id']] += 1
    return pairs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', type=Path, default=Path(__file__).with_name('candidates.jsonl'))
    parser.add_argument('--votes', nargs='+', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--bootstrap', type=int, default=200)
    args = parser.parse_args()
    if args.bootstrap < 20:
        parser.error('Use at least 20 bootstrap replicates')
    candidates = [json.loads(line) for line in args.candidates.read_text().splitlines() if line.strip()]
    ids = [row['id'] for row in candidates]
    if len(ids) != len(set(ids)) or len(ids) < 2:
        parser.error('Need at least two unique candidates')
    votes = [json.loads(line) for path in args.votes for line in path.read_text().splitlines() if line.strip()]
    report = summarize(ids, votes, args.bootstrap)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    args.out.with_name(args.out.stem + '-next-pairs.json').write_text(json.dumps(adaptive_pairs(report, round_id=args.out.stem + '-next'), indent=2) + '\n')
    print('%d complete proxy games; %d rejected' % (report['complete_games'], len(report['rejected_games'])))


if __name__ == '__main__':
    main()
