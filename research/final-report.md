# The Ceiling in the Water

Selected entry V07 is 450 UTF-8 bytes and Unicode code points. Its text is preserved in [the champion snapshot](champions/002-V07.txt) and embedded in `main.py` at entry commit `f57ae67fff032fe7148a21fe51f618a5f34b0241`. The SHA-256 of `entry.txt` is `49995356f8c6ba8c52a88350dcd735b07462381c0316a2c47fba99d52a818a29`.

## Candidate evidence

The campaign recorded 1,848 Codex reviewer opinions across 768 scheduled matchups. The pool included 120 initial drafts, ten targeted variants, and six independently authored pieces that later became eligible challengers. Fresh validation used 21 strong opponents per finalist, including 15 public competitor artifacts and six original independent baselines. The five development stages cover 612 matchups with two opinions each. The two validation rounds cover 156 unique matchups with four opinions each. See the [methodology](methodology.md), [development ranking](ranking-challenge.json), [recovery ranking](recovery-results.json), and [fresh results](fresh-results.json).

| Finalist | Fresh W–T–L | Public W–T–L | Independent W–T–L | Mean margin share | Descriptive 95% Wilson interval, decisive games |
| --- | ---: | ---: | ---: | ---: | ---: |
| V07, selected | 17–3–1 | 13–1–1 | 4–2–0 | 61.90% | 74.24%–99.01% |
| HOLD-H06, bakery | 14–3–4 | 11–2–2 | 3–1–2 | 58.81% | 54.79%–91.00% |
| V08, earlier bathwater revision | 15–0–6 | 12–0–3 | 3–0–3 | 57.02% | 50.04%–86.19% |

V07 won 17/21 fresh matchups (81.0%) and 17/18 decisive matchups (94.4%). It tied the bakery scene and beat V08 with a 60% margin share in the direct comparisons. It lost to a public still-water piece and tied one other public entry plus two independent baselines. The separate opponent bootstrap interval for its mean margin share was 58.21%–65.36%. These are descriptive intervals for intentionally selected opponents with only two reviewer contexts. The reviewers gave A 55.3% and 56.8% of their votes and changed text preference on reversal in 15/66 and 11/66 matchups. Local results do not establish the 99.5% target or measure GLM-5.3-Flash performance.

## Public benchmark and judging contract

The provisional board reviewed at November 17, 22:16 Jakarta time contained 104 entries. The leader was @amrusalim at 90.3346%, ahead of @bagus63 at 88.3436% and @aurelly-claudia at 88.0368%. The preceding 96-entry snapshot had a 74.29065% median and a 90.3623% leader. The [ten leading entries at review](leaderboard-final-review.json), [earlier snapshot statistics](leaderboard-second-statistics.json), [style analysis](leaderboard-analysis.md), and [observed rank changes](leaderboard-refresh-analysis.md) preserve the public evidence. The public provisional estimates describe fitted performance against house texts. The rules define the official model, the two-order games, and the later final rating. No independent official practice endpoint was disclosed. [Official leaderboard](https://make.fun/bounty/ai-judge-relax-01/leaderboard) · [Official rules and kit](https://make.fun/c/ai-judge-relax-01/kit)

## Technical verification and status

Python 3.13.14 produced the exact expected bytes in 20 fresh output directories under a macOS sandbox that denied network access. The source uses `os` and `pathlib` from the standard library. The research suite passed 23 tests. The official kit's preflight checked the exact entry commit and bundle, with 13 passed, zero failed, five skipped, and five deferred to submission. It parsed 18 native Codex sessions, counted 80% authored lines, and priced every recorded usage row. Private system and developer instructions were withheld in the native session copies, as permitted by the rules. The CLI applied its built-in transcript redaction. Gitleaks was unavailable locally.

The user authorized payment and submission after funding the paired wallet. The 0.50 USDC fee was paid at November 17, 22:40:07 WIB. make.fun received submission `01a1ea2b-09bc-7567-b426-64e877609ddb` at 22:40:51 WIB, naming entry commit `f57ae67fff032fe7148a21fe51f618a5f34b0241` and transcript bundle `e0b389e6f1641e3f924ce374ad8b490a72cfc8dab6cad30ad2fbf3e4c1af137b`. Its server status reached **scored**, with two runtime executions and **Valid = 1**. All 26 applicable server checks passed, with three skipped and zero failed. The official development judge rating subsequently appeared as **80.9836%**, with a displayed 90% interval of **78.3080%–83.6592%**, and rank **28 of 114** at the read. It recorded nine wins, eight draws and six losses over 23 games. The target above 92% remains unmet. One submission attempt has been used. No external API credits were spent. Entries close November 18 at 21:00 Jakarta time. [Bounty requirements](https://make.fun/api/competitions/ai-judge-relax-01/requirements)

The [official-feedback review](official-feedback-round1.md) records recurring weaknesses from the GLM reasons and the next controlled variations. Codex proxy reviewers overestimated the ability of this text to outperform the official development references. Further proxy results will be treated as editorial comparisons when deciding what might merit an authorized official attempt.
