# UI Quality Rules (portable)

Adapted from the MIT-licensed **ui-ux-pro-max** skill. A quality floor for any web/app stack.
Work top-down - category 1 outranks category 8. Apply with judgment; adapt thresholds to the platform
(pointer/keyboard for desktop-web, touch for mobile).

## 1. Accessibility - CRITICAL
Contrast ≥ 4.5:1 body / 3:1 large text & UI glyphs · visible focus ring on every interactive element
· full keyboard operation (tab order = visual order; Enter/Space activate; Esc closes; focus moves
into a dialog and returns to its trigger) · `aria-label` on icon-only buttons · `label`/`for` on
inputs · sequential headings, one h1 · never color alone for meaning · honor `prefers-reduced-motion`.

## 2. Interaction & feedback - CRITICAL
Clickable = `cursor:pointer` + a real hover state · distinct hover/active/focus/disabled for every
control · disabled = reduced opacity + disabled attribute + no action · async = disable trigger, show
progress, then success/error · confirm destructive actions, separate them from primary, offer undo.

## 3. Performance & perceived speed - HIGH
Skeleton/shimmer that reserves final layout for waits > ~300ms · reserve space for async content &
media (no layout shift) · virtualize lists > ~50 rows · debounce/throttle scroll/resize/input ·
code-split heavy/rare routes · animate transform/opacity only.

## 4. Style & consistency - HIGH
Match one style system across the app · one icon family (SVG, no emoji as structural icons) ·
consistent elevation/shadow + radius scales (no random values) · one primary CTA per view ·
design light/dark together where themed.

## 5. Layout & responsive - HIGH
Mobile-first breakpoints, then scale up; on desktop apps, ensure panes survive a resized-small window
(no overflow/horizontal scroll, no fixed px that overflow) · 4px/8px spacing rhythm · hierarchy via
size/spacing/contrast · prose line length ~60–75 chars · fixed bars reserve padding for content.

## 6. Typography & color - MEDIUM
A clear type scale; weight for hierarchy (headings 600–700, body 400, labels 500); body line-height
~1.5 · semantic color tokens, not raw hex in components · tabular/monospaced figures for numbers,
prices, timers · verify any new color pair for contrast; no gray-on-gray.

## 7. Animation & microinteraction - MEDIUM
150–300ms micro (≤400ms larger) · ease-out enter / ease-in exit, exits ~60–70% of enter · stagger
list items 30–50ms · motion expresses cause→effect, never decorative-only · 1–2 animated elements per
view · modals animate from their source · keep motion interruptible; never block input.

## 8. Forms & feedback - MEDIUM
Visible labels (not placeholder-only) · validate on blur, error beside the field, auto-focus first
invalid on submit · submit → loading → success/error with a clear recovery path · semantic input
types · `aria-live`/`role="alert"` for errors; toasts auto-dismiss 3–5s and don't steal focus ·
empty states carry a reason + a next action.

## 9. Navigation - HIGH
Current location is visibly active · placement consistent across pages · predictable back; preserve
scroll/filter state · modals for focused tasks, not primary nav; every modal has a visible close +
Esc · keep routes deep-linkable/shareable.

## 10. Charts & data - for data-dense surfaces
Match chart to data (trend→line/sparkline, comparison→bar, proportion→limited donut) · tooltips with
exact values on hover AND keyboard · legends visible, axes labeled · never color alone (labels/
patterns; data vs background ≥ 3:1) · charts need their own loading/empty/error states · tables
sortable with `aria-sort`, tabular figures, sticky header when long · locale-aware number formatting.
