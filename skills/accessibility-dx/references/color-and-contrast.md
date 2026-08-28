# Color and Contrast

Canonical color pairing rules and contrast measurement for every developer surface: terminal, console, docs, and charts.

## Color pairings

1. Never encode meaning by color alone. Every colored state has a redundant channel: text, shape, position, or pattern.
2. Red/green pairs are the worst case and are avoided for state distinction; roughly 1 in 12 men has some form of color-vision deficiency.
3. Blue/yellow and low-chroma pairs are checked the same way; only a redundant channel makes a pairing safe.
4. Default terminal palettes vary; never assume the reader sees the colors the author sees.
5. State markers: red lines carry a severity word, success markers carry SUCCESS/DONE, warnings carry WARN.

## Contrast thresholds

- normal text: 4.5:1
- large text (18pt/24px or 14pt bold): 3:1
- UI components and graphical objects: 3:1
- focus indicators: 3:1 against adjacent colors

Apply the thresholds to light and dark themes, and to every state (hover, focus, selected, error).

## Measuring contrast

Compute, never eyeball:

1. Convert each channel to linear RGB: `c = c / 12.92` when `c <= 0.03928`, else `((c + 0.055) / 1.055) ** 2.4`.
2. Relative luminance `L = 0.2126 R + 0.7152 G + 0.0722 B`.
3. Contrast ratio `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter luminance.

## Procedure

1. Enumerate every text/background pair in the surfaces under audit.
2. Compute each ratio; record the worst case per pair.
3. Flag any pair under its threshold as a contrast defect with the computed ratio as evidence.
4. Simulate color-vision deficiency on the palette: no state distinction may depend on a red/green pair alone.
5. Check grayscale rendering: nothing essential may disappear.

## Verify

- every pair meets its threshold in every shipped theme
- no finding relies on a color pair for meaning
- computed ratios, not impressions, are attached to findings
