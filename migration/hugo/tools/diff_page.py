#!/usr/bin/env python3
"""Show the first structural divergence for one or more pages, with context.

compare.py aggregates across the whole site, which is what you want for a
progress number but hides the detail. This is the drill-down.

Usage, from the repo root:
    python3 migration/hugo/tools/diff_page.py <build-dir> <page> [<page> ...]

where <page> is a path relative to docs/, e.g.
    index.html
    topics/ms/index.html
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
MASTER = os.path.join(REPO, "docs")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import Tokener, first_diff  # noqa: E402


def tokens(path):
    with open(path, encoding="utf-8") as fh:
        p = Tokener()
        p.feed(fh.read())
        p.close()
        return p.tokens


def show(tok):
    if tok is None:
        return "(none)"
    if len(tok) == 1 and tok[0][0].startswith("#"):
        s = tok[0][1]
        return "#text %r" % (s[:90] + ("..." if len(s) > 90 else ""))
    if len(tok) == 2 and tok[1] == ():
        return "%s %s" % (tok[0], tok[1])
    return str(tok)[:170]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    build = sys.argv[1]
    pages = sys.argv[2:]

    rc = 0
    for rel in pages:
        a = tokens(os.path.join(MASTER, rel))
        b = tokens(os.path.join(build, rel))
        d = first_diff(a, b)
        print("=" * 72)
        print(rel)
        print("  master tokens: %d   build tokens: %d" % (len(a), len(b)))
        if d is None:
            print("  IDENTICAL")
            continue
        rc = 1
        i, x, y = d
        print("  first divergence at token %d" % i)
        for k in range(max(0, i - 4), min(len(a), i + 5)):
            mark = ">>" if k == i else "  "
            print("  %s master: %s" % (mark, show(a[k])))
            print("  %s build : %s" % (mark, show(b[k])))
    return rc


if __name__ == "__main__":
    sys.exit(main())
