# Cloud sessions: how my setup reaches them

*How a Claude Code cloud session (phone, web, or Cloud in the desktop app) gets my global rules, modes, the brain skill, `brain-search`, and brain index rebuilds, and how to turn it on for another repo. Set up and tested on claude-assistant 2026-10-14.*

## How it works (checked 2026-10-14)
- A cloud session runs on a fresh clone of the one repo I pick. It doesn't have my PC's `~/.claude`, and hooks from `~/.claude/settings.json` don't run there; hooks from the repo's own `.claude/settings.json` do.
- A cloud session can only reach the GitHub repos picked when it starts. **`dot-claude` is public**, so anyone can clone it with a plain URL, without logging in. Everything in it, including its history, is readable by anyone (`CLAUDE.md`, the skills, this brain), so no secrets go in it.
- **No setup script (2026-10-26):** a setup script used to clone `dot-claude` into `~/.claude`. I removed it, because it ran only when the environment was built and its result was cached, so every container started from that frozen copy of `dot-claude` (24f863c), with an old `git_sync.py`, and fixes to the sync never reached new containers. Now the repo's start hook (`cloud.sh sync`) fills `~/.claude` in every new container.
- **Order at container start (seen 2026-10-26 in the cloud UI):** the container is set up, then the attached repos are cloned (into `/home/user/<repo>`), then the setup script runs, then Claude Code starts. So a repo attached to the session is already on disk before any hook runs.
- **Test of the removal, 2026-10-26 (failed):** in a new chat on claude-assistant with `dot-claude` attached, `~/.claude` was empty after the start (no `.git`, no `CLAUDE.md`, no skills), so the global rules and skills didn't load. Run by hand later in the same chat, `cloud.sh sync` cloned fine. Why it failed at start is unknown: the script hid its errors.
- **Writing to dot-claude from a cloud session (checked 2026-10-15):** when a change is needed, Claude attaches `dot-claude` partway through the session with write access (the `add_repo` tool), clones it to `/home/user/dot-claude`, commits and pushes there, then pulls into `~/.claude` (`bash .claude/cloud.sh sync`) to get the new version. Tested on 2026-10-15 from claude-assistant on the phone: a push dry-run went through. The attachment only lasts for that session.
- **Any of my repos, partway through a session (checked 2026-10-15):** the same `add_repo` attach works for every repo, not only dot-claude. Tested by moving mimitabi's `claude-tools/` into its `.brain/tools/` from a claude-assistant session on the phone: attached with write access, cloned to `/home/user/mimitabi`, committed and pushed to master. I decided this is how Claude reaches another repo on cloud (2026-10-15).
- **Tested 2026-10-22 on a new claude-assistant chat (all OK):** `~/.claude/CLAUDE.md` loaded, `brain-search` was listed, the session-start sync printed no errors, and `CLAUDE_CODE_REMOTE` was `true`.
- **The repo's own hooks** do the rest: `.claude/settings.json` calls `.claude/cloud.sh` at session start (`sync`: fills `~/.claude` with the latest `dot-claude`, see `design/git-sync.md` for how since 2026-10-26) and after every Write/Edit and at the end of each reply (`brain`: runs `brain_index.py`). `cloud.sh` exits at once unless `CLAUDE_CODE_REMOTE` is `true`, so on the PC it does nothing (there `~/.claude`'s own hooks run).
- The environment settings cover every repo. Only the two hook files are per repo.

## Turning it on for another repo (mimitabi, chatbot…)
- Copy `.claude/settings.json` and `.claude/cloud.sh` from claude-assistant into the repo's `.claude/` (merge `settings.json` if the repo already has one).
- Add `*.sh text eol=lf` to the repo's `.gitattributes`, so `cloud.sh` keeps Linux line endings.
- Commit and push to `master`.
- Test in a cloud session on that repo, with nothing else attached: `echo $CLAUDE_CODE_REMOTE` prints `true`; `~/.claude/CLAUDE.md` has "Where things go"; `brain-search` is listed; editing a file in `.brain/ideas/` updates `.brain/ideas/index.md` by itself.

## If something breaks
- No global rules or `brain-search`: read `/tmp/cloud-sync.log` (since 2026-10-26 the start sync logs every step there), then run `bash .claude/cloud.sh sync` in the session. The rules load only in the next chat after that.
- Indexes not rebuilding: check that the repo's `.claude/settings.json` has the hooks and that `~/.claude/skills/brain/brain_index.py` exists.
- Changes to the setup script take effect in the next new session (it also rebuilds the cache).
- **The cloud edits its own `~/.claude` (seen 2026-10-26):** the cloud copy's `settings.json` had `"model": "opus"` changed to `"opus[1m]"`, and Claude Code had added a built-in `skills/session-start-hook/` folder (untracked, harmless). Since 2026-10-26 the sync sets such edits aside and keeps GitHub's version if they clash (`design/git-sync.md`).
