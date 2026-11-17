# Verified specification

Evidence retrieved 17 November 2026. The objective is the strongest empirically supported entry possible, targeting first place without claiming a win in advance.

Sources: [skill v1.5.200](https://make.fun/skill.md), [competition](https://make.fun/api/competitions/ai-judge-relax-01), [requirements](https://make.fun/api/competitions/ai-judge-relax-01/requirements), and the downloaded [kit](https://make.fun/c/ai-judge-relax-01/kit). Local unmodified source snapshots are currently outside the submission repository in work/.

## Runtime and contract

- Python 3.13 main.py or Node 22 main.ts at repository root, standard library only.
- Write UTF-8 entry.txt under /output (MAKEFUN_OUTPUT_DIR may override it for local runs).
- 1–1,000 Unicode code points, including newlines, with at least one non-whitespace character.
- Two sandbox executions must produce byte-identical output. No network, read-only /bot, writable /output, 1 CPU, 512 MB RAM, 64 processes, 60 seconds.
- The judge reads only the entry file. Experiment tools and supporting results can remain in research/ without being executed by main.py.

## Judge and scoring

The RULES identify OpenRouter model z-ai/glm-5.3-flash. The bundle uses the internal alias superbot, with reasoning_effort high and max_output_tokens 12100. These descriptions refer to different layers; actual supplementary calls cannot be verified here without API access.

The disclosed substantive prompt ranks: calming effect; calm shown rather than instructed; economical, gentle rhythm and concrete words; a lingering image; freshness. It explicitly says length itself does not count. The house appends an answer-format instruction requiring a short reason, winner A/B and margin 1–5. The exact appended format is not disclosed in the downloaded kit. Do not claim to reproduce it exactly.

Each game contains two calls with A/B reversed. A winning call gives the chosen entry 0.5 + margin/10; the other gets the complement. Game score is the mean across orders. Final strength uses Bradley–Terry over fractional game scores. Displayed final rates use 95% intervals and dispersion scaling; playoff participation takes priority over rate when placing entries. Full Swiss/racing/playoff rules remain in the official rules.

Development initially compares submissions with three fixed anchors and three sealed references. This is an official submission, not a separate free practice endpoint. reproduce is null, and the scorer, reference data and judge implementation are sealed. Local execution can verify the output contract but cannot yield an official judge score.

## Account, window and quota

- Opened 17 November 2026 14:00 UTC (21:00 Jakarta).
- Entry deadline 18 November 2026 14:00 UTC (21:00 Jakarta).
- Result due 2 December 2026 22:00 UTC; results and a first-place finish are not available at submission time.
- $0.50 USDC fee once per account; authenticated fee status says unpaid, unclaimed winnings $0, and payment permissions disabled.
- Bundle competition.submission_rule says max_per_day 10, max_total 10, Force_Last. The generic requirements quota also mentions a hard maximum of 20 and country-tier daily caps; rely on the authenticated account quota before any attempt. Refused attempts count.
- A later weaker or invalid entry can replace the current entry. The final-entry selection endpoint can pin a finished eligible prior entry before the deadline.
- Login request TRMP-CRMN was approved and the CLI verified @alpaca at 14:15 UTC. Only enter/comment permissions were granted. No payment or submission has occurred.

## Repository and transcript requirements

Public GitHub repository created after opening, full commit SHA, OSI license, signed entry, authentic transcript bundle, required README badges and GitHub About metadata. Include wallet ownership proof if GitHub ownership alone does not establish the account's ownership. A source bundle is an alternative with its own freshness-anchor requirements, not the selected path at present.

The current session began 17 November 2026 14:05:21 UTC, after opening. Codex records its model as gpt-6.1-sol, provider openai, with token-count events. Do not relabel this evidence to match a configured routing display name. Kit bundle --dry-run found the parent and technical-review sessions. Final pricing and all checks remain unverified. Do not manufacture logs, timestamps, token counts or missing child sessions.

The uploaded run record must state the opening user prompt, harness/version/provider/model/effort, MCP servers used, and treatment of system/instruction files. Private instructions can be withheld with a reason. All building subagents' complete authentic logs belong in the bundle. Strict live recording is not named by this competition's deliverables.

## Experiment design and limits

Revised objective: generate at least 120 original candidates, spanning twelve specified styles; the first 60 drafts predate this revision. Use balanced, randomized comparison schedules with reversed presentation across independent reviewer agents; retain raw reports. Fit Bradley–Terry, exploratory Elo, confidence intervals, position diagnostics and bootstrap uncertainty. Allocate fresh comparisons to close contenders, compare targeted variants against parents, then hold out new finalist comparisons. Preserve promoted champions immutably. Validate the final runtime at least 20 times.

User authorization: $0 on external APIs; use agent reviewers for now. No GLM API credentials are present in the process environment. Proxy results from the available agent model cannot establish GLM preferences or a 99.5% real-judge win rate. The revised 99.5% target (99.9% stretch) is a research aspiration, not a measured result or guarantee. Reserve official submission attempts until technical validity and documented comparative evidence support an entry.

## Judge research

[OpenRouter model page](https://openrouter.ai/z-ai/glm-5.3-flash) confirms this model identifier and multiple hosting providers. [Z.ai documentation](https://docs.z.ai/guides/vlm/glm-5.3-flash) describes a text-generating multimodal model with mandatory thinking. Neither source establishes preferences for calming literature. Sensory concreteness, rhythm, emotional safety, low cognitive load, gentle progression and restrained endings remain hypotheses derived from the bounty rubric, to be tested with explicitly labeled proxy evidence.

## Outstanding evidence

Current account quota at 14:16 UTC: 0 used, 3 left today; hard limit 20 but bundle maximum10 still applies. Technical review completed independently. Still outstanding: expanded candidates; recorded comparisons and ranking; optimization and held-out selection; final main.py and LICENSE; runtime tests; public GitHub metadata; final bundle/check results; authorized fee payment if needed; submission receipt and completed development grade. Rank #1 cannot be verified before the official final heat.
