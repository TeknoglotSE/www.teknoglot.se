{{- /*

  A new post. Hugo picks this for anything under content/posts/.

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb] or [ms, ms/opsmgr2012]. The chain must
          match an existing leaf under content/topics/, otherwise the category
          has no page to link to and the breadcrumb renders nothing.

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

Write your post here.