{{- /*

  A rant. Not a how-to, not news. You are annoyed about something and you are
  writing it down in the first person, and that is the whole post.

  These are short. The published ones run from three lines to a single page,
  and the short ones are the good ones. Do not pad this out to fill the
  skeleton. If you have three things to say, use three Reasons and delete the
  rest; a rant with seven Reasons is a blog post with a chip on its shoulder.

  The body below is the shape a longer one takes:

      a few paragraphs saying what set you off
      Background  what you saw, and who you are asking to change it
      Reason #1   the first thing, numbered, in no particular order
      Reason #2   the next one
      a closing paragraph that lets yourself off the hook

  Nothing here needs a code fence. The moment you are adding one, this is
  really a how-to; use archetypes/howto.md instead.

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb] or [linux]. The chain must match an
          existing leaf under content/topics/, otherwise the category has no
          page to link to and the breadcrumb renders nothing.

  Tag it Rant; the tag cloud and the tag page key off that.

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

*What set you off. Two or three sentences in the first person, with the sentence everybody will quote near the top.*

## Background

*What you saw, where, and who you are asking to change their mind. Say up front how blunt the rest of this is going to be.*

## Reason #1 - the first thing

*The first thing that is wrong with it. Frank is fine. Quiet is not.*

## Reason #2 - the second thing

*The second. Same tone.*

## Reason #3 - and then it stops being clever

*The one where you finally say the thing everybody was thinking and did not say.*

## So there

*Let yourself off the hook. What you would actually like to see instead, in a sentence or two, and then stop.*

Thanks for your time.