# The deep-version skill
*A command that turns a big task into the version a top expert would do.*

## What it is (2026-11-09)
`/deep-version` (`skills/deep-version/SKILL.md`) is a one-off command, like `/eli5`, that I call on a big task. It answers Felix Rieseberg's four questions in plain words (what a top professional would do that I'm not asking for, the rawest material they'd start from, their methods and tools, and what outside Claude and me would show the result is right), rewrites my request into that deeper version, and waits for my answer before doing anything.

Why: I found the prompt in the r/ClaudeAI thread "What's the one prompt you keep coming back to?"; it comes from Felix's article [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/). It was the one thing from the thread I wanted to focus on, and I decided it should be a small command for big tasks. I named it "deep version".

It keeps the article's guardrails: deeper, not bigger; do what the expert does instead of role-playing them; Claude never judges its own result; big tasks only, because it can over-engineer small ones.
