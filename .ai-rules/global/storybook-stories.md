---
description: Storybook story structure and guidelines
alwaysApply: true
---

# Storybook Stories Guidelines

When creating stories for components:

## Required Storybook Pages

Every component must have exactly **3 pages** in the Storybook sidebar:

| Page | Story Name | Purpose |
|------|------------|---------|
| **Overview** | `Overview` | Shows all variants grouped by property - this is the default documentation page |
| **Props** | `Props` | Single interactive instance with all controls visible (`tags: ['show-panel']`) |
| **Source Code + Design** | `SourceCodeAndDesign` (`name: 'Source Code + Design'`) | Links to GitHub source and Figma design |

**Do NOT use autodocs** - the Overview story serves as the documentation page.

## 1. ArgTypes Organization

Organize props to match Figma's properties panel order. The Untitled UI Figma uses these variant properties:

- **Size**: sm, md, lg, xl (component sizes)
- **Hierarchy**: Primary, Secondary, Tertiary, Link color, Link gray (visual prominence)
- **State**: Default, Disabled, Focused, Hover, Loading (interactive states)
- **Icon only / Icon**: Controls icon placement (False, Leading, Only)
- **🔀 Icon swap**: Instance swap properties for icon customization

Map these to React props using meaningful categories:

```typescript
argTypes: {
  // Appearance props first - maps to Figma's Size and Hierarchy
  size: {
    control: 'select',
    options: ['sm', 'md', 'lg', 'xl', '2xl'],
    description: 'Component size',
    table: { category: 'Appearance' },
  },
  color: {
    name: 'color (Hierarchy)',  // Maps to Figma "Hierarchy" variant
    control: 'select',
    options: ['primary', 'secondary', 'tertiary', 'link-color', 'link-gray'],
    description: 'Visual hierarchy/color variant',
    table: { category: 'Appearance' },
  },

  // State props - maps to Figma's "State" variant
  isDisabled: {
    name: 'isDisabled (State)',  // Maps to Figma State=Disabled
    control: 'boolean',
    table: { category: 'State' },
  },
  isLoading: {
    name: 'isLoading (State)',  // Maps to Figma State=Loading
    control: 'boolean',
    table: { category: 'State' },
  },

  // Icon props - maps to Figma's Icon/Icon only variants and instance swaps
  iconLeading: {
    control: false,  // Icon components can't be controlled via knobs
    description: 'Icon before label (Figma: Icon=Leading)',
    table: { category: 'Icons' },
  },
  iconTrailing: {
    control: false,
    description: 'Icon after label',
    table: { category: 'Icons' },
  },

  // Content props
  children: {
    name: 'children (Label)',
    control: 'text',
    description: 'Component text content',
    table: { category: 'Content' },
  },

  // Behavior props
  href: {
    control: 'text',
    table: { category: 'Behavior' },
  },

  // Advanced/technical props last
  className: {
    control: false,
    table: { category: 'Advanced' },
  },
}
```

## 2. Standard Categories

Use these categories consistently across all components. The categories bridge Figma variant terminology to React props:

| Category | React Props | Figma Equivalents |
|----------|-------------|-------------------|
| Appearance | size, color, variant | Size, Hierarchy, Type |
| State | isDisabled, isLoading, isSelected, isCurrent | State=Disabled/Loading, Current=True |
| Icons | iconLeading, iconTrailing, icon | Icon=Leading/Trailing/Only, 🔀 Icon swap |
| Content | children, label, title, description | Text layers, Label |
| Behavior | href, onChange, onPress | Link behavior |
| Advanced | className, style | (implementation only) |

### Figma-to-React Mapping Examples

Common Untitled UI Figma variants and their React prop equivalents:

| Figma Variant | React Prop | Values |
|---------------|------------|--------|
| Size | `size` | sm, md, lg, xl, 2xl |
| Hierarchy | `color` | primary, secondary, tertiary, link-color, link-gray |
| State | `isDisabled`, `isLoading` | Boolean props (Default state = both false) |
| Icon only | Render with icon prop but no `children` | Implicit based on content |
| Icon | `iconLeading`, `iconTrailing` | False=none, Leading=iconLeading, Only=icon-only mode |
| Current | `isCurrent` or `isSelected` | Boolean for selected/active state |
| 🔀 Icon swap | Pass component to icon props | Icon components |

## 3. Required Stories

See **Required Storybook Pages** section above. Every component must export exactly 3 stories:
`Overview`, `Props`, and `SourceCodeAndDesign`.

## 4. Story File Structure

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Component } from './component'

const meta: Meta<typeof Component> = {
  title: 'Components/ComponentName',
  component: Component,
  parameters: { layout: 'centered' },
  argTypes: {
    // Organized by category (see above)
  },
  args: {
    // Default args
  },
}

export default meta
type Story = StoryObj<typeof Component>

// =============================================================================
// OVERVIEW (default - all variants by property)
// =============================================================================

export const Overview: Story = {
  render: () => (
    <div className="flex flex-col gap-8 px-12 pb-12 pt-8">
      {/* Group variants by property type: Hierarchy, Size, State, Icons, etc. */}
    </div>
  ),
}

// =============================================================================
// PROPS (with controls)
// =============================================================================

export const Props: Story = {
  tags: ['show-panel'],
  args: {
    // Interactive defaults
  },
}

// =============================================================================
// SOURCE CODE + DESIGN
// =============================================================================

export const SourceCodeAndDesign: Story = {
  name: 'Source Code + Design',
  render: () => (
    <div className="flex flex-col items-center gap-8 py-12">
      {/* GitHub and Figma links */}
    </div>
  ),
}
```
