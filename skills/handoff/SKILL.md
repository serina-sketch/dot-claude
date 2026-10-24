---
name: handoff
description: "Save where a chat stopped so a new chat can pick it up, or pick up where the last chat stopped. Save: when I say 'hand off', 'put it in the brain', 'save where we are', or that I'll start a new chat. Resume: when I say 'read the brain and continue', 'pick up where we left off', 'where did we stop', or when a chat opens with no other request and `.brain/handoff/handoff.md` exists."
---

# Handoff

Two halves: **save** right before I start a new chat, **resume** at the start of the next one. The brain is already written live during the chat, so every step is already in it. Handoff only has to write where we stopped. It must not re-read the chat or sweep the brain, to save tokens.

Save only when I ask. Resume also when a chat opens with no other request and `.brain/handoff/handoff.md` exists.

## Save

Do all of it without asking; it's routine.

1. **Update the current thread's plan file first:** its `Where I stopped:` and `Next step:` lines, and **if the chat ended on a question I hadn't answered, that question word for word, with its options**. Only that one plan; if the chat had no plan, skip this. Every thread keeps its place in its own plan file, so the handoff never holds anything that lives nowhere else.
2. **Then write `.brain/handoff/handoff.md`** (create the folder if missing; overwrite the file, there is one handoff only: the latest chat). Nothing else in the brain. Don't re-read the chat, don't check brain folders, no subagents. It holds:
   - the date and time
   - what the chat was doing
   - where it stopped: what got done (files, commits, counts that matter) and what's not done
   - the next step, and which plan file to open (the open question is in that plan)
   - any setup the next step needs (what to turn on, which command, which file)
3. **Commit and push in one command**, the way the project's `CLAUDE.md` says. A project that commits only when asked: say it's ready to commit instead.
4. **Reply in one line:** the commit, and the line the new chat starts from.

## Resume

1. Read `.brain/handoff/handoff.md` and the plan file it names, nothing else (plus `git log --oneline -5` to see if anything was committed since).
2. Say in two or three lines where we stopped. If it holds an open question, ask it again exactly as it was, with its options. Otherwise start the next step (if it changes files, the usual plan-first rule applies).
3. Then delete `handoff.md` and commit that the project's usual way. A project that commits only when asked leaves it uncommitted until I say.
4. If there's no handoff file but `.brain/index.md` still has an old `## Last stop` block (a project not migrated yet), use that block once the same way, and remove it from the index.
5. Don't read other brain files to get ready; anything deeper goes to the `brain-search` agent when it's needed.
