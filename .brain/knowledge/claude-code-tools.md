# Claude Code features and other agents

*How parts of Claude Code work (like voice dictation), and other coding agents compared to it.*

## Voice dictation: why project words come out right only sometimes (checked 2026-10-20)
- Claude Code's dictation (`/voice`, hold a key to record) streams the audio to Anthropic's servers to be transcribed; nothing is done locally. Source: [Claude Code docs](https://code.claude.com/docs/en/voice-dictation).
- The transcriber gets a short list of hint words: coding terms, the name of the project the session is opened in, and the current git branch. It doesn't learn from past chats or read files. Source: unofficial only ([AquaVoice](https://aquavoice.com/blog/voice-dictation-claude-code), [wmedia.es](https://wmedia.es/en/tips/claude-code-voice-mode-dictation), the `voiceKeyterms.ts` file in a [source mirror](https://next.tangled.org/oppi.li/claude-code/blob/main/services/voiceKeyterms.ts)); Anthropic's docs don't mention it.
- Users report there's no custom word list ([AssemblyAI](https://assemblyai.com/blog/voice-coding-dictate-to-coding-agents)).
- What I saw: "mimitabi" came out right in a session opened in the mimitabi repo, and wrong in claude-assistant. That fits the project-name hint.

## Pi, a minimal coding agent (checked 2026-10-20)
- Pi is an open-source terminal coding agent by Mario Zechner (libGDX), in the `pi-mono` repo (MIT). He made it because he found Claude Code bloated.
- It has four tools (read, write, edit, bash), a short system prompt and no permission prompts; you extend it with TypeScript extensions, skills, prompt templates and themes. As far as found, no subagents or plan mode built in, and no VS Code panel.
- It works with 20+ providers on your own API key (Anthropic, OpenAI, Google, xAI, DeepSeek, Mistral, Groq…). Its packages: `pi-ai` (model access), `pi-agent-core` (agent loop), `pi-tui`, `pi-coding-agent`, plus a Slack bot and a web UI library. OpenClaw is built on its parts.
- One source says Earendil acquired it in April 2026; only one source, unconfirmed.
- Compared to my setup: switching would mean rebuilding the hooks, agents, skills and cloud sessions, and likely paying per token.
- Sources: [urandom.io](https://urandom.io/blog/2026-03-07-pi-dev-deep-dive), [implicator.ai](https://www.implicator.ai/pi-is-not-a-claude-code-rival-it-is-a-harness-rebellion/), [dsebastien.net](https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Pi+Mono), [LLM Reference](https://www.llmreference.com/agent/pi).
