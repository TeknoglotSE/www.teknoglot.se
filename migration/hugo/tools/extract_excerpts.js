#!/usr/bin/env node
/**
 * Extract the summary-card excerpt for every post, harvested from master's
 * rendered listing pages.
 *
 * The theme registers its own `excerpt` helper
 * (themes/tg-hueman/scripts/excerpt.js):
 *
 *   excerpt = post.excerpt
 *             ? post.excerpt.replace(/<[^>]+>/g, '')
 *             : post.content.replace(/<[^>]+>/g, '').substring(0, 200)
 *
 * and renders it with EJS' unescaped `<%- %>`, so the text reaches the page
 * without a further round of HTML escaping.
 *
 * The values are harvested from the rendered pages rather than read from
 * `docs/content.json`, because content.json is lossy in two ways:
 *
 *   - it stores the excerpt HTML-escaped ("App&amp;Infra" for "App&Infra");
 *   - it normalises a non-breaking space to a plain space in at least one post,
 *     while the rendered page keeps the NBSP.
 *
 * Every post appears on at least one listing page, and the pages are checked
 * against each other: any post whose excerpt differs between pages is reported
 * as a conflict rather than silently resolved.
 *
 * Usage, from the repo root:
 *   node migration/hugo/tools/extract_excerpts.js
 */

const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..', '..');
const DOCS = path.join(REPO, 'docs');
const OUT = path.join(REPO, 'migration', 'hugo', 'findings');

function fail(msg) {
  console.error('FAIL: ' + msg);
  process.exit(1);
}

function unescapeHtml(s) {
  return s
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)))
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');
}

function walk(dir, acc) {
  for (const name of fs.readdirSync(dir)) {
    if (name.startsWith('._')) continue;
    const full = path.join(dir, name);
    if (fs.statSync(full).isDirectory()) walk(full, acc);
    else if (name === 'index.html') acc.push(full);
  }
  return acc;
}

function main() {
  const files = walk(DOCS, []);
  const hrefRe = /<h1 class="article-title" itemprop="name"><a href="([^"]+)"/g;
  const exRe = /<p class="article-excerpt">([\s\S]*?)<\/p>/g;

  const seen = new Map();   // slug -> excerpt
  const pages = new Map();  // slug -> Set(page)
  let pairs = 0;
  const problems = [];

  for (const file of files) {
    const html = fs.readFileSync(file, 'utf8');
    const hrefs = [];
    let m;
    while ((m = hrefRe.exec(html))) hrefs.push(m[1]);
    const excerpts = [];
    while ((m = exRe.exec(html))) excerpts.push(m[1]);

    if (!excerpts.length) continue;
    if (hrefs.length !== excerpts.length) {
      problems.push('title/excerpt count mismatch in ' +
        path.relative(DOCS, file) +
        ' (' + hrefs.length + ' vs ' + excerpts.length + ')');
      continue;
    }

    for (let i = 0; i < hrefs.length; i++) {
      // hrefs are percent-encoded; taxonomy.json keys slugs in raw unicode
      const raw = hrefs[i].replace(/^\/+|\/+$/g, '');
      const slug = decodeURIComponent(raw).split('/').pop();
      const text = unescapeHtml(excerpts[i]);
      pairs++;
      if (seen.has(slug) && seen.get(slug) !== text) {
        problems.push('conflicting excerpts for ' + slug + ' (' +
          path.relative(DOCS, file) + ' vs earlier page)');
      }
      seen.set(slug, text);
      if (!pages.has(slug)) pages.set(slug, new Set());
      pages.get(slug).add(path.relative(DOCS, file));
    }
  }

  if (problems.length) {
    problems.slice(0, 10).forEach(p => console.log('  ! ' + p));
    fail(problems.length + ' problem(s)');
  }
  if (seen.size !== 63) {
    fail('harvested ' + seen.size + ' posts, expected 63');
  }

  const out = {};
  for (const slug of [...seen.keys()].sort()) {
    out[slug] = { excerpt: seen.get(slug), seenOn: pages.get(slug).size };
  }
  fs.writeFileSync(path.join(OUT, 'excerpts.json'),
    JSON.stringify(out, null, 1));

  console.log('harvested ' + seen.size + ' excerpts from ' +
    pairs + ' rendered cards across ' + files.length + ' pages');
  console.log('wrote findings/excerpts.json');
}

main();
