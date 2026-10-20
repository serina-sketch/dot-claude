# Cloud git sync

*Ideas about how cloud sessions sync with master.*

## Fix the stale local master in cloud sessions
- Cloud sessions start with dot-claude's history in claude-assistant's local master, so merging into it fails. I want to investigate this on my computer. (2026-10-16, from a claude-assistant cloud chat)
- Status: planned → plans/cloud-stale-master.md, later
- Status: done 2026-10-19. The cause was a local `master` frozen since the environment was set up, not dot-claude history; cloud sessions now push the session branch straight to GitHub's `master` (design/git-sync.md).

## Use /clear instead of starting a new cloud chat
- Every new cloud chat has to start a new container, clone the repo and run the setup again. I wondered whether /clear could replace that: it wipes the conversation but keeps the same container, repo and branch, and the session-start hooks run again. Not tried yet; it's not confirmed that the web and phone apps accept /clear. (2026-10-20, from a claude-assistant cloud chat)
