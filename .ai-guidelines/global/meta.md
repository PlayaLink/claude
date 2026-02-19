---
description: Maintainer guide for the ai-guidelines source-of-truth system
---

# AI Guidelines Maintenance System

## Source of Truth

- Always edit source files in `.ai-guidelines/`.
- Never edit generated outputs directly.

Generated outputs (do not edit):
- `AGENTS.md`
- `.cursor/rules/`
- `.claude/rules/`
- `.claude/skills/`
- `.claude/commands/`
- `.agents/skills/`

Source locations (edit these):
- `.ai-guidelines/global/`
- `.ai-guidelines/conditional/`
- `.ai-guidelines/skills/`
- `.ai-guidelines/commands/`

After changing source files, run `./.ai-guidelines/sync.sh`.

## When to Update Guidelines

Update guidelines when:
- The user says to remember a rule, convention, preference, or prohibition.
- A repeatable project convention is established.
- A current guideline is wrong, outdated, or incomplete.
- The user corrects agent behavior and the correction should persist.

## Placement Decision Tree

- Applies to all projects?
1. Yes: put it in `.ai-guidelines/global/`.
2. No: put it in `{project}/.ai-guidelines/`.

- Applies to all files in that scope?
1. Yes: use `global/{topic}.md`.
2. No: use `conditional/{topic}.md` with `globs` frontmatter.

## Update Method

- If a topic file exists, edit it.
- If not, create a new descriptive kebab-case file.
- Keep guidance concise, actionable, and testable.
- Add short examples when they reduce ambiguity.

## What Does Not Belong Here

- `CLAUDE.md`: runtime/project context (stack, commands, architecture), not behavior policy.
- Session memory files (`~/.claude/projects/*/memory/`): temporary working notes, not canonical conventions.
- `.ai-guidelines/`: canonical behavior guidance, workflows, skills, and commands.
