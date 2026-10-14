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
