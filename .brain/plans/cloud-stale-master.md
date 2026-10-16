# Cloud sessions start with the wrong local master
*Find why cloud sessions of claude-assistant start with dot-claude's history in their local master branch, and fix it.*

Status: later (investigate on the PC)
Where I stopped: noticed the problem on 2026-10-16 in a cloud session of claude-assistant.
Next step: on the PC, check the cloud environment's setup script and the startup hooks.

## What we saw (2026-10-16)
- Every cloud session, the step "switch to master, pull, merge the session branch" fails with "refusing to merge unrelated histories".
- The local `master` in claude-assistant held dot-claude commits ("Cloud: clone private dot-claude with a read-only token"). Its log said "Created from refs/remotes/origin/master", so at startup the saved copy of GitHub's master pointed at dot-claude's history.
- A later `git fetch origin master` showed the right claude-assistant history. GitHub's master itself is fine.
- Workaround that worked: merge `origin/master` into the session branch, then `git push origin HEAD:master`.
- Guess, not confirmed: the startup step that downloads dot-claude into `~/.claude` (`.claude/cloud.sh sync`, the setup script or `git_sync.py`) runs a git command inside the claude-assistant folder.

## Fix options (2026-10-16)
- Cloning the repo again mid-session would give a correct copy, but in a different folder from the one the session runs in, so CLAUDE.md, hooks and settings would still point at the old copy.
- A one-line fix makes it harmless: at session start, reset the local master to GitHub's (`git branch -f master origin/master`), for example in `cloud.sh sync`. I decided to leave all fixes for the PC.

## Steps
- [ ] Read the cloud environment's setup script and the SessionStart hooks; find the command that writes dot-claude into this repo's refs
- [ ] Fix it (the one-line reset, or the root cause)
- [ ] Decide whether the cloud git rule in `CLAUDE.md` should change to `git push origin HEAD:master`
