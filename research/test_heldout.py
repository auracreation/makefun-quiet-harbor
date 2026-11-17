import unittest

import analyze_heldout


class HeldoutTests(unittest.TestCase):
    def test_four_opinions_form_one_unique_matchup(self):
        rows = []
        for judge in ('one', 'two'):
            rows.extend([
                dict(comparison_id='c', a='a', b='b', winner='A', margin=2, judge=judge),
                dict(comparison_id='c', a='b', b='a', winner='B', margin=2, judge=judge),
            ])
        games, rejected, bias = analyze_heldout.collapse(rows)
        self.assertEqual(rejected, [])
        self.assertEqual(len(games), 1)
        self.assertAlmostEqual(games[0][2], .7)
        self.assertEqual(bias['one']['winner_changed_on_reversal'], 0)

    def test_always_A_is_detected_as_order_sensitive(self):
        rows = []
        for judge in ('one', 'two'):
            rows.extend([
                dict(comparison_id='c', a='a', b='b', winner='A', margin=2, judge=judge),
                dict(comparison_id='c', a='b', b='a', winner='A', margin=2, judge=judge),
            ])
        games, rejected, bias = analyze_heldout.collapse(rows)
        self.assertAlmostEqual(games[0][2], .5)
        self.assertEqual(bias['one']['winner_changed_on_reversal'], 1)

    def test_incomplete_matchup_is_not_counted(self):
        games, rejected, bias = analyze_heldout.collapse([
            dict(comparison_id='c', a='a', b='b', winner='A', margin=2, judge='one')])
        self.assertEqual(games, [])
        self.assertEqual(len(rejected), 1)

    def test_incomplete_unknown_or_duplicate_coverage_is_rejected(self):
        expected = [('a', 'b', .6), ('a', 'x', .6), ('b', 'x', .6)]
        analyze_heldout.require_coverage(['a', 'b'], {'x': 'public'}, expected)
        for games in (expected[:-1], expected+[('a', 'unknown', .6)], expected+[expected[0]]):
            with self.assertRaises(ValueError):
                analyze_heldout.require_coverage(['a', 'b'], {'x': 'public'}, games)


if __name__ == '__main__':
    unittest.main()
