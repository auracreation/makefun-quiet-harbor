import math
import unittest

import analyze


class TournamentTests(unittest.TestCase):
    def test_margin_and_reversal(self):
        self.assertAlmostEqual(analyze.call_score('A', 1), .6)
        self.assertEqual(analyze.call_score('B', 5), 0)
        with self.assertRaises(ValueError):
            analyze.call_score('tie', 1)

    def test_bradley_terry_orders_winner(self):
        fit = analyze.fit(['a', 'b', 'c'], [('a', 'b', .9), ('b', 'c', .8), ('a', 'c', .9)])
        self.assertGreater(fit['a'], fit['b'])
        self.assertGreater(fit['b'], fit['c'])
        self.assertTrue(all(math.isfinite(v) for v in fit.values()))

    def test_balanced_cycle_is_equal(self):
        fit = analyze.fit(['a', 'b', 'c'], [('a', 'b', .8), ('b', 'c', .8), ('c', 'a', .8)])
        self.assertLess(max(fit.values()) - min(fit.values()), 1e-6)

    def test_wilson_has_uncertainty_at_perfect_record(self):
        low, high = analyze.wilson(3, 3)
        self.assertGreater(low, 0)
        self.assertLess(low, .5)
        self.assertAlmostEqual(high, 1)
        self.assertEqual(analyze.wilson(0, 0), (0, 1))

    def test_reversed_games_are_averaged_not_counted_twice(self):
        rows = [dict(pair_id='p', a='a', b='b', winner='A', margin=3, judge='one'),
                dict(pair_id='p', a='b', b='a', winner='B', margin=1, judge='two')]
        games, rejected = analyze.games_from(rows)
        self.assertEqual(rejected, [])
        self.assertEqual(len(games), 1)
        self.assertAlmostEqual(games[0][2], .7)

    def test_incomplete_and_duplicate_judgments_do_not_become_games(self):
        row = dict(pair_id='p', a='a', b='b', winner='A', margin=3, judge='one')
        games, rejected = analyze.games_from([row, row])
        self.assertEqual(games, [])
        self.assertEqual(len(rejected), 1)

    def test_adaptive_round_covers_underexplored_candidates(self):
        report = {'rankings': [{'id': str(i), 'bt_log_strength': 1-i/100, 'games': 2}
                               for i in range(60)]}
        pairs = analyze.adaptive_pairs(report, count=40, round_id='second')
        self.assertEqual(len(pairs), 40)
        self.assertEqual(len({p[k] for p in pairs for k in ('a', 'b')}), 60)
        self.assertTrue(all(p['pair_id'].startswith('second-') for p in pairs))

    def test_unseen_candidate_has_no_empirical_bootstrap_interval(self):
        rows = [dict(pair_id='p', a='a', b='b', winner='A', margin=3, judge='one'),
                dict(pair_id='p', a='b', b='a', winner='B', margin=1, judge='two')]
        report = analyze.summarize(['a', 'b', 'c'], rows, bootstrap=20)
        unseen = next(r for r in report['rankings'] if r['id']=='c')
        self.assertIsNone(unseen['bt_strength_bootstrap_95'])
        self.assertIsNone(unseen['bt_expected_share_vs_pool'])

    def test_rejected_opinions_do_not_enter_position_diagnostics(self):
        rows = [dict(pair_id='p', a='a', b='b', winner='A', margin=3, judge='one'),
                dict(pair_id='p', a='b', b='a', winner='B', margin=1, judge='two'),
                dict(pair_id='incomplete', a='a', b='b', winner='A', margin=5),
                dict(pair_id='broken', a='a', b='b', winner='A', margin=5),
                dict(pair_id='broken', a='b', b='a', winner='A', margin=5)]
        report = analyze.summarize(['a', 'b'], rows, bootstrap=20)
        self.assertEqual(report['valid_opinions'], 2)
        self.assertEqual(len(report['rejected_games']), 2)
        self.assertEqual(report['position_bias']['overall_A_win_share'], .5)


if __name__ == '__main__':
    unittest.main()
