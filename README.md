# teknoglot

This is a Hugo site. The canonical content lives under `content/`, templates
under `layouts/`, and published output under `docs/`.

## Local workflow

```sh
hugo serve
hugo new posts/my-post.md
hugo --destination "$(pwd)/docs" --cleanDestinationDir
```

New posts are created as drafts from `archetypes/default.md`. Edit the new
file, set `draft: false` when ready, and run Hugo from the repository root.

The site uses explicit front-matter URLs to preserve the established public
paths. Do not change a post URL without deliberately planning a redirect or
URL migration.

## Publishing

Run `hugo --destination "$(pwd)/docs" --cleanDestinationDir` to regenerate `docs/`. Review the generated
diff and test locally before committing. Deployment is handled by the owner's
remote publishing workflow; this repository does not push automatically.

## Assets

Static files, including migrated WordPress uploads, live under `static/` and
are published at the site root. Use root-relative paths such as
`/wp-content/uploads/...` for local assets.
