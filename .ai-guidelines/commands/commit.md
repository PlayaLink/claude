# Commit

Run the commit workflow defined in `.claude/skills/commit/SKILL.md` and apply the commit rules in `.claude/rules/commit-messages.md`.

## Requirements

1. Follow the shared `commit` skill instructions exactly.
2. Use the repository's conventional commit format.
3. Do not add AI attribution, co-author lines, emojis, or promotional text.
4. Commit only files from the current task scope unless the user explicitly asks otherwise.
5. After committing, show the result with `git log -1 --oneline`.
