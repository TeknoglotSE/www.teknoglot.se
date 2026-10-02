#!/usr/bin/env python3
"""Capture ground-truth HTML fragments from master's committed docs/.

These become golden fixtures. The Hugo build is diffed against them, so a
regression in the nav tree, sidebar, tagcloud sizing or pagination markup is
caught mechanically rather than by eye.

Source is the real minified output, not a re-derivation, so the fixtures
cannot inherit our assumptions.

Run from the repo root:
    python3 migration/hugo/tools/capture_golden.py
"""

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
DOCS = os.path.join(REPO, "docs")
OUT = os.path.join(REPO, "migration", "hugo", "findings", "golden")


def read(rel):
    path = os.path.join(DOCS, rel)
    if not os.path.exists(path):
        fail("missing %s" % rel)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def fail(msg):
    print("FAIL: " + msg, file=sys.stderr)
    sys.exit(1)


def between(s, start, end, required=True):
    i = s.find(start)
    if i < 0:
        if required:
            fail("start marker not found: %r" % start[:60])
        return None
    j = s.find(end, i)
    if j < 0:
        if required:
            fail("end marker not found for %r" % start[:60])
        return None
    return s[i:j + len(end)]


def main():
    os.makedirs(OUT, exist_ok=True)
    home = read("index.html")
    fixtures = {}

    # --- nav tree -------------------------------------------------------
    # boundary is <nav id="sub-nav">, which follows the nav list directly.
    nav = between(home, '<ul id="main-nav">', '<nav id="sub-nav">')
    fixtures["nav.html"] = nav

    # --- sidebar category widget ---------------------------------------
    catlist = between(home, '<ul class="category-list">', "</ul></div>")
    fixtures["sidebar-categories.html"] = catlist

    # --- tagcloud -------------------------------------------------------
    cloud = between(home, '<div class="widget tagcloud">', "</div>")
    fixtures["sidebar-tagcloud.html"] = cloud

    # tagcloud as structured data, for numeric comparison
    pairs = re.findall(r'href="/tag/([^"]+)/" style="font-size:([\d.]+)px"',
                       cloud)
    if len(pairs) != 94:
        fail("expected 94 tags in tagcloud, found %d" % len(pairs))
    fixtures["tagcloud.json"] = json.dumps(
        [{"tag": t, "size": float(s)} for t, s in pairs], indent=1)

    # --- sidebar order + recent posts ----------------------------------
    order = re.findall(r'<h3 class="widget-title">([^<]*)</h3>', home)
    fixtures["widget-order.json"] = json.dumps(order, indent=1)

    # Category counts are DISPLAYED data, and Hexo's own count disagrees with
    # its listing: the sidebar shows Microsoft = 42 while /topics/ms/ actually
    # lists 41 posts. That post is filed under two ms sub-chains at once, which
    # is what tips the count. Rather than reimplement Hexo's arithmetic, the 23
    # displayed counts are read straight out of the rendered sidebar.
    pairs = re.findall(
        r'href="(/topics/[^"]+)">([^<]*)</a>'
        r'<span class="category-list-count">(\d+)</span>', catlist)
    if len(pairs) != 23:
        fail("expected 23 category nodes in the sidebar, found %d" % len(pairs))
    counts = {url: int(n) for url, _, n in pairs}
    names = {url: name for url, name, _ in pairs}
    fixtures["category-counts.json"] = json.dumps(
        [{"url": u, "name": names[u], "count": counts[u]}
         for u in sorted(counts, key=str.lower)], indent=1)

    recent = between(home, '<ul id="recent-post"', "</ul></div>")
    fixtures["sidebar-recent.html"] = recent

    # --- pagination, first / middle / last ------------------------------
    p1 = between(home, '<nav id="page-nav">', "</nav>")
    fixtures["pagination-home-1.html"] = p1
    p4 = between(read("page/4/index.html"), '<nav id="page-nav">', "</nav>")
    fixtures["pagination-home-4.html"] = p4
    p7 = between(read("page/7/index.html"), '<nav id="page-nav">', "</nav>")
    fixtures["pagination-home-7.html"] = p7

    # --- archive index --------------------------------------------------
    fixtures["archives-index.html"] = read("archives/index.html")

    # --- head, for meta comparison --------------------------------------
    head = between(home, "<head>", "</head>")
    fixtures["home-head.html"] = head
    post_head = between(read("ms/opsmgr2007/change-gateway-powershell-script/index.html"),
                        "<head>", "</head>")
    fixtures["post-head.html"] = post_head

    for name, body in fixtures.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body if isinstance(body, str) else json.dumps(body, indent=1))
        size = len(body) if isinstance(body, str) else len(json.dumps(body))
        print("  %-34s %7d bytes" % (name, size))

    print("wrote %d fixtures to migration/hugo/findings/golden/" % len(fixtures))


if __name__ == "__main__":
    main()
