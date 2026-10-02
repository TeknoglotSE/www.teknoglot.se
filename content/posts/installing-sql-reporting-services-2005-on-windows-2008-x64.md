---
title: Installing SQL Reporting Services 2005 on Windows 2008 x64
date: 2009-11-02 14:33:27
year: "2009"
month: "11"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/sql/installing-sql-reporting-services-2005-on-windows-2008-x64/
url_encoded: /ms/sql/installing-sql-reporting-services-2005-on-windows-2008-x64/
description: "Let’s say you have followed this guide: http://support.microsoft.com/kb/938245/ Still not working? The one thing I forgot, or rather did not find in any of the guides, was to change the website applic"
hexo_slug: installing-sql-reporting-services-2005-on-windows-2008-x64
excerpt: "Let’s say you have followed this guide: http://support.microsoft.com/kb/938245/ Still not working? The one thing I forgot, or rather did not find in any of the guides, was to change the website application pool to “Classic .NET AppPool”. It is actually noted in KB938245 but only after the installation, during the configuration. For some reason I have not been able to install Reporting Services 2005 on Windows 2008 without changing this prior to the installation. Maybe I am doing it wrong but this seems to be working all right for me."
cats:
  - ms
  - ms/sql
tags:
  - How-To
  - IIS7
  - Reporting Services
  - x64
  - OpsMgr 2007
hexo_id: 232
---

Let’s say you have followed this guide: [http://support.microsoft.com/kb/938245/](http://support.microsoft.com/kb/938245/ "http://support.microsoft.com/kb/938245/")

Still not working? The one thing I forgot, or rather did not find in any of the guides, was to change the website application pool to “Classic .NET AppPool”. It is actually noted in [KB938245](http://support.microsoft.com/kb/938245/) but only after the installation, during the configuration. For some reason I have not been able to install Reporting Services 2005 on Windows 2008 without changing this prior to the installation.

Maybe I am doing it wrong but this seems to be working all right for me.