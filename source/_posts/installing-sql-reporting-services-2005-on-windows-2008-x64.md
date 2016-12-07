---
title: Installing SQL Reporting Services 2005 on Windows 2008 x64
tags:
  - How-To
  - IIS7
  - Reporting Services
  - x64
  - OpsMgr 2007
id: 232
categories:
  - Microsoft
  - SQL Server
date: 2009-11-02 14:33:27
---

Let’s say you have followed this guide: [http://support.microsoft.com/kb/938245/](http://support.microsoft.com/kb/938245/ "http://support.microsoft.com/kb/938245/")

Still not working? The one thing I forgot, or rather did not find in any of the guides, was to change the website application pool to “Classic .NET AppPool”. It is actually noted in [KB938245](http://support.microsoft.com/kb/938245/) but only after the installation, during the configuration. For some reason I have not been able to install Reporting Services 2005 on Windows 2008 without changing this prior to the installation.

Maybe I am doing it wrong but this seems to be working all right for me.