---
title: "The TCP Port Check: Use with caution!"
date: 2009-08-27 14:39:43
year: "2009"
month: "08"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/tcp-port-check-use-with-caution/
url_encoded: /ms/opsmgr2007/tcp-port-check-use-with-caution/
description: Just wanted to raise a word of caution about the TCP Port Check in Operations Manager 2007. Some customers have notices the the system-logs on some Unix machines are completely swamped with “connectio
hexo_slug: tcp-port-check-use-with-caution
excerpt: Just wanted to raise a word of caution about the TCP Port Check in Operations Manager 2007. Some customers have notices the the system-logs on some Unix machines are completely swamped with “connection error”, “TCP Connect failed”, “TCP Session Lost” and similar and after a bit och research the problematic servers were narrowed down to those monitored by Operations Manager. Specifically, those who are targeted by a TCP Port Check. It would seem like the TCP-connection never fully initializes on the target server. Kind of like knocking on your neighbours door and then hiding. Then when the door opens, no one is there causing your friendly neighbour to hang around waiting for something to happen. Maybe there’s a setting somewhere to modify how “deep” a Port Check should go before closing. Perhaps fully initializing and then sending a proper “Close” instead of just cutting the connection. In a few extreme cases we have noticed that the target server even goes so far as to start a session, but never ending it since there’s no closure and finally having no sessions to spare for the real users. But on most servers it’s just an annoyance since the “real” errors is very hard to be found in all the connection related logs. Anyway. Just a good thing to keep in mind when running TCP Port Checks from Operations Manager 2007. Keep an eye on the logs when implementing the port checks.
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Errors
  - Unix
hexo_id: 202
---

Just wanted to raise a word of caution about the TCP Port Check in Operations Manager 2007.

Some customers have notices the the system-logs on some Unix machines are completely swamped with "connection error", "TCP Connect failed", "TCP Session Lost" and similar and after a bit och research the problematic servers were narrowed down to those monitored by Operations Manager. Specifically, those who are targeted by a TCP Port Check.

It would seem like the TCP-connection never fully initializes on the target server. Kind of like knocking on your neighbours door and then hiding. Then when the door opens, no one is there causing your friendly neighbour to hang around waiting for something to happen.

Maybe there's a setting somewhere to modify how "deep" a Port Check should go before closing. Perhaps fully initializing and then sending a proper "Close" instead of just cutting the connection. In a few extreme cases we have noticed that the target server even goes so far as to start a session, but never ending it since there's no closure and finally having no sessions to spare for the real users. But on most servers it's just an annoyance since the "real" errors is very hard to be found in all the connection related logs.

Anyway. Just a good thing to keep in mind when running TCP Port Checks from Operations Manager 2007\. Keep an eye on the logs when implementing the port checks.