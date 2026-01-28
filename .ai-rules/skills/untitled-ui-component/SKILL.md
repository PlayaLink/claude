---
name: untitled-ui-component
description: Implement a UI component from a Figma URL using Untitled UI
---

# Untitled UI Component Skill

Implement a UI component from a Figma design URL, using Untitled UI components where available and building custom components where needed.

## Instructions

### Step 1: Get the Figma URL

If the user hasn't provided one, ask:

> Please provide the Figma URL for the component you want to implement.
> Format: `https://www.figma.com/design/{fileKey}/?node-id={nodeId}`

### Step 2: Fetch Figma Data

Use the MCP tool `get_figma_data` with:
- **fileKey**: Extract from URL (e.g., `figma.com/design/{fileKey}/...`)
- **nodeId**: Extract from URL param `node-id` (convert `1176-99947` → `1176:99947`)

### Step 3: Identify Components

Parse the Figma data and categorize all `type: INSTANCE` nodes:

| Category | How to Identify | Action |
|----------|-----------------|--------|
| Available in Untitled UI | Matches known component (Button, Badge, Input, etc.) | Import from `@/components/untitled-ui` |
| Internal Figma (`_` prefix) | Name starts with `_` (e.g., `_Nav item base`) | Build in `components/custom/` |
| Custom/app-specific | No Untitled UI equivalent | Build in `components/custom/` |

### Step 4: Request Master URLs (if building custom)

For components that need to be built, ask the user:

> I found these components that need to be built:
>
> | Component | Usage Count |
> |-----------|-------------|
> | `_Nav item base` | 9× |
>
> Please provide the Figma URLs to where each master component is defined.
> This will give me access to all variants and properties.

### Step 5: Map Properties to Props

Common Figma-to-React mappings:

| Figma Property | React Pattern |
|----------------|---------------|
| `Size=sm/md/lg` | `size="sm"` etc. |
| `State=Disabled` | `isDisabled` |
| `State=Loading` | `isLoading` |
| `Destructive=True` | `color="*-destructive"` |
| `Icon leading=True` | `iconLeading={IconComponent}` |
| Icon instance swap | Extract icon name, convert to PascalCase |

**State handling:** Hover/Focus/Active are CSS-handled, NOT props.

### Step 6: Build the Implementation

1. **Import Untitled UI components** from `@/components/untitled-ui`
2. **Import icons** from `@untitledui/icons` (kebab-case → PascalCase)
3. **Create custom components** in `components/custom/` with proper JSDoc:

```tsx
/**
 * ComponentName - Brief description
 *
 * @figma https://www.figma.com/design/XXX/?node-id=...
 * @figma-captured YYYY-MM-DD
 *
 * Figma Properties → React Props:
 * - PropertyName (variant) → propName: type
 */
```

### Step 7: Present the Result

Show the user:
1. Which Untitled UI components were used
2. Which custom components were created (with file paths)
3. The final implementation code

## Key References

- Design tokens: `/theme.css`
- Components: `components/untitled-ui/` (import from index)
- Custom: `components/custom/`
- Icons: `@untitledui/icons`
