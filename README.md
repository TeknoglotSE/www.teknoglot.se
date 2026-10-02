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

## Publishing

Run `hugo --cleanDestinationDir` to regenerate `docs/`, review the generated
diff, and test locally before committing. Deployment is handled by the owner's
remote publishing workflow; this repository does not push automatically.

## Assets

Static files, including imported WordPress uploads, live under `static/` and
are published at the site root. Use root-relative paths such as
`/wp-content/uploads/...` for local assets.