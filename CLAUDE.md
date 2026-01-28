# Jordan OS Workspace

This is a workspace containing multiple projects. Each project has its own git repository, dependencies, and environment.

## Projects

| Project | Description | Tech Stack |
|---------|-------------|------------|
| `benchmarkr/` | QC web app for factory workers | Next.js, Prisma, Supabase, Clerk |
| `untitled-ds/` | Untitled UI design system library | React, Storybook, npm publishing |

## Working Across Projects

### Important: Project Context

Each project is independent. Before running commands, ensure you're in the correct project directory:

```bash
cd benchmarkr    # or cd untitled-ds
```

### Git

Each project has its own `.git` repository. Git commands must be run from within a project:

```bash
# Option 1: cd first
cd benchmarkr && git status

# Option 2: use -C flag
git -C benchmarkr status
git -C untitled-ds log -5
```

### npm / Node

Each project has its own `package.json` and `node_modules`:

```bash
# Option 1: cd first
cd benchmarkr && npm run dev

# Option 2: use --prefix
npm --prefix benchmarkr run dev
npm --prefix untitled-ds run storybook
```

### Environment Variables

Each project has its own `.env` file. These are loaded when running from within that project directory.

## Shared AI Rules

Shared rules for all projects live in `.ai-rules/` at this level:

```
.ai-rules/
├── global/           # Applied to all projects
├── skills/           # Shared skills (/commit, /untitled-ui-component)
└── sync-ai-rules.sh  # Syncs to all projects
```

### Sync Rules

After editing shared rules, run:

```bash
./.ai-rules/sync-ai-rules.sh
```

This discovers all projects and syncs shared + project-specific rules to each.

### Rule Precedence

Project-specific rules override shared rules when filenames match:
1. Shared rules from `jordan-os/.ai-rules/`
2. Project rules from `{project}/.ai-rules/` (override shared)

## Project-Specific Instructions

For detailed project context, see each project's `CLAUDE.md`:
- `benchmarkr/CLAUDE.md` - Database schema, API patterns, component usage
- `untitled-ds/CLAUDE.md` - Component development, Storybook, npm publishing
