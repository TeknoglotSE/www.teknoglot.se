{{- /*

  A script guide. You wrote a script, it works, and now you want it written down
  so you can find it again in two years. The reader is you, or a colleague who
  has to run it, so the walkthrough matters as much as the code does.

  The body below is the shape these keep taking:

      an opening paragraph: what the script does and the scenario for it
      Prerequisites       what has to be in place before any of it runs
      Inputs              the parameters, at the top, editable on their own
      Connect             establish the session the rest of the script needs
      Do stuff            the actual work, one fence per step
      The copy/paste part the whole script in one fence, ready to run

  Two fields need a decision rather than a default:

    url   the public path. It is built from the category below, so if you move
          the post to a different category, change this line too.
    cats  the category chain, e.g. [tb], [code, code/posh] or
          [ms, ms/opsmgr2012]. The chain must match an existing leaf under
          content/topics/, otherwise the category has no page to link to and
          the breadcrumb renders nothing.

  The script belongs here as source, not only as a link to a gist. Link the
  gist in the opening paragraph too if there is one, but do not make the gist
  the post.

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

*What the script does, and the situation that made you write it. A reader without that context runs it wrong.*

## Prerequisites

*What has to be in place before any of it runs. Modules, management packs, permissions, versions.*

## Inputs

*The parameters, at the top of the script where they can be changed without touching the logic.*

```powershell
# Input the server to connect to in this session
[string]$inputServer = "server.domain.local"
# Input what the script should act on
[string]$inputTarget = "*.domain.local"
```

## Connect to the target

*Establish the session the rest of the script runs in, and get out of the way cleanly if it fails.*

```powershell
try {
    Import-Module -Name "OperationsManager"
} catch {
    Write-Output "Could not load the module"
    exit
}
New-SCOMManagementGroupConnection -ComputerName $inputServer
```

## Do stuff

*The actual work. One fence per step, with a sentence about what to expect when it runs.*

```powershell
# Whatever it is you came here to automate
```

> Note: whatever the reader is going to get bitten by. Which wildcards work,
> which parameter sets do not, what the product does that the help does not
> document.

## The copy/paste part

*The whole script in one fence. Read it, try it, adapt it.*

```powershell
### Input parameters ###
[string]$inputServer = "server.domain.local"
[string]$inputTarget = "*.domain.local"
### End of inputs ###

# ...then the steps above, in the same order.
```

GLHF!