---
name: design-extractor
description: Use when the user wants to inspect an existing application's implemented UI and extract its design language into DESIGN.md, including visual theme, colors, typography, components, layout, depth, responsive rules, evidence, exceptions, and audit notes. Use for creating or updating DESIGN.md and design-audit.md from an existing codebase without redesigning the app.
---

# Design Extractor

Use this skill to extract an existing app's visual design decisions into `DESIGN.md`.
The goal is not to invent a new design system. The goal is to read implemented UI, identify repeated patterns, record evidence, and turn high-confidence observations into reusable design rules.

## Workflow

1. Inspect the app structure and identify styling, theme, component, layout, page, and asset files.
2. Read `references/DESIGN_EXTRACTION.md` for the detailed extraction procedure.
3. Create or update `design-audit.md` first, using `assets/templates/design-audit.md` when the file is missing.
4. Create or update `DESIGN.md`, using `assets/templates/DESIGN.md` when the file is missing.
5. Keep `DESIGN.md` focused on `token` / `rule` / `rationale`.
6. Keep evidence, weak signals, exceptions, and open questions in `design-audit.md`.
7. Before finishing, verify that `DESIGN.md` and `design-audit.md` are consistent.

## File Priority

Read design evidence in this order:

1. Design tokens, theme files, global CSS, CSS variables, Tailwind config, Sass variables, or theme providers.
2. Shared components such as Button, Card, Input, Dialog, Navigation, Table, List, Toast, and Tooltip.
3. Layout shells, navigation, dashboards, detail pages, forms, onboarding, auth, settings, and main flows.
4. Assets such as logos, icons, product images, illustrations, screenshots, Storybook, and design docs.

Prefer values and patterns that appear in visible, frequently used UI. Treat old, unused, experimental, or one-off code as exceptions unless the user confirms otherwise.

## Output Rules

- Do not modify application source files while extracting design unless the user explicitly asks.
- Do not put audit notes, uncertainty, or raw observations into `DESIGN.md`.
- Do not write generic design advice such as "modern", "clean", or "minimal" without concrete implementation evidence.
- Do not list CSS values alone. Explain where each value is used and why it fits the product.
- If evidence is weak, record it in `design-audit.md` instead of asserting it in `DESIGN.md`.

## Validation

Before completing the task, check that:

- `DESIGN.md` follows the 9-section structure from the template.
- `DESIGN.md` contains concrete rules with rationale, not only token lists.
- `design-audit.md` contains file paths, observations, exceptions, weak signals, and open questions.
- Major color, typography, component, layout, depth, and responsive decisions have evidence.
- `DESIGN.md` has no unresolved placeholders.
