# Cloud sessions: how my setup reaches them

*How a Claude Code cloud session (phone, web, or Cloud in the desktop app) gets my global rules, modes, the brain skill, `brain-search`, and brain index rebuilds, and how to turn it on for another repo. Set up and tested on claude-assistant 2026-10-14.*

## How it works (checked 2026-10-14)
- A cloud session runs on a fresh clone of the one repo I pick. It doesn't have my PC's `~/.claude`, and hooks from `~/.claude/settings.json` don't run there; hooks from the repo's own `.claude/settings.json` do.
- A cloud session can only reach the GitHub repos picked when it starts. ~~`dot-claude` is private, so it's reached with a fine-grained token that can only read `dot-claude` (Contents: read-only), stored in the cloud environment's variable `DOT_CLAUDE_TOKEN`.~~ Replaced 2026-10-22: **`dot-claude` is public**, so it's cloned with a plain URL and needs no token. I made it public because I was tired of the errors from trying to reach it (the session-start sync printed "could not read Username"). Checked 2026-10-22: an anonymous `git ls-remote` from a cloud session returned the latest commit. I scanned its 39 files for tokens, keys and passwords and found none. Everything in it, including its history, is now readable by anyone (`CLAUDE.md`, the skills, this brain).
- **The environment's setup script** (claude.ai/code → environment settings → Setup script) runs before Claude starts and clones `dot-claude` into `~/.claude`, so `~/.claude/CLAUDE.md`, the skills and `brain-search` load from the first message. Its result is cached for about 7 days.
  ```bash
  #!/bin/bash
  git clone -q https://github.com/serina-sketch/dot-claude.git /tmp/dot-claude && mkdir -p ~/.claude && cp -r /tmp/dot-claude/. ~/.claude/ || true
  ```
  (Changed 2026-10-22: I set this as the default environment's script and deleted the `DOT_CLAUDE_TOKEN` variable. The old version also used the token when the variable was set.)
- **Writing to dot-claude from a cloud session (checked 2026-10-15):** the read-only token was enough (the token is gone since 2026-10-22; reading needs nothing, because the repo is public). When a change is needed, Claude attaches `dot-claude` partway through the session with write access (the `add_repo` tool), clones it to `/home/user/dot-claude`, commits and pushes there, then pulls into `~/.claude` (`bash .claude/cloud.sh sync`) to get the new version. Tested on 2026-10-15 from claude-assistant on the phone: a push dry-run went through. No write token. Making the repo public (2026-10-22) only affects reading; writing still needs this attach. The attachment only lasts for that session. If editing dot-claude from cloud gets frequent, I'm considering adding a write token as well.
- **Any of my repos, partway through a session (checked 2026-10-15):** the same `add_repo` attach works for every repo, not only dot-claude. Tested by moving mimitabi's `claude-tools/` into its `.brain/tools/` from a claude-assistant session on the phone: attached with write access, cloned to `/home/user/mimitabi`, committed and pushed to master. I decided this is how Claude reaches another repo on cloud (2026-10-15).
- **Tested 2026-10-22 on a new claude-assistant chat, with no token (all OK):** `~/.claude/CLAUDE.md` loaded, `brain-search` was listed, the session-start sync printed no errors, `DOT_CLAUDE_TOKEN` was unset, and `CLAUDE_CODE_REMOTE` was `true`. I also revoked the old token on GitHub the same day.
- **The repo's own hooks** do the rest: `.claude/settings.json` calls `.claude/cloud.sh` at session start (`sync`: pulls the latest `dot-claude`, so changes arrive despite the cache) and after every Write/Edit and at the end of each reply (`brain`: runs `brain_index.py`). `cloud.sh` exits at once unless `CLAUDE_CODE_REMOTE` is `true`, so on the PC it does nothing (there `~/.claude`'s own hooks run).
- The environment variable and the setup script belong to the environment, so they already cover every repo. Only the two hook files are per repo.

## Turning it on for another repo (mimitabi, chatbot…)
- Copy `.claude/settings.json` and `.claude/cloud.sh` from claude-assistant into the repo's `.claude/` (merge `settings.json` if the repo already has one).
- Add `*.sh text eol=lf` to the repo's `.gitattributes`, so `cloud.sh` keeps Linux line endings.
- Commit and push to `master`.
- Test in a cloud session on that repo, with nothing else attached: `echo $CLAUDE_CODE_REMOTE` prints `true`; `~/.claude/CLAUDE.md` has "Where things go"; `brain-search` is listed; editing a file in `.brain/ideas/` updates `.brain/ideas/index.md` by itself.

## If something breaks
- No global rules or `brain-search`: run `bash .claude/cloud.sh sync` in the session and read the error. ~~A rejected token means it expired or lost access: make a new one (same settings) and replace `DOT_CLAUDE_TOKEN`.~~ Replaced 2026-10-22: there's no token now. If `DOT_CLAUDE_TOKEN` is ever set again to a dead token, the clone fails even though the repo is public, so keep the variable deleted.
- Indexes not rebuilding: check that the repo's `.claude/settings.json` has the hooks and that `~/.claude/skills/brain/brain_index.py` exists.
- Changes to the setup script take effect in the next new session (it also rebuilds the cache).
