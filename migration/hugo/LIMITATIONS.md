# Accepted limitations

Accepted by the site owner before implementation. Reproduce faithfully; do
not attempt to correct during the migration. Each item states how it was
verified, so a later reader can re-check rather than trust.

## 1. Third-party services unverifiable locally

Disqus (`teknoglotse`), Google Analytics (`UA-382656-8`) and Insight search
load from external origins. Local serving cannot exercise them.

Verified instead: emitted markup, script tags, config values, and the shape
of `content.json`. Live behaviour must be checked after deploy.

## 2. Generator meta tag differs

Every master page emits `<meta name="generator" content="Hexo 7.3.0">`.
Hugo will emit its own or none. Normalised out of the diff.

## 3. Minification and whitespace differ

Master's `docs/` is minified by `hexo-all-minifier`. Hugo's output differs in
formatting. Normalised out of the diff; screenshots are the real check.

## 4. Timestamps cannot be reproduced

`article:modified_time` and `content.json`'s `updated` derive from
filesystem mtimes on master (59 distinct values). Replaced with last git
commit time. Values differ from master; the fields stay valid. Sitemap
`lastmod` likewise shifts.

## 5. Linux path casing deviates from master (intentional)

Master emits `/linux/...` URLs but stores `docs/Linux/...`, so those 5 posts
and the Linux topic tree 404 in production today.

Confirmed live before the decision:
`/linux/my-impression-of-ext4-wth/` -> 404, `/Linux/...` -> 200;
`/topics/linux/` -> 404, `/topics/Linux/` -> 200.

Hugo emits lowercase only. This is a deliberate divergence; the diff will
show the rename.

## 6. Pre-existing dead links are preserved

Content references targets that do not exist, from the WordPress era:

- `/ms/opsmgr2007/loadbalancing-ps-script-opsmgr/`
- `/code/powershell/opsmgr-2012-agent-gateway-failover-the-basics/`
- `/code/powershell/opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell/`
- `/series/om2012-failover-mgmt/`
- `/ms/opsmgr2007/failed-to-create-propertybagdata-opsmgr/`
- `/ms/opsmgr2007/change-gateway-powershell-script/attachment/changegw/`

Reproduced as-is. Repairing them is a separate content task.

## 7. Mixed content preserved

15 image references use `http://teknoglotse.nfshost.com/...` and 9 use
`http://www.teknoglot.se/...`, on an https site. Preserved verbatim.

Note: the `nfshost.com` host is long dead, so those images are already broken
in production. Fixing is out of scope.

## 8. Markdown rendering quirks preserved deliberately

- `msmq-4-and-msmq-5-mp-for-opsmgr-released-finally.md`: line 18 is
  4-space indented and therefore renders as an **indented code block**, not a
  blockquote (line 29 uses 2 spaces and does render as one). Keep the
  indentation.
- `regain-sysadmin-access-to-sql2005-or-sql2008.md`: a fenced block indented
  2 spaces inside a list (lines 34-37).
- `opsmgr-2012-agent-failover-a-faster-script-with-wildcards-opsmgr-powershell.md`:
  closing fence on line 44 has a leading space.
- 14 `<!--more-->` markers across 11 posts; 3 posts have several. Only the
  first separates the excerpt.
- One post uses singular `category:` (`Event-Id-4001-...md`).
- One post uses inline flow arrays (`20180906-...md`):
  `- [Fieldnotes,OpsMgr]`. Its URL uses only the **last** chain, which also
  leaves two orphan topic pages (`topics/Fieldnotes/`,
  `topics/ms/opsmgr1807/`). Preserved.
- Two posts carry a typo'd `s:` key, not `slug:` (`20161013-...`,
  `20180827-...`). Ignored, as in Hexo. Slugs derive from filenames.
- `w3socket-in-vbscript.md` list numbering runs 1,3,4,5,6,7,7,8,9,10. The
  renderer renumbers; that behaviour is fine.
- WP emoji shortcodes (`:shit::exclamation::question:`) and a
  `[xml highlight="7,8,9,10,11,12,13"]` WP shortcode residue inside a fence
  in `20180827-...` and `parameter-replacement-in-alertname.md` are left as
  literal text, as they render today.
- One zero-width space (U+200B) in `opsmgr-2012-r2-ur4-field-notes.md:76`.
- `¯\_(ツ)_/¯` in `20180906-...md:55`.

## 9. Front-matter `id` retained but unused

`id` exists on 52 of 63 posts. It is not used by the permalink scheme
(`permalink: :category/:title/`). Retained as data, not used for routing.

## 10. Single-element non-determinism

`date` in front matter always wins over the filename date prefix, and for the
four `20170928-*` posts it disagrees (front matter says 2017-09-25/26). That
asymmetry is reproduced: slug prefix from filename, dates from front matter.
