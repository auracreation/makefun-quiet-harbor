# Statistical integrity audit

Scope: the revised `outputs/quiet-harbor/research/analyze.py`, its eight tests, and the initial schedule. Read-only audit; no implementation or candidate edits. I did not read reviewer two's verdicts or any combined results. No external API calls.

The scoring and descriptive estimators are mathematically consistent. The revised adaptive scheduler addresses the two consequential scheduling issues found on the first pass. No remaining P1 finding applies to the currently validated workflow. The main remaining risks are malformed-input handling and interpreting descriptive resampling as calibrated inference.

## Resolved findings verified in revised code

- **Premature top-16 restriction:** the scheduler now considers all candidates and prioritizes coverage before heuristic closeness. A synthetic 60-candidate initial round with two games per candidate produced 40 pairs covering all 60. No candidate is marked eliminated. This is an appropriate conservative safeguard under sparse evidence.
- **Round-ID collisions:** the scheduler accepts a round prefix and the CLI derives it from the output stem. Two synthetic rounds with distinct prefixes had zero ID overlap. Users must continue using distinct report stems for distinct rounds; the default callable prefix alone cannot guarantee global uniqueness.
- **Zero-game bootstrap certainty:** an unobserved candidate now has `bt_strength_bootstrap_95: null` and `data_informed: false`, rather than a misleading [0,0] empirical interval.
- **Zero requested pair count:** now correctly produces zero pairs.

## Remaining prioritized findings

### P2 — Malformed or rejected opinions can crash or contaminate presentation summaries

Locations: `games_from` grouping and `summarize`'s separate `valid_votes` pass.

`valid_votes` checks only winner and margin, independently of whether the row belongs to an accepted game. A lone opinion in a rejected incomplete game still enters `valid_opinions` and `overall_A_win_share`. Reproduced: one accepted game plus one rejected lone A opinion leaves one complete game but reports three valid opinions and A share 2/3. This could be a useful raw-call statistic if named explicitly; it is not an accepted-game diagnostic.

A record with a valid winner/margin but no judge is rejected by `games_from`, then crashes `summarize` with `KeyError: 'judge'` in that second pass. A missing `pair_id` crashes outside the guarded block even earlier. Candidate membership is validated only later by `fit`, so a complete unknown-candidate pair aborts the entire report instead of appearing among rejected games.

Smallest worthwhile change: validate the minimal full row schema once, retain rejection reasons, and derive accepted-game diagnostics from accepted records. If raw valid-score opinions are wanted, report them separately. Current reviewer files were validated outside this analyzer, so this is not evidence that the present results contain malformed records.

### P2 — Bootstrap ranges are design sensitivity, not confidence bounds

Locations: `summarize`'s pair resampling, bootstrap interval and limitations.

Resampling a complete reversed-order game is better than treating its two opinions as independent samples. It still ignores the larger correlation unit. Each reviewer supplied all judgments in a shared context, so there are only two reviewer sessions, not sixty independent reviewer experiences. Repeated matchups in later rounds can add dependence. Pair resampling cannot recover unseen reviewer/model variability from this design.

Sparse resamples can disconnect the graph and let the .25 L2 prior stabilize estimated strengths. The revised null interval for completely unobserved candidates fixes the most misleading edge case; prior influence remains for observed candidates with little information. Twenty allowed replicates also make 2.5th/97.5th percentiles highly sensitive to individual draws. Increasing the count improves Monte Carlo stability, not validity under correlated sessions or adaptive selection.

The existing explicit limitations make these acceptable exploratory ranges. Prefer a name such as descriptive resampling range, and state they are not calibrated confidence bounds for either a proxy-reviewer population or GLM outcomes. Do not use the ranges to certify elimination. The revised scheduler's range-scaled closeness is a sampling heuristic rather than a hypothesis test; describe it that way.

### P3 — A-win fractions do not isolate a position effect

Locations: `position_bias` and the reviewer/order limitation.

The fractions are accurate descriptive frequencies for the rows included. They do not identify position bias: the two reviewers see opposite orderings, so disagreement may reflect preference, presentation, or both. Adaptive schedules also tend to place the higher point estimate first because rankings are sorted; a reviewer's A share then reflects candidate strength allocation as well as any label tendency. Averaging opposite orders balances labels in the combined game but does not establish why the reviewers differed.

The current confounding warning is correct. Prefer naming the field presentation outcomes or attaching `position_effect_identifiable: false`. Actual identification would require both orderings within each reviewer under a counterbalanced design, ideally with fresh contexts. Do not claim such sessions or independent replicates occurred.

### P3 — Zero cost and proxy provenance are protocol assertions

Locations: report label, `external_api_cost_usd`, arbitrary vote-file loading.

The present protocol makes no external API calls, so zero external API spend is supported by the workflow. The reusable analyzer nevertheless unconditionally reports zero and Codex proxy provenance for any input files without verifying their backend/model metadata. It does not invent outcomes, but could misattribute later records.

Smallest worthwhile change: label zero as a protocol declaration with its source, or aggregate supplied cost evidence and leave missing usage unavailable. Validate or summarize input reviewer/model/backend provenance. Never manufacture token usage or GLM verdicts.

## Mathematical assessment

- **Margin score and reversal:** correct. Margin 1 maps to .6/.4 and margin 5 to 1/0. The reversed opinion is converted to the first candidate's orientation before averaging. One completed pair is one game, not two independent games.
- **Bradley–Terry:** the coordinate updates solve the fractional cross-entropy objective with a .25 quadratic penalty. The zero-centered ridge resolves additive non-identifiability and separation, including disconnected samples. On a three-candidate synthetic graph, maximum absolute score-equation residual was approximately 1.84e-9. This is a regularized proxy summary, not the sealed official estimator.
- **Pool score:** `bt_expected_share_vs_pool` is average fitted fractional score against the supplied pool. It is not probability of winning a whole game, raw win rate, or the official house-text rating. Its value changes when the comparison pool changes.
- **Elo:** K=20 update for fractional scores is correct and explicitly exploratory. Its dependence on recorded order is expected. It is another summary of the same evidence, not independent corroboration.
- **Wilson:** the formula is correct for the integer decisive-win counts supplied, with ties omitted and [0,1] for zero trials. Its target is decisive wins against sampled opponents, not fractional score or BT strength. Correlated judgments and heterogeneous/adaptively chosen opponents prevent the usual independent-binomial coverage interpretation. Keep the descriptive label.
- **Initial design:** the initial schedule is a connected cycle of 60 candidates and 60 games, exactly two opponents per candidate. This permits regularized comparison but gives very sparse local evidence. Opponent effects and the prior can materially alter rankings.
- **Sequential safeguard:** the revised scheduler retains all candidates and minimum-coverage exploration. Fresh held-out comparisons must remain unused in adaptive selection if called held out. With only these proxy sessions, editorial selection is warranted; a statistically established GLM improvement is not.

## Verification

`python3 -m unittest discover -s outputs/quiet-harbor/research -p test_analyze.py -v`: all eight tests passed against the revised code.

Additional synthetic checks verified the revised 60-candidate coverage, distinct-prefix ID uniqueness, count=0, unobserved interval handling and the remaining missing-judge failure. Earlier synthetic checks verified the BT score-equation residual and incomplete-opinion contribution to A share. Initial schedule connectivity and degree were checked directly. No combined ranking or reviewer-two result was read.

## Worthwhile minimal additional tests

1. Generate two adaptive rounds with distinct IDs; aggregate both rounds' complete synthetic opinions and verify every game survives.
2. Validate malformed/incomplete/unknown-candidate rows consistently without crashing or contaminating accepted-game diagnostics.
3. Check BT score-equation residual, candidate-order invariance and sign reversal when all game orientations reverse.
4. Check bootstrap determinism under a fixed seed, preserving the revised no-data/null-interval case.
5. Check exactly cancelling reverse opinions produce a tie, and Wilson's decisive denominator excludes it.
6. Test mixed evidence counts in adaptive scheduling, including a low-ranked underobserved candidate, so exploration remains protected beyond the equal-count initial case.

No implementation changes were made. Independent reviewer-session uncertainty, GLM judge performance and externally billed model usage were not tested; the current evidence cannot establish them.
