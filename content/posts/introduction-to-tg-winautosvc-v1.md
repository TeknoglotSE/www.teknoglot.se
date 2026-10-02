---
title: Introduction to TG WinAutoSvc v1
date: 2011-04-29 11:35:47
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2012/introduction-to-tg-winautosvc-v1/
description: Background For quite some time now I’ve had this idea spinning around in my head to write a couple of blog-posts about some of the more useful techniques available when building management packs. Man
excerpt: "Background For quite some time now I’ve had this idea spinning around in my head to write a couple of blog-posts about some of the more useful techniques available when building management packs. Many of these techniques are already described on MSDN and Technet- or other blogs as well as on various forums, but often no more than small bits and pieces of them and I have yet to see some humanly readable information about how to tie them together into a useful management pack. I say “humanly readable” because the information you do find online so far may be clear and somewhat easy to understand for someone with a system development background and a pretty good idea of how object oriented development models tend to work. But the real life System Center Operations Manager engineer–you know the one who get those “do you think we could monitor our …-system too?” questions a couple of times a week, you know… you (most likely, being here)–tend to have a completely different background. Yet as their OpsMgr environment grows, so does the demand for custom monitoring and all of a sudden the former server engineer are now also a developer. A developer who has never before had the need to grasp such abstract concepts as classes, instances, inheritance and who probably never before have had any reason whatsoever to write any XML code. Purpose My idea for this series of posts is to shed some light into the world of the authoring console and modules and cookdown and so forth. I am by no means an accredited author, but I will do my best to stay human in this venture and in plain english try to explain why and how you do certain things when going from Management Pack templates, rules, monitors and the safe haven that is authoring in the Operations Console into making your scripts resuable, easy to extend and prime for cookdown using the Authoring Console and XML. The TG WinAutoSvc Management Pack To give the series some kind of context and at the same time not only be a matter of examples I will base them on a fully functional management pack that discovers and monitors all Windows services that are set to automatic startup. I know there is other similar management packs out there but I haven’t fancied any one of them yet, and since I had the idea of writing this series I decided that building a new one would be a good way to go. Some of the interesting features with this management pack is: You will get an instance of the service classes for each and every service. It uses different classes for Own Process services and Shared Process services (svchost for example). Every service have a health state (you can use them in distributed applications). The service state monitors are inherited from their base classes, no coding neccesary. There is only one discovery script for all kinds of windows services. Extending the discovery to include different kinds of windows services, like kernel processes, is a matter of filtering. It is Open Source and licensed under the Eclipse Public License v1. Most of these features will be described thoroughly in later posts in the series and as development of it progresses I will document what I do, how I do it and why I do it in certain ways. Hopefully you will learn something new through this and get closer to becoming that MP Dev the organization asks for. In the mean time, feel free to download, look at the source code (which it by no means perfect) and try it out. The TG WinAutoSvc monitoring management pack is available for download here: http://code.google.com/p/tg-winautosvc/downloads/detail?name=TG.WinAutoSvc.xml The latest revision of the source code is located here: http://code.google.com/p/tg-winautosvc/source/browse/trunk/TG.WinAutoSvc.xml"
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - Management Pack
  - MP Development
---

# Background

For quite some time now I've had this idea spinning around in my head to write a couple of blog-posts about some of the more useful techniques available when building management packs. Many of these techniques are already described on MSDN and Technet- or other blogs as well as on various forums, but often no more than small bits and pieces of them and I have yet to see some humanly readable information about how to tie them together into a useful management pack. I say "humanly readable" because the information you do find online so far may be clear and somewhat easy to understand for someone with a system development background and a pretty good idea of how object oriented development models tend to work. But the real life System Center Operations Manager engineer--you know the one who get those _"do you think we could monitor our ...-system too?"_ questions a couple of times a week, you know... you (most likely, being here)--tend to have a completely different background. Yet as their OpsMgr environment grows, so does the demand for custom monitoring and all of a sudden the former server engineer are now also a developer. A developer who has never before had the need to grasp such abstract concepts as classes, instances, inheritance and who probably never before have had any reason whatsoever to write any XML code.

# Purpose

My idea for this series of posts is to shed some light into the world of the authoring console and modules and cookdown and so forth. I am by no means an accredited author, but I will do my best to stay human in this venture and in plain english try to explain why and how you do certain things when going from Management Pack templates, rules, monitors and the safe haven that is authoring in the Operations Console into making your scripts resuable, easy to extend and prime for cookdown using the Authoring Console and XML.

# The TG WinAutoSvc Management Pack

To give the series some kind of context and at the same time not only be a matter of examples I will base them on a fully functional management pack that discovers and monitors all Windows services that are set to automatic startup. I know there is other similar management packs out there but I haven't fancied any one of them yet, and since I had the idea of writing this series I decided that building a new one would be a good way to go. Some of the interesting features with this management pack is:

* You will get an instance of the service classes for each and every service.
* It uses different classes for Own Process services and Shared Process services (svchost for example).
* Every service have a health state (you can use them in distributed applications).
* The service state monitors are inherited from their base classes, no coding neccesary.
* There is only one discovery script for all kinds of windows services.
* Extending the discovery to include different kinds of windows services, like kernel processes, is a matter of filtering.
* It is Open Source and licensed under the [Eclipse Public License v1](http://tg-winautosvc.googlecode.com/svn/trunk/LICENSE.TXT "Eclipse Public License v1").

Most of these features will be described thoroughly in later posts in the series and as development of it progresses I will document what I do, how I do it and why I do it in certain ways. Hopefully you will learn something new through this and get closer to becoming that MP Dev the organization asks for.
In the mean time, feel free to download, look at the source code (which it by no means perfect) and try it out.

The TG WinAutoSvc monitoring management pack is available for download here:
[http://code.google.com/p/tg-winautosvc/downloads/detail?name=TG.WinAutoSvc.xml](http://code.google.com/p/tg-winautosvc/downloads/detail?name=TG.WinAutoSvc.xml)

The latest revision of the source code is located here:
[http://code.google.com/p/tg-winautosvc/source/browse/trunk/TG.WinAutoSvc.xml](http://code.google.com/p/tg-winautosvc/source/browse/trunk/TG.WinAutoSvc.xml)

A small word of advice though. If you implement this in your environment, remember that you probably have alot more automatic services than you would expect. Because of this, discovery is disabled by default.

Best of luck, and enjoy!