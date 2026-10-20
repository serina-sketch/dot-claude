# Explain things simply

*Ideas for making Claude explain concepts in a way that's easy to understand.*

## A skill for easy explanations
- I've seen Claude skills that tell Claude to explain things in a way that's easy to understand. I want to know about these; it'd be handy for learning software concepts, like Shiori's supervisor restart (mimitabi `plans/learn-supervisor.md`). (2026-10-14)
- I want to make it a global ELI5 skill whose only job is explaining things in a way I can understand. None of my modes cover that: tutor makes me learn, coach makes me build, maid does the work. ELI5 is different, and it works together with the other modes. (2026-10-20, from a claude-assistant cloud chat)
- Existing skills found online (2026-10-20):
  - [DreambigOu/ELI5](https://github.com/DreambigOu/ELI5) (about 1.8k stars): adapts the explanation to an audience (an age, a school level, a job, a relationship; defaults to age 5). Steps: one sentence on what it is, an analogy, details only as needed, then why it matters to you. No jargon, one idea per sentence, never talk down, 80% accurate and understood beats 100% and lost.
  - [dzhng/skills eli5](https://github.com/dzhng/skills/blob/main/skills/engineering/eli5/SKILL.md): for technical specs; simplify the telling, never the claims. Walks one concrete example end to end, defines every term the first time, and passes only if the text stands alone with no follow-up questions.
  - [Community plugin eli5](https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md): ten lines; `/eli5 <topic>` makes a web page with big pictures and few words.
  - [alexknowshtml teach](https://github.com/alexknowshtml/claude-skills/blob/main/teach/SKILL.md): closer to tutor than ELI5; quizzes you item by item until you've understood a session.
- What I want from it (2026-10-20): something I call when I'm stuck on something I just don't understand. I run the command, it explains the thing, and once it's done we go back to the regular task, so it's temporary, not a mode that stays on. The best of the existing ones is dzhng's, because it walks through one example from start to finish; I need examples to understand. Not the web page with big pictures. It should be like what tutor mode knows about learning with AI, but geared toward understanding, not toward being able to solve the problem myself. For example, if I ask how AI works, it's because I know nothing about AI and need the basics, not because I want to get into AI research. It can reuse some parts of tutor mode.
- Status: done 2026-10-20 → `skills/eli5/SKILL.md`, design in design/eli5.md.
