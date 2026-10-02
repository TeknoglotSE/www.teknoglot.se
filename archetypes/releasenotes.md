{{- /*

  Release notes. Something shipped, usually a management pack or a version of
  one, and you are telling people it exists and whether it is worth their time
  today.

  The body below is the shape these keep taking:

      an opening sentence: what was released, and when
      Quick details   version, date published, language, download size
      What's new      the changes, mostly quoted from the release notes
      Release history the earlier versions, so the jump is visible
      Prerequisites   dependencies, before somebody imports it and regrets it
      Download        the link
      My take         your own opinion, which is why anybody reads it

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb] or [ms, ms/opsmgr2007] or
          [ms, ms/opsmgr2012]. The chain must match an existing leaf under
          content/topics/, otherwise the category has no page to link to and
          the breadcrumb renders nothing.

  Tag it Management Pack, plus whatever product it is for.

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

*What was released, by whom, and on what date. One sentence is the whole lead, the rest is detail.*

## Quick details

*As it appears on the download page. A code fence keeps it readable.*

```text
File Name:      Message Queuing System Center Operations Manager 2007 MP.MSI
Version:        6.0.6587.0
Date Published: 4/24/2009
Language:       English
Download Size:  502 KB
```

## What's new

*The changes that matter, one per bullet. Quote the release notes where that is clearer than your own words, and say so.*

- Fixed an issue that was preventing ...
- Added the rule "..."

## Release history

*Every version, oldest first. Mostly so the jump is visible.*

- 6/3/2008 - Initial Release, version 6.0.6278.23.
- 4/24/2009 - Updated release, version 6.0.6587.0.

## Prerequisites

*What has to be there first, and which older pack you have to retire before you import this one.*

## Download

[Download here]()

## My take

*Your own opinion, in a sentence or two. What is still missing, whether it is worth importing today, and when you are actually going to.*

Enjoy!