---
description: Default behavior requirements for DataTable components
---

# DataTable Conventions

When creating any new DataTable component, always include these features by default:

## Required Default Features

### 1. Resizable Columns
Users must be able to resize column widths by dragging column borders. This should work out of the box without requiring additional configuration.

### 2. Sortable Columns
All columns should be sortable by default. Users should be able to click column headers to sort ascending/descending.

## Implementation Notes

- These features should be enabled by default, not opt-in
- If using a library (TanStack Table, AG Grid, etc.), ensure these features are configured in the base setup
- Column resizing and sorting can be disabled per-column if explicitly needed, but the default should be enabled
