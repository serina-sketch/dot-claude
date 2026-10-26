# The tutor skill

*How I want the `/tutor` skill to work, with the date and why. The skill itself is `skills/tutor/SKILL.md`. The rules came out of studying COMP360; that course's own design is in `claude-assistant/.brain/design/math-tutor.md`.*

## Struggle is the goal (2026-10-26)
- The skill used to treat struggle as bad: many checks or big hints put a problem on a re-quiz list, as a sign I hadn't mastered the material. That's not how I want it. If something takes me a lot of tries, it means I'm trying something hard. Struggle is the goal; the goal is not to get everything right easily.
- The most useful way for me to learn is to bang my head on the hardest problems. Going back to the very fundamental stuff felt like a waste of time.
- Hints stay the same; only the framing changes: spending a long time and many tries is a sign of learning and understanding.
- The re-quiz list became "Hard problems I fought through": still recorded, with the try count (and the time, if the project tracks it), as problems I could try again, but new hard problems come first.
- **Sessions:** straight to the hardest open problem. Warm-up recall questions and the end-of-session check problem are dropped, because I don't think they really help.
- **Problem first, building blocks as tools:** a mix of working the hard problem and building up. We start from a hard problem, then bring in the material it needs as tools to solve it, instead of learning the pieces without knowing what they're for. On a topic I've already started, basics come back only when they block me.
- **Why I got it wrong:** when I gave a wrong answer, we didn't try to understand why, or which path led me there; Claude just told me the right way to think about it. A wrong answer comes from a specific lack in understanding, so we identify it: I trace my path, we name the exact gap, then fix it. I want to spend more time on this. "Why" questions on key steps help find gaps, and wrong turns are written down.
- **Similar problems** change the original (drop a condition, flip the direction, change a number), to check I built the reasoning rather than followed it.
- Inspired by the video "The Cambridge Method: Struggle First, Understand Later" (Ryan Ward), summarized in `claude-assistant/claude-obsidian/Knowledge/cambridge-method-struggle-first.md`. Not taken from it: a minimum struggle time before hints, and less handholding when I'm struggling.
