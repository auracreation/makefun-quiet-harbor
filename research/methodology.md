# Evaluation methodology and inference limits

## Fixed budget and measurement sources

The user authorized agent reviewers and $0 on external APIs. All local judgments are therefore Codex agent opinions, with the recorded model gpt-6.1-sol. They are not GLM-5.3-Flash responses, official practice grades, or final make.fun scores. The disclosed make.fun rubric guides the reviewers; the house's appended answer-format instruction is not fully disclosed.

Each reviewer reads a schedule with A/B orientation, evaluates the texts directly, and writes a reason, winner and integer margin. Scripts transcribe, validate and analyze opinions; they do not assign winners from text features. Raw verdict files and authentic parent/child session logs preserve provenance. Reading many pairs in one context creates dependencies; no claim of one independent model request per row is made.

## Datasets and separation

- Initial sixty original drafts: A–F, ten per family, 54–278 characters.
- Additional sixty original drafts: G–R, five per family, 69–515 characters. Their author did not read public competitor texts or scores.
- Twenty-one current public competitor artifacts collected at 14:16:20 UTC; six development opponents chosen from ranks 1, 3, 5, 6, 8 and 10. All others reserved for held-out comparisons. Public artifacts are identified by source URL and verified SHA-256; they are not original candidates.
- Six independently authored strong held-out baselines and four separately labeled diagnostic negatives. Frozen file SHA-256: 6523f1807bad424a1b26ed90b0be4076ee5ea7f9bc8ea5b8f4a77e59a2c6b497. Their author read no local candidates, rankings or judgments. Weak diagnostic negatives will not inflate primary performance claims.
- Public research can expose held-out texts to the parent agent. They are held out from comparative optimization results, not necessarily unseen literary content. Final validation should use fresh reviewers with no access to prior rankings or verdicts.

## Stages

The initial exploratory tournament has sixty edges in a seeded random cycle, two opponents per draft, each assessed in both presentation orders by separate reviewers. Each game averages its two fractional scores. No candidate is eliminated on this sparse screen.

The public-opponent screen freezes 240 games: every one of120 drafts faces two distinct public development opponents. In each sixty-draft batch, every pair of the six public opponents is assigned four times, giving each opponent twenty appearances. Presentation and pair order are seeded and shuffled. Reverse-order schedules are assessed separately. Six strong public opponents provide a difficult comparison pool; they do not represent the entire final field. Across the240 public-opponent games, originals won128, tied31, and lost81 under the agent proxy.

The strong stage contained32 texts: the exploratory top16, additional best representatives covering every original family, and six one-or-two-dimension seed variants. A seeded degree-six comparison graph supplies96 games, plus six parent/variant tests. This is102 games, with at least six new comparisons per selected text; nonselected originals are not permanently eliminated. Fresh reviewers saw opposing presentation orders. R05 became the provisional incumbent after8/8 proxy wins, with its exact472-character text preserved as champions/001-R05.txt. This is not a99.5% probability claim.

The anonymous challenge covered 105 games. Ten candidates played one another, then each played the six public development opponents. Reviewers received neutral identifiers and text. The codebook links the preserved anonymous verdicts to the candidate IDs.

The first held-out round had 90 unique matchups, including four candidates against 21 new opponents and all six direct finalist matchups. Two reviewers each judged both presentations. V08 led that round with 16 wins, three draws and two losses against the 21 opponents. Its loss to an independently authored bakery scene motivated a challenger round. All six independently authored pieces were eligible for selection and took part. Their authorship provenance remains in the pool. Earlier public texts and the six pieces from that validation are development evidence for this next selection.

The challenger round used 105 games among ten original pieces and against the six toughest public matchups for V08 in the first validation. V07 led the new Bradley–Terry fit. The bakery scene had the highest mean margin share against that public subset. The fresh validation includes those two pieces and V08, the strongest candidate in the first validation. It uses 15 public opponents selected by rank from the 96-entry snapshot, excluding all earlier evaluated artifact hashes, and six original baselines from a new blind writer. Two reviewers each judge both presentations of the 66 matchups.

## Scoring and analysis

A winning opinion with margin m gives its winner 0.5+m/10, loser0.5-m/10. Reversed opinions form one game, never two independent games. Invalid, incomplete, duplicate or misoriented games are reported and excluded; they are not neutral invented verdicts. Balanced cancellation yields a game tie even though each reviewer chooses a winner.

The analysis fits fractional Bradley–Terry strengths with L2 penalty0.25 toward equal strength. This explicit prior makes sparse/disconnected fits finite; it also shrinks differences. Expected share against the local pool is distinct from make.fun's fitted development rate against three house anchors. Exploratory Elo uses K20 and recorded game order.

Wilson95 intervals describe the binary proportion of decisive games won, excluding tied games and reporting tie counts separately. Bootstrap200 replicates resample complete pair games and refit the regularized model. These intervals do not establish calibrated population probabilities: shared reviewer contexts, adaptive opponent selection and the prior violate a simple independent-sampling interpretation. Unseen candidates receive no empirical bootstrap interval.

Adaptive scheduling considers the whole field, prioritizes coverage before close/uncertain matches, and uses distinct round IDs. Point-estimate top-N is not a statistically justified elimination rule. Irreversible elimination is currently disabled; sparse candidates remain eligible for further evidence.

Position diagnostics report A-win share overall and by reviewer. Reviewer and position effects are confounded in development rounds where each reviewer sees a single orientation. In both validation rounds, each reviewer evaluates both orientations, allowing a descriptive measure of winner reversals. Repeat opinions within one session share context and do not provide independent replications.

## The99.5% aspiration

Any observed win rate needs its denominator, unique-opponent count, distribution and source. A perfect tiny sample does not show99.5% true preference. Even under ideal independent binomial trials, an all-win record needs765 trials for a two-sided95% Wilson lower bound to reach99.5%; for99.9%,3838. Batched proxy judgments cannot satisfy those independence or target-model conditions.

The highest public provisional rate across the archived snapshots is 90.3623%, as of November 17 at 21:57 Jakarta time. Official measurements for our entry require an authorized submission.

## Reproduce validation from the recorded verdicts

From the research branch, run these commands with Python 3.13.

```sh
python3.13 -m unittest discover -s research -p 'test_*.py'
python3.13 research/decode_verdicts.py heldout
python3.13 research/analyze_heldout.py
python3.13 research/decode_verdicts.py fresh
python3.13 research/analyze_heldout.py --fresh
```

Public texts are referenced by source URL and hash. Run `python3.13 research/collect_public_competitors.py --scratch work/public-artifacts` to recover those used in judging. The underlying public endpoints may stop serving an old artifact after the event. No credentials or paid endpoints are required for these commands.
