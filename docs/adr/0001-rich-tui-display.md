# ADR-0001: Rich TUI Display

**Status:** Accepted  
**Date:** 2026-06-19  
**Driver:** `grill-with-docs` session with user

## Context

ImageForge had a basic interactive TUI built on `click.prompt` / `click.confirm` — functional but visually plain. The user asked for "better visual presentation" in the TUI menu flow.

## Decision

Replace `click.style` / `click.echo` with Rich's `Console`, `Panel`, `Table`, and `status` spinner globally:

- **`utils/display.py`** — all output functions (`print_banner`, `print_diff`, `print_success`, `print_info`, `print_error`) now use `rich.console.Console` with markup
- **`editor/tui.py`** — menu header rendered in a `Panel`, processing operations wrapped in `console.status()` spinner
- **`requirements.txt`** — added `rich==15.0.0`

Click prompts (`click.prompt`, `click.confirm`, `click.Choice`) are retained for user input — Rich handles display only.

## Consequences

- All CLI output (not just TUI) gets Rich styling since `utils/display.py` is shared
- Existing tests pass: Rich's auto-detection falls back to plain text in non-TTY (CliRunner) environments
- One new dependency: `rich` (pure Python, widely used, no native extensions)
