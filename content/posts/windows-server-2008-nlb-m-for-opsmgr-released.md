---
title: Windows Server 2008 NLB MP for OpsMgr released
date: 2009-04-29 12:59:54
year: "2009"
month: "04"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/windows-server-2008-nlb-m-for-opsmgr-released/
url_encoded: /ms/opsmgr2007/windows-server-2008-nlb-m-for-opsmgr-released/
description: Don’t know how I missed this when writing the last post, but Microsoft released the MP for Windows Server 2008 NLB yesterday (28&#x2F;4 -09). This is the initial release for Win2k8 NLB so I guess we just h
hexo_slug: windows-server-2008-nlb-m-for-opsmgr-released
excerpt: "Don’t know how I missed this when writing the last post, but Microsoft released the MP for Windows Server 2008 NLB yesterday (28/4 -09). This is the initial release for Win2k8 NLB so I guess we just have to try it out then. Quick Details File Name: Microsoft Server 2008 Network Load Balancing System Center Operations Manager 2007 MP.msiVersion: 6.0.6573.0Date Published: 4/28/2009Language: EnglishDownload Size: 519 KB Feature Summary Monitor the NLB Node status. Based on the status of individual cluster nodes, determine the overall state of the cluster. Where an integration management pack exists, determine the health state of a cluster node by looking at the health state of the load balanced application, such as IIS. Alert on errors and warnings that are reported by the NLB driver, such as an incorrectly configured NLB cluster. Take the node out of the NLB cluster if the underlying load-balanced application becomes unhealthy, and add the node back to the cluster when the application becomes healthy again. Requires OpsMgr 2007 SP1 or later, the Base Operating System MP for 2008, the QFEs for Windows Server 2008 and that you are not running the converted 2003 NLB MP. If you are running the old converted NLB MP, upgrade first. As an additional recommendation, Microsoft recommends in the MP Guide that you install the QFE for wmiprvse.exe problems on Windows Server 2008. No support for Mixed-mode (2008 and 2003) clusters though."
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Management Pack
hexo_id: 153
---

Don't know how I missed this when writing the last post, but Microsoft released the [MP for Windows Server 2008 NLB](http://www.microsoft.com/downloads/details.aspx?FamilyID=dc17e093-bdd7-4cb3-9981-853776ed90be&displaylang=en "Windows Server 2008 Network Load Balancing for System Center Operations Manager 2007") yesterday (28/4 -09). This is the initial release for Win2k8 NLB so I guess we just have to try it out then.

# Quick Details

```text
File Name:      Microsoft Server 2008 Network Load Balancing System Center Operations Manager 2007 MP.msi
Version:        6.0.6573.0
Date Published: 4/28/2009
Language:       English
Download Size:  519 KB
```

# Feature Summary

* Monitor the NLB Node status.
* Based on the status of individual cluster nodes, determine the overall state of the cluster.
* Where an integration management pack exists, determine the health state of a cluster node by looking at the health state of the load balanced application, such as IIS.
* Alert on errors and warnings that are reported by the NLB driver, such as an incorrectly configured NLB cluster.
* Take the node out of the NLB cluster if the underlying load-balanced application becomes unhealthy, and add the node back to the cluster when the application becomes healthy again.

Requires OpsMgr 2007 SP1 or later, the Base Operating System MP for 2008, the [QFEs for Windows Server 2008](http://support.microsoft.com/kb/953141 "Support for running System Center Operations Manager 2007 Service Pack 1 and System Center Essentials 2007 Service Pack 1 on a Windows Server 2008-based computer") and that you are not running the converted 2003 NLB MP. If you are running the old converted NLB MP, upgrade first. As an additional recommendation, Microsoft recommends in the MP Guide that you install the [QFE for wmiprvse.exe problems on Windows Server 2008](http://support.microsoft.com/kb/959493 "The WMI Provider Host program (Wmiprvse.exe) may crash on a Windows Server 2008-based computer that has the NLB feature installed2008").

No support for Mixed-mode (2008 and 2003) clusters though.