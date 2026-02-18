# Claude Workspace

This file provides workspace-level context for `/Users/jengland/claude`.
Keep process and behavior rules out of this file.

## Repositories

| Repo | Purpose |
|------|---------|
| `benchmarkr/` | QC web app for factory workflows |
| `chg/` | Multi-repo CHG product workspace |
| `crewfinder/` | Crewfinder product repo |
| `untitled-ds/` | Untitled UI design system library |

## Working Across Repos

Each project is independent and has its own git history, dependencies, and env.

```bash
# Work in a specific repo
cd benchmarkr

# Or run commands from workspace root
git -C benchmarkr status
npm --prefix benchmarkr run dev
```

## Shared Dependency Note

`benchmarkr` consumes `untitled-ds` through `npm link` during local development.
If the link breaks:

```bash
cd untitled-ds && npm link
cd benchmarkr && npm link @playalink/untitled-ds
```

For Tailwind/PostCSS imports through symlinks, prefer direct dist paths.

## Instruction Sources

- Agent behavior and process rules are synced into each repo `AGENTS.md`.
- Source of truth is `/Users/jengland/claude/.ai-rules/`.
- After rule edits, run `./.ai-rules/sync-ai-rules.sh` from `/Users/jengland/claude`.
- Shared rules can be overridden by `{project}/.ai-rules/` when filenames match.

## Repo Context Docs

Use each repo's own `CLAUDE.md` for project-specific runtime context.
