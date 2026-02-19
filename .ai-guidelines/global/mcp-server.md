---
description: MCP server configuration patterns and security best practices
---

# MCP Server Configuration

## Always Use Environment Variables for Authentication

When configuring MCP servers, **always use environment variables** instead of passing credentials via command-line arguments.

### Configuration Pattern

**Correct:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Avoid:**
```json
{
  "args": ["--token", "your-token-here"]
}
```
This is less secure and may not work reliably.

### Common Environment Variables

| Service | Environment Variable |
|---------|---------------------|
| GitHub | `GITHUB_PERSONAL_ACCESS_TOKEN` or `GITHUB_TOKEN` |
| Figma | `FIGMA_API_KEY` |
| Atlassian/Jira | `ATLASSIAN_API_TOKEN` |
| Supabase | `SUPABASE_API_KEY` |
| Vercel | `VERCEL_API_TOKEN` |

Always use the `env` object in MCP server configuration, not `--token` flags in `args`.
