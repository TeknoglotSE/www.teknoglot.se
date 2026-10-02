{{- /*

  A how-to. You did something from start to finish and you are writing down the
  order you did it in, so somebody else can do it without asking you.

  The body below is the shape these keep taking:

      an opening line: what you are installing or configuring, and why
      Prerequisites  what has to be there before the first command
      Preparations   downloads, packages, keys, the documentation to read first
      Installation   the steps, in order, one command block each
      Verification   how you know it worked, and what the output looks like
      Configuration  anything you had to change afterwards to make it behave
      Notes          the gotchas and the parts the documentation leaves out

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb], [linux, linux/rhes] or [ms, ms/sql].
          The chain must match an existing leaf under content/topics/,
          otherwise the category has no page to link to and the breadcrumb
          renders nothing.

  Tag it How-To.

  description and excerpt may be left empty: the listing falls back to an
  automatically generated summary. Pin them only when you want to control the
  wording.

  If the error is the story rather than the procedure, this is the wrong
  archetype; use archetypes/troubleshooting.md instead.

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

*What you are installing or configuring, and what made you do it. That sentence is what tells somebody whether this is still the right guide for them.*

## Prerequisites

*What has to be in place before the first command. Versions, packages, permissions, and the ones that are easy to miss.*

## Preparations

*Downloads, repositories, keys. Anything worth reading first that saved you an hour.*

```bash
# the commands that get you ready
```

*Say why each one is there, not just what it is.*

## Installation

*In order. One command block per step, and a sentence about what you should see when it works.*

```bash
# step one
```

```bash
# step two
```

## Verification

*How you know it worked, and what the output looks like. This is the section people scroll to, and the one they most often cannot find.*

```text
the command to run, and roughly what it should print back
```

## Configuration

*Anything you had to change afterwards to make it behave. Keep it short.*

## Notes

*The gotchas. What the documentation leaves out, what you would do differently, and what you have not verified yet.*

Good luck!