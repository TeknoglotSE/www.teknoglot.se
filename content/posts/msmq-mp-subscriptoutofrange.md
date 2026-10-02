---
title: "MSMQ Management Pack: Subscript Out of Range"
date: 2009-06-24 09:51:01
year: 2009
month: 06
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/msmq-mp-subscriptoutofrange/
url_encoded: /ms/opsmgr2007/msmq-mp-subscriptoutofrange/
description: "UPDATE: This problem seems to be fixed in the latest update! The MSMQ Management Pack seems to have a few problems with it’s discovery script that can lead to the following error showing up in the log"
excerpt: "UPDATE: This problem seems to be fixed in the latest update! The MSMQ Management Pack seems to have a few problems with it’s discovery script that can lead to the following error showing up in the logs: The process started at 13:34:40 failed to create System.Discovery.Data. Errors found in output:C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 499788DiscoverQueues.vbs(107, 4) Microsoft VBScript runtime error: Subscript out of range: '[number: 0]'Command executed: \"C:WINDOWSsystem32cscript.exe\" /nologo \"DiscoverQueues.vbs\" {615D37C9-477D-62E2-0833-6ECBF0E89A87} {A176AC83-CC31-01C3-5DE9-E2DFF64E7CC7} \"MASKED.server.fqdn\" \"MSMQ\" \"true\" \"true\" \"False\" \"false\"Working Directory: C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 499788One or more workflows were affected by this.Workflow name: Microsoft.MSMQ.2003.DiscoverQueuesInstance name: MASKED.server.fqdnInstance ID: {A176AC83-CC31-01C3-5DE9-E2DFF64E7CC7}Management group: MASKED This seems to be related to the discovery of public queues on some servers that has none. One quick fix, or rather work-around, is to override the discovery on these servers to set DiscoverPublic to False."
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Errors
  - MSMQ
  - Fixed
  - Quick-fix
hexo_id: 182
---

<span style="color: #800000;"><span style="text-decoration: underline;">UPDATE: This problem seems to be fixed in the latest update!</span></span>

The MSMQ Management Pack seems to have a few problems with it's discovery script that can lead to the following error showing up in the logs:

```text
The process started at 13:34:40 failed to create System.Discovery.Data. Errors found in output:

C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 499788DiscoverQueues.vbs(107, 4) Microsoft VBScript runtime error: Subscript out of range: '[number: 0]'

Command executed: "C:WINDOWSsystem32cscript.exe" /nologo "DiscoverQueues.vbs" {615D37C9-477D-62E2-0833-6ECBF0E89A87} {A176AC83-CC31-01C3-5DE9-E2DFF64E7CC7} "MASKED.server.fqdn" "MSMQ" "true" "true" "False" "false"
Working Directory: C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 499788

One or more workflows were affected by this.

Workflow name: Microsoft.MSMQ.2003.DiscoverQueues

Instance name: MASKED.server.fqdn

Instance ID: {A176AC83-CC31-01C3-5DE9-E2DFF64E7CC7}

Management group: MASKED
```

This seems to be related to the discovery of public queues on _some_ servers that has none. One quick fix, or rather work-around, is to override the discovery on these servers to set `DiscoverPublic` to `False`.
![Screenshot of Override](http://teknoglotse.nfshost.com/wp-content/uploads/2009/06/screenshot1245833173.png "screenshot1245833173")