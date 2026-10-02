#!/usr/bin/env python3
"""Verify every content heading id in the build against master's.

markdown-it-plus slugifies heading text with hexo-util's slugize, which
collapses a run of reserved characters into a single dash. Goldmark's "github"
anchor style does not, so the render hook in
layouts/_default/_markup/render-heading.html collapses and trims instead.

This checks the result rather than trusting the regex.

Usage, from the repo root:
    python3 migration/hugo/tools/check_heading_ids.py <build-dir>
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
MASTER = os.path.join(REPO, "docs")

# only headings inside the article body carry a slugified id; the theme's own
# headings (widget titles, the article h1) must be left alone
HEADING = re.compile(r"<h([1-6])[^>]*\bid=[\"']?([^\"'>\s]+)")


def headings(path):
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"article-entry[^>]*>(.*?)</article>", html, re.S)
    if not m:
        return []
    return [(lvl, i) for lvl, i in HEADING.findall(m.group(1))]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    build = sys.argv[1]

    total = 0
    checked = 0
    problems = []

    for base, dirs, files in os.walk(MASTER):
        dirs[:] = [d for d in dirs if not d.startswith("._")]
        if "index.html" not in files:
            continue
        rel = os.path.relpath(os.path.join(base, "index.html"), MASTER)
        rel = rel.replace(os.sep, "/")
        target = os.path.join(build, rel)
        if not os.path.exists(target):
            continue

        a = headings(os.path.join(MASTER, rel))
        b = headings(target)
        if not a and not b:
            continue
        total += 1
        if a == b:
            checked += 1
        else:
            problems.append((rel, a, b))

    print("pages with content headings : %d" % total)
    print("heading ids matching        : %d" % checked)
    if problems:
        print("MISMATCHES:")
        for rel, a, b in problems[:10]:
            print("  " + rel)
            print("    master: %s" % (a,))
            print("    build : %s" % (b,))
        print("\n%d page(s) differ" % len(problems))
        return 1
    print("all heading ids match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
