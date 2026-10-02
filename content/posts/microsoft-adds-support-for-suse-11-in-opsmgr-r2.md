---
title: Microsoft Adds support for SUSE 11 in OpsMgr R2
date: 2009-10-16 07:59:10
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/microsoft-adds-support-for-suse-11-in-opsmgr-r2/
description: This update hasn’t showed up in the MP Catalog yet, but the System Center Operations Manager 2007 R2 Cross Platform Update can be downloaded here. Besides SUSE 11 support, here’s the short overview.
excerpt: "This update hasn’t showed up in the MP Catalog yet, but the System Center Operations Manager 2007 R2 Cross Platform Update can be downloaded here. Besides SUSE 11 support, here’s the short overview. The System Center Operations Manager 2007 R2 Cross Platform Update adds fixes for a defunct process issue on Unix/Linux Servers, as well as, adds support for SUSE Linux Enterprise Server 11 (both 32-bit and 64-bit versions) and Solaris Zone support. Feature Summary: The System Center Operations Manager 2007 R2 Cross Platform Update supports the monitoring of Unix/Linux Servers including: Monitoring of SUSE Linux Enterprise Server 11 servers (both 32-bit and 64-bit versions)* Support of Solaris Zones* Fix for defunct Process issue* The Cross Platform Agent may not discover soft partitions on Solaris systems. Therefore, the disk provider may be unloaded, and the Cross Platform Agent may stop collecting information from the system disks.* The Cross Platform Agent may not restart after the AIX server reboots. The latest versions of all the Operations Manager 2007 R2 Unix/Linux agents are included in this update. Perfect timing, I must say, since I really need this today. 😄 Update: This is no small MP-update, which probably is the reason that we do not find it in the MP Catalog, but a ~250MB OpsMgr R2 Software Update. You need to run this on all Operations Manager Servers (RMS/MS, GW?) since it actually updates many of the agent Cross Platform binaries. It does add a new MP för SUSE 11 that you have to import from disk if you need it. So, the installation goes somewhat like this: Install the Software Update (pick the right Architecture) on all OpsMgr R2 Servers Import the SUSE 11 MP if necessary Re-discover your Unix/Linux machines. Files updated in this update for R2:"
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Management Pack
  - X-Plat
  - SUSE 11
---

This update hasn’t showed up in the <acronym title="Management Pack">MP</acronym> Catalog yet, but the [System Center Operations Manager 2007 R2 Cross Platform Update can be downloaded here](http://www.microsoft.com/downloads/details.aspx?FamilyID=4a41a8be-0a37-4bd2-b5b1-026468b317fb).

Besides SUSE 11 support, here’s the short overview.
> The System Center Operations Manager 2007 R2 Cross Platform Update adds fixes for a defunct process issue on Unix/Linux Servers, as well as, adds support for SUSE Linux Enterprise Server 11 (both 32-bit and 64-bit versions) and Solaris Zone support.
> **Feature Summary:**
> The System Center Operations Manager 2007 R2 Cross Platform Update supports the monitoring of Unix/Linux Servers including:

> * Monitoring of SUSE Linux Enterprise Server 11 servers (both 32-bit and 64-bit versions)* Support of Solaris Zones* Fix for defunct Process issue* The Cross Platform Agent may not discover soft partitions on Solaris systems. Therefore, the disk provider may be unloaded, and the Cross Platform Agent may stop collecting information from the system disks.* The Cross Platform Agent may not restart after the AIX server reboots.

> The latest versions of all the Operations Manager 2007 R2 Unix/Linux agents are included in this update.

Perfect timing, I must say, since I really need this today. :D

***Update:***
This is no small MP-update, which probably is the reason that we do not find it in the MP Catalog, but a ~250MB OpsMgr R2 Software Update. You need to run this on all Operations Manager Servers (RMS/MS, GW?) since it actually updates many of the agent Cross Platform binaries. It does add a new MP för SUSE 11 that you have to import from disk if you need it.

So, the installation goes somewhat like this:

1. Install the Software Update (pick the right Architecture) on all OpsMgr R2 Servers
2. Import the SUSE 11 MP if necessary
3. Re-discover your Unix/Linux machines.

Files updated in this update for R2:

* .Microsoft.Enterprisemanagement.UI.Administration.dll (Version 6.1.7043.1)
* .AgentManagementUnixAgentsscx-1.0.4-248.aix.5.ppc.lpp.gz
* .AgentManagementUnixAgentsscx-1.0.4-248.aix.6.ppc.lpp.gz
* .AgentManagementUnixAgentsscx-1.0.4-248.hpux.11iv2.ia64.depot.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.hpux.11iv2.parisc.depot.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.hpux.11iv3.ia64.depot.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.hpux.11iv3.parisc.depot.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.rhel.4.x64.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.rhel.4.x86.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.rhel.5.x64.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.rhel.5.x86.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.sles.10.x64.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.sles.10.x86.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.sles.9.x86.rpm
* .AgentManagementUnixAgentsscx-1.0.4-248.solaris.10.sparc.pkg.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.solaris.10.x86.pkg.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.solaris.8.sparc.pkg.Z
* .AgentManagementUnixAgentsscx-1.0.4-248.solaris.9.sparc.pkg.Z

Files added:

* Microsoft.Linux.SLES.11.MP

All in all, the update contains the following fixes:

* KB969342
* KB973583
* Q954049
* Q956240