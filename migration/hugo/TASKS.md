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

- [~] Extract all 63 posts: filename, date, id, categories, tags
- [ ] Derive the exact URL per post from master's `docs/post-sitemap.xml`
- [ ] Emit `findings/permalinks.md` as the source of truth
- [ ] Map category slug -> parent -> children, with `category_map` applied
- [ ] Copy `source/_posts` -> `content/posts` with explicit `url` in front matter
- Proof: generated path set == master's path set, modulo the Linux rename

## P2 Templates

- [ ] `baseof.html` + head/header/footer/sidebar partials
- [ ] Archive listing, summary card, pagination (incl. ellipsis window)
- [ ] article/post, date, tag, nav, share, disqus, insight search
- [ ] Widgets: recent_posts, category, tagcloud, links
- [ ] Tagcloud 10-20px linear interpolation between min/max tag counts
- [ ] Assets: compiled `style.css` + `vendor/` carried over from `tg-hueman`
- [ ] Goldmark `unsafe`, `hardWraps`, highlight class, Europe/Stockholm tz
- Proof: DOM diff vs master, screenshots

## P3 Non-template outputs

Hugo has no equivalents, so these are hand-built.

- [ ] `content.json` (Insight search index)
- [ ] `rss.xml` with 50-item cap
- [ ] `sitemap.xml` index + `post-`/`page-`/`category-`/`tag-sitemap.xml`
- [ ] `sitemap.xsl`
- Proof: structural diff, item counts

## P4 Verification

- [ ] Path-set diff vs master's `docs/`
- [ ] Page-by-page diff, normalising generator/minification/timestamps
- [ ] Internal link crawl, zero 404s
- [ ] Paired screenshots in `screenshots/{before,after}/`
- Proof: harness output committed under `findings/`

## P5 Switch-over prep (not executed)

- [ ] Commit `docs/`
- [ ] Leave push to the owner
- [ ] Owner pushes when satisfied
