# Tasks

Status legend: `[ ]` todo, `[~]` in progress, `[x]` done, `[!]` blocked.

Proof means something checkable that a cold reader can re-run: a command, a
file under `findings/`, or a screenshot pair.

## P0 Setup

- [x] Create branch `hugo-migration` from master
- [x] Add `._*` and `.DS_Store` to `.gitignore`
- [x] Write `README.md`, `TASKS.md`, `LOG.md`, `LIMITATIONS.md`
- Proof: `git log --oneline -1`, `git status` clean

## P1 Permalink extraction (highest risk)

An error here silently breaks inbound links, so this is done and proven
before anything else.

- [x] Extract all 63 posts: filename, date, id, categories, tags
- [x] Derive the exact URL per post from master's `docs/post-sitemap.xml`
- [x] Emit `findings/permalinks.md` as the source of truth
- [x] Map category slug -> parent -> children, with `category_map` applied
- [x] Copy `source/_posts` -> `content/posts` with explicit `url` in front matter
- Proof: generated path set == master's path set, modulo the Linux rename

## P2 Templates

- [x] `baseof.html` + head/header/footer/sidebar partials
- [x] Archive listing, summary card, pagination (incl. ellipsis window)
- [x] article/post, date, tag, nav, share, disqus, insight search
- [x] Widgets: recent_posts, category, tagcloud, links
- [x] Tagcloud 10-20px linear interpolation between min/max tag counts
- [x] Assets: compiled `style.css` + `vendor/` carried over from `tg-hueman`
- [x] Goldmark `unsafe`, `hardWraps`, highlight class, Europe/Stockholm tz
- Proof: DOM diff vs master, screenshots

## P3 Non-template outputs

Hugo's built-in sitemap and RSS outputs are acceptable for this migration.

- [x] `content.json` (Insight search index)
- [x] Built-in `rss.xml`
- [x] Built-in `sitemap.xml`
- Proof: structural diff, item counts

## P4 Verification

- [x] Path-set diff vs master's `docs/`
- [~] Page-by-page diff, normalising generator/minification/timestamps
- [x] Internal link crawl, zero 404s
- [!] Paired screenshots in `screenshots/{before,after}/` — desktop browser was
  unavailable in this environment; owner should capture during local tests
- Proof: harness output committed under `findings/`

## P5 Switch-over prep (not executed)

- [ ] Commit `docs/`
- [ ] Leave push to the owner
- [ ] Owner pushes when satisfied

## P6 Post-migration: native Hugo authoring

The migration scripts are one-time conversion and verification tooling only.
After the Hugo site is accepted, future publishing should use Hugo natively
and must not depend on regenerating `content/` from the old Hexo sources.

- [ ] Make `content/` the canonical source for new and edited posts
- [ ] Add `archetypes/default.md` (and any post/page archetypes needed)
- [ ] Verify `hugo new posts/<slug>.md` creates a usable draft
- [ ] Add native section layouts so section warnings are eliminated
- [ ] Enable/configure native Hugo taxonomies for the desired tag/category UX
- [ ] Add or update native taxonomy templates and verify generated URLs
- [ ] Document the post-migration publishing workflow in `README.md`
- [ ] Mark `source/`, Hexo config, and migration generators as legacy/archive
  inputs once the owner confirms they are no longer needed
- [ ] Keep `migration/hugo/tools/` for historical comparison/reproducibility,
  but remove it from the normal publish workflow

This follow-up must preserve the already-approved permalink and output
behavior unless the owner explicitly approves a separate URL migration.
