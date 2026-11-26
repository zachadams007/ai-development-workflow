# Expressive Range & Creative Freedom (portable)

The quality rules are a **floor and a cliché filter - not a template.** Within them, aim for a
**modern, kinetic, visually rich, interactive** result, and **vary the design per screen.** Sameness
across screens is the failure mode; a distinct concept each time is the goal.

## Principles
- **Anti-generic ≠ minimal.** Depth, motion, and richness are encouraged when deliberate.
- **Bring a point of view** per screen: a composition, a signature interaction, a focal visual idea.
- **Spend a visual-energy budget.** You can't make everything loud - decide where it goes:
  - **Signature / hero / onboarding / empty / transition moments → expressive.**
  - **Dense data surfaces (feeds, tables, dashboards) → clarity-first, but still alive** (hover
    richness, subtle reveals, animated values). Calm ≠ dead.

## Modern interactive toolbox (use 1–2 per screen)
- **Scroll-driven**: reveal-on-enter, scroll progress, pinned/sticky sections, scroll-snap,
  sticky-stacking cards, subtle section parallax, count-ups as elements enter view.
- **Entrance choreography**: staggered list/grid items (30–50ms apart), directional slides that imply
  hierarchy, shared-element / hero transitions between routes.
- **Depth & material**: layered glass, soft glow, an elevation scale, gradient/aurora accents used
  sparingly against a considered base.
- **Alive data**: animated sparklines/charts, ticking values (tabular figures), smooth enter/exit on
  filter changes, optimistic micro-feedback.
- **Pointer richness**: card lift/tilt/spotlight on hover, cursor-aware highlights, magnetic buttons -
  where they add delight without harming clarity.

## Keep "rich" from becoming "noisy"
One signature move per screen; everything else supports it · motion must mean something (continuity,
cause→effect, state) · performance: transform/opacity, compositor-driven scroll, virtualized lists ·
**always** branch on `prefers-reduced-motion` and degrade JS/scroll effects to instant/static ·
keep a consistent motion language (shared easing + duration) so the app feels choreographed.

## Calibration (target aesthetic)
The modern product-craft and kinetic-site lineage - **Linear / Vercel / Stripe / Arc / Family /
Raycast** - plus lively, polished feeds. Depth, motion, and polish with restraint. When in doubt,
make the **signature** moment bolder and the **dense data** calmer.
