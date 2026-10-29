"""Set phone alarms on Rain's Razr through ntfy, for the Claude Alarm app (repo claude-alarm).

    python ~/.claude/skills/alarm/alarm.py now "Wash clothes"
    python ~/.claude/skills/alarm/alarm.py in 5m "Wash clothes"          # s, m, h, d; combos like 1h30m
    python ~/.claude/skills/alarm/alarm.py at 3:30pm "Wash clothes"      # Montreal time: 3:30pm, 3pm, 15:30, 3:30 pm
    python ~/.claude/skills/alarm/alarm.py at 7am "Wake up" --date 2026-10-26
    python ~/.claude/skills/alarm/alarm.py list                          # alarms still waiting to ring, with their ids
    python ~/.claude/skills/alarm/alarm.py cancel <id>                   # remove a waiting alarm from the phone

Settings are read from config.json next to this script (server, topic, timezone).
config.json is not in git (dot-claude is public). If it is missing, the copy in
the private claude-assistant repo (secrets/alarm-config.json) is used. The
ALARM_TOPIC environment variable, if set, overrides the topic (that is how
cloud sessions get it).
Standard library only; runs on Windows and on the Linux cloud container (cloud
needs ntfy.sh on its network allow list).

Each alarm is sent right away as a JSON message with an id and its ring time;
the app on the phone schedules it and rings it. A cancel is a JSON message too:
  {"type":"alarm","id":"...","at":<unix seconds>,"label":"..."}
  {"type":"cancel","id":"..."}

Notes:
- `list` only sees the last 12 hours of messages, because ntfy.sh keeps them
  that long. The app's own screen is the full list.
"""
import argparse
import base64
import json
import os
import pathlib
import secrets
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
BACKUP_CONFIGS = [
    pathlib.Path.home() / "home/serina-sketch/claude-assistant/secrets/alarm-config.json",
    pathlib.Path.home() / "claude-assistant/secrets/alarm-config.json",
    pathlib.Path("/home/user/claude-assistant/secrets/alarm-config.json"),
]
UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def load_config():
    cfg = {"server": "https://ntfy.sh", "timezone": "America/Toronto"}
    path = HERE / "config.json"
    if not path.exists():
        path = next((p for p in BACKUP_CONFIGS if p.exists()), path)
    if path.exists():
        cfg.update(json.loads(path.read_text(encoding="utf-8")))
    if os.environ.get("ALARM_TOPIC"):
        cfg["topic"] = os.environ["ALARM_TOPIC"]
    if not cfg.get("topic"):
        sys.exit("No ntfy topic: set ALARM_TOPIC, or put \"topic\" in " + str(path))
    return cfg


def get_tz(cfg):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(cfg["timezone"])
    except Exception:
        # No tzdata (Windows): None means the machine's local time, which follows DST.
        return None


def parse_delay(text):
    """'5m' -> 300, '1h30m' -> 5400. Raises ValueError on anything else."""
    s = text.strip().lower().replace(" ", "")
    if not re.fullmatch(r"(\d+[smhd])+", s):
        raise ValueError(f'Bad delay "{text}". Use a number plus s/m/h/d, like 5m or 1h30m.')
    total = sum(int(n) * UNITS[u] for n, u in re.findall(r"(\d+)([smhd])", s))
    if total <= 0:
        raise ValueError("Delay must be more than zero.")
    return total


def parse_clock(text):
    """'3:30pm', '3pm', '15:30', '3:30 pm' -> (hour, minute). Raises ValueError."""
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text.strip().lower())
    if not m:
        raise ValueError(f'Bad time "{text}". Use 3:30pm, 3pm or 15:30.')
    hour, minute, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if ap:
        if not 1 <= hour <= 12:
            raise ValueError(f'Bad time "{text}": hour must be 1-12 with am/pm.')
        hour = hour % 12 + (12 if ap == "pm" else 0)
    elif not m.group(2):
        raise ValueError(f'Bad time "{text}". Add am/pm or minutes (3pm, 15:30).')
    if hour > 23 or minute > 59:
        raise ValueError(f'Bad time "{text}".')
    return hour, minute


def resolve_at(time_text, date_text, tz, now=None):
    """Return (unix timestamp, note). note is set when it rolled to tomorrow."""
    hour, minute = parse_clock(time_text)
    now = now or datetime.now(tz)
    note = ""
    if date_text:
        try:
            d = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f'Bad date "{date_text}". Use YYYY-MM-DD.')
        target = datetime(d.year, d.month, d.day, hour, minute, tzinfo=tz)
    else:
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)
            note = "That time already passed today, so it is set for tomorrow."
    return int(target.timestamp()), note


def fmt(ts, tz):
    d = datetime.fromtimestamp(ts, tz)
    return d.strftime("%a %Y-%m-%d ") + d.strftime("%I:%M %p").lstrip("0")


def encode_header(value):
    try:
        value.encode("ascii")
        return value
    except UnicodeEncodeError:
        return "=?UTF-8?B?" + base64.b64encode(value.encode("utf-8")).decode("ascii") + "?="


def send(cfg, payload):
    url = f"{cfg['server']}/{cfg['topic']}"
    headers = {
        # Lowest priority, so the ntfy app (if still subscribed) stays quiet; the alarm app does the ringing.
        "Priority": "1",
        "Title": encode_header("Claude Alarm"),
        "User-Agent": "claude-assistant-alarm/1.0",
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"Could not reach {cfg['server']}: {e}\n"
                 "(On a cloud session the likely cause is ntfy.sh missing from the network allow list.)")


def cmd_list(cfg, tz):
    url = f"{cfg['server']}/{cfg['topic']}/json?poll=1&since=all"
    req = urllib.request.Request(url, headers={"User-Agent": "claude-assistant-alarm/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8")
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"Could not reach {cfg['server']}: {e}\n"
                 "(On a cloud session the likely cause is ntfy.sh missing from the network allow list.)")
    alarms = {}
    for line in body.splitlines():
        try:
            o = json.loads(line)
            m = json.loads(o.get("message", "")) if o.get("event") == "message" else None
        except ValueError:
            continue
        if not isinstance(m, dict):
            continue
        if m.get("type") == "alarm":
            alarms[m["id"]] = m
        elif m.get("type") == "cancel":
            alarms.pop(m.get("id"), None)
    items = sorted((m for m in alarms.values() if m["at"] > time.time()), key=lambda m: m["at"])
    if not items:
        print("No alarms waiting (from the last 12 hours).")
        return
    for m in items:
        print(f"{fmt(m['at'], tz)}  —  {m['label']}  (id {m['id']})")


def main():
    p = argparse.ArgumentParser(description="Set phone alarms through ntfy.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("now", help="ring immediately")
    sp.add_argument("message")
    sp = sub.add_parser("in", help="ring after a delay (5m, 1h30m)")
    sp.add_argument("delay")
    sp.add_argument("message")
    sp = sub.add_parser("at", help="ring at a clock time (Montreal)")
    sp.add_argument("time")
    sp.add_argument("message")
    sp.add_argument("--date", help="YYYY-MM-DD")
    sub.add_parser("list", help="show alarms waiting to ring")
    sp = sub.add_parser("cancel", help="remove a waiting alarm by its id")
    sp.add_argument("id")
    a = p.parse_args()

    cfg = load_config()
    tz = get_tz(cfg)
    try:
        if a.cmd == "list":
            return cmd_list(cfg, tz)
        if a.cmd == "cancel":
            send(cfg, {"type": "cancel", "id": a.id})
            print(f"Cancelled alarm {a.id}")
            return
        note = ""
        if a.cmd == "now":
            ts = int(time.time())
        elif a.cmd == "in":
            ts = int(time.time()) + parse_delay(a.delay)
        else:
            ts, note = resolve_at(a.time, a.date, tz)
            if ts <= time.time():
                raise ValueError("That time is in the past.")
    except ValueError as e:
        sys.exit(f"Error: {e}")
    if note:
        print(note)
    alarm_id = secrets.token_hex(3)
    send(cfg, {"type": "alarm", "id": alarm_id, "at": ts, "label": a.message})
    when = "now" if a.cmd == "now" else f"at {fmt(ts, tz)}"
    print(f'Set: "{a.message}" rings {when} (id {alarm_id})')


if __name__ == "__main__":
    main()
