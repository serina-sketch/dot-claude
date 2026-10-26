# A phone app for reminders and alarms that actually ring
*Made 2026-10-25. Status: active (building my own alarm app, 2026-10-25).*

- **Where I stopped:** the Claude Alarm app (repo `claude-alarm`) is on my Razr, and `alarm.py` sends it alarms with ids and a `cancel` command (2026-10-25). On 2026-10-26 it became the global `alarm` skill in dot-claude (`skills/alarm/`), so I can set alarms from any project.
- **Next step:** in the claude.ai cloud environment settings, add `ALARM_TOPIC` (the topic from `~/.claude/skills/alarm/config.json` on the PC) and `ntfy.sh` to the network allow list, then test an alarm from a cloud session.

I want an app on my phone where I can talk to Claude and set up reminders and alarms. What I'm missing is alarms that actually ring and actually remind me. Today a reminder only shows up as a message inside a chat (found out 2026-10-25, when I asked Claude to remind me to wash my clothes in 5 minutes), and I often forget these small things. Research on the options: [phone-alarms.md](../knowledge/phone-alarms.md).

## Try ntfy first (my decision, 2026-10-25)
- [x] Install ntfy on the Razr and subscribe to my private topic (the topic name is in the chat of 2026-10-25, not saved here yet).
- [x] Check that a max-priority message arrives right away and when scheduled 1 minute later.
- ~~Get the alerts to make sound and repeat until dismissed.~~ Replaced 2026-10-25: my own app rings the alarm instead (below).
- [ ] Decide where Claude keeps the list of alarms, and how a cloud session sends them (ntfy.sh on the cloud network allow list).

## The alarm script (my decision, 2026-10-25)
A dedicated `alarms/` folder with a Python script that works on the PC and on cloud. The sound problem is the phone app's, separate from sending.
- [x] `alarms/alarm.py` (now / in / at / list), `config.json` with the topic, `README.md`.
- [x] CLAUDE.md: use it when I ask for a reminder or alarm; add `alarms/` to the folder table.
- [x] Test one alarm from the PC, then commit.
- [ ] Test it from a cloud session (after adding ntfy.sh to the cloud network allow list).
- ~~Cancelling isn't possible.~~ Replaced 2026-10-25: `alarm.py cancel <id>` works through the app. Cancelling isn't possible with plain ntfy: ntfy.sh keeps a scheduled message even after a delete (tested 2026-10-25). Listing the waiting alarms works. The app below makes cancelling possible.

## Moved to the global setup (my decision, 2026-10-26)
I want to access alarms anywhere: just tell Claude to set one in any project. So the script moved from `claude-assistant/alarms/` to the global `alarm` skill (`~/.claude/skills/alarm/`), with a line in the global CLAUDE.md, and this plan and the research moved to dot-claude's brain. dot-claude is public, so the private topic is never committed: `config.json` stays only on the PC (ignored by git), and cloud sessions read it from the `ALARM_TOPIC` environment variable.
- [x] Skill with `SKILL.md`, `alarm.py` (reads `ALARM_TOPIC` first, then `config.json`), tested `list` from the PC.
- [x] Global CLAUDE.md rule; old `alarms/` folder and rule removed from claude-assistant; claude-alarm points to the skill.
- [ ] Cloud: `ALARM_TOPIC` and `ntfy.sh` in the environment settings, then a test.

## My own alarm app (my decision, 2026-10-25)
A native Android app (Kotlin) in its own repo, `claude-alarm`, because that's easier to manage. Its design and build plan live in that repo's brain since 2026-10-25. What stays here is the sending side.

### Update `alarm.py` for the app
- [x] Messages carry an id and the ring time, and are sent immediately.
- [x] A `cancel` command, and `list` reads what's been sent (only the last 12 hours, ntfy.sh's limit).
- [x] Update `alarms/README.md` and the reminder rule in CLAUDE.md.
