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
