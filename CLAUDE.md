# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A browser-based Tic Tac Toe game delivered as a single self-contained HTML file (`tictactoe.html`). No build tools, no dependencies, no server — open the file directly in a browser.

## Running the project

```powershell
Start-Process tictactoe.html   # opens in default browser
```

## Architecture

Everything lives in `tictactoe.html` in three co-located sections:

- **HTML** — a 3×3 grid of `.cell` divs with `data-index` attributes (0–8)
- **CSS** — dark theme (`#1a1a2e` background), grid layout, win-pulse animation
- **JavaScript** — vanilla JS, no frameworks. Key state: `board` (9-element array), `current` (active player), `gameOver`, `scores`. Win detection iterates `WINS` (8 hardcoded triplets). All DOM updates go through `setStatus()` and direct class manipulation on `.cell` elements.

## Git workflow

- Remote: `https://github.com/TheOostman/ClaudeCodeTest`
- Branch: `master`
- Every commit must have a descriptive subject line (imperative mood, ≤72 chars) and a short body when the change warrants explanation.
