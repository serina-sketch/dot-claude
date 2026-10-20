# The ELI5 skill

*How I want the `/eli5` skill to work, with the date and why. The skill itself is `skills/eli5/SKILL.md`.*

## What it is
- A skill I call when I'm stuck on something I just don't understand. It explains, and once it's done we go back to the regular task. It's temporary, not a mode that stays on, and it works together with tutor, coach and maid (2026-10-20).
- Different from tutor mode: tutor makes me learn so I can solve problems myself; ELI5 is for getting into a topic and understanding it. If I ask how AI works, it's because I know nothing about AI and need the basics, not because I want to do AI research. It reuses some parts of tutor mode (2026-10-20).

## Decisions (2026-10-20)
- **Called by me only:** `/eli5` or "ELI5 this"; never turns on by itself.
- **One example from start to finish:** taken from dzhng's ELI5 skill, the best of the ones found online, because I need examples to understand. Not the community plugin's web page with big pictures.
- **Ask first:** before explaining, it asks one short question about which part loses me.
- **No check at the end:** it just stops, and I ask more if I want.
- **Simple first, true later:** taken from DreambigOu's ELI5. Being about 80% right and understood beats being fully accurate. Just as much detail as I need to get the idea. Like the solar system diagram: once I've understood the planets in their neat circles, add that they're actually much smaller and farther apart, then add the real physics.
- **From tutor mode:** find which background idea I'm missing and explain that first; a small example right after a definition; one idea at a time. Left out: making me solve things, hints instead of answers, confidence ratings, justifying answers.
- **"What this simplified" line (2026-10-20):** every explanation ends with a short line naming what the simple version left out or bent. I liked it the first time I used the skill and want to keep it.
