# Notes for every project

- **Browser Claude has a `site-study` skill** (source: `~/.claude/browser-skills/site-study/`, uploaded to claude.ai as a zip; not loaded locally). When I need to know how a website looks or works (to copy its UI, layout or flow), write the user a short message for Claude in the browser that uses the skill: the URL, the goals (what we're building, our data, which screens matter) and any specific questions.

# Plans (added 2026-10-13)
- **Show the plan first.** Before changing files or doing any multi-step work, show me the plan and wait for my OK. Quick questions get a direct answer with no plan. Routine writes a project's own rules already require (like the journal and its commits) don't need a plan either.
- **Format:** big categories as headings `### A. Name`, `### B. Name`. The steps under each category as a numbered list 1, 2, 3, one short line each.
- **Save every plan** in `.brain/plans/` at the project root (create it if missing): one file per plan, named after it (like `second-brain.md`), with each step as a checkbox `- [ ]`. `plans/index.md` starts with **Now** (which plan and step I'm on; update it whenever I move), then one line per plan with its status. I often ask for one step at a time: do only that step, check it off, and leave the rest in the file so we can come back to it. If I put a step on hold, mark it "(on hold)" instead of deleting it. When a whole plan is done, delete its file and its line.
- **Bring it back:** at the start of a session, read `.brain/plans/index.md` and mention Now in one line. When I ask "what's left?" or "the plan", show the unchecked steps.
