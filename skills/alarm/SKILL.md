---
name: alarm
description: "Set, list or cancel alarms that ring on Rain's phone (the Claude Alarm app, through ntfy). Use whenever Rain asks to be reminded of something, to set an alarm or a timer, or to cancel or see his alarms, in any project, on the PC or on cloud. Never answer a reminder request only with a message in the chat."
---

# Alarms

Claude sets alarms on Rain's Razr through ntfy. The Claude Alarm app on the phone (repo `claude-alarm`) receives each alarm right away, schedules it, and rings it full-screen until dismissed.

## Commands
- Ring now: `python ~/.claude/skills/alarm/alarm.py now "Wash clothes"`
- Ring after a delay (s, m, h, d, or combos): `python ~/.claude/skills/alarm/alarm.py in 1h30m "Wash clothes"`
- Ring at a clock time, Montreal time: `python ~/.claude/skills/alarm/alarm.py at 3:30pm "Wash clothes"`
  - Also accepts `3pm`, `15:30`, `3:30 pm`.
  - Add `--date 2026-10-26` for another day. If the time already passed today, it uses tomorrow and says so.
- See alarms still waiting, with their ids: `python ~/.claude/skills/alarm/alarm.py list`
- Remove a waiting alarm: `python ~/.claude/skills/alarm/alarm.py cancel <id>` (the id is printed when the alarm is set, and by `list`).

After setting one, tell Rain the ring time and the alarm's id.

## Good to know
- The topic is private and `dot-claude` is public, so it is never committed: on the PC it's in `config.json` next to the script (ignored by git); if that is missing, the script uses the copy in the private `claude-assistant` repo, `secrets/alarm-config.json`; on cloud it comes from the `ALARM_TOPIC` environment variable. If the script says there's no topic, tell Rain which one is missing.
- `config.json` looks like this (use the real topic, never commit it): `{"server": "https://ntfy.sh", "topic": "<your-private-topic>", "timezone": "America/Toronto"}`. `server` and `timezone` are optional and default to these values, so on cloud `ALARM_TOPIC` alone is enough.
- A cloud session also needs `ntfy.sh` on its network allow list, or sending fails.
- `list` only sees alarms set in the last 12 hours, because ntfy.sh keeps messages that long. The app's own screen shows every waiting alarm.
- If the phone is offline for more than 12 hours, alarms sent in that time are lost.
- Research behind this: `~/.claude/.brain/knowledge/phone-alarms.md`.
