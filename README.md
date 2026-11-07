# GTG Advisor

A personal advisor for **Invincible: Guarding the Globe**: next moves, PvP and Boss Raid teams, GDA ops (with wave logging and swaps between ops), artifact plans, a battle planner for campaign stages and case files, and team positions. Everything is worked out from your own roster, which you enter in the app.

**Open it:** https://mkeegan-stack.github.io/gtg-advisor/ — then add it to your Home Screen (iPhone: Safari → ⋯ → Share → Add to Home Screen; Android: Install). It runs full screen, works offline and keeps your data on your phone only. Use More → Backup to save a backup file.

## How the advice is built

- **Game data** (heroes, skills, stats, factions, ops, costs): compiled from the game files via gacha.gg and GTG Hub into `src/data/game-data.base.json`.
- **Community research** (ratings, artifact pairings, op teams, skill priorities): r/invinciblegtg threads, counted and checked by hand, plus LincGames' guide notes. Applied by `src/overrides.py`, which documents where each decision comes from. Only pairings or opinions several players agree on are used.
- **Your data** stays in your browser's storage. Nothing is sent anywhere.

## Updating after a game patch

1. Edit `src/overrides.py` (and, for new heroes or stats, `src/data/game-data.base.json`).
2. `python3 src/build.py` — writes `index.html`, `sw.js`, `manifest.webmanifest` and launch screens at the repo root. The service-worker cache version changes with every build, so phones pick up the update.
3. `python3 src/tests/test.py` (needs Playwright + Chromium) — install guide, every screen at 320/390/430 px, startup animation, offline loading, data surviving a reload, no requests to other sites.
4. Commit and push. On the phone: swipe the app closed and reopen it (twice if needed).

`tools/reddit/` has the scripts used for the research (Reddit RSS; output goes to an untracked `reddit-data/` folder).

## Credits and licences

- Fonts: Saira Condensed and Rubik, SIL Open Font License (`fonts/OFL-*.txt`).
- QR codes: [qrcode-generator](https://github.com/kazuhikoarase/qrcode-generator) by Kazuhiko Arase, MIT (`vendor/LICENSE-qrcode-generator.txt`).
- Not affiliated with Ubisoft or Skybound. Character and game names belong to their owners.
