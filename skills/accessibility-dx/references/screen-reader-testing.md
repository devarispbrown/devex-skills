# Screen-Reader Testing for Developer Tools

Procedure for testing terminal output and web consoles with a screen reader, plus the evidence rules that make results usable.

## Tooling

- macOS: VoiceOver (Terminal, Safari, Chrome)
- Windows: NVDA (Firefox or Chrome)
- Linux: Orca (Firefox or Chromium)

Use the platform's default reader for the report unless a reader is named with its version.

## Terminal output

1. Run the command in the reader's host terminal with the reader on.
2. Confirm the error message is announced as text: severity word, cause, recovery.
3. Confirm color adds nothing that text does not: a red-only signal is a defect.
4. Confirm spinners and progress produce announcements and that the final summary line is read.
5. Confirm carriage-return redraws do not garble the final output.

## Console and portal

1. Keyboard-only walkthrough: tab through every control, activate every action, complete the main flows with visible focus.
2. Read the page title, landmarks, and heading list; confirm they describe the page.
3. Confirm every field is labeled and errors are announced with their field.
4. Confirm dialogs announce on open, contain focus, and restore focus on close.
5. Confirm status changes are announced through live regions, not silent.

## Docs and charts

1. Navigate by headings only: the outline must read as a table of contents.
2. Confirm alt text and diagram equivalents are announced.
3. Confirm chart tables or descriptions are reachable and announced.

## Evidence

Label every result Observed, CI-observed, or Estimated:

- **Observed:** a human or scripted reader session actually performed and recorded.
- **CI-observed:** run in automation; useful for drift but understates human listening time.
- **Estimated:** reasoned from code without execution. Never present an estimate as proof.

Record reader, OS, browser/terminal, and surface for every entry.

## Pass criteria

- no meaning is carried by color alone, animation alone, or the mouse alone
- every interactive element is named, reachable, and operable by keyboard
- errors and status changes are announced
- a screen-reader pass completes the main flows
