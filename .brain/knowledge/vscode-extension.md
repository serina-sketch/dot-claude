# Claude Code in VS Code: selection and shortcuts

*Checked 2026-10-22 by the claude-code-guide agent from https://code.claude.com/docs/en/vs-code.md (docs, not a running build; keys may differ by version). Windows keys.*

## Selection reaching Claude
- The prompt box footer shows how many lines are selected; the **X** on it stops the selection being sent, and it comes back with the next selection. That was the first thing to check when Claude stopped seeing selections.
- Not sent: a queued message (keeps the selection it had when Enter was pressed); a path with a `Read` deny rule; with "Attach Open File" off, the file path is sent only while text is selected.
- **Alt+K** (editor focused) inserts an @-mention like `@file.md#40-60` of the selected lines.

## Shortcuts
- Focus Input: Ctrl+Esc (Windows opens the Start menu on it; rebind if it does nothing)
- Open in New Tab: Ctrl+Shift+Esc (Windows: Task Manager)
- New Conversation: Ctrl+N, only with the setting `enableNewConversationShortcut` true (default false) and Claude focused
- Reopen Closed Session: Ctrl+Shift+T
- Insert @-Mention Reference: Alt+K
- Toggle Focus view: Ctrl+Alt+F
- No default key: Accept / Reject Change at Cursor, Open in Side Bar, Open in New Window, Rename Session Tab.
- Rebind in Keyboard Shortcuts (Ctrl+K Ctrl+S), search "Claude Code"; command IDs are in `%USERPROFILE%\.vscode\extensions\anthropic.claude-code-*\package.json`.
