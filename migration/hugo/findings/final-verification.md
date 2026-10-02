# Final local verification

Generated from a scratch build; `docs/` was not replaced.

## Build

Command:

```sh
./migration/hugo/tools/build.sh
```

Results:

- Hugo build completed.
- 254 HTML pages generated.
- 0 AppleDouble sidecars remained.
- Path sets match master modulo the 9 documented Linux casing moves.
- Heading IDs: 35/35 pages match.
- Structural comparison: 173/245 comparable pages identical; 72 differ.

## Generated data

- `content.json`: 63 posts, 23 categories, 94 tags.
- Built-in `rss.xml`: valid XML.
- Built-in `sitemap.xml`: valid XML.

## Link check

The scratch output was crawled for root-relative internal links. No missing
targets were found.

## Remaining review

The structural differences are concentrated in legacy Markdown/code rendering
and listing-page text. A desktop browser was not available in this environment,
so paired visual screenshots remain for the owner's local test pass.
