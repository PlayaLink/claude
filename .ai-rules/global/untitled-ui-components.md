---
description: Creating new components in untitled-ds from Figma designs
---

# Creating Components in untitled-ds

This guide covers the workflow for adding new components to the `untitled-ds` design system package.

---

## Step 1: Pull from Untitled UI CLI

Start by importing the component from the Untitled UI CLI:

```bash
cd untitled-ds
npx untitledui@latest add <component-name> --path src/components --overwrite
```

This gives you a working React Aria implementation as a starting point.

---

## Step 2: Fetch Figma Data for Parity Check

Use the MCP tool `get_figma_data` to fetch the master component from Figma:

- **fileKey**: Extract from URL (e.g., `figma.com/design/{fileKey}/...`)
- **nodeId**: Extract from URL param `node-id` (convert `1176-99947` → `1176:99947`)

Request the **master component URL** (not an instance) to see ALL variants and properties.

---

## Step 3: Verify Prop/Variant Parity

Compare the Figma component properties with the React implementation. Ensure 1:1 parity:

### Figma Properties → React Props

| Figma Property Type | React Equivalent |
|---------------------|------------------|
| Variant (e.g., `Size=sm/md/lg`) | `size?: 'sm' \| 'md' \| 'lg'` |
| Boolean (e.g., `Icon leading=true/false`) | `iconLeading?: FC<{ className?: string }>` |
| Instance swap (e.g., `Icon swap`) | Value for the boolean prop above |
| Text (e.g., `Label`) | `children: ReactNode` |

### Common Gaps to Check

1. **Missing variants** - Figma has sizes/colors the React code doesn't support
2. **Missing boolean toggles** - Figma has show/hide options not exposed as props
3. **Hardcoded values** - React code has hardcoded strings that should be props
4. **Extra functionality** - React code has features not in Figma (remove or flag)

### Documenting Parity

Add a JSDoc comment mapping Figma properties to React props:

```tsx
/**
 * Badge component
 * @docs https://www.untitledui.com/react/components/badges
 * @figma https://www.figma.com/design/XXX/?node-id=19483-6597
 *
 * Figma Properties → React Props:
 * - Size (variant) → size: 'sm' | 'md' | 'lg'
 * - Type (variant) → type: 'pill-color' | 'badge-color' | 'badge-modern'
 * - Color (variant) → color: BadgeColor
 * - Icon leading (boolean) → iconLeading?: FC
 * - Icon trailing (boolean) → iconTrailing?: FC
 * - Dot (boolean) → dot?: boolean
 * - Avatar (boolean) → image?: string
 * - Button (boolean) → button?: BadgeButtonProps
 */
```

---

## Step 4: Replace @untitledui/icons with Icon Component

Untitled UI CLI imports use `@untitledui/icons`. Replace these with our `Icon` component architecture.

### In Component Files

Replace direct icon imports with `createIcon`:

```tsx
// ❌ Before (Untitled UI pattern)
import { ChevronDown, Check, X } from '@untitledui/icons'

<Button iconTrailing={ChevronDown}>Options</Button>

// ✅ After (untitled-ds pattern)
import { createIcon } from '../icon'

const ChevronDownIcon = createIcon('chevron-down', 'sm')
const CheckIcon = createIcon('check', 'sm')

<Button iconTrailing={ChevronDownIcon}>Options</Button>
```

### In Storybook Stories

Always use `createIcon` for demo icons:

```tsx
import { createIcon } from '../icon'

// Icons for demos
const ArrowRightIcon = createIcon('arrow-right', 'sm')
const ChevronDownIcon = createIcon('chevron-down', 'sm')
const CheckIcon = createIcon('check', 'sm')
```

### Adding New Icons to the Registry

If an icon doesn't exist in `Icon.tsx`, add it to the `iconMap`:

```tsx
// src/components/icon/Icon.tsx
import { faNewIcon } from '@fortawesome/free-solid-svg-icons'

const iconMap = {
  // ... existing icons
  'new-icon': faNewIcon,
} as const
```

### Icon Size Reference

| Size | Tailwind | Pixels | Use Case |
|------|----------|--------|----------|
| `2xs` | `size-2` | 8px | Tiny dots |
| `xs` | `size-2.5` | 10px | Small indicators |
| `sm` | `size-3` | 12px | Badge icons, small buttons |
| `md` | `size-4` | 16px | Default |
| `lg` | `size-5` | 20px | Standard UI icons |
| `xl` | `size-6` | 24px | Large icons (Figma default) |
| `2xl` | `size-8` | 32px | Max size |

---

## Step 5: Apply Semantic Color Tokens

Replace primitive grayscale colors with semantic tokens for dark mode support:

| Replace | With |
|---------|------|
| `text-gray-900` | `text-primary` |
| `text-gray-700`, `text-gray-800` | `text-secondary` |
| `text-gray-500`, `text-gray-600` | `text-tertiary` |
| `bg-base-white` | `bg-primary` |
| `bg-gray-50` | `bg-secondary` |
| `border-gray-300` | `border-primary` |
| `border-gray-200` | `border-secondary` |

**Keep primitives** for intentionally colored elements (brand colors, status indicators).

---

## Step 6: Organize Styles with sortCx

Structure styles for IntelliSense support:

```tsx
import { cx, sortCx } from '@/utils/cx'

export const styles = sortCx({
  base: 'inline-flex items-center font-medium',
  size: {
    sm: { base: 'px-2 py-0.5 text-xs', withIcon: 'pl-1.5 pr-2 gap-1' },
    md: { base: 'px-2.5 py-0.5 text-sm', withIcon: 'pl-2 pr-2.5 gap-1' },
  },
  color: {
    gray: { root: 'bg-secondary text-secondary', icon: 'text-tertiary' },
    brand: { root: 'bg-brand-50 text-brand-700', icon: 'text-brand-500' },
  },
})
```

---

## Step 7: Create Storybook Stories

Create `<component>.stories.tsx` with exactly **3 stories**:

| Story | Purpose |
|-------|---------|
| `Overview` | Visual showcase of ALL variants by property |
| `Props` | Interactive playground with `tags: ['show-panel']` |
| `SourceCodeAndDesign` | Links to GitHub and Figma |

```tsx
export const Overview: Story = {
  render: () => (
    <div className="flex flex-col gap-8">
      {/* Group by variant property */}
      <Section title="Size">
        {sizes.map(size => <Component size={size} />)}
      </Section>
      <Section title="Color">
        {colors.map(color => <Component color={color} />)}
      </Section>
    </div>
  ),
}

export const Props: Story = {
  tags: ['show-panel'],
  args: { /* default props */ },
}

export const SourceCodeAndDesign: Story = {
  name: 'Source Code + Design',
  render: () => (
    <div className="flex gap-4">
      <Button href="https://github.com/..." iconLeading={GitHubIcon}>
        View on GitHub
      </Button>
      <Button href="https://figma.com/..." iconLeading={FigmaIcon}>
        View in Figma
      </Button>
    </div>
  ),
}
```

---

## Step 8: Export from Index Files

```tsx
// src/components/<name>/index.ts
export { Component, type ComponentProps, styles } from './component'

// src/index.ts
export { Component, type ComponentProps, styles as componentStyles } from './components/<name>'
```

---

## Component Enhancement Philosophy

**Enhance atomic components with optional props rather than creating variant components.**

### ❌ Don't: Create Many Variant Components

```tsx
// Avoid this pattern
export const Badge = ...
export const BadgeWithDot = ...
export const BadgeWithIcon = ...
export const BadgeWithImage = ...
export const BadgeWithButton = ...
```

### ✅ Do: Add Optional Props to Base Component

```tsx
// Single component with optional features
interface BadgeProps {
  children?: ReactNode
  size?: BadgeSize
  color?: BadgeColor
  iconLeading?: FC<{ className?: string }>
  iconTrailing?: FC<{ className?: string }>  // optional
  dot?: boolean                               // optional
  image?: string                              // optional
  button?: BadgeButtonProps                   // optional
}
```

This keeps the design system DRY and maintainable.

---

## File Structure

```
src/components/<name>/
├── <name>.tsx           # Component with JSDoc header
├── <name>.stories.tsx   # Storybook (3 stories)
└── index.ts             # Barrel exports
```

---

## Checklist

- [ ] Pulled component from Untitled UI CLI
- [ ] Fetched Figma master component data
- [ ] Verified prop/variant parity (documented in JSDoc)
- [ ] Replaced `@untitledui/icons` with `createIcon`
- [ ] Applied semantic color tokens
- [ ] Organized styles with `sortCx`
- [ ] Created 3 Storybook stories
- [ ] Exported from index files
- [ ] Built library: `npm run build:lib`
- [ ] Tested in Storybook: `npm run dev`
