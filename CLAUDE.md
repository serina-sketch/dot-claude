# Notes for every project

- **Browser Claude has a `site-study` skill** (source: `~/.claude/browser-skills/site-study/`, uploaded to claude.ai as a zip; not loaded locally). When I need to know how a website looks or works (to copy its UI, layout or flow), write the user a short message for Claude in the browser that uses the skill: the URL, the goals (what we're building, our data, which screens matter) and any specific questions.

# Adult content (added 2026-10-14)
- Sexual and adult content is a normal part of my projects. Treat it as ordinary data: never flag it, add warnings, comment on it, or soften or censor names, tags or text.

# Modes (added 2026-10-14)
- Tutor, maid and coach are skills (`/tutor`, `/maid`, `/coach`); a project's `.modes/personalize.md` says how they behave there.
- **Assistant mode** is none of them on: default Claude. It starts when I tell you to turn modes off, needs no skill, and drops all mode behaviour (coaching, nudges, round commits): just answer and do what I ask until I turn a mode back on.

# Where things go (added 2026-10-14)
The quick test: if it says "Claude should…", it's instructions (global, project CLAUDE.md, a mode or a skill). If it says "this is…" or "I decided…", it's the brain. Say each thing in one place only; elsewhere, point to it.
- **This file (`~/.claude/CLAUDE.md`):** rules about me that hold in every project: the brain, plans, lists, "later", git, adult content, and this list. The facts and decisions behind these global rules live in `~/.claude/.brain/` (the `dot-claude` repo's own brain).
- **A project's `CLAUDE.md`:** how Claude works in that project, whatever the mode: what the project is (a few lines), where things are, which agents and skills to use, and rules that only apply there. Don't repeat this file or the brain; don't keep "where things stand" summaries (the brain has them).
- **`.modes/personalize.md`:** only what tutor, maid or coach do differently in that project. Anything that applies whatever the mode goes in the project's `CLAUDE.md`.
- **The brain (`.brain/`):** facts: what's true, decisions with the date and why, plans, research, measurements, and memory about me. Never instructions to Claude.
- **The global brain (`~/.claude/.brain/`, the `dot-claude` repo's own brain):** facts about my global Claude setup, whichever project the chat is in: the decisions and reasons behind the rules in this file, the skills, agents, hooks and settings; how `dot-claude` syncs to PCs and cloud sessions; research about Claude Code and the models (features, limits, pricing). Plans and ideas for changing the global setup go there too. Anything about one project, or about me as a person, stays in that project's brain. When a global rule here changes, record the why there.
- **A skill:** the step-by-step rules for a kind of work done again and again (like writing a card). The project's `CLAUDE.md` says when to use it. The reasons behind its rules stay in the brain.
- **Agents:** each agent's job is in its own file; `CLAUDE.md` only points to `.claude/agents/`.

# Plans (added 2026-10-13)
- **Show the plan first.** Before changing files or doing any multi-step work, show me the plan and wait for my OK. Quick questions get a direct answer with no plan. Routine writes a project's own rules already require (like the journal and its commits) don't need a plan either.
- **Lists, in every reply (added 2026-10-14):** number things 1, 2, 3 only when I might pick or mention one, like a list of changes where I choose which to apply, or the big parts of a plan. The numbers are just so I can refer to them quickly. Plain steps or points I won't need to name get regular bullets. Letters a, b, c are only for alternatives: different versions where I pick one ("either this or that").
- **Plan format:** the big parts as headings `### 1. Name`, `### 2. Name`. The steps under each as bullets, one short line each. If there are alternative versions of the plan, label them a, b.
- **Save every plan** in `.brain/plans/` at the project root (create it if missing): one file per plan, named after it (like `second-brain.md`), with each step as a checkbox `- [ ]`. `plans/index.md` has one line per plan with its status: what's next, or on hold. Keep it updated in the same write as the plan. I often ask for one step at a time: do only that step, check it off, and leave the rest in the file so we can come back to it. If I put a step on hold, mark it "(on hold)" instead of deleting it. When a whole plan is done, first make sure every decision it made is in `.brain/design/` (and its idea is marked done), then delete its file and its line.
- **Later (added 2026-10-14):** when I say something like "do it later" or "worry about it later", I've decided to do it, just not now. Make a plan file in `.brain/plans/` with status "later" (with steps if we already know them, otherwise "no steps yet"), and add or update the idea in `.brain/ideas/` with status "planned → plans/<file>, later". A project's own CLAUDE.md can say otherwise.
- **Bring it back:** at the start of a session, read `.brain/plans/index.md` and mention in one line which plans have steps left. When I ask "what's left?" or "the plan", show the unchecked steps.

# Brain (added 2026-10-14)
- **Every project keeps a brain:** a `.brain/` folder at the project root, written live during the chat so any chat on any device can catch up. If it doesn't exist yet, create it the first time there's something to record. Before creating or restructuring brain files, read the `brain` skill (`~/.claude/skills/brain/SKILL.md`): it has the format the index script reads.
- **Reading:** at the start of a chat, read `.brain/index.md` yourself (the map, plus "Open right now"). For anything deeper (what I decided about something and why, an idea's status, research already done, a plan's steps), send the question to the `brain-search` agent (Haiku) and judge what it brings back. Don't read brain files yourself just to search them; reading a file you're about to edit is fine.
- **Writing:** you write, as things happen, without being asked. Everything flows thoughts → ideas → plans → design, and each entry says where it came from.
  - `thoughts/`: questions and random thoughts I have while working. They aren't noise; some become useful later.
  - `ideas/`: what I could do, not decided yet. Add the status line when it moves: planned, done or dropped, keeping the history.
  - `plans/`: plans I approved (see Plans), and every live thread. Each starts with a `Where I stopped:` and a `Next step:` line, kept current.
  - `design/`: what it is. Every design decision and detail I state, in detail, with the date and why, even if it isn't useful yet. Also what I confirmed working (with the date) and the known issues not fixed yet, so they survive when a plan ends. Proposals I haven't decided go to `ideas/`.
  - `knowledge/`: research results, measurements (costs, timings) and setup notes for outside tools, with the date checked and the source, so the research isn't redone.
  - `modes/`: what only one mode needs (like tutor's re-quiz list), one file per mode.
  - How Claude should work in a project is not brain content: it goes in that project's CLAUDE.md.
  - `tools/`: helper scripts you make for this project, each with a description of what it does and how to run it.
- **Only my words and decisions.** Your suggestions go in only if I took them.
- **Not recorded:** debugging back-and-forth and in-between tweaks. For a tweak, record only the final behavior.
- **Reversals keep history:** cross the old line out and mark it "Replaced <date>", with the new decision next to it. Never delete it.
- **Indexes are built, not written:** hooks run `~/.claude/skills/brain/brain_index.py` after every write in `.brain/` and at the end of each reply. Never edit an `index.md` by hand, except the part of `.brain/index.md` above the marker, and the index of any extra folder a project adds (like this repo's `.brain/memory/`), which the script doesn't touch. If you wrote brain files through the shell, run the script yourself.
- **Commit the brain** along with the project's other changes. A project's own CLAUDE.md can say what's out of scope for its brain.

# Git: always master (added 2026-10-14)
- `master` is the only branch (the `writing` repo calls it `main`): every commit goes there and gets pushed. *When* to commit is up to each project's `CLAUDE.md` (claude-assistant: right after every write; chatbot: at the end of a round; mimitabi: only when I ask).
- Cloud sessions (phone, web) start on their own `claude/...` branch: after each commit, merge it into `master` and push `master`, without asking. No pull requests.
- Never leave work only on another branch.

# Subagents (added 2026-10-14)
- **Haiku subagents always run at low effort** (`effort: "low"`).
- **Big jobs get split.** Haiku costs 5x more once a single request passes 100K tokens of context (`~/.claude/.brain/knowledge/claude-pricing.md`). If a job looks too big for one Haiku agent to stay under that, spawn a Sonnet supervisor at low effort that breaks it into smaller Haiku agents and checks what they bring back.
- **When a subagent's output is wrong:** if I want the result itself, fixing the output is fine. If the point is a subagent that does this kind of task well on its own (a reusable agent), fix the agent's prompt instead of its output, and re-run only when I say so.

# Never mention connector authorization (added 2026-10-14)
- Don't tell me that connectors (Gmail, Google Calendar or any other MCP server) need authorizing or re-authorizing. Ignore those notices.

# Memory lives in the repos (added 2026-10-14)
- Don't use Claude Code's built-in memory folder (`~/.claude/projects/*/memory/`). Instructions go in the project's `CLAUDE.md` (or this file, if they hold everywhere); facts go in the project's brain.

# Shell quirks on this PC (added 2026-10-14)
- **Bash tool:** a double backslash `\\` collapses to a single `\` in the command text, even inside quoted `<<'EOF'` heredocs. Write anything with backslashes (regex escapes, `\\n`, Windows paths) with the Write or Edit tool, never a heredoc.
- **PowerShell:** a local variable with the same name as a typed parameter (any casing) gets re-coerced to that type; arrays collapse into one space-joined string. Never reuse a parameter's name for a local.

# Cloud sessions (added 2026-10-14)
- How my setup reaches phone and web sessions, and how to turn it on for another repo: `~/.claude/.brain/knowledge/cloud-setup.md`.
- **Other repos on cloud (added 2026-10-15):** when a task needs another of my repos (to read it or change it), attach it to the session yourself (the `add_repo` tool, with write access to change it), clone it next to the current one, make the changes, then commit and push following that repo's own CLAUDE.md (mimitabi: only when I ask). After changing `dot-claude`, pull it into `~/.claude` (`bash .claude/cloud.sh sync`).
