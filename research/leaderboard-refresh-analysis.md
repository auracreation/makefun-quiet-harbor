# Public leaderboard refresh

Full board collected **2026-11-17T14:36:01.348855+00:00** from [https://make.fun/api/competitions/ai-judge-relax-01/leaderboard?phase=dev&view=performance&rows=all](https://make.fun/api/competitions/ai-judge-relax-01/leaderboard?phase=dev&view=performance&rows=all). This is the development phase and provisional; **59 public entries**, highest displayed real rate **90.2564%**. `judge` values are micro rates, divided by 1,000,000; percent divides by 10,000. `rows=all` returned no `next_cursor` and no abbreviated `rest`, so all returned rows are covered.

All **59** current artifacts were downloaded or matched against earlier preserved downloads, then verified against SHA-256, reported exact UTF-8 bytes and inline text. **43** artifact files were newly downloaded. Raw artifact texts and response bytes remain only in `work/public-artifacts`; sanitized metadata and scratch paths are in `competitors-refresh.jsonl` and `leaderboard-refresh.json`. Earlier raw snapshots and artifacts were preserved. No service mutation, credentials, authentication, payment, feedback, submission or model API spend occurred.

## Same-submission comparison with the earlier 21-row board

Earlier board timestamp: **2026-11-17T14:16:20.080714+00:00**. There are **16 identical submission IDs** in both boards; **16** show a changed reported rate and **15** show a changed rank. Rank movements alone can result from newly arriving/revised entrants and do not demonstrate a change in the artifact's strength. The following compares actual full-board reads for identical IDs, not the lagging live cache.

| Handle | Rank, old → current | Real rate, old → current | Micro-rate change | Artifact hash |
| --- | --- | --- | ---: | --- |
| @xiinnq799-boop | 2 → 2 | 85.5136% → 86.2547% | +7411 | same |
| @rapid-panda-66 | 4 → 8 | 81.5811% → 83.9583% | +23772 | same |
| @golden-coyote-11 | 5 → 12 | 81.2434% → 80.5928% | -6506 | same |
| @timmyfknhenry | 6 → 11 | 79.2334% → 80.9548% | +17214 | same |
| @tstore | 7 → 19 | 77.9534% → 78.8481% | +8947 | same |
| @kiruntz | 9 → 38 | 74.4374% → 71.4724% | -29650 | same |
| @hilman-fatoni | 10 → 35 | 72.2499% → 72.3885% | +1386 | same |
| @wongkere | 12 → 39 | 71.2168% → 71.1188% | -980 | same |
| @coral-beacon-11 | 13 → 45 | 71.2168% → 69.6450% | -15718 | same |
| @nimble-koala-32 | 14 → 42 | 69.9409% → 69.9304% | -105 | same |
| @pangrib | 15 → 43 | 69.9409% → 69.9186% | -223 | same |
| @stakeratom | 16 → 41 | 69.5060% → 70.1520% | +6460 | same |
| @plucky-marten-62 | 18 → 56 | 66.5078% → 63.6978% | -28100 | same |
| @leung-cyrus | 19 → 57 | 65.2904% → 63.1183% | -21721 | same |
| @hodlr | 20 → 58 | 63.9887% → 62.4931% | -14956 | same |
| @antoniw87 | 21 → 59 | 60.6213% → 57.6004% | -30209 | same |

Where the same ID's reported rate changes, that is an observed two-snapshot change. It does not establish a distribution of score volatility, a cause, or an estimate of final-placement probability. Hash status is reported explicitly.

## Replacements, separate from rate changes

- @amrusalim: `01a1e9d6-2518-71fa-9691-c7a2fec94e3d` replaced by `01a1e9db-2a6b-74a3-973d-27e1ae397280`; 87.5946% → 90.2564%; artifact changed.
- @huangyanzu036-hue: `01a1e9d8-c036-72e5-963b-8a0553e6c72e` replaced by `01a1e9e1-930f-72db-84fd-0badf6855f59`; 84.5849% → 72.8541%; artifact changed.
- @brisk-walrus-71: `01a1e9d6-d4aa-7434-b551-5efef23e7f3b` replaced by `01a1e9e6-3dae-74c1-8c30-e1dad013a014`; 77.8058% → 66.6489%; artifact changed.
- @powel: `01a1e9d1-7047-774e-bbb4-77888a30e998` replaced by `01a1e9dc-e876-75e9-8850-e9a82364a4c7`; 71.6332% → 77.9348%; artifact changed.
- @steady-ibis-90: `01a1e9d8-ccf0-7656-ba20-0877b9ad36b3` replaced by `01a1e9e9-5f21-742a-99ff-6b00e6d20a7a`; 68.1706% → 65.8310%; artifact changed.

New submission IDs compared with the earlier board: **43**. This includes replacements. This is not a complete submission-history archive; missing older IDs may also reflect replacements, removal, or eligibility/visibility changes.

## Live/history freshness and available history

[Live](https://make.fun/api/competitions/ai-judge-relax-01/live) at 2026-11-17T14:36:01.518380+00:00 reports total **47**, returning **10** rows. It omits **49** IDs present in the current full board and includes **0** IDs absent there. [History](https://make.fun/api/competitions/ai-judge-relax-01/standings/history?phase=dev) at 2026-11-17T14:36:02.472483+00:00 has **10** entrant lines and **53** timestamps, latest **2026-11-17T14:22:28.644000+00:00**. The route's documented cap is 120 instants and normally ten current entrant lines; it is not an exhaustive archive.

These are different published surface snapshots. A discrepancy demonstrates freshness/coverage lag, not measured score volatility. This refresh does not infer hidden outcomes or reconstruct unexposed games.

## Frozen public held-out pool

`heldout-public-refresh.jsonl` contains **15** anonymous public opponents. Selection uses the strongest ten eligible current public rows, then five additions chosen for lower overlap in scene vocabulary from the next twenty eligible high ranks. The six `development` entries in `evaluation-pool.jsonl` were excluded using only their identity/source/hash metadata; no candidate text, candidate ranking, or proxy judgment was inspected. Identical development artifact hashes are also excluded. The held-out file contains anonymous IDs, source URLs, raw-artifact scratch paths, SHA-256 and provenance, with `split=heldout`; it contains no full texts, scores, ranks or comparison outcomes.

The selection is frozen before finalist comparison. It is a challenging contemporary public pool, not a random sample of future entrants. Earlier public exposure and the development/held-out distinction do not create statistical independence from broad contest themes. No full competitor text appears in these new repository research files.
