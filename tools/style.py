#!/usr/bin/env python3
"""Mechanical style checks for post bodies.

STYLE.md is the authority on voice and on which rules exist. This implements the
machine-checkable subset of it. It reports and never rewrites: the author's
register, his contractions and his genuine typos are his, and an agent that
"smooths" them has done the damage this tool exists to make visible.

Every rule is expressed as a change, not as a state. The previous committed
version of a post is the baseline, so the existing corpus cannot fail a check
simply for being old, and a rewrite that removes half the author's voice shows
up as a removal rather than passing unnoticed.

    python3 tools/style.py                    check changed posts against HEAD
    python3 tools/style.py --against b52df3de check against an older revision
    python3 tools/style.py content/posts/x.md check specific files
    python3 tools/style.py --list             list rule ids and descriptions

Exits 1 if any rule finds something. Run it before committing a post.
"""

import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

POSTS = Path("content/posts")

# Front matter keys, in the order the corpus keeps them.
FRONT_ORDER = ["title", "date", "lastmod", "url", "description", "excerpt",
               "cats", "tags"]

# Languages the corpus actually fences with. Anything else is a new dependency
# on a highlighter the site may not style.
FENCE_LANGS = {"", "powershell", "text", "bash", "xml", "bat", "vbs", "cmd",
               "sql", "csharp"}

STOPWORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in",
             "into", "nor", "of", "on", "onto", "or", "over", "per", "the",
             "to", "up", "via", "with", "vs"}

CONNECTIVES = ["And", "So", "But", "Anyway", "Anyhow", "Since", "With", "As"]

HEDGE_ADDED = re.compile(
    r"\b(?:it(?:'s| is) worth noting|it should be noted|generally speaking"
    r"|typically|arguably|relatively|in most cases|it is important to note"
    r"|needless to say)\b", re.I)

HEDGE_KEPT = re.compile(
    r"\b(?:I think|I guess|I assume|I presume|probably|maybe|perhaps|seems"
    r"|not sure|I have not verified|I have not tested|sort of|kind of)\b", re.I)

FILLER = re.compile(
    r"\b(?:delve\w*|tapestry|testament\w*|underscor\w+|landscape|realm"
    r"|robust|seamless|leverage[sd]?|game-?changer|supercharge|unlock"
    r"|holistic|paradigm)\b", re.I)

BRITISH = re.compile(
    r"\b(?:colours?|coloured|favourite|behaviour\w*|organis\w*|recognis\w*"
    r"|analys\w*|centre|programme|licence|defence|favour\w*|honour\w*"
    r"|catalogue|dialogue|whilst|amongst|learnt|travelled|modelling"
    r"|cancelled|grey)\b", re.I)

# Reported separately from SPELL-001 because the fix is different: -ise/-ize is
# a house rule, whereas the rest are ordinary British spellings.
SPELL002 = re.compile(r"\b(?:utilis\w*|utiliz\w*)\b", re.I)

SWEDISH = re.compile(r"\b(?:och|för)\b")
LOWER_I = re.compile(r"(?:^|[.!?;]\s|\n)\s*i\s+[a-z]")
OXFORD = re.compile(r"\b[\w'-]+,\s+[\w'-]+,\s+(?:and|or)\s+[\w'-]+\b")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
BANNER = re.compile(r"(?:#{1,6}|---|:::|===)\s*$")
TABLE = re.compile(r"^\s*\|.*\|\s*$|^\S[^|\n]*(?:\|[^|\n]+){2,}\s*$")
FENCE = re.compile(r"^(\s*)(`{3,})\s*(\S*)")
BULLET = re.compile(r"^\s*[-*+]\s+\S", re.M)
NUMBERED = re.compile(r"^\s*\d+[.)]\s+\S", re.M)
QUOTE = re.compile(r"^\s*>", re.M)
HEADING = re.compile(r"^(#{1,6})\s+(\S.*?)\s*$")
CONTRACTION = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.I)
FIRSTPERSON = re.compile(
    r"\b(?:I|I'm|I've|I'd|I'll|me|my|mine|myself|we|our|us)\b")
PASSIVE = re.compile(r"\b(?:is|was|are|were|be|been|being)\s+\w+(?:ed|en)\b")


def strip_fences(text):
    """Remove fenced code blocks, keeping the fence lines themselves."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def prose(text):
    """Body text with fences, HTML and shortcodes removed."""
    t = strip_fences(text)
    t = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return t


def split_front(raw):
    """Return (front_matter_text, body). Handles --- fences only.

    A file whose closing fence is missing or glued to the next line yields an
    empty front matter rather than a guess, so the FRONT rules go quiet instead
    of reporting nonsense about a file that is already broken.
    """
    lines = raw.split("\n")
    if not lines or lines[0].strip() != "---":
        return "", raw
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", raw


def front_keys(front):
    return [m.group(1) for m in re.finditer(r"^([A-Za-z_][\w-]*):", front, re.M)]


def front_value(front, key):
    m = re.search(rf"^{key}:[ \t]*(.*)$", front, re.M)
    return m.group(1).strip().strip('"') if m else None


def is_title_cased(text):
    toks = [t for t in re.findall(r"[A-Za-z][\w'-]*", text)][1:]
    toks = [t for t in toks if t.lower() not in STOPWORDS]
    if len(toks) < 2:
        return False
    return sum(1 for t in toks if t[:1].isupper()) / len(toks) >= 0.8


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text))
    return [p.strip() for p in parts if len(p.strip()) > 3]


def median_words(text):
    s = sentences(text)
    if not s:
        return None
    counts = sorted(len(x.split()) for x in s)
    mid = len(counts) // 2
    return counts[mid] if len(counts) % 2 else (counts[mid - 1] + counts[mid]) / 2


def density(pattern, text):
    return len(pattern.findall(text)) / max(len(text), 1) * 10000


class Finding:
    def __init__(self, rule, path, line, message):
        self.rule, self.path, self.line, self.message = rule, path, line, message


def changed_lines(old, new):
    """1-based line numbers in `new` that are added or modified."""
    a, b = old.split("\n"), new.split("\n")
    out = set()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            continue
        for j in range(j1, j2):
            out.add(j + 1)
    return out


def fences(text):
    """(open_line_no, info_string, content_lines) for each fenced block."""
    blocks, open_at, info, buf = [], None, "", []
    for n, line in enumerate(text.split("\n"), 1):
        m = FENCE.match(line)
        if m:
            if open_at is None:
                open_at, info, buf = n, m.group(3), []
            else:
                blocks.append((open_at, info, buf))
                open_at, info, buf = None, "", []
            continue
        if open_at is not None:
            buf.append(line)
    if open_at is not None:
        blocks.append((open_at, info, buf))
    return blocks


def check(path, old_raw, new_raw, find):
    old_front, old_body = split_front(old_raw)
    new_front, new_body = split_front(new_raw)
    added = changed_lines(old_raw, new_raw)
    new_lines = new_raw.split("\n")
    pbody = prose(new_body)
    pold = prose(old_body)

    # --- line-scoped: only on lines the author or agent actually touched ---
    for n in sorted(added):
        line = new_lines[n - 1]
        if line.lstrip().startswith(("---", "#")) or not line.strip():
            continue
        for m in BRITISH.finditer(line):
            find("SPELL-001", n, f"British spelling {m.group(0)!r}; this site is American")
        for m in SPELL002.finditer(line):
            find("SPELL-002", n, f"{m.group(0)!r}; write it with -ize")
        for m in SWEDISH.finditer(line):
            find("LANG-001", n, f"Swedish word {m.group(0)!r} in an English post")
        if LOWER_I.search(line):
            find("LANG-002", n, "lowercase 'i' as a pronoun; use 'I'")
        for m in OXFORD.finditer(line):
            find("PUNCT-001", n, f"possible Oxford comma: {m.group(0)!r}")
        for m in EMOJI.finditer(line):
            find("PUNCT-002", n, f"emoji {m.group(0)!r} in the body")

    # --- headings ---
    for n, level, text in (
            (i, m.group(1), m.group(2)) for i, line in enumerate(new_lines, 1)
            for m in [HEADING.match(line)] if m):
        first_alpha = next((c for c in text if c.isalpha()), "")
        if first_alpha.islower() and not text.startswith("..."):
            find("HEAD-001", n, f"heading starts lowercase: {text!r}")
        if is_title_cased(text) and n in added:
            find("HEAD-002", n, f"Title Cased heading: {text!r}")
        if BANNER.search(text):
            find("HEAD-003", n, f"banner marker in heading: {text!r}")

    # --- title ---
    # Only when it changed. Every title in the corpus is Title-Cased to some
    # degree, so reporting an untouched one is noise, not a finding.
    title = front_value(new_front, "title")
    if title and title != front_value(old_front, "title") and is_title_cased(title):
        find("TITLE-001", 1, f"Title Cased title: {title!r}")

    # --- punctuation counts that must not drift ---
    for rule, chars, label in (
            ("PUNCT-004", "—–", "dash"),
            ("PUNCT-005", "…", "ellipsis character")):
        o = sum(pold.count(c) for c in chars)
        nw = sum(pbody.count(c) for c in chars)
        if o != nw:
            find(rule, None, f"{label} count changed {o} -> {nw}")
    if len(re.findall(r"(?<!-)--(?!-)", pold)) != len(re.findall(r"(?<!-)--(?!-)", pbody)):
        find("PUNCT-004", None, "ASCII '--' count changed")

    # --- voice ---
    for m in FILLER.finditer(pbody):
        if m.start() >= 0:
            line = next((n for n in sorted(added)
                         if m.group(0) in new_lines[n - 1]), None)
            find("VOICE-003", line, f"filler phrase {m.group(0)!r}")

    added_hedge = [h for h in HEDGE_ADDED.findall(pbody)
                   if h not in HEDGE_ADDED.findall(pold)]
    for h in set(added_hedge):
        find("HEDGE-001", None, f"hedge added: {h!r}")
    for h in set(HEDGE_KEPT.findall(pold)) - set(HEDGE_KEPT.findall(pbody)):
        find("HEDGE-002", None, f"author's hedge removed: {h!r}")

    # Density rules need a body long enough for a rate to mean anything. On a
    # two-line draft every ratio is extreme and every rule would cry wolf.
    if len(pbody) >= 400:
        fp = density(FIRSTPERSON, pbody)
        if fp < 15:
            find("VOICE-001", None,
                 f"first-person density {fp:.1f}/10k, corpus baseline is 31.6")
        pv = density(PASSIVE, pbody)
        if pv > 12:
            find("VOICE-002", None,
                 f"passive density {pv:.1f}/10k, corpus baseline is 5.2")
        if density(CONTRACTION, pbody) > 30 and \
                len(CONTRACTION.findall(pbody)) > 1.5 * max(len(CONTRACTION.findall(pold)), 1):
            find("VOICE-004", None, "contraction density more than doubled")

    if len(CONTRACTION.findall(pbody)) < len(CONTRACTION.findall(pold)):
        find("VOICE-005", None, "contractions were removed")

    for word in CONNECTIVES:
        o = len(re.findall(rf"(?:^|[.!?]\s)\s*{word}\s", pold))
        nw = len(re.findall(rf"(?:^|[.!?]\s)\s*{word}\s", pbody))
        if o and nw < o / 2:
            find("VOICE-006", None, f"sentence-initial {word!r} dropped {o} -> {nw}")

    med = median_words(pbody)
    if med is not None:
        if not 5 <= med <= 35:
            find("LEN-001", None, f"median sentence {med:.0f} words, corpus range is 5-35")
        oldmed = median_words(pold)
        # A 40% move is only meaningful with enough sentences to have a median.
        if oldmed and len(sentences(pbody)) >= 8 and abs(med - oldmed) / oldmed > 0.4:
            find("LEN-001", None, f"median sentence moved {oldmed:.0f} -> {med:.0f}")

    for para in re.split(r"\n\s*\n", pbody):
        if len(para.split()) > 300:
            find("LEN-002", None, f"paragraph of {len(para.split())} words")

    # --- structure ---
    ob = len(BULLET.findall(pold)) + len(NUMBERED.findall(pold))
    nb = len(BULLET.findall(pbody)) + len(NUMBERED.findall(pbody))
    if nb > ob:
        find("LIST-001", None, f"list items {ob} -> {nb}; prose may have become bullets")
    if any(TABLE.match(l) for l in new_body.split("\n")):
        if not any(TABLE.match(l) for l in old_body.split("\n")):
            find("LIST-002", None, "a pipe table was added; the corpus has one, in a 2017 talk")
    if len(QUOTE.findall(pbody)) != len(QUOTE.findall(pold)):
        find("LIST-003", None, "blockquote count changed")

    fb, ob_ = fences(new_body), fences(old_body)
    if len(fb) != len(ob_):
        find("FENCE-001", None, f"fence count {len(ob_)} -> {len(fb)} (unbalanced?)")
    for (n, info, _), (_, oldinfo, _) in zip(fb, ob_):
        if info.lower() not in FENCE_LANGS:
            find("FENCE-001", n, f"fence language {info!r} is not one this site uses")
        elif bool(info) != bool(oldinfo):
            find("FENCE-002", n, "fence language tag added or removed")

    # --- front matter ---
    ok, nk = front_keys(old_front), front_keys(new_front)
    if ok != nk:
        find("FRONT-001", 1, f"front matter keys changed {ok} -> {nk}")
    for key, pattern in (("date", r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"),
                          ("lastmod", r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")):
        val = front_value(new_front, key)
        if val and val != front_value(old_front, key) and not re.match(pattern, val):
            find("FRONT-002", 1,
                 f"{key} is {val!r}; the corpus writes "
                 + ("'YYYY-MM-DD HH:MM:SS'" if key == "date"
                    else "'YYYY-MM-DDTHH:MM:SS+HH:MM'"))
    url = front_value(new_front, "url")
    if url and not (url.startswith("/") and url.endswith("/")):
        find("FRONT-004", 1, f"url {url!r} must start and end with a slash")

    # --- assets and shortcodes ---
    for n in sorted(added):
        line = new_lines[n - 1]
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", line):
            if not (m.group(1).startswith("/") or m.group(1).startswith("http")):
                find("IMG-001", n, f"image target {m.group(1)!r} is not root-relative")
        for m in re.finditer(r"\{\{\s*([<%])", line):
            if m.group(1) == "%" or not re.match(r"\{\{< gist ", line):
                find("SHORTCODE-001", n, "only {{< gist >}} is available on this site")
                break


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="post files to check (default: changed posts)")
    ap.add_argument("--against", default="HEAD", help="revision to compare against")
    ap.add_argument("--list", action="store_true", help="list rule ids and exit")
    args = ap.parse_args()

    if args.list:
        for line in __doc__.splitlines():
            if line.strip().startswith(("SPELL-", "LANG-", "HEAD-", "TITLE-", "PUNCT-",
                                       "VOICE-", "HEDGE-", "LEN-", "LIST-", "FENCE-",
                                       "FRONT-", "IMG-", "SHORTCODE-")):
                print(" ", line.strip().rstrip("."))
        return 0

    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        r = subprocess.run(["git", "diff", "--name-only", args.against, "--",
                            str(POSTS)], capture_output=True, text=True)
        targets = [Path(p) for p in r.stdout.split() if p.endswith(".md")]

    if not targets:
        print(f"no changed posts against {args.against}")
        return 0

    findings = []
    for path in targets:
        if not path.exists():
            continue
        new_raw = path.read_text(encoding="utf-8")

        def find(rule, line, message, _p=path):
            findings.append(Finding(rule, _p, line, message))

        check(path, git_show(args.against, str(path)), new_raw, find)

    for f in findings:
        where = f"{f.path}:{f.line}" if f.line else str(f.path)
        print(f"  {f.rule}  {where}\n        {f.message}")

    if not findings:
        print(f"style clean: {len(targets)} post(s) against {args.against}")
        return 0

    print(f"\n{len(findings)} finding(s) in {len(targets)} post(s).")
    print("These are mechanical, not opinions. STYLE.md says which are real defects;")
    print("deliberate roughness, contractions and the author's own typos stay.")
    return 1


if __name__ == "__main__":
    sys.exit(main())