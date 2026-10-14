# How people sync their Claude setup

## What people do (checked 2026-10-14)
- Claude Code has no built-in sync between machines.
- Most common: a dotfiles repo. Either `~/.claude` itself is a git repo, or a separate repo plus an install script. Tools like `dotclaude` wrap this.
- Some keep skills in a plugin marketplace repo, but plugins don't load in cloud sessions.
- Source: https://github.com/elizabethfuentes12/claude-code-dotfiles, https://gitblind.noratr.app/daniel7an/dotclaude, https://github.com/CTHua/dotai

## Where Claude Code keeps things on this PC (checked 2026-10-13)
- Chat transcripts: `~/.claude/projects/<project folder>/<session id>.jsonl`, one file per chat. They contain my messages and Claude's replies.
- `~/.claude/.credentials.json` is the login. It must never be pushed anywhere.
