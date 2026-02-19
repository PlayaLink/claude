---
description: Semantic markup and DOM reference requirements for easy debugging and code searchability
---

# Semantic Markup Requirements

## Core Principle
**Always include semantic markup** to help with readability and debugging, especially for DOM inspection and code reference.

## Required Attributes

### data-referenceid
- **MUST be included** on all interactive and structural elements
- **MUST be a static string value** - **NEVER use variables**
- **MUST be short and hyphenated** (e.g., `"action-button"`, `"delete-image"`)
- Purpose: Copyable identifier that can be copied from the DOM and then found in the code using global search in IDE

### Requirements
- Use static strings: `data-referenceid="prototype-detail-header"`
- Never use variables: ~~`data-referenceid={buttonId}`~~
- Short and descriptive: `data-referenceid="drag-handle"`
- Hyphenated format: `data-referenceid="save-prototype-description"`
- Avoid dynamic values: ~~`data-referenceid={`button-${id}`}`~~

## When to Use

### Interactive Elements
- Buttons
- Links
- Form inputs
- Clickable components
- Interactive controls

### Structural Elements
- Sections (`<section>`)
- Headers (`<header>`)
- Navigation (`<nav>`)
- Main content (`<main>`)
- Aside panels (`<aside>`)
- Footer (`<footer>`)

## Semantic HTML Elements
Prefer semantic HTML elements over generic `<div>` elements:
- Use `<button>` for clickable actions
- Use `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `<section>` for page structure
- Use `<form>`, `<fieldset>`, `<legend>` for form structure
- Use semantic elements to improve accessibility and code readability

## Examples

### Correct Usage
```tsx
<button
  onClick={handleSave}
  data-referenceid="save-prototype-description"
  aria-label="Save prototype description"
>
  Save Description
</button>

<section
  data-referenceid="prototype-screenshots"
  aria-label="Prototype screenshots"
>
  <h3>Screenshots</h3>
  {/* Content */}
</section>

<div
  data-referenceid="prototype-image-wrapper"
  className="relative group"
>
  <img src={photo.publicUrl} alt="Prototype image" />
</div>
```

### Incorrect Usage
```tsx
// Using variables
<button
  data-referenceid={buttonId}  // NEVER use variables
>
  Save
</button>

// Using dynamic values
<div
  data-referenceid={`image-${photo.id}`}  // NEVER use dynamic values
>
  Content
</div>

// Too long or not hyphenated
<div
  data-referenceid="prototypeDetailViewScreenshotSectionPrimaryImageContainer"  // Too long
>
  Content
</div>
```

## Workflow
1. **When creating new components**: Always add `data-referenceid` to interactive and structural elements
2. **When adding new functionality**: Include `data-referenceid` on new UI elements
3. **Format**: Use short, hyphenated, descriptive names that are easy to copy from DOM and search in code

## Rationale
- **Easy DOM inspection**: Copy `data-referenceid` from browser DevTools
- **Fast code search**: Use global search in IDE to find the element in code
- **No test coupling**: Unlike `data-testid`, this is purely for developer reference
- **Static values**: Ensures reliable searching without variable resolution issues
