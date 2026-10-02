#!/usr/bin/env python3
"""Generate Hugo content from master's docs/ plus the Hexo sources.

Design decision: every post carries an explicit `url` in its front matter.

Hugo's own slug derivation differs from Hexo's on unicode and reserved
characters, so relying on it would silently change permalinks. Reading the
permalink Hexo actually emitted and pinning it as data removes the entire
class of risk.

Post *bodies* are copied byte-for-byte (everything after the original front
matter) so that markdown rendering is unaffected by this migration.

Category and tag pages are generated as explicit content leaves rather than
using Hugo taxonomies, because the site's category URLs are nested
(`/topics/ms/opsmgr2012/`), partly case-preserving (`/topics/Events/`), and
partly orphaned by a source-file anomaly. Taxonomies cannot express all of
that; explicit leaves can.

Run from the repo root:
    python3 migration/hugo/tools/generate_content.py
"""

import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
POSTS_SRC = os.path.join(REPO, "source", "_posts")
FINDINGS = os.path.join(REPO, "migration", "hugo", "findings")
CONTENT = os.path.join(REPO, "content")

# posts whose category pages must exist but hold no post of their own
# (produced by the inline flow-array anomaly in 20180906-*.md)


def fail(msg):
    print("FAIL: " + msg, file=sys.stderr)
    sys.exit(1)


def split_front_matter(path):
    """Return (front_matter_text, body) with the body untouched."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def yaml_scalar(value):
    """Emit a YAML scalar that round-trips safely, including unicode."""
    if value == "":
        return '""'
    # quote anything that could be misread: leading indicators, colons,
    # hashes, braces, quotes, or leading/trailing space
    needs_quote = (
        value[0] in "-?:,[]{}#&*!|>'\"%@` " or
        value[-1] == " " or
        ": " in value or " #" in value or
        value in ("true", "false", "null", "~", "yes", "no", "on", "off")
    )
    if needs_quote:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def yaml_list(items, indent=""):
    if not items:
        return "[]"
    return "\n" + "\n".join('%s- %s' % (indent, yaml_scalar(i)) for i in items)


def git_last_commit_iso(relpath):
    """Last commit date touching a path, as an ISO-8601 string."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", relpath],
            cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        out = ""
    return out or None


def front_matter_date(raw):
    """Pull the front-matter `date` value verbatim."""
    m = re.search(r"^date:\s*(\S.*?)\s*$", raw, re.M)
    return m.group(1).strip("'\"") if m else None


def main():
    tax_path = os.path.join(FINDINGS, "taxonomy.json")
    if not os.path.exists(tax_path):
        fail("findings/taxonomy.json missing - run extract_permalinks.py first")
    with open(tax_path, encoding="utf-8") as fh:
        tax = json.load(fh)
    rows = tax["posts"]
    if len(rows) != 63:
        fail("expected 63 posts in taxonomy.json, found %d" % len(rows))

    # --- clean previous run ---------------------------------------------
    # This volume regenerates AppleDouble `._*` sidecars as files appear, and
    # they race with rmtree. Remove them first, then ignore transient errors.
    if os.path.isdir(CONTENT):
        for root, dirs, files in os.walk(CONTENT):
            for f in files:
                if f.startswith("._"):
                    try:
                        os.unlink(os.path.join(root, f))
                    except OSError:
                        pass
        shutil.rmtree(CONTENT, ignore_errors=True)
    posts_dir = os.path.join(CONTENT, "posts")
    topics_dir = os.path.join(CONTENT, "topics")
    tags_dir = os.path.join(CONTENT, "tags")
    pages_dir = os.path.join(CONTENT, "pages")
    for d in (posts_dir, topics_dir, tags_dir, pages_dir):
        os.makedirs(d)

    # --- posts ------------------------------------------------------------
    written = 0
    for r in rows:
        src = os.path.join(POSTS_SRC, r["file"])
        raw, body = split_front_matter(src)

        # Hugo wants the local wall-clock time; the site timezone is set in
        # hugo.toml so this reproduces Hexo's local->UTC rendering.
        date = front_matter_date(raw)
        if not date:
            fail("no front-matter date in %s" % r["file"])

        lastmod = git_last_commit_iso(
            os.path.join("source", "_posts", r["file"]))

        chains = [c["slug"] for c in r["categories"]]
        tags = r["tags"]

        fm = []
        fm.append("---")
        fm.append("title: %s" % yaml_scalar(r["title"]))
        fm.append("date: %s" % yaml_scalar(date))
        if lastmod:
            fm.append("lastmod: %s" % yaml_scalar(lastmod))
        # Explicit permalink: the whole point of this generator.
        # `dir` (not `url`) is used because it is the path Hexo itself wrote:
        # lowercase for the Linux categories, and raw unicode for the
        # Event-Id post. The sitemap form is percent-encoded and is kept
        # separately for sitemap generation.
        fm.append("url: /%s" % yaml_scalar(r["dir"]))
        fm.append("url_encoded: %s" % yaml_scalar(r["url"]))
        fm.append("cats:%s" % yaml_list(chains, "  "))
        fm.append("tags:%s" % yaml_list(tags, "  "))
        # preserved for reference only; never used for routing
        if "id" in r["fm_keys"]:
            m = re.search(r"^id:\s*(\S+)\s*$", raw, re.M)
            if m:
                fm.append("hexo_id: %s" % m.group(1))
        if r["notes"]:
            fm.append("migration_notes: %s"
                      % yaml_scalar("; ".join(r["notes"])))
        fm.append("---")

        out = os.path.join(posts_dir, r["slug"] + ".md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fm) + "\n" + body)
        written += 1

    if written != 63:
        fail("wrote %d posts, expected 63" % written)

    # --- category pages ---------------------------------------------------
    # map chain -> name, and chain -> ordered post urls
    cat_name = {}
    cat_posts = {}
    for r in rows:
        for c in r["categories"]:
            cat_name[c["slug"]] = c["name"]
            cat_posts.setdefault(c["slug"], []).append(r)

    # declared taxonomy also includes nodes with no posts
    for c in tax["categories"]:
        slug = c["url"].replace("/topics/", "").strip("/")
        cat_name.setdefault(slug, c["name"])

    for c in tax["categories"]:
        slug = c["url"].replace("/topics/", "").strip("/")
        posts = cat_posts.get(slug, [])
        # order by date desc, matching master's listings
        posts = sorted(posts, key=lambda p: p["date_local"], reverse=True)
        parent = slug.rsplit("/", 1)[0] if "/" in slug else ""
        depth = slug.count("/") + 1
        fm = [
            "---",
            "title: %s" % yaml_scalar(cat_name.get(slug, slug)),
            "type: topic",
            "url: %s" % yaml_scalar(c["url"]),
            "cat: %s" % yaml_scalar(slug),
            "chain_depth: %d" % depth,
            "post_count: %d" % len(posts),
            "---",
            "",
        ]
        path = os.path.join(topics_dir, slug, "_index.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fm))

    # --- tag pages --------------------------------------------------------
    tag_name = {}
    tag_posts = {}
    for r in rows:
        for t in r["tags"]:
            tag_posts.setdefault(t, []).append(r)
    for t in tax["tags"]:
        tag_name[t["name"]] = t["name"]

    for t in tax["tags"]:
        url = t["url"]
        slug = url.replace("/tag/", "").strip("/")
        posts = sorted(tag_posts.get(t["name"], []),
                       key=lambda p: p["date_local"], reverse=True)
        fm = [
            "---",
            "title: %s" % yaml_scalar(t["name"]),
            "type: tagpage",
            "url: %s" % yaml_scalar(url),
            "tag: %s" % yaml_scalar(t["name"]),
            "tag_slug: %s" % yaml_scalar(slug),
            "post_count: %d" % len(posts),
            "---",
            "",
        ]
        path = os.path.join(tags_dir, slug, "_index.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fm))

    # --- standalone pages -------------------------------------------------
    about_src = os.path.join(REPO, "source", "About", "index.md")
    raw, body = split_front_matter(about_src)
    date = front_matter_date(raw) or "2025-01-17 11:34:00"
    fm = [
        "---",
        "title: About",
        "date: %s" % yaml_scalar(date),
        "lastmod: %s" % yaml_scalar(
            git_last_commit_iso(os.path.join("source", "About", "index.md"))
            or date),
        "url: /About/",
        "layout: page",
        "---",
    ]
    with open(os.path.join(pages_dir, "about.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + "\n" + body)

    print("posts    : %d" % written)
    print("topics   : %d" % len(tax["categories"]))
    print("tags     : %d" % len(tax["tags"]))
    print("pages    : 1")
    print("wrote content/{posts,topics,tags,pages}")


if __name__ == "__main__":
    main()
