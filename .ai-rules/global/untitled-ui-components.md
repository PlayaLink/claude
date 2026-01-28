---
description: Untitled UI design system usage, Figma workflow, and component patterns
---

# Untitled UI + Figma Workflow

This project uses the Untitled UI design system with Figma integration via MCP.

## Quick Reference

- **Design tokens**: `/theme.css`
- **Components**: `components/untitled-ui/` (pre-installed, import from index)
- **Custom components**: `components/custom/` (app-specific, yours to edit)
- **Icons**: `@untitledui/icons`
- **Import pattern**: `import { Button, Input, Select } from '@/components/untitled-ui'`

---

# Part 1: Figma URL Workflow

When the user provides a Figma URL:

## Step 1: Fetch Figma Data

Use the MCP tool `get_figma_data` with:
- **fileKey**: Extract from URL (e.g., `figma.com/design/{fileKey}/...`)
- **nodeId**: Extract from URL param `node-id` (convert `1176-99947` → `1176:99947`)

## Step 2: Identify Components

Parse the Figma data and categorize all `type: INSTANCE` nodes:

| Category | How to Identify | Action |
|----------|-----------------|--------|
| Available in CLI | Matches known component (Button, Badge, etc.) | Import from `@/components/untitled-ui` |
| Internal Figma (`_` prefix) | Name starts with `_` (e.g., `_Nav item base`) | Must build in `components/custom/` |
| Custom/app-specific | No CLI equivalent exists | Must build in `components/custom/` |

## Step 3: Request Master Component URLs

For components that need to be built, **ask the user for master component URLs**:

> I found these components that need to be built:
>
> | Component | Usage Count |
> |-----------|-------------|
> | `_Nav item base` | 9× |
> | `_Nav account card` | 1× |
> | `Company logo` | 1× |
>
> Please provide the Figma URLs to where each master component is defined.
> Format: `https://www.figma.com/design/{fileKey}/?node-id={componentSetId}`
>
> This will give me access to all variants and properties for complete implementations.

**Why master URLs?** Instance data only shows the *used* configuration. Master components show ALL variants, boolean toggles, and instance swap slots.

## Step 4: Fetch Master Component Data

Use `get_figma_data` with each user-provided URL to retrieve:
- All variant combinations (e.g., `Current=True/False`, `State=Default/Hover/Active`)
- All boolean properties (show/hide toggles like `Icon leading`, `Badge`, `Dot`)
- All instance swap slots (e.g., `Icon swap` for custom icons)
- Default values for each property

## Step 5: Build Components

Create components in `components/custom/` with:
- Props derived from Figma variants/properties
- `@figma` annotation linking to master component URL (user-provided)
- `@figma-captured` timestamp (for detecting stale links if Figma reorganizes)
- Complete TypeScript interface matching all Figma options

### Component JSDoc Format

```tsx
/**
 * NavItem - Navigation item wrapper
 *
 * @figma https://www.figma.com/design/XXX/?node-id=2:9020
 * @figma-captured 2025-12-26
 * Master component: _Nav item base
 *
 * Figma Properties → React Props:
 * - Current (variant) → isCurrent: boolean
 * - State (variant) → CSS handles (hover/focus)
 * - Icon leading (boolean) → iconLeading?: FC
 * - Icon swap (instance) → iconLeading value
 * - Icon trailing (boolean) → iconTrailing?: FC
 * - Badge (boolean) → badge?: ReactNode
 * - Dot (boolean) → dot?: boolean
 */
```

## Step 6: Use Components

1. Import available components from `@/components/untitled-ui`
2. Import custom components from `@/components/custom`
3. Follow design tokens from `/theme.css`

**All base and application components are pre-installed.** Just import and use them.

---

# Part 2: Design Tokens

All tokens are defined in `/theme.css` using Tailwind CSS v4 `@theme` syntax.

## Colors

**Base scales** (25-950): `gray`, `brand`, `error`, `warning`, `success`, `blue`, `indigo`, `purple`, `pink`, `rose`, `orange`, `teal`, `cyan`

```tsx
<div className="bg-gray-50 text-gray-900 border-gray-200">
<button className="bg-brand-600 hover:bg-brand-700 text-white">
<span className="text-error-500">Error</span>
```

## Border Radius

| Token | Tailwind |
|-------|----------|
| `--radius-xs` | `rounded-xs` |
| `--radius-sm` | `rounded-sm` |
| `--radius-md` | `rounded-md` |
| `--radius-lg` | `rounded-lg` |
| `--radius-xl` | `rounded-xl` |
| `--radius-2xl` | `rounded-2xl` |
| `--radius-full` | `rounded-full` |

## Shadows

| Token | Tailwind |
|-------|----------|
| `--shadow-xs` | `shadow-xs` |
| `--shadow-sm` | `shadow-sm` |
| `--shadow-md` | `shadow-md` |
| `--shadow-lg` | `shadow-lg` |
| `--shadow-xl` | `shadow-xl` |

---

# Part 3: Available Components

## Pre-installed Components

All these components are ready to import from `@/components/untitled-ui`:

### Base Components
- `Button`, `ButtonGroup`, `ButtonGroupItem`
- `Checkbox`, `CheckboxBase`
- `Dropdown` (compound: `Dropdown.Root`, `.Menu`, `.Item`, etc.)
- `FeaturedIcon`
- `Input`, `InputBase`, `TextField`, `Label`, `HintText`
- `RadioGroup.*` variants
- `Select`, `ComboBox`, `MultiSelect`, `SelectItem`
- `Slider`
- `TagGroup`, `TagList`, `Tag`
- `TextArea`, `TextAreaBase`
- `Toggle`, `ToggleBase`
- `Tooltip`, `TooltipTrigger`

### Application Components
- `Breadcrumbs`, `BreadcrumbItem`
- `DatePicker`, `DateRangePicker`, `Calendar`, `RangeCalendar`
- `EmptyState`
- `Tabs`, `TabList`, `TabPanel`, `Tab`

### Shared Assets
- `BackgroundPattern`
- `Illustration`

## Custom Components (Build with Tailwind)

These patterns are NOT in the library - compose from primitives or build with Tailwind:
- Sidebar navigation
- Page headers / Nav items
- Cards (account, pricing, custom)
- Tables (use HTML + Tailwind)
- Modals (use React Aria directly)

---

# Part 4: Icons

Import from `@untitledui/icons`:

```tsx
import { ArrowRight, Check, X, Plus, Search } from '@untitledui/icons';

// Pass as component (recommended)
<Button iconTrailing={ArrowRight}>Continue</Button>

// Or as element
<Button iconLeading={<Check data-icon />}>Confirm</Button>
```

**Figma name → Import**: kebab-case to PascalCase
- `arrow-right` → `ArrowRight`
- `check-circle` → `CheckCircle`
- `user-plus-01` → `UserPlus01`

---

# Part 5: State Handling

**Figma states are NOT React props** (except disabled/loading):

| Figma State | React |
|-------------|-------|
| `State=Default` | Normal render |
| `State=Hover` | CSS handles automatically |
| `State=Focus` | CSS handles automatically |
| `State=Disabled` | `isDisabled={true}` |
| `State=Loading` | `isLoading={true}` |
| `Destructive=True` | `color="primary-destructive"` |

---

# Part 6: Component Organization

## Directory Structure

```
components/
├── custom/               # CUSTOM - app-specific components
│   ├── empty-states/     # Empty state components
│   ├── labels/           # Label-related components
│   └── *.tsx             # Your composed/custom components
│
└── untitled-ui/          # PURE - CLI-installed, never manually edit
    ├── base/             # Primitive components (matches Figma Base file)
    ├── application/      # App UI components (matches Figma Application file)
    ├── shared-assets/    # Patterns, illustrations (matches Figma Shared Assets file)
    ├── foundations/      # Design foundations (FeaturedIcon)
    └── index.ts          # Re-exports all components
```

## Rules

| Scenario | Directory | Approach |
|----------|-----------|----------|
| Using component as-is | `untitled-ui/` | Import directly, never modify |
| Composing components | `custom/` | Create new component that imports from `untitled-ui/` |
| Modifying a component | `custom/` | Copy from `untitled-ui/`, rename, add `@forked-from` |
| Building from scratch | `custom/` | Build with Tailwind, may use `untitled-ui/` primitives |

## Documentation Links

After installing an Untitled UI component via the CLI, add a `@docs` annotation to the main component file linking to the official documentation:

```tsx
/**
 * Button component
 * @docs https://www.untitledui.com/components/button
 */
```

**URL Pattern**: `https://www.untitledui.com/components/[component-name]`

---

# Part 7: Untitled UI Architecture & Forking

## How Untitled UI Works

Untitled UI uses a **copy-to-codebase model** (like shadcn/ui):

```bash
npx untitledui@latest add [component-name]  # Copies source to components/untitled-ui/
```

**From NPM packages:**
- `@untitledui/icons` - Icon components only
- `@untitledui/file-icons` - File type icons only

**Everything else is copied source code** - not imported from a package.

## When to Fork vs Use Directly

| Scenario | Approach | Example |
|----------|----------|---------|
| Need subset of variants/props | Use directly | Button with only `color="primary"` |
| Component has hardcoded demo data | Fork | NavAccountCard with placeholder accounts |
| Need fundamentally different behavior | Fork | Account display vs account switching |
| Want to simplify complex component | Fork | Remove unused features/variants |

## Forking Workflow

When the user's Figma design uses a simplified version of an Untitled UI component:

### Step 1: Copy to Custom
```bash
cp components/untitled-ui/.../component.tsx components/custom/component.tsx
```

### Step 2: Strip Unneeded Functionality
Remove:
- Unused variants and their styles
- Hardcoded demo/placeholder data
- Features not needed (e.g., account switching, keyboard nav)
- Unused imports and dependencies

### Step 3: Add Documentation
```tsx
/**
 * NavAccountCard - Simplified user account display
 *
 * @figma https://www.figma.com/design/CUSTOM_FILE/?node-id=...
 * @forked-from components/untitled-ui/application/app-navigation/base-components/nav-account-card.tsx
 * @figma-captured 2025-01-05
 *
 * Simplified from Untitled UI version:
 * - Removed: Account switching, popover menu, keyboard navigation
 * - Kept: Avatar, name, email display, logout button
 */
```
