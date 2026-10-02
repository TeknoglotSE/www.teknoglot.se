# Final review handoff

## Current state

- Branch: `hugo-migration`
- `docs/` has not been replaced.
- No remote push or deployment action has been performed.
- `hugo server` is available at `http://127.0.0.1:1313/`.

## Automated checks

Run from the repository root:

```sh
./migration/hugo/tools/build.sh
```

Latest results:

- Hugo scratch build completed.
- 254 master/build pages; path sets match modulo the 9 documented Linux moves.
- 0 AppleDouble sidecars.
- Heading IDs: 35/35 match.
- Structural comparison: 171/245 comparable pages identical; 74 differ.
- Built-in `/rss.xml` and `/sitemap.xml` are generated.
- `content.json` contains 63 posts, 23 categories, and 94 tags.

## Owner smoke tests completed

- Images and local relative image paths
- Navigation and layouts
- Permalinks
- RSS
- Insight search
- Window resizing
- Sitemap

## Deployment-time checks

- Disqus comments
- Google Analytics
- Final live-site URL and mixed-content review

## Do not do yet

- Do not run `./migration/hugo/tools/build.sh --publish` until the owner
  approves replacing `docs/`.
- Do not push the branch.
