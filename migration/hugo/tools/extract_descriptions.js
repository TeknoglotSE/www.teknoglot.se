#!/usr/bin/env node
/**
 * Read the `<meta name="description">` value for every single page.
 *
 * Hexo's `open_graph()` computes it as:
 *
 *   escapeHTML(stripHTML(src).substring(0, 200).trim()).replace(/\n/g, ' ')
 *
 * where src is `page.description || page.excerpt || content || config.description`.
 *
 * Two traps make recomputation unreliable, so the values are read from master
 * and pinned as data instead:
 *
 *  1. open_graph() ran against the UN-minified rendered content, where block
 *     elements are separated by newlines. `hexo-all-minifier` removed those
 *     newlines afterwards, so recomputing from the built file loses the spaces
 *     that `replace(/\n/g, ' ')` used to insert.
 *  2. The result is 200 SOURCE characters, but escaping expands it, so the
 *     attribute can exceed 200 (e.g. '/' becomes '&#x2F;'). Truncating the
 *     attribute itself would corrupt it.
 *
 * Listing pages (home, category, tag, archive) have no content of their own,
 * so they fall back to the site description and need no entry here.
 *
 * Usage, from the repo root:
 *   node migration/hugo/tools/extract_descriptions.js
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

function metaDescription(html) {
  const m = html.match(/<meta name="description" content="([^"]*)">/);
  return m ? m[1] : null;
}

/**
 * Undo one round of HTML escaping.
 *
 * The raw attribute holds entities such as `&#x2F;` for a slash, because Hexo
 * escaped the value on the way out. Storing that escaped text in front matter
 * makes Hugo escape it again when it writes the attribute, producing
 * `&amp;#x2F;` and a doubly-escaped value. Storing the decoded form lets Hugo
 * do the single escaping pass, which matches master after decoding.
 */
function unescapeHtml(s) {
  return s
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)))
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');
}

function main() {
  const tax = JSON.parse(
    fs.readFileSync(path.join(OUT, 'taxonomy.json'), 'utf8'));

  const results = {};
  const problems = [];

  function record(key, file) {
    if (!fs.existsSync(file)) {
      problems.push('missing built page: ' + file);
      return;
    }
    const actual = metaDescription(fs.readFileSync(file, 'utf8'));
    if (actual === null) {
      problems.push('no description meta in ' + key);
      return;
    }
    const decoded = unescapeHtml(actual);
    if (!decoded.trim()) {
      problems.push('empty description in ' + key);
      return;
    }
    // 200 source chars; escaping can expand it, so allow headroom.
    if (actual.length > 260) {
      problems.push('suspiciously long description in ' + key +
        ' (' + actual.length + ' chars)');
    }
    results[key] = decoded;
  }

  for (const post of tax.posts) {
    record(post.dir, path.join(DOCS, post.dir, 'index.html'));
  }
  record('About/', path.join(DOCS, 'About', 'index.html'));

  if (problems.length) {
    problems.slice(0, 10).forEach(p => console.log('  ! ' + p));
    fail(problems.length + ' problem(s); nothing written');
  }

  const expected = tax.posts.length + 1;
  if (Object.keys(results).length !== expected) {
    fail('expected ' + expected + ' descriptions, got ' +
      Object.keys(results).length);
  }

  fs.writeFileSync(
    path.join(OUT, 'descriptions.json'),
    JSON.stringify(results, null, 1));

  console.log('read ' + Object.keys(results).length + ' descriptions');
  console.log('wrote findings/descriptions.json');
}

main();
