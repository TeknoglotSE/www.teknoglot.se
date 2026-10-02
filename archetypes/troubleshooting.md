{{- /*

  Troubleshooting. Something broke, you worked out why, and you want it findable
  the next time it happens on somebody else's box. This is a post-mortem on a
  single error, not a guide: say what the error is, say what caused it, say
  what made it go away.

  The body below is the shape these keep taking:

      an opening sentence, in your own words, with the error in it
      Problem        what was going on when it hit
      Symptoms       what you saw: the alert, the event log, the console
      Probable cause why it happened, and how far you got before you knew
      Workaround     what made it go away, in the order that worked
      Read more      the KB, the Connect entry or the forum thread

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb] or [ms, ms/opsmgr2007] or
          [ms, ms/windows]. The chain must match an existing leaf under
          content/topics/, otherwise the category has no page to link to and
          the breadcrumb renders nothing.

  Tag it Errors. TroubleShooting is the other tag these carry.

  description and excerpt may be left empty: the listing falls back to an
  automatically generated summary. Pin them only when you want to control the
  wording.

  If what you are actually writing is the procedure that fixes it, from
  nothing to done, this is the wrong archetype; use archetypes/howto.md.

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

*State the problem in your own words first, with the error message in it. That sentence is what people paste into a search engine.*

## Problem

*What you were doing when it hit, and what "it" is. One or two sentences.*

## Symptoms

*What you actually saw, pasted as it came out.*

```text
The process started at 14:29:26 failed to create System.PropertyBagData, no errors detected in the output.
```

*What you have already ruled out, so nobody asks about it again.*

## Probable cause

*Why it happened. Say how sure you are. "I am not really sure, but" is an honest answer and it has appeared here more than once.*

## Workaround

*What made it go away, numbered, in the order that worked.*

1. *The first thing.*
2. *The second thing.*

*Or a command, if that is all it took.*

```powershell
# the command that fixed it
```

## Read more

> [The KB article]()
> [The Connect entry]()
> [The forum thread somebody else had already solved it in]()

Good luck!