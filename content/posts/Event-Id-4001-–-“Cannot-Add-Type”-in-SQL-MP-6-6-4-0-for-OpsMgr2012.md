---
title: Event Id 4001 – “Cannot Add Type” in [#SQL] MP 6.6.4.0 for [#OpsMgr2012]
date: 2016-02-15 12:22:28
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2012/Event-Id-4001-–-“Cannot-Add-Type”-in-SQL-MP-6-6-4-0-for-OpsMgr2012/
url_encoded: /ms/opsmgr2012/Event-Id-4001-%E2%80%93-%E2%80%9CCannot-Add-Type%E2%80%9D-in-SQL-MP-6-6-4-0-for-OpsMgr2012/
cats:
  - ms
  - ms/opsmgr2012
tags:[]
migration_notes: singular `category:` key
---

Was troubleshooting this little error message for a customer after deploying the SQL Server Management Pack version 6.6.4.0.

The event is the generic "Health Service Script" with id 4001.

```text
Management Group: REDACTED. Script: Main Module: CPUUsagePercentDataSource.ps1 :
Computer Name = "REDACTED.redacted.com" WMI = "ComputerManagement11" Service Name = "MSSQLSERVER" SQL Instance Name = "MSSQLSERVER"
Error occured during CPU Usage for SQL Instances data source executing.
Computer: REDACTED
Reason: Cannot add type. Compilation errors occurred.
Position:256
Offset:21
Detailed error output: Cannot add type. Compilation errors occurred.
--------
(0) : No source files specified

(1) : using System;

--------
(0) : Source file "C:\Windows\TEMP\njdqtgfb.0.cs" could not be found

(1) : using System;
```

There are some known errors to the 6.6.4.0 version of the SQL management packs, and one of them does mention *"Cannot add type. Compilation errors occured."*
In a [thread on the Technet Forums](https://social.technet.microsoft.com/Forums/en-US/operationsmanagergeneral/thread/92796ead-739d-4128-9afb-1e6f770099d6/#3004a2fc-88ad-4c74-936a-8ed3c8aa70fa) it was suggested that it has to do with rights, but focusing mainly on the SQL instance. What caught our eyes, however, was the fact that the script is using the `C:\Windows\TEMP` folder instead of its private one. And this seems to be because it is using a few .Net components that do some sort of JIT compilation.
We took a quick look using *procmon*, filtered on C:\Windows\TEMP\ and yes indeed. The monitoring account used is trying to create and delete its temporary files in that very folder.

# A wild work-around appears!

The work-around is simple, but cumbersome. Just make sure that the assigned RunAs account have read/write/delete rights on C:\Windows\TEMP.
Now you just have to manage this on all your SQL-servers! (yaaaay)