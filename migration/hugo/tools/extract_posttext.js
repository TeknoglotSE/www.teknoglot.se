#!/usr/bin/env node
/**
 * Extract the `text` field for every post and page from master's content.json
 * into data/posttext.json.
 *
 * This value is pinned rather than computed. master's text cannot be
 * reproduced by stripping tags from the rendered HTML, because the two posts
 * disagree about the same construct:
 *
 *   ms/opsmgr1801/Upgrading-...  renders "...others.</span><br><span class="line">The main"
 *   ms/opsmgr2016/om1801-...    renders "...program.<br>No upgrade"
 *
 * Both are hard breaks, yet stripping tags would join both without a space
 * while master joins only one. The `text` field is also unused by the theme
 * except as search-index input, so the value is simply read and stored.
 *
 * Keyed by post slug. Pages are keyed "About".
 *
 * Usage, from the repo root:
 *   node migration/hugo/tools/extract_posttext.js
 */

const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..', '..');
const DOCS = path.join(REPO, 'docs');
const OUT = path.join(REPO, 'data');

function fail(msg) {
  console.error('FAIL: ' + msg);
  process.exit(1);
}

function main() {
  const cjPath = path.join(DOCS, 'content.json');
  if (!fs.existsSync(cjPath)) fail('docs/content.json missing');

  const cj = JSON.parse(fs.readFileSync(cjPath, 'utf8'));
  const out = {};

  for (const p of cj.posts) {
    if (!p.slug) fail('post with empty slug');
    out[p.slug] = p.text || '';
  }
  for (const p of (cj.pages || [])) {
    // the About page has no slug in master; key it by its path
    out[p.path.replace(/index\.html$/, '').replace(/^\//, '')] = p.text || '';
  }

  const posts = Object.keys(out).length;
  if (cj.posts.length !== 63) {
    fail('expected 63 posts in content.json, found ' + cj.posts.length);
  }
  if (posts < 63) fail('only ' + posts + ' text entries collected');

  fs.mkdirSync(OUT, { recursive: true });
  const target = path.join(OUT, 'posttext.json');
  fs.writeFileSync(target, JSON.stringify(out));

  const bytes = fs.statSync(target).size;
  console.log('wrote data/posttext.json: ' + posts + ' entries, ' +
    Math.round(bytes / 1024) + ' KiB');
}

main();
