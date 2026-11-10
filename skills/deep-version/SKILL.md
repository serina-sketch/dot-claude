---
name: deep-version
description: "Make a big task deeper, not bigger: say what a top professional in the field would do that I'm not asking for, the rawest material they'd start from, their methods and tools, and what outside you and me would show the result is right, then rewrite my request into that deeper version and ask before doing it. From Felix Rieseberg's 'How to be more ambitious'. One-off, not a mode. Use when I type /deep-version or ask for the deep version of a task. Don't turn it on by yourself otherwise."
---

# What this is
- The source is Felix Rieseberg's article "How to be more ambitious: A tutorial for humans with models" (https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/). His prompt, word for word:
  > "I want a deeper version of this task, not a bigger one. Before rewriting it: (1) say what a top professional in this field would do here that I'm not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right. Then rewrite my prompt to ask for exactly that."
- The idea: people ask for small, safe versions of things because they don't believe more is possible. This asks for the task done the way the best expert in the field would do it.
- It's for big tasks and projects only. It can over-engineer small things. If my task is small, say so in one line and ask whether I still want it.
- It's one-off: it doesn't switch off whatever mode is on, and once it's done we go back to what we were doing.
- If I give no task, use the task we're on. If that isn't clear, ask what it is.

# How it runs
1. **Answer the four questions.** A few plain lines each, specific to my task and my real situation (read the project files that matter if needed), never generic.
   - What a top professional in this field would do that I'm not asking for.
   - The rawest material they'd start from: the real data, the original source, my actual work, instead of a summary or something already digested.
   - The specific methods and tools they'd use: real instruments of the field, named by name (for example a database or a statistical test instead of a markdown table).
   - What, other than you or me, would show the result is right: an outside check, like real data, a test, a real person in the field, or real-world results.
2. **Rewrite my request** into the deeper version, as a prompt I could send, in a block.
3. **Ask** whether to go with it, keep the original, or change something. Do nothing else until I answer.

# Rules
- Deeper, not bigger: more expert and closer to the raw material, not more features or more steps.
- Do what the expert does, don't role-play them. Ask for what a short seller does to research a position, not for writing like a short seller. No personas.
- Never let Claude be the judge of its own result. The check in question 4 has to come from outside the model and me.
- Aim high. A specific hard goal beats "do your best". If the expert's standard sounds unreasonable, say so plainly anyway.
- Plain words, short sentences, one idea per sentence. Explain any field term the first time it shows up.
- The project's own instructions (voice, character, plan-first rules) still apply on top of this.
