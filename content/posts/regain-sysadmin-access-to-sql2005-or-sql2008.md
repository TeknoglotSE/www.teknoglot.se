---
title: (re)Gain sysadmin access to SQL2005 or SQL2008
date: 2009-11-19 14:08:10
lastmod: 2016-06-14T13:18:36+02:00
url: /ms/sql/regain-sysadmin-access-to-sql2005-or-sql2008/
description: In SQL Server 2005 and 2008 the local Administrators account is not sysadmin by default. This makes it even more important that the one setting up the Database also remembers to add a SQL Server admin
excerpt: "In SQL Server 2005 and 2008 the local Administrators account is not sysadmin by default. This makes it even more important that the one setting up the Database also remembers to add a SQL Server admins group to the sysadmin role. If this step is forgotten, the user installing the database server is the only one that will ever be sysadmin. In some extreme cases I’ve seen situations where no one except some dude on vacation is sysadmin and I need to install or upgrade a bunch of applications and services. In these cases I have also been assigned Local Administrator rights on the server, but since the local Administrators group isn’t sysadmin either I still cannot login to the SQL server. What to do!? Thanks to Raul Carcia’s blog post it’s not that a big deal. The instructions are written for SQL Server 2005 but works equally fine on SQL Server 2008 and the only pre-requirement is that you are a local server administrator. Here’s what to do: Open the SQL Server Configuration Manager. In SQL Server Services, open the properties for the SQL Server instance you need access to. In the Advanced tab, find Startup Parameters. Add “;-m” to the end of that line. Press OK and restart the SQL Server into “Maintenance Mode” or “Single User Mode” if you like. (check that a restart is OK first 😉) Open a command prompt (right-click, “Run as Administrator” in Windows 2008) and go to C:\\Program Files\\Microsoft SQL Server\\100\\Tools\\Binn (C:\\Program Files\\Microsoft SQL Server_90_\\Tools\\Binn for SQL2005) Execute sqlcmd /A /E /S <INSTANCE> (use . for local default instance and .INSTANCE for local named instance) In the CLI, execute: EXEC sp_addsrvrolemember 'DOMAIN\\yourusername', 'sysadmin';GO Return to the SQL Server Configuration Manager and restore the Startup Parameters to it’s previous settings. Restart the SQL Server instance to allow users to get access to it again. Now, you should be able to login to the SQL server with sysadmin rights using your current user. This would also be a good time to actually set up a SQL Server Admins group (local or domain) to add to the sysadmin role to avoid having others to the above steps when you, yourself, are on vacation. 😉 As Raul Carcia point out in his original post, this is really a disaster recovery procedure and there’s definitely nothing sneaky about it since it leaves a lot of trails in the event logs. All in all, a Great article by Raul and all credit should go his way."
cats:
  - ms
  - ms/sql
tags:
  - How-To
  - SQL Server
  - SQL Server 2005
  - SQL Server 2008
---

In SQL Server 2005 and 2008 the local Administrators account is not sysadmin by default. This makes it even more important that the one setting up the Database also remembers to add a SQL Server admins group to the sysadmin role. If this step is forgotten, the user installing the database server is the only one that will ever be sysadmin.

In some extreme cases I’ve seen situations where no one except some dude on vacation is sysadmin and I need to install or upgrade a bunch of applications and services. In these cases I have also been assigned Local Administrator rights on the server, but since the local Administrators group isn’t sysadmin either I still cannot login to the SQL server.
What to do!?

Thanks to [Raul Carcia’s blog post](http://blogs.msdn.com/raulga/archive/2007/07/12/disaster-recovery-what-to-do-when-the-sa-account-password-is-lost-in-sql-server-2005.aspx) it’s not that a big deal. The instructions are written for SQL Server 2005 but works equally fine on SQL Server 2008 and the only pre-requirement is that you are a local server administrator.
Here’s what to do:

1. Open the _SQL Server Configuration Manager._
3. In _SQL Server Services_, open the properties for the SQL Server instance you need access to.
4. In the _Advanced_ tab, find _Startup Parameters_.
5. Add “;-m” to the end of that line.
6. Press OK and restart the SQL Server into “Maintenance Mode” or “Single User Mode” if you like. (check that a restart is OK first ;))
7. Open a command prompt (right-click, “Run as Administrator” in Windows 2008) and go to C:\Program Files\Microsoft SQL Server\100\Tools\Binn
(C:\Program Files\Microsoft SQL Server\_90_\Tools\Binn for SQL2005)
7. Execute `sqlcmd /A /E /S <INSTANCE>`  
  (use . for local default instance and .INSTANCE for local named instance)
8. In the CLI, execute:

  ```sql
  EXEC sp_addsrvrolemember 'DOMAIN\yourusername', 'sysadmin';
  GO
  ```
9. Return to the _SQL Server Configuration Manager_ and restore the _Startup Parameters_ to it’s previous settings.
10. Restart the SQL Server instance to allow users to get access to it again.

Now, you should be able to login to the SQL server with sysadmin rights using your current user. This would also be a good time to actually set up a SQL Server Admins group (local or domain) to add to the sysadmin role to avoid having others to the above steps when you, yourself, are on vacation. ;)

As Raul Carcia point out in his original post, this is really a disaster recovery procedure and there’s definitely nothing sneaky about it since it leaves a lot of trails in the event logs.

All in all, a Great article by [Raul](http://blogs.msdn.com/raulga/) and all credit should go his way.