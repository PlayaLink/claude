---
description: Flag potential component duplication to keep design system lightweight
---

# Component Variation Awareness

Keep the design system lightweight and consistent. Flag potential duplication proactively.

## When to Flag

Notify the user when a Figma design appears to introduce unnecessary variation:

- A component that's very close to an existing CLI component but with minor styling tweaks
- A component that duplicates functionality already in `components/app/`
- Multiple similar components in the same design that could be consolidated

## How to Flag

Don't block the workflow. Just include a brief note when relevant:

> **Heads up:** `_Custom Card` looks similar to the existing `ActionCard` in `components/app/`. The main difference is [X]. Want me to extend the existing component instead, or proceed with a new one?

Or:

> **Note:** This design uses 3 slightly different button styles. The CLI `Button` with different `color` props could handle all of these. Worth simplifying?

## Goal

- Consistency over novelty
- Fewer components to maintain
- Catch accidental variation before it ships

## Don't Flag

- Genuinely unique components with no existing equivalent
- Components where the user has already indicated they want something custom
- Minor prop differences that existing components already support
