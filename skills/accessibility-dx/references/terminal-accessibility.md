# Terminal and CLI Accessibility

Rules and verification for terminal output: color use, spinners and progress, and screen-reader-safe output. Applies to every CLI, build tool, daemon, and script that prints to stdout or stderr.

## Color never carries meaning alone

1. Pair every colored signal with a text marker: ERROR, WARN, or SUCCESS (or an equivalent severity word) on the same output. A red line that prints only `request 500` is a defect; `ERROR: request 500 failed` is fine.
2. Never use red/green as the only distinction between states. Color-vision deficiency affects roughly 1 in 12 men; add text, shape, position, or pattern as a second channel.
3. Emit color only when the stream is a TTY. Honor NO_COLOR and provide --color/--no-color flags so pipes and CI logs stay plain text.
4. Keep the palette small and verify every pairing against the `color-and-contrast.md` thresholds.
5. Do not encode meaning in style alone (bold, italic, underline). Style is not speech and screen readers ignore it.

## Spinners and progress without animation

1. Every spinner or progress indicator carries a static text label and ends with a complete plain-text summary line, for example `3 of 7 checks passed`.
2. Nothing essential is conveyed by the animation itself. A spinning frame alone is not a message.
3. Do not use blinking or marquee text for meaning.
4. Progress must be pipe-safe: auto-disable when stdout is not a TTY, or provide --no-progress; the final summary is always printed as a normal line.
5. Show progress as text (percent, counts) in addition to any bar or glyph.

## Screen-reader-safe output

1. Announce errors as full lines: severity word first, then what happened, where, and how to recover.
2. Avoid carriage-return frame redraws that screen readers garble. Print the final state as one complete line.
3. Errors go to stderr with the same text content as the colored channel. Color is additive, never the only copy.
4. Anything rendered as a box, table, or chart in a TUI has a plain-text equivalent line or row.

## Verify

- `scripts/check_cli_colors.py` finds no color-only findings in the tool's source
- piping the output shows no escape bytes and loses no meaning
- with NO_COLOR (or --no-color) set, no information is lost
- a screen reader announces the error message and the final progress state
