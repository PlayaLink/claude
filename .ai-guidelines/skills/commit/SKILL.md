---
name: commit
description: Create a git commit; trigger when user asks to commit or types /commit
---

# Commit Skill

Create a git commit following the project's commit conventions.

## Instructions

1. **Check git status** to see what files have changed
2. **Review the changes** using `git diff --staged` (or `git diff` for unstaged changes)
3. **Generate a commit message** following this format:

```
<type>(<scope>): <message title>

- Bullet points summarizing what was updated
```

### Commit Types

| Type     | Description                           |
| -------- | ------------------------------------- |
| feat     | New feature                           |
| fix      | Bug fix                               |
| chore    | Maintenance (e.g., tooling, deps)     |
| docs     | Documentation changes                 |
| refactor | Code restructure (no behavior change) |
| test     | Adding or refactoring tests           |
| style    | Code formatting (no logic change)     |
| perf     | Performance improvements              |

### Rules

- Title is **lowercase**, no period at the end
- Title should be a clear summary, **max 50 characters**
- Use the body to explain *why*, not just *what*
- Bullet points should be concise and high-level

### Critical

- **DO NOT** add "Generated with Claude Code" or any AI attribution
- **DO NOT** add "Co-Authored-By: Claude" lines
- **DO NOT** add emojis or promotional footers
- Only commit files that were changed during this session

## Execution

1. Stage the appropriate files (prefer specific files over `git add -A`)
2. Create the commit with the generated message
3. Show the result with `git log -1`
