---
name: brain
description: "The format of a project's .brain/ folder (thoughts, ideas, plans, design, knowledge, tools) and the script that rebuilds its indexes. Read it before creating or restructuring files in .brain/, or when an index looks wrong."
---

# The brain

Every project keeps a `.brain/` folder at its root, written live during chats, so any chat on any device can catch up from it. The flow is **thoughts → ideas → plans → design**, plus **knowledge** (research) and **tools** (Claude's helper scripts).

## Indexes are built, never hand-written

`brain_index.py` (next to this file) rebuilds every folder's `index.md` and the part of `.brain/index.md` below the `<!-- auto ... -->` marker. A hook runs it after every Write/Edit in `.brain/` and at the end of every reply. If files were written another way (a shell command), or on a machine without the hook, run it yourself:

    python ~/.claude/skills/brain/brain_index.py

Everything above the marker in `.brain/index.md` is hand-written: what the project is and what each folder is for.

## Format the script reads

Every file starts with `# Title`, then one line in italics saying what it holds. That line becomes its entry in the folder index.

- **thoughts/**: one file per topic. Each question or thought is a `## Heading (date)`, with what it led to.
- **ideas/**: one file per topic. Each idea is a `## Name`, followed by a status line:
  `- **Status:** planned 2026-10-14 → plans/<file>.md`
  No status line means it's still just an idea. Statuses: planned, done, dropped. Keep the history on the same line: `planned 10-14 → dropped 10-16 (reason) → planned 10-20`. The ideas index groups every idea by its latest status.
- **plans/**: one file per plan. The italic line says `Made <date>. Status: <...>.` Steps are checkboxes `- [ ]` / `- [x]`; a paused step is `- [ ] (on hold) ...`. The index counts steps left. A plan for later with no steps yet is fine.
- **design/**: one file per topic. Every decision with its date and why. A reversal keeps the old line crossed out with `Replaced <date>`.
- **knowledge/**: one file per topic. Each finding is a `## Heading (checked <date>)` with its source.
- **tools/**: scripts. Each one starts with a docstring (Python) or comment block saying what it does and how to run it.
