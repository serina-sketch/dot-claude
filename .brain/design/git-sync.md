# Git auto-sync across repos

- **Decided 2026-10-15:** every repo pulls `master` automatically, through hooks, not just a written rule. Why: I now work in about five repos at once (five folders in one VS Code workspace), on the PC and in cloud sessions at the same time, and the copies drifted out of sync. Too much to track by hand.
- **Pull automatically** rather than only warning (my choice, 2026-10-15).
- **How it works:** `git_sync.py` at the root of `dot-claude`. It runs at session start, before every `git commit` or `git push`, and after every push to check the repo matches GitHub. It covers the current repo, every sibling repo in the same parent folder whose GitHub owner is serina-sketch, and `~/.claude`. A conflicting merge is aborted, never forced; the commit is blocked with a message.
- **Workspace folders (2026-10-15):** I keep a `.code-workspace` file at the root of each main repo, tracked in git, listing every folder I have open. The script reads it, so it syncs exactly my open folders wherever they live. Repos in the same parent folder are the fallback.
