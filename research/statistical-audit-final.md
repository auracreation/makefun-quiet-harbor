# Independent final statistical audit

Reviewed `analyze.py`, `analyze_heldout.py`, the analysis tests, `heldout-design.json`, and `methodology.md`. Ran all 23 tests successfully and additional synthetic checks. No candidate, champion, analysis implementation, or verdict files were edited. After the parent completed decoding, I also checked `heldout-results.json`. No raw held-out verdicts or held-out texts were read; no external API calls were made.

**Assessment:** the current arithmetic and aggregation support an honest descriptive proxy comparison. I found no mathematical blocker to using a complete, schedule-validated run for editorial selection. The analysis cannot establish a 99.5% preference rate or an official GLM performance improvement. The meaningful remaining issues concern completeness validation, dependence, and selection inference.

## Findings in priority order

### Resolved — Incomplete, unexpected and duplicated held-out coverage is rejected

The revised `require_coverage` checks every registered finalist/opponent combination and all finalist head-to-head pairs before `main` writes a summary. Missing whole matchups, unknown candidate pairs and duplicated unordered pairs now raise a validation error. `main` also refuses any group rejected during four-opinion collapse. This closes the meaningful completeness gap from the first audit pass.

Verified independently with four synthetic finalists and 21 opponents: exactly 90 matchups pass; removing one, adding an unknown opponent, or duplicating a matchup each fails with the appropriate counts. The new regression test checks the same cases on a smaller complete graph. The registered frozen pool and finalist metadata remain the definition of the expected design. The decoded report subsequently passed the 90-matchup/360-opinion coverage checks described below; raw opinion rows were not reread.

### P2 — Descriptive intervals must not become population or finalist-superiority claims

`analyze_heldout.py`, per-opponent summary and limitations; `analyze.py` bootstrap and Wilson summaries

Collapsing four opinions into one unique matchup is the right unit for the opponent summaries. It prevents 360 presentations or 180 nominal games from masquerading as independent trials. Nonetheless, the 90 matchups share only two reviewer contexts, and the 21 strong opponents are deliberately selected rather than randomly sampled. Resampling opponents conditions on those reviewer opinions and does not measure fresh-reviewer variation, model uncertainty, or GLM variability. Wilson likewise does not acquire calibrated coverage merely because its denominator is now unique opponents.

The report explicitly labels both intervals descriptive and disclaims calibrated GLM confidence; preserve those qualifications when presenting results. The limitation also applies to population claims about Codex proxy reviewers. A point-degenerate opponent bootstrap range can be perfectly correct as empirical resampling when all observed scores match; it is not proof of certainty about future opinions.

The script gives separate bootstrap intervals for each finalist. Because finalists share opponents, these are not a paired difference analysis. Overlap or non-overlap must not be used as a significance test of one finalist beating another. If a descriptive difference range is useful, resample the same opponent IDs jointly and compute the mean score difference on each draw. This would remain conditional and descriptive under the two shared contexts.

**Not a blocker:** the current labels permit honest finite-pool summaries. No additional model calls or fictitious independent replications are needed to finish that descriptive task.

### P2 — Selecting among four finalists uses the held-out evidence for selection

`heldout-design.json` promotion rule; `methodology.md` stages and separation

Fresh reviewers, frozen candidate texts, and opponents excluded from development comparisons provide a meaningful check against development overfitting. The method also acknowledges that the parent may have seen held-out public literary content, so these opponents are held out from comparative optimization results rather than guaranteed unseen content.

If the eventual champion is selected among these four using this run, its best observed held-out result is subject to winner-selection optimism. It is valid to say the run supports choosing that text within this fixed pool; it is not an untouched confirmatory estimate for the selected winner. Further revisions tuned to losses would also turn this pool into development data. Preserve the four finalists' full results and losses, identify the selection rule, and avoid interpreting the selected winner's individual interval as a post-selection guarantee.

The parent now plans to challenge the finalist using the strong independent baselines exposed by this run. This is a sensible response to retained losses, but makes this first held-out pool diagnostic training for that next selection. New challengers or revisions must not be advertised as freshly validated by this same pool; another fresh pool is needed for that claim. The frozen original four-candidate results remain valid descriptions of the run that actually occurred.

**Not a blocker:** the existing conservative promotion rule and immutable snapshots are suitable for an editorial decision. No arbitrary new approval or performance threshold is warranted by this audit.

### P3 — Missing grouping identifiers fail abruptly rather than receiving a rejection record

`analyze_heldout.py` and `analyze.py`, initial grouping loops

A missing `comparison_id` or `pair_id` raises `KeyError` before the guarded per-group validation. Within identified groups, missing judges, invalid margins, inconsistent candidates, duplicate orientations, wrong reviewer count, and incomplete groups are excluded rather than filled with invented neutral scores. The earlier rejected-group contamination in `analyze.py` is fixed: accepted-opinion diagnostics now skip rejected group IDs, and the new regression test covers it.

Failing on a missing grouping key does not silently corrupt results, so this is a robustness issue rather than an inference blocker for validated records. A minimal boundary test should either require a clear validation error or attach a row-number rejection; no broad schema framework is necessary.

### P3 — Final documentation should distinguish the development and held-out order designs

The development report correctly warns that different reviewers saw reversed orders, confounding reviewer and position effects. The held-out design improves this: each reviewer sees each candidate pair in both orders. Its `winner_changed_on_reversal` and balanced A-win fractions are useful descriptive order-sensitivity diagnostics. They still combine presentation sensitivity, stochastic preference changes, and possible context carryover; they are not a clean causal effect estimate from independent sessions.

`methodology.md` still describes the held-out phase as pending and says finalists are not selected, while `heldout-design.json` names four finalists. Update the final methodology to state the frozen stage and interpretation accurately once the run is checked. Preserve the distinction between unique matchups, nominal two-opinion games, and raw opinions.

## Arithmetic and implementation verified

- The official disclosed margin transformation is implemented correctly: the winner receives .5 plus .1 times its integer margin. Reverse presentations are converted to a canonical candidate orientation before averaging.
- Held-out `collapse` requires four opinions for the same unordered pair, exactly two reviewers, and both orientations within each reviewer. Only fully accepted groups enter its diagnostics. Four correctly oriented synthetic opinions with margins 3 and 1 collapsed to a single score of .7 as expected.
- With the frozen complete design, 4×21 external pairings plus six finalist pairings equals 90 unique matchups. Two reviewers times two orientations equals 360 opinions. Calling this 180 nominal two-opinion games is compatible with the scoring protocol, but 180 is not the primary independent-opponent denominator.
- Each finalist/opponent pair receives one averaged score. Source sections weight opponents equally; diagnostic negatives are excluded by constructing `opponent_types` only from public and `heldout_strong_baseline` records. Finalist head-to-head scores are kept separate from the 21-opponent primary pool.
- Wins, ties and losses are derived from the averaged margin share around .5. `observed_win_fraction_all_opponents` counts ties in the denominator; `decisive_win_fraction` and its Wilson interval omit ties. `mean_margin_share` is a separate, correctly named fractional-score quantity. None equals an official house-anchor rating.
- The Wilson formula is correct. Even under an ideal independent binomial interpretation, 21 wins in 21 trials has a two-sided 95% Wilson lower bound of approximately .845361, not .995. The methodology's ideal all-win requirements of 765 for .995 and 3,838 for .999 were numerically verified. The current batched proxy design does not meet that ideal independence assumption.
- The regularized fractional Bradley–Terry implementation remains correct for its stated objective; Elo is explicitly exploratory and order dependent. These are two summaries of the same proxy evidence, not independent replications. Unseen candidates now have no empirical bootstrap interval and no expected-share estimate.
- Both report labels clearly say Codex proxy and disavow GLM/official performance. The raw model names and zero external API spend are protocol/provenance declarations, not fabricated paid-model usage. No official scorer call, GLM sample, or target-model probability is created by these scripts.

## Verification record and remaining scope

Ran `python3 -m unittest discover -s outputs/quiet-harbor/research -p 'test_*.py' -v`: **23/23 passed**. These include nine development-analysis tests, four held-out analysis tests, collection-security tests and runtime-output checks. Additional in-memory synthetic checks verified asymmetric-margin collapse, fixed-design 90-matchup coverage, rejection of missing/unknown/duplicated matchups, missing-ID failure, and the Wilson numerical claims. No network model calls were used.

After decoding, I checked the saved report independently: 90 unique matchups, 360 raw opinions, no rejected groups, complete coverage, six distinct finalist head-to-head pairs, and 21 external opponents per finalist. Each source subsection had the expected 15 public or six independent opponents; wins+ties+losses matched its denominator. All recorded per-opponent shares were bounded, all section Wilson intervals matched recomputation, and the primary mean shares matched the stored per-opponent values.

The observed primary results were R05 14W/2D/5L, V07 14W/4D/3L, V08 16W/3D/2L, and M05 14W/2D/5L, each against 21 opponents. V08's public subsection was 13W/1D/1L; its independent subsection was 3W/2D/1L. Its independent scores retained HOLD-H06 as a loss (.4) and HOLD-H01/HOLD-H03 as ties (.5). Thus even the selected point-estimate leader was neither unbeaten nor established at a near-perfect preference rate. These checks verify internal report arithmetic and retained failures, not a fresh evaluation of the literature or an independent replay of the raw reviewer judgments.

Raw schedule-row correspondence and detailed reversal diagnoses were not re-audited in this pass. The remaining scientific limit is substantive: two correlated proxy reviewer contexts and a fixed selected opponent pool cannot establish GLM performance or a calibrated near-perfect preference rate.
