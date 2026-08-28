# Console and Portal Accessibility

Rules for developer consoles, portals, admin UIs, dashboards, and devtools panels: keyboard, contrast, motion, and screen-reader announcements.

## Keyboard

1. Every interactive element is reachable and operable by keyboard alone, in a logical focus order.
2. Focus is always visible.
3. No keyboard traps: focus can leave every widget, and dialogs return focus to their trigger.
4. Custom widgets implement their expected key behavior (arrows inside tablists and grids, Escape closing dialogs).
5. Shortcuts are documented and never the only way to reach an action.

## Contrast

1. Text meets the contrast thresholds in `color-and-contrast.md`: 4.5:1 for normal text, 3:1 for large text and UI components.
2. Interactive states (hover, focus, selected, error) are distinguishable by more than color.
3. Verify ratios for the actual shipped themes, including dark mode, not the default theme only.

## Motion

1. Honor prefers-reduced-motion; disable or replace animation when it is set.
2. Nothing essential is conveyed only by animation: status changes are also announced or shown as static text.
3. No auto-playing, blinking, or scrolling content that cannot be paused.

## Screen readers

1. Every control has an accessible name; forms label every input and associate errors with their field.
2. Status changes use live regions with an appropriate politeness level.
3. Landmarks and a single h1 structure the page; tabular data uses real table semantics with headers.
4. Dialogs set focus on open, contain it, and restore focus on close; they are announced with their purpose.

## Verify

- a keyboard-only pass completes every main flow with visible focus at all times
- tab order matches reading order; no widget traps focus
- contrast ratios are computed for every text/background pair in every theme
- a screen reader announces each page title, form field, error, and status change
- prefers-reduced-motion removes animation without losing information
