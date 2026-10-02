#!/usr/bin/env python3
"""Generate Hugo content from master's docs/ plus the Hexo sources.

Design decision: every post carries an explicit `url` in its front matter.

Hugo's own slug derivation differs from Hexo's on unicode and reserved
characters, so relying on it would silently change permalinks. Reading the
permalink Hexo actually emitted and pinning it as data removes the entire
class of risk.

Post *bodies* are copied from the original source, with only migration-safe
rewrites: local image assets are changed to root-relative URLs when the file is
present in `static/`, and Hexo's excerpt marker is preserved as an anchor.

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
STATIC = os.path.join(REPO, "static")

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


def rewrite_local_image_urls(body):
    """Use local static assets when the old absolute URL is available locally."""
    pattern = re.compile(
        r"https?://(?:www\.teknoglot\.se|teknoglotse\.nfshost\.com)"
        r"(?P<path>/wp-content/uploads/[^\s\"')>]+)"
    )

    def replace(match):
        path = match.group("path")
        if os.path.isfile(os.path.join(STATIC, path.lstrip("/"))):
            return path
        return match.group(0)

    return pattern.sub(replace, body)


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
        return " []"
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

    desc_path = os.path.join(FINDINGS, "descriptions.json")
    if not os.path.exists(desc_path):
        fail("findings/descriptions.json missing - "
             "run extract_descriptions.js first")
    with open(desc_path, encoding="utf-8") as fh:
        descriptions = json.load(fh)

    exc_path = os.path.join(FINDINGS, "excerpts.json")
    if not os.path.exists(exc_path):
        fail("findings/excerpts.json missing - "
             "run extract_excerpts.js first")
    with open(exc_path, encoding="utf-8") as fh:
        excerpts = json.load(fh)

    counts_path = os.path.join(FINDINGS, "golden", "category-counts.json")
    if not os.path.exists(counts_path):
        fail("findings/golden/category-counts.json missing - "
             "run capture_golden.py first")
    with open(counts_path, encoding="utf-8") as fh:
        counts_by_url = {c["url"]: c["count"]
                         for c in json.load(fh)}

    cloud_path = os.path.join(FINDINGS, "golden", "tagcloud.json")
    if not os.path.exists(cloud_path):
        fail("findings/golden/tagcloud.json missing - "
             "run capture_golden.py first")
    with open(cloud_path, encoding="utf-8") as fh:
        tagcloud_order = {c["tag"]: i
                          for i, c in enumerate(json.load(fh))}

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
    archives_dir = os.path.join(CONTENT, "archives")
    for d in (posts_dir, topics_dir, tags_dir, pages_dir, archives_dir):
        os.makedirs(d)

    # --- posts ------------------------------------------------------------
    written = 0
    for r in rows:
        src = os.path.join(POSTS_SRC, r["file"])
        raw, body = split_front_matter(src)
        body = rewrite_local_image_urls(body)
        # Hexo's excerpt marker is also rendered as an empty anchor in the
        # article body. Hugo consumes the marker as a summary separator, so
        # preserve the visible anchor explicitly; summaries use the harvested
        # Hexo excerpts below rather than Hugo's automatic split.
        body = body.replace("<!--more-->", '\n\n<a id="more"></a>\n\n')
        # Hexo starts duplicate heading suffixes at 2, while Goldmark starts
        # them at 1. Pin the one repeated heading sequence whose anchor IDs
        # are part of the legacy public output.
        if r["file"] == "20180827-om1801-upgrade-gotchas.md":
            workaround = 0
            lines = []
            for line in body.splitlines(keepends=True):
                if line.rstrip("\r\n") == "### Workaround":
                    workaround += 1
                    if workaround > 1:
                        ending = line[len(line.rstrip("\r\n")):]
                        line = "### Workaround {#workaround-%d}%s" % (workaround, ending)
                lines.append(line)
            body = "".join(lines)

        # Hugo wants the local wall-clock time; the site timezone is set in
        # hugo.toml so this reproduces Hexo's local->UTC rendering.
        date = front_matter_date(raw)
        if not date:
            fail("no front-matter date in %s" % r["file"])

        lastmod = git_last_commit_iso(
            os.path.join("source", "_posts", r["file"]))

        desc = descriptions.get(r["dir"])
        if not desc:
            fail("no description for %s (key %r)" % (r["file"], r["dir"]))
        exc = excerpts.get(r["slug"])
        if not exc:
            fail("no excerpt for %s" % r["slug"])

        chains = [c["slug"] for c in r["categories"]]
        # One post carries an empty tag (a bare "- " in its front matter).
        # Hexo drops it everywhere: no tag page, and no entry in the keywords
        # or article:tag metas.
        tags = [t for t in r["tags"] if t and t.strip()]

        # Year and month as plain strings, for archive grouping. Derived from the
        # front-matter wall-clock date, which is what Hexo's post.date.year()
        # saw. Filtering on these avoids Hugo's Date.Year accessor, which does
        # not behave in `where` on this version.
        m = re.match(r"^(\d{4})-(\d{2})", date)
        if not m:
            fail("unparseable date %r in %s" % (date, r["file"]))
        year_s, month_s = m.group(1), m.group(2)

        fm = []
        fm.append("---")
        fm.append("title: %s" % yaml_scalar(r["title"]))
        fm.append("date: %s" % yaml_scalar(date))
        fm.append('year: "%s"' % year_s)
        fm.append('month: "%s"' % month_s)
        if lastmod:
            fm.append("lastmod: %s" % yaml_scalar(lastmod))
        # Explicit permalink: the whole point of this generator.
        # `dir` (not `url`) is used because it is the path Hexo itself wrote:
        # lowercase for the Linux categories, and raw unicode for the
        # Event-Id post. The sitemap form is percent-encoded and is kept
        # separately for sitemap generation.
        fm.append("url: /%s" % yaml_scalar(r["dir"]))
        fm.append("url_encoded: %s" % yaml_scalar(r["url"]))
        # read from master's built output; not recomputable, see
        # tools/extract_descriptions.js for why
        fm.append("description: %s" % yaml_scalar(desc))
        # Hexo keys the article element on post.slug, which comes from the
        # filename. The About page has none, so its id really is "page-".
        fm.append("hexo_slug: %s" % yaml_scalar(r["slug"]))
        # harvested from master's rendered cards; contains a non-breaking space
        # in at least one post, and is emitted unescaped as Hexo did
        fm.append("excerpt: %s" % yaml_scalar(exc["excerpt"]))
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
        # Counts are read from master's rendered sidebar rather than computed.
        # Hexo's own count disagrees with its listing for Microsoft (42 shown,
        # 41 listed) because one post sits under two ms sub-chains at once.
        # Every other node agrees with a prefix-deduplicated count.
        count = counts_by_url.get(c["url"])
        if count is None:
            fail("no sidebar count for %s" % c["url"])
        parent = slug.rsplit("/", 1)[0] if "/" in slug else ""
        depth = slug.count("/") + 1
        fm = [
            "---",
            "title: %s" % yaml_scalar(cat_name.get(slug, slug)),
            "type: topic",
            "url: %s" % yaml_scalar(c["url"]),
            "cat: %s" % yaml_scalar(slug),
            "cat_parent: %s" % yaml_scalar(parent),
            "chain_depth: %d" % depth,
            "post_count: %d" % count,
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
        # The tagcloud order is byte-wise on the tag name, which Hugo's `sort`
        # does not reproduce (it collates): it would put "Gist" before "GSM",
        # where master puts "GSM" first, since 'S' (0x53) < 'i' (0x69). The
        # order is displayed data, so it is read from master's rendered cloud
        # and pinned rather than re-derived. The fixture keys on tag slug.
        order = tagcloud_order.get(slug)
        if order is None:
            fail("tag slug %r missing from master's tagcloud order" % slug)
        fm = [
            "---",
            "title: %s" % yaml_scalar(t["name"]),
            "type: tagpage",
            "url: %s" % yaml_scalar(url),
            "tag: %s" % yaml_scalar(t["name"]),
            "tag_slug: %s" % yaml_scalar(slug),
            "post_count: %d" % len(posts),
            "cloud_order: %d" % order,
            "---",
            "",
        ]
        path = os.path.join(tags_dir, slug, "_index.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fm))

    # --- archive pages -----------------------------------------------------
    # The shape of the archive tree is read from master's output rather than
    # derived, because it is not simply "every year that has posts": the tree
    # holds a page per year and per month, and only the root is paginated.
    archives_root = os.path.join(REPO, "docs", "archives")
    archive_paths = []
    for root, dirs, files in os.walk(archives_root):
        dirs[:] = [d for d in dirs
                   if not d.startswith("._") and d != "page"]
        if "index.html" not in files:
            continue
        rel = os.path.relpath(root, archives_root).replace(os.sep, "/")
        if rel == ".":
            rel = ""
        archive_paths.append(rel)
    archive_paths.sort(key=lambda p: (p.count("/"), p))

    archive_written = 0
    for rel in archive_paths:
        url = "/archives/" + (rel + "/" if rel else "")
        fm = [
            "---",
            "title: %s" % yaml_scalar("Archive"),
            "type: archive",
            "url: %s" % yaml_scalar(url),
            "archive_path: %s" % yaml_scalar(rel),
        ]
        if rel:
            parts = rel.split("/")
            fm.append('year: "%s"' % parts[0])
            if len(parts) > 1:
                fm.append('month: "%s"' % parts[1])
                # The page title renders the month as a bare number, so
                # /archives/2007/04/ is titled "Archive: 2007/4" while the
                # directory keeps its zero padding.
                fm.append('month_num: "%s"' % str(int(parts[1])))
        fm.append("---")
        fm.append("")
        path = os.path.join(archives_dir, rel, "_index.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fm))
        archive_written += 1

    # --- standalone pages -------------------------------------------------
    about_src = os.path.join(REPO, "source", "About", "index.md")
    raw, body = split_front_matter(about_src)
    date = front_matter_date(raw) or "2025-01-17 11:34:00"
    about_desc = descriptions.get("About/")
    fm = [
        "---",
        "title: About",
        "date: %s" % yaml_scalar(date),
        "lastmod: %s" % yaml_scalar(
            git_last_commit_iso(os.path.join("source", "About", "index.md"))
            or date),
        "url: /About/",
        "layout: page",
        'hexo_slug: ""',
    ]
    if about_desc:
        fm.append("description: %s" % yaml_scalar(about_desc))
    fm.append("---")
    with open(os.path.join(pages_dir, "about.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(fm) + "\n" + body)

    print("posts    : %d" % written)
    print("topics   : %d" % len(tax["categories"]))
    print("tags     : %d" % len(tax["tags"]))
    print("archives : %d" % archive_written)
    print("pages    : 1")
    print("wrote content/{posts,topics,tags,pages}")


if __name__ == "__main__":
    main()
