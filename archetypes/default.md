---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
excerpt: ""
cats:
  - tb
tags: []
url: /tb/{{ .Name | urlize }}/
---

Write your post here.
