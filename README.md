# Claude dotfiles

My global Claude Code setup (`~/.claude`), synced through GitHub so every PC and cloud session gets the same rules and skills.

- `CLAUDE.md`: global rules for every project (plans, brain).
- `settings.json`: global settings.
- `skills/`: my skills (tutor, maid, coach, commit). The mode skills' source is `claude-assistant/tools/modes/`.
- `browser-skills/`: skills uploaded to claude.ai for Claude in the browser.

Only the files allowed in `.gitignore` are tracked. Logins, chat transcripts and caches never leave the machine.

## Install on another PC
Clone into `~/.claude` (before or after logging in to Claude Code):

    git clone <repo-url> ~/.claude-dotfiles
    cp -r ~/.claude-dotfiles/. ~/.claude/   # if ~/.claude already exists
    # or, on a fresh machine: git clone <repo-url> ~/.claude

Update with `git pull` inside `~/.claude`.
