{{- /*

  A category leaf, which is what gives a category chain its page under
  /topics/. Create it at the depth you need:

      hugo new topics/linux/_index.md
      hugo new topics/ms/opsmgr2013/_index.md

  cat and url are derived from the path, so a leaf always agrees with where it
  lives. One thing is left for you:

    title    the display name, e.g. "OpsMgr 2013" for ms/opsmgr2013. It is
             shown in the nav, the sidebar and the breadcrumb.

  cat_parent is derived too: the chain above this one, empty at the top level.
  The nav and sidebar trees walk it, so a nested category needs its parent to
  exist as a leaf of its own.

  A category also needs to appear in the cats front matter of at least one post
  before it lists anything.

*/ -}}
{{- $cat := replaceRE "^topics/" "" (strings.Trim .File.Dir "/") -}}
{{- $parent := path.Dir $cat -}}
{{- if eq $parent "." }}{{ $parent = "" }}{{ end -}}
---
title: REPLACE-WITH-DISPLAY-NAME
type: topic
url: /topics/{{ $cat }}/
cat: {{ $cat }}
cat_parent: "{{ $parent }}"
---

Category page for {{ $cat }}. Posts are selected by their cats front matter, so
there is nothing to list here.