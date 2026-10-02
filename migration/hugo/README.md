# Hugo migration (Hexo -> Hugo)

Branch: `hugo-migration` (from `master`). Do not push.

Goal: `docs/` output visually and structurally identical to master's Hexo
output, with all 63 permalinks byte-identical.

## Resuming work

1. Read `TASKS.md` for current state.
2. Read `LOG.md` for decisions already made and things already tried.
3. `findings/permalinks.md` is the source of truth for every URL.
4. Check the toolchain: `hugo version`. Needs **extended** (for SCSS).
   Verified working: Hugo v0.166.0 extended, Go, Node 26.

Task state and decisions live in these files rather than in any agent's
context, specifically so a cold start can pick up exactly where a previous
session stopped.

## Layout

The Hexo half is kept intact as a working fallback until switch-over:
`_config.yml`, `source/`, `themes/`, `package.json`, `db.json`.

The Hugo half: `hugo.toml`, `content/`, `layouts/`, `assets/`, `static/`.

`migration/` is outside Hugo's scope. Hugo only reads `hugo.toml`,
`content/`, `layouts/`, `assets/`, `static/`, `data/`, `i18n/`,
`archetypes/`, so a root-level folder is inert and never rendered.

## Rules

- **Never `git push`.** Never create remotes or tags. GitHub Actions and
  Pages must not be triggered until the owner decides to switch over.
- Commit locally only.
- Regenerate with `hugo` (never `hugo new`, which would scaffold).
- Output goes to `docs/`.

## Reference

- `LIMITATIONS.md` — deviations from master that are signed off. Do not
  "fix" these during the migration.
- `findings/` — extracted data and verification output.
- `screenshots/` — paired before/after captures.
