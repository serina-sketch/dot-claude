---
name: handoff
description: "Save where a chat stopped into the project's brain so a new chat can pick it up, or pick up where the last chat stopped. Save: when I say 'put it in the brain', 'hand off', 'save where we are', or that I'll start a new chat. Resume: when I say 'read the brain and continue', 'pick up where we left off', 'where did we stop', or start a chat by asking to continue. Claude also uses it on its own: save when a long chat is close to being summarized, when a big piece of work just finished and was committed, or when I say I'm stopping for now; resume when a chat opens with no request but the project's brain has a Last stop."
---

# Handoff

Two halves: **save** at the end of a chat, **resume** at the start of the next. The point: a new chat continues exactly where the old one stopped, right before I said to save, without me re-explaining. Brain format: the `brain` skill.

**When Claude calls it without being asked:** save when the chat is long enough that it may soon be summarized, when a big piece of work was just finished and committed, or when I say I'm stopping for now; say in one line that it saved. Resume when a new chat starts with only a greeting or "continue" and the brain has a Last stop.

## Save

Do all of it without asking; it's routine.

1. **Catch up the last stretch first.** The brain is written live, but the last few messages often aren't in it yet. Go back from the end of the chat to the last time the brain was written, and record whatever from those messages isn't in it yet, each in its folder (`brain` skill). Not the whole chat: what was written live stays as it is.
   - `thoughts/`: questions and passing thoughts I had.
   - `ideas/`: things I said I could do, with their status; "later" ones get a plan with status later.
   - `plans/`: plans I OK'd that have no file yet, and steps done but not ticked.
   - `design/`: every decision and detail I stated (date and why), what I confirmed working, known issues left open; reversals crossed out with `Replaced <date>`.
   - `knowledge/`: research, measurements, setup notes, with the date and source.
   - `tools/`: helper scripts made for the project.
   
   Check each one against what's already there before writing (read the file you'd edit; for anything else, ask `brain-search`), so nothing is written twice. Only my words and decisions, never Claude's suggestions I didn't take; no debugging back-and-forth, only final behavior.
2. **Every plan this chat touched** (`.brain/plans/`): rewrite its two lines so a chat with no memory of this one can act on them.
   - `Where I stopped:` the date, what got done (files, commits, counts that matter), and what's still not done or not tried.
   - `Next step:` the very next thing. **If the chat ended on a question I hadn't answered yet, write that question here word for word, with its options**, so it can be put back to me unchanged. Add any setup it needs (what to turn on, which command, which file).
   - Tick the steps that are done; a plan made in this chat and not saved yet gets its file now.
3. **The `## Last stop` block** in `.brain/index.md`, above the `<!-- auto ... -->` marker (create it there if missing): replace its text with one or two lines: the date, what the chat was doing, and the plan file to pick up from. Only one last stop: overwrite, don't append.
4. **Commit** the way the project's `CLAUDE.md` says (chatbot: the `commit-merge` agent; a project that commits only when asked: say it's ready to commit instead).
5. **Tell me** in a few lines: what's saved, the commit, and the one line a new chat will start from.

## Resume

1. Read `.brain/index.md`: its `## Last stop` block, and "Open right now" for the rest.
2. Read the plan file the last stop names, and only that (plus any file it says to read first). Run `git log --oneline -5` to see if anything was committed after the save (another chat, another device).
3. Say in two or three lines where we stopped. Then, if its `Next step` holds an open question, **ask it again exactly as it was, with its options**; otherwise start on the next step (if it changes files, the usual plan-first rule applies).
4. Don't read the other brain files to get ready; anything deeper goes to the `brain-search` agent when it's needed.
