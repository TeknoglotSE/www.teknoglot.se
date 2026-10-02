---
title: ESENT Error When Modifying OpsMgr Agent
date: 2010-03-19 10:34:17
lastmod: 2018-08-28T15:16:14+02:00
url: /ms/opsmgr2007/esent-error-when-modifying-opsmgr-agent/
url_encoded: /ms/opsmgr2007/esent-error-when-modifying-opsmgr-agent/
cats:
  - ms
  - ms/opsmgr2007
tags:
  - Windows
  - OpsMgr
  - Errors
  - How-To
  - Windows Installer
  - WMI
hexo_id: 260
---

Getting `ESENT Kerys are required to install this application` when you are trying to modify/change an agent installation?

![ESENT Error Dialog](/wp-content/uploads/2010/03/image_thumb.png "ESENT Error Dialog")

This seems to be  most common on Windows 2008 and i guess it’s because of the UAC and the fact that opening the Control Panel isn’t running in administrative mode.

To work around this you need to run the msiexec command on the correct installation GUID from an administrative command prompt.

Besides running through the registry to find the GUID, one of the easier ways is this:

1. Open an administrative command prompt.
2. run `wmic product`
3. Locate your product by its name, the GUID (looks a bit like this `{25097770-2B1F-49F6-AB9D-1C708B96262A}`) directly after that is the one you want. Copy it.
4. run `msiexec /i <PASTEYOURGUIDHERE>`
5. Modify the agent as pleased

That’s pretty much it. Good luck.