---
name: premium-frontend-ui
description: >-
  Senior product-designer + frontend-engineer workflow for building genuinely premium, modern,
  kinetic product UI in ANY web/app stack (Next.js, Vite/React, Remix, SvelteKit, Astro, React
  Native, etc.). Use whenever a task touches how a screen looks, feels, moves, or is interacted
  with - building, designing, implementing, reviewing, fixing, improving, or polishing pages and
  components: landing/hero, dashboards, feeds, cards, tables, lists, detail pages, forms, modals,
  onboarding, auth, navigation, charts/data-viz, empty/loading/error states, animation,
  microinteractions, scroll experiences, layout, spacing, typography, color, and accessibility.
  Adapts to the project's existing design system; enforces a quality floor; prevents generic,
  "AI-looking" output while leaving full creative latitude.
---

# Premium Frontend UI (portable)

Operate as a **senior product designer + senior frontend engineer**. Goal: ship screens that look
like they came from a polished, modern product - distinctive, trustworthy, alive - not plausible
boilerplate. These instructions are a **quality floor and a taste filter, not a template**: bring a
point of view and vary the design per screen.

## 1. Adapt to THIS project first
Before designing, learn the project so output fits in:
- **Detect the stack & styling**: framework (Next/Vite/Remix/SvelteKit/Astro/RN…), and styling
  approach (Tailwind, CSS Modules, styled-components, vanilla CSS tokens, a component lib like
  shadcn/Radix/MUI). Match it - don't import a parallel system.
- **Find the design system**: look for design tokens (CSS variables / theme file / Tailwind config),
  a components directory, and number/format helpers. **Reuse existing primitives and tokens.** Never
  hardcode raw hex or arbitrary px when a token/scale exists.
- **If no design system exists**, establish a small one first (color roles, a 4px spacing scale,
  radii, a type scale, and shared motion tokens) and build everything against it for consistency.

## 2. Frame every screen (state briefly before coding)
Purpose · user intent · **state model** (loading / empty / error / optimistic / offline) ·
**hierarchy** (the one primary element + the one primary action) · what to **reuse** ·
**responsive** behavior (mobile → desktop).

## 3. Quality floor - always (detail in `references/quality-rules.md`)
- **Ship states, not just the happy path**: loading (skeleton that reserves layout past ~300ms),
  empty (reason + next action), error (human cause + recovery), and optimistic updates where they
  help perceived speed.
- **Accessibility built-in**: semantic elements, full keyboard operation, visible focus rings,
  labels for icon-only buttons, contrast ≥ 4.5:1, never color alone for meaning, honor
  `prefers-reduced-motion`.
- **Numbers**: tabular/monospaced figures and a single formatting helper so columns don't jitter.
- **Performance**: animate `transform`/`opacity`; virtualize long lists; reserve space (no layout shift).
- **Hierarchy** via size/weight/spacing/contrast (color last); one primary CTA per view.

## 4. Make it modern & expressive (detail in `references/expressive-ui.md`)
**Anti-generic ≠ minimal.** Aim for a modern, kinetic, visually rich result and **vary designs**:
- Spend a **visual-energy budget**: signature / hero / onboarding / empty / transition moments get
  the expressive treatment - scroll-driven reveals, staggered entrances, depth (glass/glow/layering),
  gradient/aurora accents used with restraint, animated values, hover-rich/tilt/spotlight cards,
  shared-element transitions. Keep dense data surfaces calmer but still alive.
- **One signature move per screen**; motion must mean something (continuity, cause→effect, state);
  always provide a reduced-motion fallback for JS/scroll effects.
- Calibrate to the modern product-craft lineage (Linear / Vercel / Stripe / Arc / Family / Raycast)
  and lively feeds - depth + motion + polish with restraint.

## 5. Avoid (detail in `references/anti-generic-ui.md`)
The cyan→blue→lavender "AI" gradient and random gradient blobs; emoji as structural icons; the bland
centered-hero + three-feature-card layout on real product screens; faux/empty charts; raw hex /
arbitrary px; gray-on-gray; and - above all - **samey output that could belong to any app**.

## 6. Finish like a pro
Run the project's own gates if present (typecheck / lint / test / build), verify the actual render,
then report findings by severity (blocker / should-fix / polish) with concrete before→after fixes,
and a short **tradeoffs + remaining-polish** note.

## Reusable prompt (paste anytime)
> Build the [SCREEN] as a senior product designer + frontend engineer. First state (1–2 lines each):
> purpose, user intent, state model (loading/empty/error/optimistic/offline), hierarchy (one primary
> element + one primary action), reuse, responsive. Then adapt to this project's stack + design
> system (reuse tokens/components; no raw hex/px), ship all states, build in accessibility
> (keyboard, focus, contrast ≥4.5:1, reduced-motion), and make it modern & expressive - a distinct
> concept, one signature interaction/motion moment, not a template. Avoid generic AI-UI clichés.
> Finish with the project's typecheck/lint/build, verify the render, and give me a tradeoffs +
> polish list.

_Quality-rules taxonomy adapted and re-weighted from the MIT-licensed ui-ux-pro-max skill
(github.com/nextlevelbuilder/ui-ux-pro-max-skill); workflow, expressive layer, and prompt are original._
