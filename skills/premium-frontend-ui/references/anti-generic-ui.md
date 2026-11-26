# Anti-Generic UI - make it look designed, not generated (portable)

The failure mode to avoid: output that screams "an AI made a SaaS template." Stay distinctive and
apply the judgments below. (Anti-generic ≠ minimal - see `expressive-ui.md`.)

## Hard avoids
- The **cyan→blue→lavender "AI" gradient** and default purple/pink hero gradients.
- **Random gradient blobs / mesh** as decorative filler behind content.
- **Emoji as structural icons** - use one consistent SVG icon family.
- **Bland centered hero + three-feature-card grid** on real product screens.
- **Faux/empty charts** or fake sparklines with no data - show a real empty/loading state.
- **Raw hex / arbitrary px** in components; inconsistent spacing, radii, shadows.
- **Placeholder-feeling cards**: same-weight everything, lorem density, no clear primary element.
- **Gray-on-gray** low-contrast text; tiny body text; non-tabular numbers that jitter in columns.
- **Samey output** - the same composition reused on every screen.

## Do instead (the senior-designer moves)
- **Earn hierarchy.** One clear primary element and one primary action per view; use size, weight,
  spacing, contrast - color is the last lever.
- **Make data the hero** where it matters: tabular figures, decisive up/down treatment, a confident
  focal metric. Density that feels considered.
- **Differentiate states.** A real loading skeleton, a helpful empty state with a next action, and an
  honest error with recovery are what separate product UI from a mockup.
- **Microinteractions with intent** (transform/opacity, 150–300ms) and a bolder signature moment per
  screen (see `expressive-ui.md`).
- **Edge-case the layout**: long strings, huge numbers, empty lists, small windows - design those.
- **Trust cues**: clear sourcing/timestamps, honest framing, precise formatting.

## The "is this generic?" gut check (before finishing)
1. Could this belong to any random SaaS, or is it unmistakably *this* product?
2. One clear focal point and one primary action - or is everything the same weight?
3. Are loading / empty / error states designed, or only the happy path?
4. Do numbers line up (tabular) via a shared formatter?
5. Is every color/spacing/radius a token? Any raw hex or stray px?
6. Does motion mean something, and does it respect reduced-motion?
7. Keyboard-only: can I reach and operate everything, with visible focus?
8. Does it feel modern and alive - or quiet and templated?

If any answer is weak, it isn't done.
