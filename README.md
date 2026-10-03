# teknoglot

This is a Hugo site. The canonical content lives under `content/`, templates
under `layouts/`, and published output under `docs/`.

## Local workflow

```sh
hugo new posts/my-post.md
hugo server --renderToMemory
hugo --cleanDestinationDir
```

New posts are created as drafts from `archetypes/default.md`. Edit the new
file and flip `draft: false` when ready.

`docs/` is set in `hugo.toml` as `publishDir`, so a plain `hugo` writes there.
Pass `--destination` only to build somewhere else, and then give it an
absolute path: a relative one is resolved against the repository root, so
`--destination docs` would build into the publish directory itself.

Always pass `--renderToMemory` to `hugo server`. Without it the dev server
writes to `publishDir`, which overwrites the committed `docs/` with a build
full of `localhost` URLs and a livereload script tag. If that happens, a plain
`hugo --cleanDestinationDir` restores it.

The site uses explicit front-matter URLs to preserve the established public
paths. Do not change a post URL without deliberately planning a redirect or
URL migration.

## Page kinds

`content/` is organised into sections, each with its own `_index.md`:

| Section | Layout | URL |
| --- | --- | --- |
| `posts/` | `layouts/_default/single.html` | varies per post |
| `pages/` | `layouts/_default/single.html` | `/About/` |
| `topics/` | `layouts/topic/list.html` | `/topics/...` |
| `tags/` | `layouts/tagpage/list.html` | `/tag/...` |
| `archives/` | `layouts/archive/list.html` | `/archives/...` |

The section indexes for `posts/`, `pages/`, `tags/` and `topics/` are marked
`build: render: false`: those URLs are not part of the public site.
`layouts/_default/section.html`, `taxonomy.html` and `term.html` exist so a new
section, or a taxonomy enabled in `hugo.toml`, renders correctly.

Categories and tags are plain front-matter keys (`cats`, `tags`), not Hugo
taxonomies. `[taxonomies]` is empty on purpose, because the established topic
and tag URLs are nested, partly case-preserving and partly orphaned, which no
Hugo taxonomy can express. The listing pages resolve their links through the
`content/topics/` and `content/tags/` leaves, so a new post's `cats` and `tags`
values only take effect once a matching leaf exists.

## Writing

Each content kind has its own archetype, so `hugo new` fills in what can be
derived from the path:

```sh
hugo new posts/my-post.md               # title, date, cats, url
hugo new topics/ms/opsmgr2013/_index.md # cat, cat_parent, url from the path
hugo new tags/Kubernetes/_index.md      # tag, tag_slug, url from the path
hugo new archives/2026/_index.md        # year
hugo new archives/2026/10/_index.md     # year and month
```

A post needs no `description` and no `excerpt`: both fall back to a summary
Hugo generates from the body. Pin them only to control the wording.

A new period needs archive leaves before its posts can appear in the archive.
The same holds for a new category or tag, which needs a leaf under
`content/topics/` or `content/tags/`.

Two things to know:

- **Future-dated posts are not built.** Hugo skips a page dated later than the
  build, so a `date:` in the future makes the post silently disappear. Date a
  post in the past when publishing it now.
- **A tag needs a `cloud_order`.** It is the one number here that cannot be
  derived. The cloud is ordered byte-wise by name, so `Gist` precedes `GSM`,
  while Hugo's own sort collates and reverses those. The archetype parks a new
  tag at 999; only the cloud's reading order depends on the value.

The permalink guard reads the git index, so stage new files before checking it.

## Style

`STYLE.md` documents the voice, measured rather than guessed: American spelling,
sentence-case headings, the 5-to-35 word spread in sentence length that is the
voice rather than a defect, the recurring heading vocabulary per genre, and an
explicit list of the things an agent must not "improve". Read it before drafting
a post or editing an existing one.

`tools/style.py` checks the mechanical subset before you commit:

```sh
python3 tools/style.py                    # changed posts, against HEAD
python3 tools/style.py --against <rev>    # against an older revision
python3 tools/style.py content/posts/x.md # one file
```

It reports and never rewrites, and it exits non-zero on findings. Every rule is
phrased as a *change* against the previous committed version, so the existing
corpus can never fail for being old, and a rewrite that quietly strips the
author's contractions or first person shows up as a removal. The rules that are
implemented, and the ones that are not, are listed at the end of `STYLE.md`.

## Publishing

Run `hugo --cleanDestinationDir` to regenerate `docs/`, then verify the
permalink set, review the generated diff, and test locally before committing.
Deployment is handled by the owner's remote publishing workflow; this
repository does not push automatically.

## Permalinks are permanent

Every URL the site serves is in `permalinks.txt`. Check it before committing:

```sh
python3 tools/permalinks.py
```

It exits non-zero and lists additions and removals if the set moved. Adding a
post adds a URL and that is expected. Losing one breaks inbound links, so a
removal needs a redirect on the old path before the manifest is updated:

```sh
python3 tools/permalinks.py --update
```

The check reads the **git index**, not the files on disk, because this volume
is case-insensitive and `core.ignorecase` is set. The filesystem reports
whichever casing it happens to hold while the index records what will actually
be deployed, and the web server is case-sensitive. That gap shipped a real
outage once: the tree held `docs/Linux/` while every link pointed at
`/linux/`, and ten URLs 404'd. Only the index can see it, so no build is
needed to check.

Paths in the manifest are site-relative, so changing the domain is not a
permalink change. Letter case is significant.

## Assets

Static files, including imported WordPress uploads, live under `static/` and
are published at the site root. Use root-relative paths such as
`/wp-content/uploads/...` for local assets.