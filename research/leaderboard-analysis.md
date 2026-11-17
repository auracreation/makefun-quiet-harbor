# Public competitive intelligence: ai-judge-relax-01

Collected anonymously on 2026-11-17. Current board: **2026-11-17T14:16:20.080714+00:00**. This is a development snapshot, not an official final placement or a forecast.

## Collection and provenance

- [Full public leaderboard](https://make.fun/api/competitions/ai-judge-relax-01/leaderboard?phase=dev&view=performance&rows=all): 21 full entries, `rows=all`; no `next_cursor`, cursor field, or abbreviated `rest` was returned. The public OpenAPI documents `rows=all` as the default and no cursor parameter on this route. Thus this response is the full public ranked field at collection, not only its first page. Unknown pending, unranked, private, house, or later entries are outside the observed field.
- [Public live snapshot](https://make.fun/api/competitions/ai-judge-relax-01/live): collected 2026-11-17T14:16:20.217824+00:00; 9 rows.
- [Public standings history](https://make.fun/api/competitions/ai-judge-relax-01/standings/history?phase=dev): collected 2026-11-17T14:16:21.056630+00:00; 9 entrant lines at 10 timestamps.
- [Public OpenAPI](https://make.fun/api/openapi.public.json) and the previously downloaded skill's “Optional: watch a competition live” identify the Feed as the leaderboard's `judge.artifact` plus each linked `GET /api/submissions/<id>/artifact.txt?phase=dev`. No separate public Feed endpoint was found in the OpenAPI. All 21 current artifacts and the initial snapshot's one superseded artifact were fetched using those listed same-host URLs only. No comments, comment links, private endpoints, login, credentials, feedback, payment, or submission were used.
- **22 unique downloaded UTF-8 artifacts; every SHA-256, reported byte length, and inline-text equality check passed.** `competitors.jsonl` contains 33 observations: initial 12 and current 21. Every observation records source URL, snapshot time, receipt time, id, handle, rank, raw rate, converted rate, counts, interval, hash, and scratch path. Repeated artifacts retain independent initial/current rank observations.
- Raw downloaded texts and raw new responses are only in `work/public-artifacts`. No full competitor text is copied into this report or new research summaries. Original `leaderboard-snapshot.json` and `live-snapshot.json` remain untouched. The new `*-collected-summary.json` files retain source metadata; the leaderboard summary removes inline competitor text. `collect_public_competitors.py` uses only the standard library, refuses off-host artifact URLs and redirects, and asserts hashes/byte lengths. It consumes the archived snapshots and fetches only missing public artifact files.

## Exact rates and field size

The board's `judge` is `win_rate_micro`; divide by 1,000,000 for the rate or by 10,000 for percent. Its unformatted `875946` is **87.5946%**, not 875,946 wins or 875,946%. Each current row reports 15 matches. The rules define the provisional rate as fitted strength expressed as expected wins against three fixed anchor texts; it is not the raw wins divided by 15 (the leader reports 13 wins, 1 draw, 1 loss). All are provisional development results.

| Rank | Handle | Raw micro rate | Real rate | Characters | UTF-8 bytes |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | @amrusalim | 875946 | 87.5946% | 669 | 669 |
| 2 | @xiinnq799-boop | 855136 | 85.5136% | 534 | 534 |
| 3 | @huangyanzu036-hue | 845849 | 84.5849% | 676 | 676 |
| 4 | @rapid-panda-66 | 815811 | 81.5811% | 674 | 674 |
| 5 | @golden-coyote-11 | 812434 | 81.2434% | 681 | 681 |
| 6 | @timmyfknhenry | 792334 | 79.2334% | 426 | 426 |
| 7 | @tstore | 779534 | 77.9534% | 868 | 868 |
| 8 | @brisk-walrus-71 | 778058 | 77.8058% | 819 | 819 |
| 9 | @kiruntz | 744374 | 74.4374% | 513 | 513 |
| 10 | @hilman-fatoni | 722499 | 72.2499% | 563 | 563 |
| 11 | @powel | 716332 | 71.6332% | 695 | 697 |
| 12 | @wongkere | 712168 | 71.2168% | 345 | 345 |
| 13 | @coral-beacon-11 | 712168 | 71.2168% | 616 | 620 |
| 14 | @nimble-koala-32 | 699409 | 69.9409% | 645 | 645 |
| 15 | @pangrib | 699409 | 69.9409% | 756 | 756 |
| 16 | @stakeratom | 695060 | 69.5060% | 584 | 590 |
| 17 | @steady-ibis-90 | 681706 | 68.1706% | 680 | 680 |
| 18 | @plucky-marten-62 | 665078 | 66.5078% | 809 | 809 |
| 19 | @leung-cyrus | 652904 | 65.2904% | 683 | 685 |
| 20 | @hodlr | 639887 | 63.9887% | 828 | 828 |
| 21 | @antoniw87 | 606213 | 60.6213% | 662 | 662 |

- Highest: **87.5946%**, @amrusalim. Second: **85.5136%**, @xiinnq799-boop. Gap: **20,810 micro = 0.020810 rate = 2.0810 percentage points**.
- Top 3 exact rates: **87.5946%, 85.5136%, 84.5849%**; mean **85.8977%**.
- Top 5 add **81.5811%, 81.2434%**; fifth-place cutoff **81.2434%**, mean **84.10352%**.
- Top 10 add **79.2334%, 77.9534%, 77.8058%, 74.4374%, 72.2499%**; tenth-place cutoff **72.2499%**, mean **80.21975%**.
- Field median (21 entries, rank 11): **71.6332%**. Range: **60.6213%–87.5946%**.
- The leader's displayed 90% interval is **84.8981%–90.2911%**, and the second's **82.5918%–88.4354%**: they overlap. Their displayed rank ranges are 1–2 and 1–5. Small development differences do not establish a decisive final advantage.

## Length and style

Characters are decoded Unicode code points; bytes are the exact downloaded UTF-8 size. Across 21 entries: character min **345**, Q1 **584**, median **674**, Q3 **695**, max **868**, mean **653.62**. Quartiles use Python's inclusive interpolation. Byte min **345**, median **674**, max **868**; character and byte counts differ for four entries with non-ASCII punctuation. Word counts range **69–163**, median **126**. Top 3 span **534–676** characters; top 5 **534–681**; top 10 **426–868**. A 426-character entry ranks sixth; an 868-character entry ranks seventh. There is no observed length optimum.

Qualitative findings from reading all 21 current public artifacts (interpretation, not a controlled test):

- **Stronger cluster:** the top three follow a concrete scene through slow physical change: a dog tracking sunlight, roof rain dwindling to isolated sounds, or an empty dining car moving through night. Ordinary objects, sound, time, and small movement carry the experience. They offer a coherent miniature event rather than many interchangeable comfort claims. All three avoid explicit breathing/body-scan instructions and direct claims about the model's cognition.
- **Useful variation:** top ranks include both prose paragraphs and broken lines. The top two differ substantially in lineation and subject, so copying a visual format is not supported. The fourth and fifth entries contain mild second-person permission while remaining grounded in a scene; second person itself is not disqualifying.
- **Weaker cluster:** ranks 20–21 lean on general bodily relaxation, imagery instructions, and repeated abstract reassurance; rank 19 directly addresses prediction, context, model weights, and rest. These fare below the scene-led leaders in this field. The material may assume a human body or tell the judge how to feel instead of letting the scene work.
- **Counterexamples prevent a formula:** a technical empty-queue scene ranks 10, while another model-facing queue piece ranks 19. Sensory kitchen/rain motifs appear at ranks 2, 6, 12, 13, and 15 with different scores. Scene subject or a list of calming words alone does not explain the differences. The revised @wongkere artifact closely recombines motifs visible elsewhere in the public field; its improvement after revision is only an observation, not evidence that recombination caused improvement. No competitor text should be reused as an original entry.

Character length versus reported rate has Pearson **r = -0.1452** and Spearman **rho = -0.2190**, a small negative cross-sectional association here. It does not show that shortening a candidate improves it. With only 21 selected entrants, 15 reported matches per artifact, adaptive house-opponent selection, fitted rates, repeated stylistic themes, and no random assignment, the style and length patterns are exploratory. There are no per-match scores, judge rationales, or controlled ablations in these public reads.

## Surface lag, actual history, and revisions

The initial snapshots were taken at **14:15:00 UTC**: full board 12 rows, live 9. At **14:16:20 UTC**, the full board has **21** rows; the live read one-half second later still lists the same 9 older rows. It omits 12 current full-board artifacts, including the current leader and third-place entry. Because one account revised its entry, live also retains a superseded @wongkere submission. For the eight identical submission ids shared with the current board, live rates equal full-board rates. The discrepancy shows **surface freshness/coverage lag**, not measured score volatility or evidence that the leader lost.

The public history route is available, but its latest timestamp is only **14:08:47.893 UTC** and its lines correspond to that older nine-entry field. It is incomplete relative to the 21-row board. Its documented design caps the timeline at 120 timestamps and normally includes at most ten current top entrants, so even a fresh response would not be a complete archive of all entrants and all past revisions.

Within the actual available history, leader changes are visible as entries arrive: @wongkere at **14:03:13.756**, @powel at **14:03:24.215**, @timmyfknhenry at **14:03:51.132**, then @xiinnq799-boop at **14:05:09.113**, which remains first through that history's last point. These are observed rank histories, not repeated trials of an unchanged field or numerical volatility estimates.

Comparing the two saved full boards, the top two submission ids and their exact rates remain unchanged. @huangyanzu036-hue enters third, shifting prior ranks below it. The original @wongkere entry (id `01a1e9d1-62a5-7183-b911-6a117b0ad3e8`) has **64.5968%**, 572 bytes; the current one (id `01a1e9d9-0ca9-752f-8cbc-b4c2d10198ca`) has **71.2168%**, 345 bytes. This is a **different artifact**, not a score change for an unchanged candidate. No complete replacement history was exposed by these reads.

## Completeness limits

This is exhaustive for the 21 full rows returned by the selected development board at its collection timestamp, plus the initial 12-row snapshot. It is not exhaustive of all past submissions, in-flight runs, nonpublic entries, later entries, or final judging. The live and history surfaces are demonstrably behind the full board, so their older placements must not be presented as current. No continuous polling, raw match records, match-opponent reconstruction, or causal style test was performed. Public rates are provisional; no measured volatility or final-winning probability is claimed.
