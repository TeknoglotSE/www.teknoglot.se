# STYLE.md — voice and rules for teknoglot.se

## Who this is for and how to use it

This file is for an AI agent that is either drafting a new post for
`content/posts/` or proofreading an existing one before it goes out. The site
belongs to one person, and his voice is the product: a Swedish systems
engineer writing field notes to himself at the end of a long day. The
instructions below exist to stop an agent from "improving" that voice into
something generic. Every number here was measured from the 63 published posts,
so you can re-run the check yourself rather than trusting me. Where a rule
exists, follow it; where this file is silent, do less, not more.

## The voice, with evidence

**Register: first person, present tense, unhedged opinion.** Measured over
~190,000 characters of post body (front matter excluded): first-person
pronouns at **31.6 per 10k chars** (`I/me/my/we/our`), second-person at
**23.0 per 10k**, and true passive (`is|was|are|were + -ed|-en`) at only
**5.2 per 10k**. He writes *at* the reader and *about* himself in the same
breath. Sentences beginning with `And` (36), `So` (17), `But` (15), `As` (20),
`Since` (8), `With` (6) — i.e. conjunctive fragments as standalone sentences —
are a signature, not a defect.

**Sentence length varies enormously, and that variance *is* the voice.** Whole
corpus, code fences and HTML stripped: 1,360 sentences, median **15 words**,
mean 17.0, p90 33; 21% are ≤6 words, 16% ≥30 words. Per-post medians run from
**5** (`esent-error-when-modifying-opsmgr-agent.md`) and 6
(`MSIgnite-2017-KEY01-Vision-Keynote.md`, `lets-split.md`) to **35**
(`snmp-get-errors-in-eventlog.md`) and 28 (`networkadaptercheck-fails-on-win2k.md`).
The short end is conference notes and punchline-driven rants; the long end is
troubleshooting write-ups where a single logical step takes a paragraph. Do not
normalise this. Do not compute a corpus median and "fix" an outlier toward it.

**Paragraph length, same spread.** 531 prose paragraphs: median 26 words,
mean 36.7, p90 85, max 284. 26% are ≤12 words — often a single sentence on its
own line, e.g. `Soooo… have fun!` in
`load-balanced-scom2012-sdk-services-for-network-illiterates-opsmgr-nlb.md`,
or `This means screenshots. Lots of screenshots.` in
`Resize-all-images-in-a-Word-document-with-vbs-macro.md`. 18% are ≥60 words.
Both are normal. 23% of prose blocks contain internal single newlines
(hard-wrapped mid-paragraph); `hardWraps = true` is set in `hugo.toml` because
roughly half the corpus relies on it.

**Contractions are load-bearing.** 13.1 per 10k chars, present in 55 of 63
posts. Commonest: `it's` 38, `here's` 27, `don't` 25, `I've` 22, `that's` 17,
`I'm` 10. There is not one `wouldn't` or `couldn't` in the corpus — he reaches
for the plain form and lets the sentence carry it.

**Punctuation habits** (per 10k chars, prose only): colon 33.4, parentheses
20.4, `?` 5.3, `!` 6.6, semicolon 4.2, `...` 2.2. He uses the colon as his
main structural mark, not the semicolon, and he uses the semicolon where a
comma would go: `And remember; with great powers come great responsibility.`
Dashes: only 8 real em dashes (U+2014) and 7 en dashes in the whole corpus, but
**30 ASCII `--` pairs in prose**, which is how he actually writes a dash —
`as well--maybe "hack" would be a better name for it--`. Never convert one to
the other.

**Apostrophes and quotes are mixed on purpose.** Prose has 245 straight `'`
against 59 curly `’`, and 532 straight `"` against 66 curly quotes. Both styles
coexist within single posts. Do not normalise.

**No emoji in the body.** Zero emoji in any post body. The nine emoji in the
corpus (`😉` ×6, `😛` ×2, `😄` ×1) are all inside front-matter `description` /
`excerpt` strings inherited from WordPress. In the body he uses ASCII: `;)` ×8,
`:D` ×1, `:P` ×2.

**No Oxford comma.** ~60 three-item lists read `a, b and c`; 4 read
`a, b, and c`, and two of those are not serial lists at all. Evidence:
`letting Management Servers, Reporting Servers and Web Console servers`
(`Upgrading-OpsMgr-1801-to-1807-Fieldnotes.md`).

**American spelling, decisively.** Body counts: `while` 24, `center` 5,
`program` 5, `catalog` 3, `license` 2, `dialog` 2, `behavior` 0. Zero
occurrences of `whilst`, `amongst`, `learnt`, `travelled`, `modelling`,
`cancelled`, `centre`, `programme`, `licence`. The handful of strays
(`favourite` ×2, `behaviour` ×1, `colour` ×1, `organisation` ×1, `grey` ×1)
are import artifacts, not intent.

**Structure is sparse and functional.** 29 of 63 posts have **no headings at
all** — they open with prose. Where headings exist: 197 across 34 posts (56 `#`,
61 `##`, 72 `###`, 2 `####`, 6 `#####`); 187 of 189 `#`/`##`/`###` start with
a capital letter (the two exceptions are `# ...and why you should not use it`
and `## references:`). Casing within headings is *not* uniform: 95 are
sentence case, 72 Title Case, 30 mixed. Sentence case is the dominant default,
not a law. Recurring exact headings: `Background` (4),
`Installation` (3), and `TLDR`, `The Script`, `Links`, `Workaround`,
`Quick Details`, `The Copy/Paste Part`, `Preparation`, `Issues - So Far`,
`Planning`, `Summary`, `Comments` (2 each). Lists are rarer than paragraphs:
bullets in 18 posts, numbered lists in 9, blockquotes in 19, images in 8, bold
in 9, italics in 24. Exactly one markdown pipe table exists
(`MSIgnite-2017-BRK1039-Windows-Server-Software-Defined.md`) plus two raw HTML
`<table>` blocks. Eleven posts still carry the WordPress `<a id="more"></a>`
"read more" anchor; two use the Hugo `{{< gist >}}` shortcode.

**Code fences: 141 total, 70 tagged, 71 untagged (exactly half).** Languages
actually used: `powershell` 26, `text` 20, `bash` 8, `xml` 6, `bat` 3,
`vbs` 3, `cmd` 2, `sql` 1, `csharp` 1. Do not go back and tag the untagged
ones; do not feel obliged to tag new ones either.

**Lexical tics, all measured in prose:** `simple` 37, `easy` 24,
`pretty much` 18, `straight-forward` 5, `breeze` 3, `no biggie` 2. `delve`
appears exactly **once** in 63 posts, and that once inside a disclaimer that
says he is *not* going to do it
(`Note: We are not going to delve into the Cluster Operation Mode in this
guide`). Other recurring moves: `As you may notice` (3), `Anyway` (17 across
cases), `Soooo` (1), `Aaaanyway.` (1), `O_o` (1), `GLHF!` (4), `straight-forward`
(5), `wrestled` (2), `fiddl*` (5), `work-around` (6).

**How he hedges.** Sparse and load-bearing, never piled on: `I think` 6,
`I guess` 4, `seems` 15, `probably` 19, `maybe` 9, `perhaps` 7 — against
declarative absolutes like `You absolutely _must_ wait for it to complete`
(`opsmgr-2012-r2-ur4-field-notes.md`). The distinctive form is a flat admission
of not knowing, kept in the author's voice:

- `I have not verified this, but I am not sure if Alert Suppression is
  actually parsing the parameters as well.` (`parameter-replacement-in-alertname.md`)
- `I am not really sure, but after a quite a bit of troubleshooting I am pretty
  sure it all boils down to a malformed WMI-query.`
  (`networkadaptercheck-fails-on-win2k.md`)
- `If this is still true on SQL Express 2008, I don't know and I haven't found
  any information about it (yet).` (`whynotusesqlexpress-itsforfree.md`)
- `Not entirely sure what gives?` (`Upgrading-OpsMgr-1801-to-1807-Fieldnotes.md`)
- `I have serious doubts about it being a supported feature.`

**How he opens.** Usually one or two sentences of concrete first-person
context, in medias res, before any structure: `Was troubleshooting this little
error message for a customer after deploying the SQL Server Management Pack
version 6.6.4.0.` / `Ok, so I reinstalled my linux partition with Ubuntu 9.04
x64 and decided to try EXT4 on the root partition. Like, yesterday.` / `Here's
a little something-something for the wicked.` He opens field notes with an
italic strapline: `_Quick and unrefined notes on Update Roll-up 4 for System
Center 2012 R2 - Operations Manager_`. Event notes open with `# <session code>
- <session title>` then a date/time line then an honesty notice.

**How he closes.** One short line, often a stock sign-off, half the time with
an exclamation mark and never with a summary of what the reader just learned.
`GLHF!` (4 posts), `Enjoy!` (4), `Have fun`, `Best of luck!`, `Good luck!`,
`Cheers! Oh, and happy holidays!`, `Have a nice day!`, `Ah, well. Thanks for
your time.`, `Ugh!`, `¯\_(ツ)_/¯`, `*Sheesh! This post got out of hand!*`.

**How he introduces code.** One sentence of setup in the imperative, then the
fence, then a sentence of what you should see. The recurring frame is
`...looks like this` / `should return something like this` / `Like this.`
Commands in `bash` fences carry `# ` comments that restate the step
(`# mkdir /mnt/ISO`, `# yum install adjtimex`). Error text is pasted verbatim
into a `text` fence, unedited — including the vendor's own typos:
`ESENT Kerys are required to install this application`
(`esent-error-when-modifying-opsmgr-agent.md`) and
`Error occured during CPU Usage for SQL Instances data source executing.`
(`Event-Id-4001-...-for-OpsMgr2012.md`).

**Front matter is uniform.** All 63 posts carry exactly these eight keys, in
this order: `title`, `date`, `lastmod`, `url`, `description`, `excerpt`, `cats`,
`tags`. No `draft:` and no `type:` survive in published posts. `date` is always
bare `YYYY-MM-DD HH:MM:SS` with no quotes. Titles are sentence case (57 of 63)
rather than Title Case; 15 titles carry inline `#hashtags` (`#opsmgr` 10×,
`#powershell` 5×, `#MSIgnite` 4×), sometimes mid-title
(`Event Id 4001 – "Cannot Add Type" in [#SQL] MP 6.6.4.0 for [#OpsMgr2012]`).

**Technical-term capitalisation is loose and must stay loose.** `powershell`
lowercase 53, `Powershell` 7, `PowerShell` 1, `PoSH` 1. `OpsMgr` 27,
`opsmgr` 17, `Operations Manager` 77. Hyphenation is likewise inconsistent on
purpose: `fail-over` 19 / `failover` 16, `IP-address` 17 / `IP-Address` 2,
`SNMP GET` 4 (uppercase, as if a product name), `management pack` 37 /
`Management Pack` 39 / `MP` 36.

## Non-negotiable mechanical rules

1. **American spelling.** No `behaviour`, `colour`, `favourite`, `organise`,
   `centre`, `programme`, `licence`, `whilst`, `amongst`, `learnt`. If British
   forms are already in the text you are editing, leave them and say so in your
   report — they are almost certainly import artifacts, and un-importing them
   is also a change to the author's text.
2. **Headings: capitalise the first word and proper nouns only.** Do not
   Title-Case new headings. `Create a dashboard` and `Add a widget` are correct;
   `Create A Dashboard` and `Add A Widget` are not. Note that 72 of the 189
   published `#`–`###` headings *are* Title Case, so this is a rule for what
   you write, not licence to re-case the author's. Do not add or remove the
   `#` level of an existing heading.
3. **Never Title-Case a front-matter `title`.** Sentence case.
4. **Keep contractions exactly as they are.** Do not expand `it's` to `it is`,
   `don't` to `do not`, `I've` to `I have`. Do not *add* contractions to text
   that lacks them either.
5. **Do not add an Oxford comma, and do not remove one that is already there.**
   Both directions are edits.
6. **Do not convert prose to bullet lists**, in either direction. Paragraphs
   stay paragraphs. If the author's text is a paragraph, it stays a paragraph
   even when it would obviously "read better" as four bullets.
7. **Do not add hedging.** No new `it is worth noting`, `it should be noted`,
   `generally`, `typically`, `arguably`, `somewhat`, `relatively`, `in most
   cases`. Do not delete hedging that is there.
8. **Do not register-shift.** Never rewrite casual into corporate, and never
   rewrite corporate into casual. `Pagerank, baby!` and `Why the export PATH
   command?` are the author's register. A polished rewrite of either is a
   violation.
9. **Do not fix the author's typos** (§ *Deliberate casualness vs genuine
   errors* below).
10. **Do not change opinions, conclusions, severity assessments, or the order of
    steps**, even when you believe a different order is better.
11. **Do not unify punctuation**: not apostrophes, not quotes, not `--` versus
    `—`, not `...` versus `…`.
12. **Do not introduce emoji into the body.** ASCII `;)`, `:D`, `:P` only.
13. **Do not retro-tag existing code fences**, and do not add a language tag to
    a new fence out of anxiety — half the corpus is untagged.
14. **Do not rewrite quoted material.** Error output, vendor text, forum quotes
    and `get-help` output stay byte-for-byte as pasted, typos included. If you
    are reproducing a source, paste it again and diff it.
15. **Do not run the site build or touch `docs/` or git.** Editing content only.

## Genre skeletons

The repo ships one archetype per genre in `archetypes/`. Use those as the
scaffold; the sequences below are what the published posts actually do, and
they override the archetype where the two disagree. Typical length is the
published range.

### Field notes — `archetypes/fieldnotes.md`
For: work you just did and want findable next time (update roll-ups, upgrades,
discovery sweeps). **1,100–6,000 chars.** Not a manual, not a how-to.

The two roll-up notes are the purest form: an italic strapline
(`_Quick and unrefined notes on Update Roll-up 4 for System Center 2012 R2 -
Operations Manager_`), then `## Preparation` → `## Issues - So Far` → `## Planning`
→ `## Installation` → `## Summary`, with one `###` per server role under
`Installation` (`### Management Servers`, `### SQL-Scripts`, `### Management
Packs`, `### Console`, `### Gateway`, `### Web Console`, `### Agents`) and the
update order as a bullet list. It closes `GLHF!`. The 1801→1807 note uses the
newer shape instead: a fenced `text` disclaimer (`My Fieldnotes are quick,
unrefined notations and reflections from the field.`), `## Abstract`, `## Links`
(a bullet list of KB / download / announcement blog), `## Notes` with `###` per
step, `## Afterthoughts`. `om1801-upgrade-gotchas.md` is the same instinct with
a rant's voice: `## <one issue>` then `### Workaround` per issue.

### Script guide — `archetypes/scriptguide.md`
For: a script you wrote that works, written down so future you can find it.
**1,400–11,000 chars.**

Progressive disclosure: one fence per step with a sentence of what to expect,
then the whole thing again in one fence. Real sequences:
`### Inputs` → `### Connect to Your Management Group` → `### Rally Your Agents
(and Management Servers)` → `### Do Stuff` → `### The Copy/Paste Part` →
`### Done!` (`opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell.md`);
`### The cmdlet` → `#### The One-Liners!` → `##### Set Primary Management
Server on Agent` → `#### A few reflections` → `### Related Snippets`
(`opsmgr-2012-agent-gateway-failover-the-basics.md`); `# Disclaimer!` → `# The
Script` → `## The Copy/Paste part` (`quick-hack-send-sms-through-powershell-powershell.md`);
`# Background` → `# Attribution` → `# How you do it` → `# The Copy-Paste part`
(`cloudflare-dynamic-dns-mikrotik.md`). Two posts carry a
`{{< gist ... >}}` shortcode instead of an inline body; that is fine. Blockquoted
`Note:` boxes carry the gotchas. Closes `Enjoy!` or `GLHF!`.

### Troubleshooting — `archetypes/troubleshooting.md`
For: one error, its cause, its cure. **2,000–9,600 chars.**

`# Problem` → `# Symptoms` → `# Probable Cause` → `# Comments`
(`networkadaptercheck-fails-on-win2k.md`); `# Error Description` → `# Workaround`
with `## 1.` … `## 5.` numbered steps, each a `text` fence plus a sentence
(`linux-discovery-not-enough-entropy.md`); `# A wild work-around appears!` as a
single-section post (`Event-Id-4001-...`); no headings at all, just a numbered
list of five steps (`esent-error-when-modifying-opsmgr-agent.md`). The longer
argumentative version runs `# ...and why you should not use it` → `## A
Disclaimer` → `## The Good News` → `## How To Do It` → `## The Downside` →
`## The Conclusion`
(`parameter-replacement-in-alertname.md`). The probability word is *probable*:
`# Probable Cause`, not `# Root Cause`. Ends with what made it go away.

### Event notes — `archetypes/eventnotes.md`
For: a session you sat in, written between sessions. **3,400–5,100 chars.**

Always: `# <SESSION CODE> - <Session Title>`, then a bare date/time line
(`Sep 25, 9:00 am – 10:00 am`), then an honesty notice in a blockquote
(`> UNSTRUCTURED NOTES! Also, mixed Swedish and English, sorry for that. Will
update at a later time`; and `>UNSTRUCTURED NOTES AWARENESS NOTICE!` on its own
line, `Also written on phone, will come back and refine` on the next). Then one
heading per topic (`## Office`,
`## Excel`, `## Teamwork`, `## OneDrive`, `## Other notes`), `###` where a topic
has parts, bullets under each, and the sentences are fragments
(`deleting stuff with pen, highlights etc`). The 1807 drafts add `## Personal
Reflections` or `## Quick Notes` at the end — the personal-ranting part is the
reason anyone reads them. Session tagline goes in backticks on its own line.
Tag `MSIgnite` and `Presentation Notes`; the category chain is
`Events` / `Events/MSIgnite-2017`.

### Release notes — `archetypes/releasenotes.md`
For: a management pack shipped, and whether to import it today.
**1,500–5,700 chars.** Usually no headings at all.

Lead sentence stating what and when (`Microsoft has released an update to the
MSMQ (version 3) management pack.`), then a `text` fence or blockquote holding
the vendor's own Quick Details (`Version:` / `Released on:` / `Language:`
verbatim), then the change list quoted from the release notes in a blockquote,
then his own take in one or two sentences (`Emphasis by me.`,
`Perfect timing, I must say, since I really need this today. :D`,
`Cheers! Oh, and happy holidays!`). Where headings exist: `# Quick Details`
and `# Release History` (`msmq-3-mp-for-opsmgr-v6065870-released.md`) or
`### Message Queuing 4.0 Management Pack for Operations Manager 2007` per
pack, each followed by `> **Quick Details**` (`msmq-4-and-msmq-5-...md`). An
inserted correction is `***Update:***` or `**UPDATE!**`, not a rewrite.

### How-to — `archetypes/howto.md`
For: a procedure from nothing to done, in order, for somebody else to follow.
**1,800–11,000 chars.**

Open with one sentence naming what you are installing and why, then
`# Preparations` → `# Installation` → `# Verification` → `# Configuration` →
`# Additional Comments` (`install-linuxis21-rhes5.md`); or the discursive form
`# Prelude` → `# Prerequisites` → `# Create a New Cluster` →
`## Post-Configuration` → `# Adding Hosts to the Cluster` →
`# Final Verification` → `# Postlude`
(`load-balanced-scom2012-sdk-services-for-network-illiterates-opsmgr-nlb.md`).
`# Verification` exists because people scroll to it — always give the expected
output in a `text` fence. Instructions are bare imperatives in a numbered or
`bat`/```text` fence showing a realistic prompt. Explain each command's *why*
in the sentence after it (`Why the export PATH command?`). Ends `Good luck!`.

### Rant — `archetypes/rant.md`
For: you are annoyed, you say so in the first person, that is the whole post.
**1,400–5,500 chars.** Short ones are the good ones; do not pad.

`# Background` → `## Reason #1 - <the thing>` numbered to five, no particular
order, then a closing paragraph that lets him off the hook (`Ah, well. Thanks
for your time.`) — `rant-the-concept-of-booth-babes.md`. The compressed version
has no headings at all, just five parallel short paragraphs stepping through a
sequence (`First reboot gave me a "let's FSCK!".` / `Second reboot gave me a
"let's FSCK!".` …) ending on the punchline — `my-impression-of-ext4-wth.md`.
Blunt is allowed to be blunt: `Yeah, I know, this is stupid.`,
`Your Management Server is **no longer a Management Server**!`. No code fences.

## Deliberate casualness vs genuine errors

Both are the author's text. Neither is yours to fix. This section exists because
the two look alike and the wrong call destroys the post.

**Genuine mistakes, verified in the files.** `I dont need that right now` and
`in it's current form` (`Resize-all-images-in-a-Word-document-with-vbs-macro.md`);
`a whole slew of feautures` (`in-transit-again.md`); `take not of known issues`
(`opsmgr-2012-r2-ur4-field-notes.md`); `I general, the updates goes smooth`,
`Alhough,`, `dissapointed` (`Upgrading-OpsMgr-1801-to-1807-Fieldnotes.md`);
`Prerequisute`, `When the upgrade failes`, `Unfortunatly`
(`om1801-upgrade-gotchas.md`); `Aftr the reboot`, `allready`, `done som
spring-cleaning`, `insert-shorter-word-for-buttocks`
(`install-linuxis21-rhes5.md`); `a bit och research`
(`tcp-port-check-use-with-caution.md`); `Stese steps`,
`Check you current entropy`
(`linux-discovery-not-enough-entropy.md`); `requires med to connect`,
`VB6 och .Net i cannot`, `has release a nifty`
(`w3socket-in-vbscript.md`); `I implore to to read the code`,
`the FQDN of you Root Management Server`
(`bulk-disable-acs-forwarders-with-wildcards.md`); `this information in also
available on` (`networkadaptercheck-fails-on-win2k.md`); `crasches`,
`hickups`, `abrevations`, `I think i want those back`
(`intel-drivers-causes-old-school-freezes-on-windows-vista.md`); `alot` in two
posts; lowercase pronoun `i` in 12 places across 11 posts; and
two broken numbered lists (a duplicated `### 2.` in
`whynotusesqlexpress-itsforfree.md`, and `1, 3, 4, 5, 6, 7, 7, 8, 9, 10` in
`regain-sysadmin-access-to-sql2005-or-sql2008.md`).

Swedish leakage is in the same category and equally preserved: `och` in two
posts, `för` in two, and the mixed Swedish/English that the keynote note
apologises for in its own first blockquote.

**Intentional informality, and why you cannot tell them apart by polish level.**
`Ok, so ...` / `Soooo… have fun!` / `Aaaanyway.` / `Christ!` / `O_o` /
`Ugh!` / `(yaaaay)` / `Pagerank, baby!` / `Yes, thats right.` /
`insert-shorter-word-for-buttocks` / `giggling frantically in a corner at your
feeble attempts` / `quite frankly I prefer to have my systems monitored yet
slightly less secure than not monitored at all` / `the wicked`. The dialect is
also deliberate and consistent: Nordic third-person singular on verbs (`the
setup think it does`, `it actually do try`, `have simply been removed by
Microsoft without any form of redirection`, `The drivers will also give you a
couple of SCSI-devices`, `I usually takes`, `How do you know that the driver are
installed?`). This is a Swedish speaker's English and it is consistent across 63
posts and 13 years. It is not a set of unrelated slips.

**How to tell a genuine mistake from intentional informality.** Ask three
questions, in order, and stop at the first "yes":

1. **Is it inside quoted material, a URL, a filename, a tag, a `cats`/`tags`
   value, or a front-matter string?** Then leave it. `Error occured during CPU
   Usage for SQL Instances data source executing.` is the vendor's string.
   `ESENT Kerys are required to install this application` is a literal
   screenshot of a dialog. `GS01 - Microsoft for the Modern Data Estate` is the
   session's registered title.
2. **Would changing it move the voice?** Elongation, `Ok, so`, `Anyway`,
   `quite frankly`, `Yes, thats right`, emoticons, `GLHF`, the
   `Me and my apprentice is` agreement, `First reboot gave me a "let's FSCK!"`
   — leave. These are load-bearing.
3. **Is it a plain orthographic slip inside the author's own sentence, in
   Swedish-influenced dialect, or in a list/bullet/filename?** Leave it, and
   report it. This is the `feautures` / `Aftr` / `alot` / `som spring-cleaning`
   category.

In short: there is no category here that you may silently repair. If the author
asks for a typo sweep, then fix them, one file at a time, and show the diff.

**Forbidden edits, verbatim.**

| Published (keep) | Forbidden rewrite |
| --- | --- |
| `...and people has been asking about how far off the article is.` | `...and people have been asking...` |
| `I do not like to monitor things to cannot have health.` | `...to not have health.` |
| `this is not only errors that will abort the installation` | `...are not only errors...` |
| `there's three “do you need”-questions  and there are highly optional.` | `There are three ... and they are highly optional.` |
| `you probes may very well be using SNMP v2c instead` | `your probes may ...` |
| `Just make sure that the assigned RunAs account have read/write/delete rights` | `...account has read/write/delete rights` |
| `you haves to specify which SNMP version to use` | `you have to specify ...` |
| `they might actually be able to help you all the way is you ask nicely` | `...all the way if you ask nicely` |
| `Here's my list of the issues I've seen and wrestled so far.` | `Here is a list of the issues I have encountered.` |
| `Fairly simple update, the SQL Scripts can catch your off-guard` | `A fairly painless update` / `the SQL scripts can surprise you` |
| `Note: We are not going to delve into the Cluster Operation Mode in this guide` | `Note: we do not discuss the Cluster Operation Mode in this guide` |
| `Yes, thats right. Your Management Server is **no longer a Management Server**!` | `In other words, the role has been removed from your server.` |
| paragraph: `Me and my apprentice is currently decommissioning an entire Management Group` | bullet list, one clause per bullet, `Me and my apprentice are currently...` |
| `First reboot gave me a "let's FSCK!".` / `Second reboot gave me a "let's FSCK!".` | merged into one sentence, or bulleted with the ordinals removed |
| `I have not verified this, but I am not sure if Alert Suppression is actually parsing the parameters as well.` | `Alert Suppression may not parse the parameters; this has not been verified.` |
| `I was wondering if perhaps it might be worth...` (added hedge) | — hedges are never *added* |
| `Updated: MP for System Center Configurations Manager 2007 SP2 on x64` | `How to Fix a Failing Out-of-Band Monitor` |

## Proofreading checklist

Run this in order. Stop and report rather than guess.

1. **Diff scope.** Confirm only the intended file changed. Confirm no build was
   run and `docs/` and git state are untouched.
2. **Front matter.** Exactly eight keys in the canonical order: `title`,
   `date`, `lastmod`, `url`, `description`, `excerpt`, `cats`, `tags`. `date`
   bare, no quotes, in the past (a future date silently removes the post from
   the build). `url` consistent with the file path and the `cats` chain. `cats`
   and `tags` values match leaves under `content/topics/` and `content/tags/`.
3. **Title.** Sentence case, not Title Case. Any `#hashtags` preserved exactly.
4. **Headings.** First letter capitalised (except the two known ellipsis/colon
   cases). No content word capitalised for style. Heading levels unchanged from
   the source. No heading invented to fill a gap, none deleted to "tighten".
5. **Spelling.** American throughout. List any British form found in a pre-
   existing line rather than changing it.
6. **Dialect left intact.** Verb agreement, `is/have/do` after Swedish
   subjects, lowercase `i`, Swedish words (`och`, `för`) — all untouched.
7. **Contractions.** Same count as the input, same forms. No expansions.
8. **Comma policy.** No Oxford comma added; none removed; `a, b and c` order
   and wording unchanged.
9. **Punctuation inventory.** Colons, semicolons, `--`, `...`, parentheses and
   `?`/`!` counts match the input. Apostrophe and quote style unchanged
   (straight and curly both allowed, per file as found).
10. **No emoji in the body.** ASCII `;)`, `:D`, `:P` only.
11. **Sentence-length shape.** The post's own median should sit in the 6–35
    band; short and long paragraphs both present is normal. No two adjacent
    sentences fused into one; no fragment promoted to a full sentence.
12. **Hedging diff.** The set of hedge words (`I think`, `I guess`, `seems`,
    `probably`, `maybe`, `perhaps`, `not sure`, `I have not verified`,
    `I have not tested`, `I assume`) is unchanged or smaller. Never larger.
13. **Register.** Reread for corporate drift: `leverage`, `delve`, `robust`,
    `seamless`, `landscape`, `realm`, `utilize`, `a comprehensive guide`,
    `it's important to note`, `in today's fast-paced`. Zero tolerance. `delve`
    belongs to no post in this corpus.
14. **Lists and tables.** Bullet count and numbered-list count match the input.
    No pipe tables added. No prose converted to bullets.
15. **Fences.** Opening and closing counts match. Tagged and untagged counts
    each match the input. `text` used for pasted error output; do not add
    language tags to previously untagged fences.
16. **Quoted material.** Re-paste every blockquote and fence that contains
    external text and diff it byte-for-byte. Vendor typos survive.
17. **Code untouched.** No comment reformatting, no whitespace normalization,
    no "fixing" of `# ` banners or `###` section markers inside fences.
18. **Images.** Only `/wp-content/uploads/...` root-relative paths, alt text
    present, no new images invented.
19. **Closing line.** Present, short, in his register. Do not add a summary,
    a call to action, a "conclusion" paragraph, or a question to the reader.
20. **Typos.** Enumerate every suspected genuine error with file, line and
    quoted context in your report. Change none of them.
21. **Opinions.** Every verdict, risk assessment, ordering and recommendation
    is byte-identical to the input. If you disagree, say so in the report.

## What an agent must never do

1. **De-contract.** `it's` → `it is`, `don't` → `do not`, `I've` → `I have`,
   `here's` → `here is`. Also never add contractions where there were none.
2. **Title-Case headings or titles.** `Add A Widget`, `The Conclusion`, and a
   capitalised `The` in a front-matter title are all failures.
3. **Convert paragraphs into bullet lists**, or merge bullets back into
   paragraphs. The `First reboot / Second reboot / Third boot` sequence in
   `my-impression-of-ext4-wth.md` is prose and must stay prose.
4. **Add filler or lift register.** `delve into`, `tapestry`, `testament to`,
   `underscores`, `navigate the complexities`, `a journey`, `game-changer`,
   `unlock`, `supercharge`. His actual words are `pretty much`, `straight-forward`,
   `a breeze`, `no biggie`, `it's not half-bad`.
5. **Smooth rough edges.** Do not tidy the semicolon in `And remember; with
   great powers come great responsibility`, the double space, the run-on, the
   284-word paragraph in `linux-discovery-not-enough-entropy.md`, the triple
   `!!!!!` in `MAKE SURE YOUR BACKUPS ARE WORKING!!!`, or the `¯\_(ツ)_/¯`.
6. **Tidy punctuation habits.** Do not unify `--` to an em dash, `...` to `…`,
   straight quotes to curly, or the file's apostrophe style. Do not replace his
   semicolons with commas or vice versa.
7. **Fix typos, Swedish leakage, or Nordic verb agreement.** Report, do not
   repair.
8. **Change an opinion, a step order, a severity call, or a recommendation.**
   `You absolutely _must_ wait for it to complete` stays exactly that.
9. **Fix quoted vendor output**, including `occured`, `Kerys`, and the double
   `displaylang=en` in a download URL.
10. **Re-tag existing code fences** or add language tags reflexively.
11. **Add an Oxford comma**, or remove one.
12. **Add or remove hedging** in either direction.
13. **Introduce emoji, a summary box, a TL;DR the author did not write, a
    "Conclusion" section, or a call to action.**
14. **Reformat images, add alt text that was not there, or insert a diagram**
    that the author did not make.
15. **Rewrite quoted speech.** `Too many times have I had a conversation like
    this:` followed by a `text` fence of dialogue stays dialogue.
16. **"Improve" the front matter description** to be a marketing summary. It is
    an auto-derived excerpt of the body; leave it alone unless it is broken.
17. **Run `hugo`, `hugo --cleanDestinationDir`, or any build with
    `--destination docs`.** `publishDir` is `docs/` and the committed output must
    not be clobbered. Use `hugo server --renderToMemory` only, and only if you
    must.
18. **Touch git.** No `git add`, `commit`, `push`, or `checkout`.

## Machine-checkable rules

Scope for all rules: `content/posts/*.md` excluding `_index.md`. Front matter is
the text between the first two `---` lines; "prose" is the body with fenced code
blocks, HTML tags, and front matter removed. Each rule is a defect: nonzero
findings mean the file changed incorrectly.

**Spelling and language**

- `SPELL-001` — flag any word matching `\b(colour|colours|coloured|favourite|
  favourite|behaviour|behavioural|organise\w*|organis\w*|recognise\w*|analyse\w*|
  centre|programme|licence|defence|favour\w*|honour\w*|catalogue|dialogue|
  whilst|amongst|learnt|travelled|modelling|cancelled|grey)\b` in prose, case
  insensitive. Exemption: none. Existing occurrences are reported, not fixed.
- `SPELL-002` — flag `\b(utilis\w*|utiliz\w*)\b` and the blocklist in
  `VOICE-003`. Zero occurrences in the corpus.
- `LANG-001` — flag standalone `\b(och|för|med|inte|och)\b` in prose.
  `med` and `inte` are excluded because they collide with English usage
  (`inte` = integer appears in code); `och` and `för` have no English reading
  and are the actual defects. Zero tolerance in new text; report existing.
- `LANG-002` — flag lowercase first-person pronoun `\bi\b` appearing at the start
  of a sentence or clause: pattern `(?:^|[.!?;]\s|\n)\s*i\s+[a-z]` in prose,
  outside code fences. 12 existing occurrences across 11 posts; report only.

**Typography**

- `HEAD-001` — flag a markdown heading (`^#{1,6}\s+\S`, outside code fences) whose
  first alphabetic character is lowercase. Exemption: a heading that starts with
  `...` or a single letter followed by `:` (the two published cases:
  `# ...and why you should not use it`, `## references:`).
- `HEAD-002` — flag a heading where every content word is capitalised, i.e. at
  least 80% of the tokens after the first begin with an uppercase letter,
  excluding a stop-word list `a an and as at but by for from in into nor of on
  onto or over per the to up via with vs`. This is a **regression** rule, not a
  zero-tolerance one: of the 189 published `#`/`##`/`###` headings, 95 are
  sentence case, 72 are Title Case and 30 are mixed. So flag a *new* heading
  that trips it, or a rise in Title-Cased headings relative to the input — and
  never "fix" a pre-existing Title-Cased heading. Sentence case is the author's
  dominant default, not his only mode.
- `HEAD-003` — flag any heading text ending in `###`, `#`, `---`, `:::`, or any
  banner marker. The `### END ###` / `### Connect to SCOM 2012 Management Group
  ###` habit exists only *inside* PowerShell fences and must not escape into
  markdown.
- `HEAD-004` — flag a change in heading level for any pre-existing heading.
- `TITLE-001` — flag a front-matter `title` where ≥80% of tokens after the
  first are capitalised, same stop-word list as `HEAD-002`. 57 of 63 published
  titles are sentence case; match the majority.
- `TITLE-002` — flag any change to a `#hashtag` token inside a title, or a
  `title` whose hashtags were removed. 15 published titles carry them.
- `PUNCT-001` — flag an inserted Oxford comma: pattern
  `\b[\w'-]+,\s+[\w'-]+,\s+(?:and|or)\s+[\w'-]+\b` occurring in a line that was
  not serial before. Baseline: 4 hits corpus-wide, 2 of them not serial lists.
  Any new one is a defect.
- `PUNCT-002` — flag any emoji (U+1F300–U+1FAFF, U+2600–U+27BF) in the body.
  Exemption: front-matter `description`/`excerpt` may contain them — that is
  where all 9 corpus occurrences live.
- `PUNCT-003` — flag an apostrophe-style flip: the count of `'` vs `’` in a
  post changed. Baseline per post is mixed (245 straight / 59 curly corpus-wide).
- `PUNCT-004` — flag an em/en dash substitution: `\u2014` or `\u2013` count
  changed, or `(?<!-)--(?!-)` count changed. Baseline: 8 `\u2014`, 7 `\u2013`,
  30 `--` in prose.
- `PUNCT-005` — flag `...` replaced by `…` or vice versa. Baseline: 39 `...`,
  4 `…` in prose.

**Voice**

- `VOICE-001` — flag a post whose first-person density (tokens matching
  `\b(I|I'm|I've|I'd|I'll|me|my|mine|myself|we|our|us)\b` ÷ prose chars × 10000)
  is below 15. Baseline 31.6; a post dropping below half the corpus rate has
  been depersonalised.
- `VOICE-002` — flag a post whose passive density (tokens matching
  `\b(is|was|are|were|be|been|being)\s+\w+(?:ed|en)\b` ÷ prose chars × 10000)
  is above 12. Baseline 5.2.
- `VOICE-003` — flag any occurrence in prose of `\b(delve\w*|tapestry|
  testament\w*|underscor\w+|landscape|realm|robust|seamless|leverage[sd]?|
  game-?changer|supercharge|unlock|holistic|paradigm|utilis\w*)\b`. Corpus
  count: `delve` 1, inside a sentence disclaiming it. All others zero.
- `VOICE-004` — flag contractions density (`\b\w+'(?:s|t|re|ve|ll|d)\b` ÷ prose
  chars × 10000) above 30 in a post whose input was below 20, and flag any
  individual contraction expansion (`\bit is\b` where `\bit's\b` was,
  and the equivalents for do/does/did/will/can/have/had). Baseline 13.1.
- `VOICE-005` — flag contraction *removal*: the contraction token count in the
  output is lower than in the input. Report only; never restore silently.
- `VOICE-006` — flag sentence-initial `And|So|But|Anyway|Anyhow|Since|With|As`
  count falling to less than half the input value. Baseline corpus:
  `And` 36, `So` 17, `But` 15, `As` 20, `Since` 8, `With` 6, `Anyway` 17.
- `HEDGE-001` — flag any of `\b(it(?:'s| is) worth noting|it should be noted|
  generally speaking|typically|arguably|relatively|in most cases|it is
  important to note|needless to say)\b` that was not in the input.
- `HEDGE-002` — flag removal of any of
  `\b(I think|I guess|I assume|I presume|probably|maybe|perhaps|seems|
  not sure|I have not verified|I have not tested|I assume|sort of|kind of)\b`
  that was in the input.
- `LEN-001` — flag a post whose median sentence length (words, prose only)
  falls outside 6–35. Baseline per-post range is exactly 5–35, median corpus 15.
  Also flag if the post's median moves more than 40% from its input value.
- `LEN-002` — flag a prose paragraph of >300 words, or a merge of two adjacent
  sentences where either input sentence was ≤8 words. Baseline max paragraph
  284 words.

**Structure**

- `LIST-001` — flag any increase in bullet-item count
  (`^\s*[-*+]\s+\S`) or numbered-item count (`^\s*\d+[.)]\s+\S`) relative to
  the input, when the increase is not matched by an equal decrease in
  prose-paragraph count. This is the prose→bullets converter.
- `LIST-002` — flag a markdown pipe table (`^\s*\|.*\|` or a line matching
  `^\S+(\|\S+){2,}$` followed by a `---` delimiter row) added to a post. Baseline:
  exactly one in the whole corpus.
- `LIST-003` — flag a change to a pre-existing blockquote (`^\s*>`) count.
  Baseline 19 posts; they are used for quoted vendor text, `Note:` gotchas and
  sources.
- `FENCE-001` — flag an unbalanced fence count, or a fence opened with a
  language that the corpus never uses
  (`^(?!```$)(?!```(?:powershell|text|bash|xml|bat|vbs|cmd|sql|csharp)\s*$)````).
- `FENCE-002` — flag a language tag added to a fence that was untagged in the
  input, or removed from one that was tagged. Half the corpus (71 of 141) is
  untagged.
- `FENCE-003` — flag any change to the character content of a fenced block.
  Includes comment reformatting and whitespace changes.
- `QUOTE-001` — for every blockquote and every `text`-tagged fence containing
  external text, re-paste from the source and diff. Flag any byte difference
  other than the author's own surrounding prose.
- `HEAD-005` — flag a heading added or deleted relative to the input.
- `HEAD-006` — flag a post that ends with a `## Summary`, `## Conclusion` or
  `## TL;DR` heading when the input did not, or where a closing sign-off
  (`GLHF!`, `Enjoy!`, `Good luck!`, `Best of luck!`, `Cheers!`, `Have fun.`)
  was removed or replaced.

**Front matter and assets**

- `FRONT-001` — flag any front matter key set that is not exactly
  `{title, date, lastmod, url, description, excerpt, cats, tags}`, or any change
  in their order.
- `FRONT-002` — flag a `date` that is not bare `YYYY-MM-DD HH:MM:SS`, or a
  `lastmod` that is not `YYYY-MM-DDTHH:MM:SS±HH:MM`. The two are deliberately
  different: all 63 posts write `date` bare (that is what `hugo new` emits) and
  all 63 write `lastmod` with a timezone offset. Either value changing to the
  other shape is the defect, not the shape itself. Also flag a `date` later than
  the build clock — a future date makes Hugo skip the page entirely.
- `FRONT-003` — flag removal of `description` or `excerpt` keys, or any change
  to `description`/`excerpt` text that was not authored by the agent.
- `FRONT-004` — flag a `url` whose path does not begin with `/` and end with `/`,
  or whose first segment is not the first segment of the `cats` chain.
- `IMG-001` — flag any `![](...)` target that is not
  `^\/wp-content\/uploads\/` or an explicit `http(s)://` embed. Root-relative
  only; assets live under `static/`.
- `IMG-002` — flag an added image, or a changed alt text on an existing image.
  Baseline: 8 posts, 28 images, all WordPress-era uploads.
- `SHORTCODE-001` — flag `{{<` other than `{{< gist `, and flag any `{{%`
  (all 9 corpus occurrences were converted to `{{< ... >}}`).
- `TYPO-001` — flag any edit to a body line that a dictionary-based spell
  checker would reject. This rule exists to make such an edit *visible* in a
  diff, not to be auto-fixed. Known-preserved tokens to whitelist from any
  dictionary check: `feautures`, `allready`, `alot`, `Aftr`, `Alhough`,
  `dissapointed`, `failes`, `Unfortunatly`, `Prerequisute`, `Stese`,
  `med`, `och`, `för`, `rekommendations`, `abrevations`, `crasches`,
  `hickups`, `looke`, `wich`, `techique`, `datasouce`,
  `supression`, `the the`.
- `REPO-001` — flag if `docs/` is modified, or if any file outside the single
  targeted `content/posts/*.md` has changed. Prose drafts run nowhere near the
  build.

## Implementation status

`tools/style.py` implements the following, and reports them by id:

`SPELL-001` `SPELL-002` `LANG-001` `LANG-002` `HEAD-001` `HEAD-002` `HEAD-003`
`TITLE-001` `PUNCT-001` `PUNCT-002` `PUNCT-004` `PUNCT-005` `VOICE-001`
`VOICE-002` `VOICE-003` `VOICE-004` `VOICE-005` `VOICE-006` `HEDGE-001`
`HEDGE-002` `LEN-001` `LEN-002` `LIST-001` `LIST-002` `LIST-003` `FENCE-001`
`FENCE-002` `FRONT-001` `FRONT-002` `FRONT-004` `IMG-001` `SHORTCODE-001`

These are **not** implemented, and an agent must still check them by hand:

| Rule | Why not |
| --- | --- |
| `HEAD-004`, `HEAD-005` | Heading added, removed or re-levelled. Needs an intent to compare against: a new post legitimately has headings the old one lacked. |
| `HEAD-006` | Sign-off removal. The sign-offs are a closed list, but which one belongs to which post is a judgement. |
| `TITLE-002` | Hashtag changes in a title. Fifteen posts carry them; deciding whether one was dropped on purpose is not mechanical. |
| `PUNCT-003` | Apostrophe-style flip. Both styles coexist inside single posts, so a per-post change means nothing without reading it. |
| `FENCE-003` | Changed characters inside a code block. A diff already shows this; a second report is noise. |
| `FRONT-003` | `description`/`excerpt` authorship. Nothing records who wrote a given string. |
| `IMG-002` | Added image or changed alt text. Whether an image earns its place is an editorial call. |
| `QUOTE-001` | Re-paste quoted vendor text from source and diff. Inherently manual; the tool cannot reach the source. |
| `TYPO-001` | Needs a dictionary the repository does not carry. The whitelist above is what such a check should exempt. |
| `REPO-001` | Needs to know which file was targeted. `tools/permalinks.py` already fails loudly on a moved URL, which covers the part that matters. |

Two rules are deliberately weaker than written above, because the strict form
produced false positives on real posts: `HEAD-002` and `TITLE-001` fire only on
headings and titles that **changed**, since most of the corpus is Title-Cased to
some degree and reporting an untouched one is noise. `LEN-001`'s relative check
only runs on posts with at least eight sentences, because a 40% move in a
two-sentence draft is arithmetic, not signal.
