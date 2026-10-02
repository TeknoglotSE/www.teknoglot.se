{{- /*
  Fallback scaffold for anything without a section-specific archetype.

  Sections with their own shape: posts.md, topics.md, tags.md, archives.md.
  Prefer those; this one makes no assumptions about category or URL, because a
  page under content/pages/ has neither.
*/ -}}
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---

Write the page here.