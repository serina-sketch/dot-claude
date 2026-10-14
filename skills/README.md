# My three modes

Three ways for Claude to work with me. Each one is a Claude Code skill: a folder with a `SKILL.md` (the rules) and a `goal.md` (why I made it).

| Mode | Type | Who thinks | Who does the work | The point |
| --- | --- | --- | --- | --- |
| Tutor | `/tutor` | Me | Me | Learn it so I can do it alone (school, skills) |
| Coach | `/coach` | Me | Claude | Build it and understand how it works |
| Maid | `/maid` | Me (ideas first) | Claude | Get it made; output over learning |

Each mode stays on until I say "<mode> mode off" or switch to another one.

## Where they live

The modes' source is here, in the `dot-claude` repo (`~/.claude/skills/`). Edit them here directly, then commit and push `~/.claude` so other devices get the change with `git pull`. There's no install step.

## Personalize for a project

Each project can have its own version of the modes, without changing the originals.

**The easy way:** open Claude Code in that project, turn on a mode (for example `/coach`), and say **"personalize coach mode."** Claude asks up to three short questions, then writes the file for you.

**By hand:** create `.modes/personalize.md` in the project's root folder:

```markdown
# Modes in this project
## All modes
<what this project is, files to read first, rules that apply to every mode>
## Tutor
<changes to tutor mode here, or "none">
## Maid
<changes to maid mode here, or "none">
## Coach
<changes to coach mode here, or "none">
```

Whenever a mode turns on, it reads this file. These rules add to the mode's own rules, and win where they disagree. Good things to put there:
- What the project is and what I'm doing in it.
- Files to read first (course notes, a design doc, the main script).
- Where notes go. By default all modes share `.modes/notes.md`, one section per mode.
- Anything to do differently here: what to skip, what words to use, how often to stop.

Example for a chatbot project:

```markdown
# Modes in this project
## All modes
This is my chatbot character for SillyTavern. The character card is `card.json`; read it first.
## Tutor
none
## Maid
none
## Coach
I'm learning how character cards work. Explain each section of the card (personality, scenario, first message, example dialogue) the first time we touch it. I decide what goes in each section; you write it out.
```

## brain

Not a mode: the format of every project's `.brain/` folder, and `brain_index.py`, which rebuilds its indexes. Hooks in `settings.json` run it after every write in `.brain/` and at the end of each reply.
