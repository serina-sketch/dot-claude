# Brain index

*The map of the `dot-claude` brain. Each folder has its own `index.md` listing its files.*

## This project
`dot-claude` is my global Claude Code setup (`~/.claude`): the global rules in `CLAUDE.md`, the modes and the brain skill in `skills/`, the `brain-search` agent, and the settings and hooks. It syncs through GitHub to every PC, and each repo's start hook (`.claude/cloud.sh sync`) puts it into every cloud session. This brain holds the facts and decisions behind the global setup, so any project, on any machine, can find them at `~/.claude/.brain/`.

## Folders
- `design/`: decisions about the global setup: the brain, plans, and how `dot-claude` syncs.
- `knowledge/`: research and setup notes: cloud sessions, model pricing, how others sync their setup.
- `plans/`, `ideas/`, `thoughts/`: created when there's work on the global setup to plan or think about.

The work that built most of this happened in claude-assistant (its plans, ideas and thoughts stay there).

<!-- auto: everything below is rebuilt by brain_index.py -->

## Open right now

**Plans with steps left:**
- [A phone app for reminders and alarms that actually ring](plans/phone-reminders-app.md): next: in the claude.ai cloud environment settings, add `ALARM_TOPIC` (the topic from `~/.claude/skills/alarm/config.json` on the PC) and `ntfy.sh` to the network allow list, then test an alarm from a cloud session.

**Ideas not decided yet:**
- **Fix the stale local master in cloud sessions** ([cloud-git.md](ideas/cloud-git.md))
- **Use /clear instead of starting a new cloud chat** ([cloud-git.md](ideas/cloud-git.md))
- **A skill for easy explanations** ([explain-simply.md](ideas/explain-simply.md))
