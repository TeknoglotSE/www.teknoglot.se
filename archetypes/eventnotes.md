{{- /*

  Event notes. Live notes from a session at a conference, written on a phone or
  on a pad between sessions and cleaned up afterwards. They are meant to be
  short and honest: what was said, what was demoed, what you did not get.

  The body below is the shape these keep taking:

      the session code and title, exactly as on the schedule
      the slot it ran in, date and time
      an honesty notice when the notes are rough
      a section per topic, bullets underneath, ### where a topic has parts
      Personal reflections, which is the reason anyone reads them

  The opening heading repeats the page title the layout already renders. The
  published event notes do exactly that, so keep it unless you would rather
  have one H1 than two.

  Three fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too. The event
          notes live under an event leaf, /Events/MSIgnite-2017/, which is
          case-preserving.
    cats  the category chain, e.g. [Events, Events/MSIgnite-2017]. The chain
          must match an existing leaf under content/topics/, otherwise the
          category has no page to link to and the breadcrumb renders nothing.
    title derived from a filename it comes out title-cased. These are posted
          as "#MSIgnite 2017: BRK1039 - Windows Server Software Defined",
          with the event, the real session code and the real session title, so
          this one you rewrite by hand.

  Tag it MSIgnite and Presentation Notes, plus whatever the session was about.

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

# BRK1039 - Windows Server Software Defined

Sep 26, 11:45 am – 12:30 pm

> UNSTRUCTURED NOTES! Also written on a phone, will come back and refine

*The session's pitch in a line, straight from the schedule.*

## Quick notes

*What you heard before you had a heading for it yet. One bullet per thought, in the order you heard them.*

## The main topic

*The part you came for. Head this after the product or the feature, and nest with ### where it has parts, the way you would section it on a whiteboard.*

## The demo

*What they showed, and what it actually did when it ran. A demo that falls over is worth a line of its own.*

## Personal reflections

*What you have to say to your own customers about this one. The gap between the demo and what you see in the field is the whole reason these notes exist.*

## Links

- [The session on the schedule]()
- [Slides or recording, if there is one]()