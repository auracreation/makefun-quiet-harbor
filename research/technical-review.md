# Independent technical compliance review — ai-judge-relax-01

Reviewed 2026-11-17. This is a read-only competition review, not a submission or a grading result.

## Sources and completeness

- **The full make.fun skill was actually read:** `work/makefun-skill.md`, version **1.5.200**, 291,024 UTF-8 bytes / 291,009 characters / 971 lines. Read in contiguous 14,500-character chunks through EOF; chunks affected by initial tool-output truncation were reread separately. Source: [skill](https://make.fun/skill.md).
- **The full kit RULES.txt was actually read:** 80,679 bytes, 378 lines, in contiguous chunks through EOF. It contains the contest rules plus the CLI/transcript/escrow instructions. [Kit](https://make.fun/c/ai-judge-relax-01/kit).
- Inspected the supplied `work/requirements.json` (effective check thresholds, deliverables, submission template, quota, fees, deadlines, escrow) and `work/competition.json` (rules, bundle configuration, phases, judge, submission rule). [Requirements](https://make.fun/api/competitions/ai-judge-relax-01/requirements), [competition](https://make.fun/api/competitions/ai-judge-relax-01).
- Also read the current public [OpenAPI](https://make.fun/api/openapi.public.json) route inventory for judge/practice routes and relevant shipped CLI source; read current [pricing models](https://make.fun/api/pricing/models). No credentials, private keys, account-authenticated endpoint, feedback, payment or other make.fun write was used.

## Exact artifact and execution constraints

- Root `main.py` (Python 3.13) or `main.ts` (Node 22), standard library only. Nothing is installed before running. For the requested minimal Python runtime, root `main.py` can write the chosen constant text using the standard library; research scripts can remain in the public repository without being executed by the entrypoint.
- Write `entry.txt` under `MAKEFUN_OUTPUT_DIR` (officially `/output`). UTF-8, **1–1,000 Unicode code points**, including every newline; at least one non-whitespace character. The judge sees exactly that file's bytes.
- Official Python command: `python3 -P -s /bot/main.py`. User 65534:65534; read-only `/bot` and root filesystem, writable `/output`, `/tmp` tmpfs 256 MiB; no network; 1 CPU, 512 MiB, 64 processes, 60 seconds, exit 0. Environment includes `MAKEFUN_BOT_DIR`, `MAKEFUN_OUTPUT_DIR`, TZ UTC, PYTHONHASHSEED 0, LANG C.UTF-8.
- Two independent executions must write identical bytes. Test in two fresh output directories, compare bytes and validate UTF-8/code-point count/nonblankness. A local runtime test establishes format and determinism, not the judge score.
- No entry-size cap applies to this program/v1 contest (`entry_size.applies=false`). General intake snapshot/upload limits still exist. Avoid shipping logs/credentials. Public research scripts are allowed ordinary code, and their lines also affect transcript authorship coverage.

## Submission and ownership

- Opens **2026-11-17 14:00 UTC**; submit before **2026-11-18 14:00 UTC** (21:00 Asia/Jakarta). The escrow's 14:10 entries-root deadline is a later organizer commitment deadline, **not ten extra minutes to submit**.
- Public GitHub repository, created at or after opening, with OSI license, full 40-character commit SHA on a branch. Prove ownership through matching linked GitHub identity or committed `.makefun/owner.json` naming an account wallet. Keep repository public, license and submitted commit available through verification.
- Required README: all three live make.fun badges for this slug and this exact repository, with a make.fun link and no URL placeholders. GitHub About: make.fun website and topic `makefun`; fill the other supplied template fields/recommended topics too. README is counted for authorship.
- Multipart POST `/api/competitions/ai-judge-relax-01/submissions` with `repo_url`, `commit_sha`, transcript bundle or loose transcripts, optional public title, `entry_message`, `entry_signature`. This escrow is funded, so signature is required. CLI `submit` signs v1, or v2 if an existing payout pin requires it, for the account wallet; signature age <=600 seconds, future skew <=60 seconds, nonce fresh. Never publish a secret in title.
- A source-bundle alternative is allowed: whole SHA-1 git history in a v2 bundle <=512 MiB, root containing only `.makefun/freshness.json`, anchor round >=**34040212**, emitted after opening, wallet on account. `init --license MIT` creates the anchor/license before entry files. Source signature names uploaded bundle SHA-256 on Source line. Do not rewrite the root.
- Submission rule is `Force_Last`: newest receipt counts by default, even if lower/invalid. Skill documents choosing an earlier finished, unrejected entry using final-entry before closing; explicit pick persists until changed. Later pushes cannot alter an already snapshotted entry. A 202 receipt is not a transcript or grading pass; poll status.

## Authentic transcripts and authoring

- Required bundle or loose native session logs, **all entry-building sessions complete, including parent and every subagent/worker/child**. Top-level agent bundles after children finish. Preserve native records unchanged; kit redaction is allowed. Do not synthesize messages, estimates, timestamps or usage; do not convert a native log into a different harness format.
- Every timestamp must be within opening to receipt, with 60-second skew; start a genuinely new session after opening. Exporting only a later slice of an old session does not repair it.
- Effective `thinking_reproduces`: >=**30% authored** counted lines; <=**40% unwritten** counted text lines when there are >=10 unwritten lines; **each included entrypoint** needs >=1 authored line. First appearance in the agent's own write/edit earns authorship. Copied/retyped/renamed/reformatted code from read files or messages does not. Kit starter lines are excluded. Public research scripts must therefore be authored in included sessions too.
- >=**5 assistant turns carrying text/thinking** across the upload (tool-only turns do not count); >=**2 assistant writes/edits contributing final content** to one code file. Write/test/revise naturally; one completed file followed by a no-op rewrite does not establish revision.
- `thinking_priced`: **100%** of usage records must match a known model. Native harness-recorded logs with no usage have nothing to price; a self-exported session needs provider usage on >=50% of assistant messages and <=500 output tokens/second across its span. Muse app additionally needs >=1 genuine usage row. Never rename a model in logs to pass pricing.
- Current public pricing revision `c6fcfac2cd8c1a316582690b02362df43ca26403f81019dbc528d75df1fb04e0` matches `cx/gpt-5.6-sol-high` via row 26 pattern `gpt-5\.6-sol` (patterns match anywhere); the prefix alone does not make that recorded ID unpriced. This checks the published matching rule, not any actual session record.
- `handed_over_places=none`: accurately handed-over sessions may be ranked but cannot take a paid place. This cannot substitute for available authentic Codex logs.
- **No strict live recording requirement here:** `how_to_submit.strict_transcripts` is absent and `transcripts_witnessed.applies=false`. Normal bundles/loose logs are accepted; starting a live recorder now is not necessary for this contest.
- Source freshness: min_fresh_share=100%, quote the real `makefun anchor <root> round <round>` output before first counted write in credited sessions (Codex forks/parent lineage may inherit). Missing quote/insufficient fresh share is explicitly an advisory skip with no prize hold; a quote timestamped before the beacon round fails. GitHub entries skip this source-anchor check. Session timing still applies regardless.
- Run record **required for entries received since 2026-11-17 00:00 UTC**: actual human opening prompt verbatim, truthful origin/via, harness/version/provider/model/effort, system-prompt status, instructions status, every used MCP server by name. Agent delegation brief and compaction summary cannot replace the person's prompt. Use `--prompt-file` and origin/via when needed. Builtin is only for servers the harness actually ships (Codex's documented name is `codex_apps`); external servers need real URL or stdio command/package, no secrets.
- System prompt and instructions may be withheld with truthful one-line reasons; this does not disqualify the entry. Do not expose hidden system instructions. Authorship-relevant code, reasoning, commands and tool output cannot be removed as privacy redaction.
- No `build_meter` in this bundle: no make.fun metered build key needed; build cost does not decide prize rank. A final bundle/check needs the actual sessions, not this compliance report.

## Fees and quota

- Entry fee **$0.50 USDC once per account per bounty**, 500000 base units, not per submission. Inspect account fee status separately; public `walletPaid=false` is not authenticated proof of the user's status. Payment is a user-money action and was not performed here.
- Published contest cap **10/UTC day, 10 total**; effective day cap is the lower of 10 and country tier: high risk 3, high-risk podium 10, medium 5, premium no added cap. Account reputation may lower either. Absolute hard limit **20 attempts** per account/competition, whether checks pass or fail; 100 GitHub repository checks/hour, max 2 concurrent source uploads.
- Taken entries/refusals from repository checks count toward the day and hard limit; rejected entries do not consume successful total, and platform-failed rounds count toward none. Branding-only README/About refusals count toward none. 429 quota refusal itself does not count. Read actual account quota `can_submit`, day/hard/total and refusal text before each live attempt; no authenticated quota was checked here.
- Base prizes: $20/$7.50/$5, $1 for 4–10, $0.70 for 11–25; one paid place per entrant, house can hold unpaid places. Fees add to payouts. Pot values in downloaded files are time-dependent snapshots, not fixed rewards or a contradiction.

## Practice API and judge limits

- **No documented public practice/judge API was found.** Current public OpenAPI contains no path with `practice` or `judge`; no practice capability is listed in supplied requirements or skill. RULES expressly says **no local grade**, and `competition.reproduce=null`: scorer/reference files stay server-side. The shipped CLI's internal `grade-local --judge` facility requires a full judge competition directory, not this public sealed kit.
- Official dev judgement is obtained by a real submitted entry and consumes quota. Do not probe invented endpoints or send extra submissions as supposed free practice. Direct external model trials, if separately available and authorized, are research proxies, not the official sealed judge or its score.
- Published rules identify **z-ai/glm-5.3-flash via OpenRouter**, max 12100 output tokens, and reveal the exact persona criteria. Bundle's internal `judge.agent.model` instead says `superbot`, reasoning_effort `high`; treat it as an internal selector, not proof that a public model named superbot can reproduce the judge.
- Every game uses two orders; win share per call =0.5+0.1*margin (margin 1–5), mean across calls. Judge nondeterminism is expected; official verdicts are reproduced from records, not by reasking.
- Author original text. Referencing public work for research is possible, but reproducing the house reference texts case/whitespace-insensitively takes no prize; copying someone else's wording/work creates ownership/disqualification risk. The judge permits text addressed to it; steering the separate security audit/reviewers is outside that allowance.

## Differences and ambiguities to handle

1. **No material conflict between downloaded RULES transcript thresholds and current requirements**: both say 30% authored, 40% unwritten, 5 turns, 2 writes, 100% usage pricing, source freshness advisory for missing quotes, and required run record.
2. RULES' simple ten-per-day statement omits lower country/account caps and hard-attempt accounting that requirements publishes. Use requirements plus authenticated quota.
3. Bundle `min_authored_coverage=0` is not the effective transcript gate: requirements/RULES publish 30%. Use the named check, not that legacy bundle field.
4. Source freshness's numeric 100% sounds mandatory while its prose explicitly makes missing quotes advisory; actual early/impossible quote times still fail. Do not conflate it with `thinking_in_window` or source-root freshness, which remain mandatory.
5. RULES counts the transcript checks as ten plus one even though the added run-record row makes twelve named rows; this is a stale count, not an exemption.
6. Entry close 14:00 versus escrow commitment deadline 14:10 are different operations; final scheduled end Nov 18 22:00 versus resolve safety deadline Dec 2 22:00 are different milestones.
7. Skill's generic claim that commands otherwise ask a local dev server is superseded for this downloaded kit by RULES/site.json's make.fun origin; pass explicit origin where there is any ambiguity.
8. Internal judge selector `superbot` versus public model name above is a configuration naming discrepancy; do not claim exact independent reproduction from it.

Skipped: implementation, actual session discovery/bundling/check, authenticated fee/quota, any live submission/payment or official grade. Main remaining risk is authentic-session completeness and correct run-record declaration; this review alone cannot establish acceptance or score.
