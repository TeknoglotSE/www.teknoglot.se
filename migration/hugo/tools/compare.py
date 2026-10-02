#!/usr/bin/env python3
"""Compare the Hugo build against master's committed docs/, page by page.

Why structural rather than byte comparison:

  - master's HTML is minified by hexo-all-minifier and the Hugo build by
    tdewolff, so whitespace and attribute quoting differ even when the rendered
    result is identical. tdewolff legitimately drops quotes around values with
    no spaces (`class=article-summary-inner`), which is valid HTML.
  - `generator` meta differs by design.
  - timestamps differ by design (see LIMITATIONS.md).

So both sides are parsed and reduced to a stream of (tag, sorted attributes,
collapsed text) tokens. Anything that survives that normalisation is a real
structural difference, which is what would change what a visitor sees.

Usage, from the repo root:
    python3 migration/hugo/tools/compare.py <build-dir>
"""

import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
MASTER = os.path.join(REPO, "docs")

# deviation 5 in LIMITATIONS.md: master emits /linux/ but stores docs/Linux/
EXPECTED_MOVED = [
    ("Linux/my-impression-of-ext4-wth/index.html",
     "linux/my-impression-of-ext4-wth/index.html"),
    ("Linux/rhes/install-linuxis21-rhes5/index.html",
     "linux/rhes/install-linuxis21-rhes5/index.html"),
    ("Linux/sles/linux-discovery-not-enough-entropy/index.html",
     "linux/sles/linux-discovery-not-enough-entropy/index.html"),
    ("Linux/ubuntu/nvidia-problems-in-ubuntu-810/index.html",
     "linux/ubuntu/nvidia-problems-in-ubuntu-810/index.html"),
    ("Linux/virtual-openvpn-server-at-home/index.html",
     "linux/virtual-openvpn-server-at-home/index.html"),
    ("topics/Linux/index.html", "topics/linux/index.html"),
    ("topics/Linux/rhes/index.html", "topics/linux/rhes/index.html"),
    ("topics/Linux/sles/index.html", "topics/linux/sles/index.html"),
    ("topics/Linux/ubuntu/index.html", "topics/linux/ubuntu/index.html"),
]

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
SKIP_TAGS = {"script", "style"}
WS = re.compile(r"\s+")

# The footer carries the year the site was last generated, so it legitimately
# changes between builds. master was generated in 2025.
FOOTER_YEAR = re.compile(r"^© \d{4} Samuel Tegenfeldt$")

# Accepted differences, per LIMITATIONS.md. These are normalised away so the
# comparison reports only differences a visitor could notice.
#   article:modified_time / article:published_time - master used filesystem
#     mtimes (59 distinct values); the build uses last git commit time.
#   generator - Hexo stamps its own; Hugo does not.
IGNORED_PROPS = {"article:modified_time", "article:published_time", "generator"}

# data-id on the share link is a per-post hash Hexo generated; it only names
# the transient share popup's DOM id and cannot be reproduced. Compare it as
# present-but-unknown rather than flagging every single page.
NORMALISED_ATTRS = {"data-id": ""}


class Tokener(HTMLParser):
    """Reduce HTML to a comparable token stream."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tokens = []
        self.skip_depth = 0
        self.skip_tag = None
        self.gen_next = False

    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            if tag == self.skip_tag:
                self.skip_depth += 1
            return
        if tag in SKIP_TAGS:
            self.skip_depth = 1
            self.skip_tag = tag
            return
        amap = dict((k, v) for k, v in attrs)
        # The footer credits the generator. master says Hexo; the build says
        # Hugo, which is the one deliberate content change, since claiming Hexo
        # after the switch would be untrue. Normalised here, recorded in
        # LIMITATIONS.md. Flip the footer partial if the owner prefers Hexo.
        if tag == "a" and amap.get("href") in ("//hexo.io/", "//hugo.io/"):
            self.tokens.append(("a", (("href", "<generator>"),)))
            self.gen_next = True
            return
        kept = []
        for k, v in attrs:
            if k == "generator":
                continue
            if k in ("property", "name") and v in IGNORED_PROPS:
                # drop the whole tag, not just the attribute, otherwise the
                # differing content value still shows up as a mismatch
                return
            if k in NORMALISED_ATTRS:
                v = NORMALISED_ATTRS[k]
            kept.append((k, v if v is not None else ""))
        self.tokens.append((tag, tuple(sorted(kept))))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self.skip_depth:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if not self.skip_depth:
                    self.skip_tag = None
            return
        if tag not in VOID:
            self.tokens.append(("</%s>" % tag,))

    def handle_data(self, data):
        if self.skip_depth:
            return
        text = WS.sub(" ", data).strip()
        if text:
            if FOOTER_YEAR.match(text):
                text = "© <year> Samuel Tegenfeldt"
            if self.gen_next:
                text = "<generator>"
                self.gen_next = False
            self.tokens.append(("#text", text))


def tokens(path):
    with open(path, encoding="utf-8") as fh:
        p = Tokener()
        p.feed(fh.read())
        p.close()
        return p.tokens


def listing(root):
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith("._")]
        for name in files:
            if name == "index.html":
                rel = os.path.relpath(os.path.join(base, name), root)
                out.append(rel.replace(os.sep, "/"))
    return set(out)


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, x, y
    if len(a) != len(b):
        i = min(len(a), len(b))
        return i, a[i] if i < len(a) else None, b[i] if i < len(b) else None
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    build = sys.argv[1]

    m = listing(MASTER)
    n = listing(build)

    moved_to = {new for _, new in EXPECTED_MOVED}
    moved_from = {old for old, _ in EXPECTED_MOVED}

    only_new = sorted(n - m - moved_to)
    only_master = sorted(m - n - moved_from)

    print("master pages : %d" % len(m))
    print("build pages  : %d" % len(n))
    print("expected moves: %d" % len(EXPECTED_MOVED))
    print()
    if only_new:
        print("EXTRA in build (%d):" % len(only_new))
        for p in only_new[:15]:
            print("  + " + p)
        print()
    if only_master:
        print("MISSING from build (%d):" % len(only_master))
        for p in only_master[:15]:
            print("  - " + p)
        print()
    if not only_new and not only_master:
        print("path sets match (modulo the intended Linux moves)")
        print()

    # structural comparison
    common = sorted((m & n) - moved_from)
    identical = 0
    differing = []
    for rel in common:
        ta = tokens(os.path.join(MASTER, rel))
        tb = tokens(os.path.join(build, rel))
        if ta == tb:
            identical += 1
        else:
            d = first_diff(ta, tb)
            differing.append((rel, d))

    print("structurally identical : %d / %d" % (identical, len(common)))
    print("differing              : %d" % len(differing))
    print()

    # group by the first differing token, to see whether failures share a cause
    causes = defaultdict(list)
    for rel, d in differing:
        if d is None:
            causes[("length", "")].append(rel)
        else:
            i, x, y = d
            key = (x[0] if x else "?", y[0] if y else "?")
            causes[key].append(rel)

    print("first divergence by tag:")
    for key, rels in sorted(causes.items(), key=lambda kv: -len(kv[1])):
        print("  %-28s %4d pages   e.g. %s" % (str(key), len(rels), rels[0]))
    print()

    print("sample divergences:")
    for rel, d in differing[:8]:
        print("  " + rel)
        if d:
            i, x, y = d
            print("    at token %d" % i)
            print("      master: %s" % (str(x)[:150],))
            print("      build : %s" % (str(y)[:150],))
        else:
            print("      token streams differ in length only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
