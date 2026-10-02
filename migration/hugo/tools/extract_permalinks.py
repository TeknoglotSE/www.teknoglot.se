#!/usr/bin/env python3
"""Extract the authoritative permalink + taxonomy dataset from master's docs/.

Ground truth is the committed Hexo output, not a re-derivation of Hexo's slug
rules. For every post we read the permalink Hexo actually emitted, so a Hugo
build cannot drift from it.

Emits:
  findings/permalinks.md   human-readable source of truth
  findings/taxonomy.json   machine-readable taxonomy for Hugo templates

Run from the repo root:
    python3 migration/hugo/tools/extract_permalinks.py
"""

import json
import os
import re
import sys
from collections import OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
DOCS = os.path.join(REPO, "docs")
POSTS_SRC = os.path.join(REPO, "source", "_posts")
OUT = os.path.join(REPO, "migration", "hugo", "findings")


def fail(msg):
    print("FAIL: " + msg, file=sys.stderr)
    sys.exit(1)


def load_sitemap_urls(name):
    with open(os.path.join(DOCS, name), encoding="utf-8") as fh:
        body = fh.read()
    return re.findall(r"<loc>(.*?)</loc>", body)


def parse_front_matter(path):
    """Minimal YAML front-matter reader.

    Deliberately does not interpret the YAML. We want the raw text so that
    anomalies (the `s:` typo, singular `category:`, inline flow arrays) stay
    visible instead of being normalised away.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, "", text
    raw = m.group(1)
    keys = re.findall(r"^([A-Za-z_][\w-]*):", raw, re.M)
    return {"__keys__": keys, "__raw__": raw}, raw, text[m.end():]


def list_items(raw, key):
    """Return the raw list items under `key`, preserving flow arrays."""
    m = re.search(r"^%s:\s*$" % re.escape(key), raw, re.M)
    if not m:
        return None
    tail = raw[m.end():]
    out = []
    for line in tail.split("\n"):
        im = re.match(r"^\s*-\s?(.*)$", line)
        if im:
            out.append(im.group(1).strip())
        elif line.strip() == "" or line.startswith((" ", "\t")):
            continue
        else:
            break
    return out


def main():
    cj_path = os.path.join(DOCS, "content.json")
    if not os.path.exists(cj_path):
        fail("docs/content.json missing - run the Hexo build first")
    with open(cj_path, encoding="utf-8") as fh:
        cj = json.load(fh)

    posts = cj["posts"]
    sitemap = load_sitemap_urls("post-sitemap.xml")

    # --- integrity assertions -------------------------------------------
    errors = []
    # sitemap includes the homepage as its first entry
    home = "https://www.teknoglot.se/"
    if sitemap and sitemap[0] == home:
        sitemap = sitemap[1:]
    if len(sitemap) != len(posts):
        errors.append("sitemap has %d post URLs, content.json has %d posts"
                      % (len(sitemap), len(posts)))

    sitemap_set = set(sitemap)
    permalink_set = {p["permalink"] for p in posts}
    missing_from_sitemap = sorted(permalink_set - sitemap_set)
    extra_in_sitemap = sorted(sitemap_set - permalink_set)
    if missing_from_sitemap:
        errors.append("in content.json but not sitemap: %s"
                      % missing_from_sitemap)
    if extra_in_sitemap:
        errors.append("in sitemap but not content.json: %s" % extra_in_sitemap)

    slugs = [p["slug"] for p in posts]
    if len(set(slugs)) != len(slugs):
        errors.append("duplicate slugs present")

    for p in posts:
        if not os.path.isdir(os.path.join(DOCS, p["path"].strip("/"))):
            errors.append("no directory for %s (%s)" % (p["slug"], p["path"]))

    if errors:
        for e in errors:
            print("  ! " + e, file=sys.stderr)
        fail("%d integrity problem(s); refusing to emit findings" % len(errors))

    # --- join source posts to their emitted permalinks --------------------
    by_slug = {p["slug"]: p for p in posts}
    src_files = sorted(f for f in os.listdir(POSTS_SRC)
                       if f.endswith(".md") and not f.startswith("._"))
    if len(src_files) != len(posts):
        fail("%d source files vs %d posts" % (len(src_files), len(posts)))

    rows = []
    unmatched = []
    for fn in src_files:
        stem = fn[:-3]
        # strip a leading YYYYMMDD- prefix the way Hexo's filename handling does
        slug = re.sub(r"^\d{8}-", "", stem)
        fm, raw, body = parse_front_matter(os.path.join(POSTS_SRC, fn))
        if slug not in by_slug:
            unmatched.append((fn, slug))
            continue
        emitted = by_slug[slug]
        keys = [k for k in fm.get("__keys__", [])]
        notes = []
        if "s" in keys:
            notes.append("front-matter `s:` key (typo for slug); ignored by Hexo")
        if "category" in keys and "categories" not in keys:
            notes.append("singular `category:` key")
        cats = list_items(raw, "categories") or list_items(raw, "category") or []
        flow = [c for c in cats if c.startswith("[")]
        if flow:
            notes.append("inline flow array(s): %s" % ", ".join(flow))
        rows.append({
            "file": fn,
            "slug": slug,
            "url": emitted["permalink"].replace("https://www.teknoglot.se", ""),
            "dir": emitted["path"],
            "date_local": emitted["date"],
            "title": emitted["title"],
            "categories": [{"name": c["name"], "slug": c["slug"]}
                           for c in emitted["categories"]],
            "tags": [t["name"] for t in emitted["tags"]],
            "fm_keys": keys,
            "notes": notes,
        })

    if unmatched:
        fail("source posts with no emitted permalink: %s" % unmatched)

    rows.sort(key=lambda r: r["url"].lower())
    if len(rows) != len(posts):
        fail("row count mismatch: %d vs %d" % (len(rows), len(posts)))

    # --- taxonomy ---------------------------------------------------------
    cat_permalinks = {}
    for p in posts:
        for c in p["categories"]:
            cat_permalinks.setdefault(c["permalink"], c["name"])
    for name in cj["categories"]:
        cat_permalinks.setdefault(name["permalink"], name["name"])
    for name in cj["tags"]:
        cat_permalinks.setdefault(name["permalink"], name["name"])

    topic_urls = [u for u in cat_permalinks if "/topics/" in u]
    tag_urls = [u for u in cat_permalinks if "/tag/" in u]

    # --- emit -------------------------------------------------------------
    os.makedirs(OUT, exist_ok=True)

    lines = []
    lines.append("# Permalinks (source of truth)")
    lines.append("")
    lines.append("Generated by `migration/hugo/tools/extract_permalinks.py` from")
    lines.append("master's committed `docs/`. Do not hand-edit; regenerate instead.")
    lines.append("")
    lines.append("- posts: **%d**" % len(rows))
    lines.append("- post URLs in `post-sitemap.xml`: **%d**" % len(sitemap))
    lines.append("- category pages: **%d**" % len(topic_urls))
    lines.append("- tag pages: **%d**" % len(tag_urls))
    lines.append("")
    lines.append("Integrity checks passed: every content.json permalink appears in the")
    lines.append("sitemap, slugs are unique, and every path has a directory on disk.")
    lines.append("")
    lines.append("`date_local` is UTC as emitted by Hexo (the visible local date and the")
    lines.append("`datetime` attribute are derived separately in the templates).")
    lines.append("")

    lines.append("## Posts")
    lines.append("")
    lines.append("| # | URL | slug | date (UTC) | categories | notes |")
    lines.append("|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        cats = " > ".join(c["slug"] for c in r["categories"])
        notes = "; ".join(r["notes"])
        lines.append("| %d | `%s` | `%s` | %s | %s | %s |" % (
            i, r["url"], r["slug"], r["date_local"], cats, notes))
    lines.append("")

    lines.append("## Category pages")
    lines.append("")
    for u in sorted(topic_urls, key=str.lower):
        lines.append("- `%s` -> %s" % (u.replace("https://www.teknoglot.se", ""),
                                        cat_permalinks[u]))
    lines.append("")

    lines.append("## Tag pages")
    lines.append("")
    lines.append("%d total." % len(tag_urls))
    lines.append("")
    for u in sorted(tag_urls, key=str.lower):
        lines.append("- `%s` -> %s" % (u.replace("https://www.teknoglot.se", ""),
                                        cat_permalinks[u]))
    lines.append("")

    with open(os.path.join(OUT, "permalinks.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    taxonomy = {
        "generated_from": "docs/content.json + docs/post-sitemap.xml",
        "posts": rows,
        "categories": [{"url": u.replace("https://www.teknoglot.se", ""),
                        "name": cat_permalinks[u]}
                       for u in sorted(topic_urls, key=str.lower)],
        "tags": [{"url": u.replace("https://www.teknoglot.se", ""),
                  "name": cat_permalinks[u]}
                 for u in sorted(tag_urls, key=str.lower)],
    }
    with open(os.path.join(OUT, "taxonomy.json"), "w", encoding="utf-8") as fh:
        json.dump(taxonomy, fh, indent=1, ensure_ascii=False)

    print("posts      : %d" % len(rows))
    print("categories : %d" % len(topic_urls))
    print("tags       : %d" % len(tag_urls))
    print("wrote findings/permalinks.md, findings/taxonomy.json")


if __name__ == "__main__":
    main()
