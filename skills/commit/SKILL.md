---
name: commit
description: Stage, commit, and push all current changes with a generated commit message
context: fork
model: haiku
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
---
Commit and push all changes in the current git repository.

1. Run `git status` and `git diff HEAD` to see what changed. Run `git log --oneline -10` to match the repo's commit message style.
2. Stage everything with `git add -A`.
3. Write a concise commit message: a short summary line, plus a body only if the change needs explaining. If $ARGUMENTS is given, use it as guidance for the message.
4. Commit. End the message with:
   Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>
5. Push with `git push`. If the branch has no upstream, use `git push -u origin <branch>`. Never force-push; if the push is rejected, report the error and stop.
6. Report the commit hash, message, and push result.

If there is nothing to commit, say so and stop. If a pre-commit hook fails, report the error; do not bypass it with --no-verify.
