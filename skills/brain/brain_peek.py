"""Show another repo's brain the first time Claude touches that repo (hook script).

What it does: when Claude reads, edits, writes or searches a path inside a
different repo than the one the session runs in, and that repo has a
.brain/index.md, this prints the index into Claude's context so Claude checks
that brain before working there. Once per repo per session.

How to run (a PreToolUse hook on Read|Edit|Write|MultiEdit|Glob|Grep calls it,
with the hook JSON on stdin):
  python brain_peek.py
"""
import json
import os
import sys
import tempfile


def repo_root(path):
    p = os.path.abspath(path)
    if not os.path.isdir(p):
        p = os.path.dirname(p)
    while True:
        if os.path.exists(os.path.join(p, ".git")):
            return os.path.normcase(p)
        parent = os.path.dirname(p)
        if parent == p:
            return None
        p = parent


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("path")
    if not target:
        return 0
    cwd = data.get("cwd") or os.getcwd()
    if not os.path.isabs(target):
        target = os.path.join(cwd, target)
    root = repo_root(target)
    if not root or root == repo_root(cwd):
        return 0
    index = os.path.join(root, ".brain", "index.md")
    if not os.path.isfile(index):
        return 0

    seen_file = os.path.join(tempfile.gettempdir(), f"brain_peek_{data.get('session_id', 'none')}.json")
    try:
        with open(seen_file, encoding="utf-8") as f:
            seen = json.load(f)
    except (OSError, ValueError):
        seen = []
    if root in seen:
        return 0
    seen.append(root)
    with open(seen_file, "w", encoding="utf-8") as f:
        json.dump(seen, f)

    with open(index, encoding="utf-8") as f:
        text = f.read()
    note = (f"This file is in another repo with its own brain: {root}. "
            f"Its .brain/index.md is below. Check it (and its plans, design, knowledge) "
            f"before working there; record work about that repo in its brain.\n\n{text}")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "additionalContext": note}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
