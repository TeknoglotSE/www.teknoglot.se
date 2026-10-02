# Log

Append-only, newest last. Records decisions and dead ends so a later session
does not repeat work.

## 2026-10-02 — Investigation and planning

### Environment

Session started one level above the repo (`/Volumes/P01/dev`). All analysis
done by absolute path, then the session was moved into
`/Volumes/P01/dev/www.teknoglot.se`. No work was lost.

The volume was littered with AppleDouble `._*` files, including 43 inside
`.git`, which caused `non-monotonic index` errors on some git commands. The
owner ran `dot_clean`; afterwards 0 `._*` files remained and `git status`
returned clean with no errors. These regenerate as files are edited on this
volume, hence the `.gitignore` rule rather than a one-off cleanup.

Toolchain verified: Hugo v0.166.0 extended (extended needed for SCSS), Go,
Node 26.

### Repository shape

- 63 posts in `source/_posts`, one standalone page (`source/About/index.md`).
- `docs/` is the Hexo output and is committed. It is the comparison baseline.
- Theme `themes/tg-hueman`, a fork of ppoffice's hueman.
- Hexo config: `permalink: :category/:title/`, `category_dir: topics`,
  `tag_dir: tag`, `per_page: 10`, `timezone: Europe/Stockholm`,
  `public_dir: docs`.

### Deployment mechanism: unknown

There is **no `.github/` directory and no CI config anywhere in the repo.**
Checked: the working tree, all tracked files, every branch (`master`,
`origin/develop`), and the full commit history for any added path under
`.github/`. Nothing.

The owner states a GitHub Actions workflow exists **outside this repo**.
Consequence agreed: generate `docs/` and commit it; publishing is entirely the
owner's business. No CI config is to be added here.

### Decision: Linux path casing — fix to lowercase

Master emits `/linux/...` URLs everywhere (nav, sitemap, RSS, pagination) but
stores `docs/Linux/...` and `docs/topics/Linux/...`. Cause: `category_map`
gained `Linux: linux` after the directories were first created, and the
case-insensitive macOS volume collapsed the second write into the first.

Verified live before deciding:

    404  /linux/my-impression-of-ext4-wth/
    200  /Linux/my-impression-of-ext4-wth/
    404  /topics/linux/
    200  /topics/Linux/

So 5 posts plus the Linux topic tree are broken in production right now, and
Google has the 404ing lowercase URLs indexed via the sitemap. Hugo emits
lowercase only. Recorded as limitation 5.

Note this will **not** reproduce from a clean checkout under Hexo either: a
case-sensitive filesystem would have produced `docs/linux/` all along. The
current state is an artefact of the author's machine.

### Decision: timestamps from git

`article:modified_time` and `content.json`'s `updated` derive from filesystem
mtimes (59 distinct values across posts). Not reproducible in a deterministic
build. Replaced with last git commit time per post. Recorded as limitation 4.

### Decision: keep the Hexo half intact

`_config.yml`, `source/`, `themes/` and `package.json` stay untouched and
working, so the old site can still be regenerated as a fallback until
switch-over. Hugo lives alongside, and takes over `docs/` at the end.

### Risk assessment

Highest risk is permalink fidelity, because `:title` derives from the
**filename** (not the front-matter title) with Hexo's own slug rules, which
differ from Hugo's `urlize` on unicode and reserved characters. The case
`Event-Id-4001-–-“Cannot-Add-Type”-in-SQL-MP-6-6-4-0-for-OpsMgr2012`
percent-encodes to `%E2%80%93` / `%E2%80%9C` / `%E2%80%9D` in the sitemap and
must survive exactly.

Therefore each post will carry an explicit `url` in front matter rather than
relying on Hugo to derive it. Taxonomy behaviour cannot then perturb routing.

### Content traps recorded

Noted during audit so they are not "cleaned up" by mistake. Full detail in
`LIMITATIONS.md` section 8. Highlights: a typo'd `s:` key on two posts (not
`slug:`, silently ignored by Hexo), singular `category:` on one post, inline
flow arrays on one post, `<!--more-->` markers on 14 lines across 11 posts,
and a 4-space-indented line that renders as a code block rather than a
blockquote.

### Scaffolding written

`README.md`, `TASKS.md`, `LOG.md`, `LIMITATIONS.md`. First draft of
`TASKS.md` incorrectly marked all phases complete; corrected to reflect real
state before any work started.

Correction: an earlier draft of `TASKS.md` had every task checked. That was a
transcription error, not progress. Only P0 is complete.
