# Claude usage limits: what changed in 2026

*Checked 2026-10-27. Sources are third-party coverage of Anthropic's posts on X; I found no Anthropic help-center page. Asked by Rain because the weekly limits feel nerfed.*

- **Aug 2025:** Anthropic added weekly limits for Pro and Max, on top of the 5-hour limit, saying they'd hit under 5% of subscribers.
- **Mar 2026:** the 5-hour session limit got tighter during peak hours (weekdays 5-11 am Pacific). Anthropic said weekly limits were unchanged and that about 7% of users would hit limits they wouldn't have before, mostly on Pro.
- **May 6, 2026:** Claude Code 5-hour limits doubled for Pro, Max, Team. Weekly caps unchanged.
- **May to Sep 13, 2026:** a temporary +50% boost on Claude Code weekly limits.
- **Aug 29, 2026 (announced on X):** from Sep 14 the boost becomes a permanent +25% over the old baseline. Measured against the boosted level people had been using, that is about 17% less ([BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-is-cutting-claude-codes-current-weekly-limits-by-17-percent/)).
- **Late Oct 2026:** one measurement site found no further cut between two recent weeks, and found Max 20x gives roughly 10x Pro's weekly limit, not 20x ([Wokey](https://wokey.ai/claude-usage-limits)).
- Not found: any official statement that the limits were cut beyond the above, and anything about the Claude chat apps (the changes are about Claude Code).

Other sources: [TechRadar on peak hours](https://www.techradar.com/ai-platforms-assistants/claude/claude-is-limiting-usage-more-aggressively-during-peak-hours-heres-what-changed), [Manton Reece on the announcement](https://www.manton.org/2026/08/29/anthropic-announced-a-limits-change.html), [Explainx timeline](https://www.explainx.ai/blog/claude-usage-limits-2026-timeline-explained).

## Since Opus 5.5 (checked 2026-10-27)
- **No solid independent measurement found.** Only anecdotes, and they conflict. SmartScope (early Oct 2026) says posts on X are split: some call Opus 5.5 nearly unlimited on the $200 plan, others run out of the weekly limit fast. A Towards AI writer saw a big session barely move the bar.
- One $200 user posted that their output tokens fell from 34.6M to 28.4M week over week (-18%) and the limit ran out in about 3 days. Unverified.
- **Reported bug:** Agent SDK / non-interactive use (`claude -p`) hits the 5-hour limit up to 1.8x faster than interactive Claude Code, per Theo (t3.gg), who reported it to Anthropic. Weekly caps said to be fine. Not confirmed by Anthropic.
- At launch Anthropic raised 5-hour limits (no weekly change, no published percentage), and there was a one-time limit reset until 2026-10-22. Anthropic no longer publishes exact limit figures.
- Launch partners say Opus 5.5 uses fewer tokens for the same work (vendor-reported). Effort level matters: higher effort burns the window faster.
- **Way to measure it myself:** run `/usage` in Claude Code before and after a fixed amount of Opus work. Tools: [BurnRate](https://tommcfarlin.com/burnrate-claude-code-usage/) (macOS menu bar app, uses the same endpoint).
- Sources: [SmartScope](https://smartscope.blog/en/blog/claude-opus-5-5-weekly-limit-max-plan-2026/), [Towards AI](https://pub.towardsai.net/opus-5-5-might-be-the-weirdest-ai-upgrade-yet-9904ec217b17), [InventivHQ](https://inventivehq.com/blog/claude-code-rate-limits-explained), [Anthropic: models, usage and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code).
