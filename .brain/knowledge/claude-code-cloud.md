# What Claude Code cloud sessions load

*Cloud sessions are the ones started from the phone app, claude.ai/code in the browser, or `claude --cloud`.*

## What carries over (checked 2026-10-14)
- A cloud session starts from a fresh clone of the one repo I pick. Anything committed to it is available: its `CLAUDE.md`, `.claude/settings.json` hooks and permissions, `.claude/skills/`, `.claude/agents/`, `.mcp.json`.
- Not available: my `~/.claude/CLAUDE.md`, `~/.claude/skills/`, user settings, plugins (even ones a repo turns on), and MCP servers added at user scope.
- Skills I enable on claude.ai do load in cloud sessions.
- A cloud environment can have a setup script that runs before each session. It can write files into `~/.claude/`, which is how `dot-claude` can reach phone and web sessions.
- Source: https://code.claude.com/docs/en/cloud-environments and https://code.claude.com/docs/en/settings
