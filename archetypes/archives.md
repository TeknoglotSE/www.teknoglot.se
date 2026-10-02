{{- /*
  An archive leaf. year and month are plain numbers and month is unpadded, so
  08 is written 8; the /archives/2018/8/ title depends on that.

      hugo new archives/2026/_index.md          a year
      hugo new archives/2026/10/_index.md       a month within it

  Create these when the first post of a period is published. Until a period has
  a leaf it has no page at all, and its posts are missing from the archive.
*/ -}}
{{- $path := replaceRE "^archives/" "" (strings.Trim .File.Dir "/") -}}
{{- $segments := split $path "/" -}}
{{- $year := index $segments 0 -}}
{{- $month := "" -}}
{{- if eq (len $segments) 2 }}{{ $month = index $segments 1 }}{{ end -}}
---
title: Archive
type: archive
url: /archives/{{ $path }}/
archive_path: {{ $path }}
year: {{ $year }}
{{- with $month }}
month: {{ . }}
{{- end }}
---

Archive for {{ $path }}. Posts are selected by date, so there is nothing to
list here.