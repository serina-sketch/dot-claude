# My Claude setup on every device

*Decisions about syncing my global Claude Code setup, and why.*

- **`~/.claude` is the repo (2026-10-14):** it's the public GitHub repo `serina-sketch/dot-claude`. On another PC I clone it into `~/.claude`, and `git pull` updates it. Chosen over a separate repo with an install script because there's no extra step.
- **Allow-list (2026-10-14):** the `.gitignore` ignores everything, then lets through only `CLAUDE.md`, `settings.json`, `skills/` (without `synced/`), `browser-skills/`, `agents/` and `commands/`. The login (`.credentials.json`) and the chat transcripts (`projects/`) must never be pushed.
- **The modes live there (2026-10-14):** tutor, maid and coach are edited directly in `~/.claude/skills/`. `tools/modes/` in this repo was deleted, and so was the old `.claude/skills/` copy kept for cloud, once cloud got them from `dot-claude`. Claude can start a mode too, when I ask for it (`/tutor`, "tutor mode on").
- **Separate from this repo (2026-10-14):** this repo holds my therapy notes and journal, so cloud sessions in other projects shouldn't have to pull it just to get my rules.
- ~~**Phone and web (2026-10-14):** cloud sessions don't have my `~/.claude`, so each repo's own hooks (`.claude/settings.json` + `.claude/cloud.sh`, cloud only) put `dot-claude` into it at session start and rebuild the brain indexes (user-level hooks don't run on cloud).~~ Replaced 2026-10-26: the cloud environment's setup script clones `dot-claude` into `~/.claude`, and then `~/.claude`'s own hooks run there like on the PC (`knowledge/cloud-setup.md`).
- **Public (2026-10-22):** anyone can read it, so cloud sessions clone it without logging in, and no secrets go in it (like the alarm topic, which stays out of git).
- **Alarm topic copy (2026-10-28):** I was tired of the alarm config going missing on every new PC, so a copy of it lives in the private claude-assistant repo, at `secrets/alarm-config.json`. `alarm.py` reads `ALARM_TOPIC` first, then `config.json` next to it, then that copy. Only the path is in `dot-claude`, never the topic.

## Confirmed working
- On a new PC with no `config.json`, an alarm set with `alarm.py in 20m` rang on my phone, reading the topic from claude-assistant's `secrets/alarm-config.json` (2026-10-28).
- A cloud session on claude-assistant without `dot-claude` attached has the global rules and `brain-search` from the first message; the brain index rebuilds after an edit (2026-10-14).
- A real cloud session on claude-assistant wrote thoughts, ideas, plans and knowledge, and every index was rebuilt correctly by the cloud hooks (2026-10-14).
