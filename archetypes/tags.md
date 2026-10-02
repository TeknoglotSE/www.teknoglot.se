{{- /*

  A tag leaf, which is what gives a tag its page under /tag/.

      hugo new tags/Kubernetes/_index.md

  url and tag_slug follow the directory name. tag is the display name, which
  may differ: a leaf in Field-Notes is tagged "Field Notes".

  cloud_order is the one number on this site that cannot be derived. The tag
  cloud is ordered by byte-wise name, so Gist comes before GSM because 'i' is
  below 's'. Hugo's own sort collates instead, which reverses those, so the
  order is pinned per leaf. 999 parks a new tag last; move it into the right
  position once the set of tags has settled. Nothing else depends on the value.

*/ -}}
---
title: {{ replace .Name "-" " " | title }}
type: tagpage
url: /tag/{{ .Name }}/
tag: {{ replace .Name "-" " " }}
tag_slug: {{ .Name }}
cloud_order: 999
---

Tag page for {{ .Name }}. Posts appear here by way of their tags front
matter; nothing needs to be listed on this page.