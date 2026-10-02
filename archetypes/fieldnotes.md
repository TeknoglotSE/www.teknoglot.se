{{- /*

  Field notes. Quick, unrefined notes taken while actually doing the work: an
  update roll-up, an upgrade, a discovery sweep. Not a manual and not a
  how-to. The point is that they are searchable later, when the same thing
  happens again on somebody else's box.

  The body below is the shape these keep taking. Rename or drop the headings as
  the work demands, but keep the order:

      a strapline saying what this is
      Abstract     what you were doing, and whether it went smoothly
      Links        the KB, the download, the announcement blog
      Notes        the notes themselves, one subheading per step or role
      Afterthoughts what surprised you once it was done

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb] or [ms, Fieldnotes, Fieldnotes/OpsMgr].
          The chain must match an existing leaf under content/topics/,
          otherwise the category has no page to link to and the breadcrumb
          renders nothing. The field notes live under the Fieldnotes leaf.

  Tag it Fieldnotes as well; the tag cloud and the tag page key off that.

  description and excerpt may be left empty: the listing falls back to an
  automatically generated summary. Pin them only when you want to control the
  wording.

*/ -}}
{{- $cat := "tb" -}}
---
title: "{{ replace .Name "-" " " | title }}"
type: posts
date: {{ .Date }}
draft: true
description: ""
excerpt: ""
cats:
  - {{ $cat }}
tags: []
url: /{{ $cat }}/{{ .Name | urlize }}/
---

_Quick and unrefined notes on the thing you just did._

## Abstract

*What you were doing, on what, and whether it went smoothly. One paragraph is plenty.*

## Links

- [Official documentation]()
- [Download location]()
- [Announcement blog]()

## Notes

### The first step

*What you did and what came back. Errors, event log entries, how long it took.*

### The next thing

*Same again. One subheading per step or per server role, so it stays findable.*

### The bit that bit back

*The thing that went wrong, in the order it went wrong. Keep it even when the rest of it worked.*

## Afterthoughts

*What surprised you, what you will do differently next time, and what you have not verified yet.*

GLHF!