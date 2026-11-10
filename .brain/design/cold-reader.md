# The cold-reader agent
*An independent evaluator that reads a document knowing nothing and says whether it makes sense.*

## What it is (2026-11-09)
`agents/cold-reader.md` is a global, read-only agent. Claude calls it, but only when I tell it to. Its file holds the definition of a cold reader; each time, Claude gives it the file(s), who will really read them and what that reader has to be able to do afterward. It reads with no other context and reports where it got lost, what it had to guess, unclear words and contradictions, plus a one-line verdict. It suggests no rewrites; Claude and I decide the fix.

Why: from the r/ClaudeAI thread "What's the one prompt you keep coming back to?" (show a document to a cold reader and ask if they get it). I wanted an agent rather than a skill, basically an independent evaluator. It runs on Opus at medium effort, because judging makes more sense on Opus, and we won't use it a lot.
