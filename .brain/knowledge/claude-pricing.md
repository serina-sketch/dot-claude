# Claude model pricing

*What the models cost per token, for deciding how to run subagents. From Anthropic's own pricing reference (bundled with Claude Code's claude-api skill, cached 2026-10-06).*

## Per million tokens (checked 2026-10-14)
- **Claude Haiku 5.5:** $0.10 input / $0.50 output for prompts up to 100K tokens; **$0.50 / $2.50 beyond 100K**, so 5x once a single request's context passes 100K.
- **Claude Sonnet 5.5:** $2 / $10. No long-context step listed.
- **Claude Opus 5.5:** $4 / $20. No long-context step listed.
- Source: the claude-api skill's model table (Anthropic first-party API rates).

## What it means for subagents (checked 2026-10-14)
- A subagent re-sends its whole context on every turn, so a Haiku agent that reads a lot crosses 100K and every later turn costs 5x. The audits on 2026-10-14 ran at about 70-110K tokens each, right around the line.
- I'm on the Pro plan, so this shows up as usage limits rather than a bill; how the limits weigh each model isn't published here, but bigger contexts use them up faster either way.

## Effort levels: tokens and quality (checked 2026-10-20)
- The effort setting (low, medium, high, xhigh, max) doesn't change the price per token; it changes how many tokens the model spends thinking, so the cost per task.
- **Defaults:** Opus 5.5 and Haiku 5.5 default to medium. Sonnet 5.5 defaults to medium in the Claude apps, high on the API; sources disagree for Claude Code (medium in most).
- **Sonnet 5.5 tokens per task** (Artificial Analysis): about 14K at low, 19K at medium, 34K at high, 74K at xhigh, about 193K at max. Its Intelligence Index score: 41 at medium, 47 at high, 56 at max, with max costing about 6.8x high. On FrontierCode it scored lower at max (46.2%) than at xhigh (52.1%).
- **Opus 5.5:** on CursorBench, 52.5% at medium (about $3 a task), 56.0% at high (about $4), 57.8% at max. About 119K tokens per task at max. Low effort hurts a lot on knowledge work: 1285 on AA-Briefcase at low against 1642 at medium.
- **Haiku 5.5:** no per-effort breakdown found.
- **Takeaway from the data:** medium to high gives a small, real gain; high to max costs several times more for little or nothing; low saves tokens but loses a lot on hard tasks.
- Sources: [Kingy AI on Sonnet 5.5 effort](https://kingy.ai/blog/claude-sonnet-5-5-effort-levels/), [Dreasays](https://dreasays.substack.com/p/claude-55-is-brilliant-confusing), [Codersera Opus 5.5 guide](https://codersera.com/blog/claude-opus-5-5-complete-guide-2026/), [Tosea Opus 5.5 guide](https://tosea.ai/blog/claude-opus-5-5-complete-guide), [Tosea Sonnet 5.5 guide](https://tosea.ai/blog/claude-sonnet-5-5-complete-guide), [Kingy AI on Haiku 5.5](https://kingy.ai/blog/claude-haiku-5-5-benchmarks-specs-sol-luna/), [Kingy AI on Opus 5.5](https://kingy.ai/blog/claude-opus-5-5-specs-benchmarks-pricing-comparison/), [Taskade](https://www.taskade.com/blog/claude-models-explained), [Developers Digest on effort levels](https://www.developersdigest.tech/blog/fable-5-effort-levels-explained). Mostly third-party blogs.

## Low and medium effort compared across Haiku, Sonnet and Opus 5.5 (checked 2026-10-20)
- **Artificial Analysis Intelligence Index, cost per task:** Opus 5.5 medium scores 51 at $1.34 a task (about 26K output tokens; $1,627 to run the whole index), Opus 5.5 max 58 at $5.98. Sonnet 5.5 medium 41 at about $0.59 a task, high 47 at $1.12 (from a blog quoting AA). Haiku 5.5 high 38 at $0.08 a task, max 43 at $0.21.
- **Not measured:** Opus 5.5 at low; Haiku and Sonnet scores at low. Haiku's cost to run the whole index (blog, unconfirmed): low $34, medium $56, high $94, max $330.
- **Reading:** Opus medium beats Sonnet high on the index for about the same cost per task. Sonnet medium costs about 45% of Opus medium and scores 10 points lower. Haiku costs a few cents a task and is for simple or bulk work. Low saves about a quarter to 40% of tokens against medium but loses a lot on hard tasks (Opus on AA-Briefcase: 1285 at low against 1642 at medium).
- Sources: [AA: Opus 5.5 medium](https://artificialanalysis.ai/models/claude-opus-5-5-medium), [AA: Haiku 5.5 max vs Opus 5.5 medium](https://artificialanalysis.ai/models/comparisons/claude-haiku-5-5-vs-claude-opus-5-5-medium), [AA: Haiku 5.5 high](https://artificialanalysis.ai/models/claude-haiku-5-5-high), [AA: Opus 5.5 article](https://artificialanalysis.ai/articles/claude-opus-5-5), [eesel on Haiku 5.5 pricing](https://www.eesel.ai/blog/claude-haiku-5-5-pricing), [Beam on Haiku 5.5](https://beam.ai/agentic-insights/claude-haiku-5-5-subagents), [Kingy AI on Sonnet 5.5 effort](https://kingy.ai/blog/claude-sonnet-5-5-effort-levels/).

## Effort recommendations and low-effort scores (checked 2026-10-20)
- **Anthropic's effort docs** list low as the choice for "simpler tasks that need the best speed and lowest costs, such as subagents." Haiku 5.5 supports effort; it defaults to medium (Claude Code docs).
- **Per-subagent effort may not apply:** a Claude Code GitHub issue (#43083) says the docs and the actual behavior disagree on whether `effort` in a subagent's settings is honored. Unverified either way.
- **Sonnet 5.5 on the Artificial Analysis index:** low 36, medium 41, high 47, xhigh 52, max 56 (median of comparable models: 26). Opus 5.5: medium 51, max 58; no low score published that I found.
- Sources: [Effort, Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/effort), [Model configuration, Claude Code Docs](https://code.claude.com/docs/en/model-config), [GitHub issue #43083](https://github.com/anthropics/claude-code/issues/43083), [AA: Sonnet 5.5 low](https://artificialanalysis.ai/models/claude-sonnet-5-5-low), [AA: Sonnet 5.5 xhigh](https://artificialanalysis.ai/models/claude-sonnet-5-5-xhigh), [NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/claude-sonnet-5-5-ranks-2-at-56-behind-only-opus-5-5/), [Apidog on Haiku 5.5 in Claude Code](https://apidog.com/blog/claude-haiku-5-5-claude-code/), [DataCamp on Haiku 5.5](https://www.datacamp.com/blog/claude-haiku-5-5).

## What a subscription is worth in API prices (checked 2026-10-20)
- **No official number:** Anthropic doesn't publish how many tokens the Pro or Max limits allow, and adjusts them over time. These are outside measurements.
- **Pro ($20 a month):** one measurement puts a full week of Pro at about $170 of API use (about 25.7M uncached tokens, about 13 five-hour windows). Used fully every week, that's roughly $700 a month of API value for $20.
- **Max 20x ($200 a month):** about $1,643 a week of API value (measured October 12 to 19, 2026), only about 9.7x Pro, not 20x. Another user tallied $1,588 of API value over 30 days on Max.
- **Light users** get less than they pay for; the value only shows up when the limits are used. Caching changes the numbers a lot.
- Sources: [Wokey usage limits](https://wokey.ai/claude-usage-limits), [Toolcolumn: Pro and Max vs API](https://www.toolcolumn.com/learn/claude-pro-max-vs-api-pricing), [Morph](https://www.morphllm.com/claude-code-pricing), [Product Compass](https://www.productcompass.pm/p/claude-code-pricing), [NxCode](https://www.nxcode.io/resources/news/claude-code-pricing-2026-free-api-costs-max-plan). Third-party, not Anthropic.
