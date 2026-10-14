# Cloud sessions: how my setup reaches them

*How a Claude Code cloud session (phone, web, or Cloud in the desktop app) gets my global rules, modes, the brain skill, `brain-search`, and brain index rebuilds, and how to turn it on for another repo. Set up and tested on claude-assistant 2026-10-14.*

## How it works (checked 2026-10-14)
- A cloud session runs on a fresh clone of the one repo I pick. It doesn't have my PC's `~/.claude`, and hooks from `~/.claude/settings.json` don't run there; hooks from the repo's own `.claude/settings.json` do.
- A cloud session can only reach the GitHub repos picked when it starts. `dot-claude` is private, so it's reached with a fine-grained token that can only read `dot-claude` (Contents: read-only), stored in the cloud environment's variable `DOT_CLAUDE_TOKEN`.
- **The environment's setup script** (claude.ai/code → environment settings → Setup script) runs before Claude starts and clones `dot-claude` into `~/.claude`, so `~/.claude/CLAUDE.md`, the skills and `brain-search` load from the first message. Its result is cached for about 7 days.
  ```bash
  #!/bin/bash
  U=https://github.com/serina-sketch/dot-claude.git
  [ -n "$DOT_CLAUDE_TOKEN" ] && U="https://x-access-token:${DOT_CLAUDE_TOKEN}@github.com/serina-sketch/dot-claude.git"
  git clone -q "$U" /tmp/dot-claude && mkdir -p ~/.claude && cp -r /tmp/dot-claude/. ~/.claude/ || true
  ```
- **The repo's own hooks** do the rest: `.claude/settings.json` calls `.claude/cloud.sh` at session start (`sync`: pulls the latest `dot-claude`, so changes arrive despite the cache) and after every Write/Edit and at the end of each reply (`brain`: runs `brain_index.py`). `cloud.sh` exits at once unless `CLAUDE_CODE_REMOTE` is `true`, so on the PC it does nothing (there `~/.claude`'s own hooks run).
- The environment variable and the setup script belong to the environment, so they already cover every repo. Only the two hook files are per repo.

## Turning it on for another repo (mimitabi, chatbot…)
- Copy `.claude/settings.json` and `.claude/cloud.sh` from claude-assistant into the repo's `.claude/` (merge `settings.json` if the repo already has one).
- Add `*.sh text eol=lf` to the repo's `.gitattributes`, so `cloud.sh` keeps Linux line endings.
- Commit and push to `master`.
- Test in a cloud session on that repo, with nothing else attached: `echo $CLAUDE_CODE_REMOTE` prints `true`; `~/.claude/CLAUDE.md` has "Where things go"; `brain-search` is listed; editing a file in `.brain/ideas/` updates `.brain/ideas/index.md` by itself.

## If something breaks
- No global rules or `brain-search`: run `bash .claude/cloud.sh sync` in the session and read the error. A rejected token means it expired or lost access: make a new one (same settings) and replace `DOT_CLAUDE_TOKEN`.
- Indexes not rebuilding: check that the repo's `.claude/settings.json` has the hooks and that `~/.claude/skills/brain/brain_index.py` exists.
- Changes to the setup script take effect in the next new session (it also rebuilds the cache).
