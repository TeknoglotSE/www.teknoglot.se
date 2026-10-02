---
title: "#OpsMgr 1801 Upgrade - The Fail Anthology"
date: 2018-08-27 15:42:17
lastmod: 2019-07-30T16:15:14+02:00
url: /ms/opsmgr2016/om1801-upgrade-gotchas/
url_encoded: /ms/opsmgr2016/om1801-upgrade-gotchas/
cats:
  - ms
  - ms/opsmgr2016
tags:
  - OpsMgr 1801
  - OpsMgr 2016
  - Upgrade
  - Issues
  - Rant
migration_notes: front-matter `s:` key (typo for slug); ignored by Hexo
---

# A Collection of OpsMgr Upgrade Fails

I'll be frank on this one; Microsoft really dropped the ball on the 1801 setup program.  
No upgrade or update has been this ridden with faults and obscure errors, not even the infamous SCOM 2007 SP1 setup. And this is not only errors that will abort the installation, they will actively remove your existing SCOM Components and cause a restore, either from snapshot/checkpoint or from backup. 

**MAKE SURE YOUR BACKUPS ARE WORKING!!!**

Rollbacks don't work in 1801, at all. You have been warned. 

Here's my list of the issues I've seen and wrestled so far.

## .NET 3.5 Pre-requisites

Although neither SCOM 2016 nor 1801 actually has a .NET 3.5 requirement, the setup think it does.  
The Prerequisute checker isn't aware though, meaning it will happily try to upgrade and then fail. And, boy, does it fail spectacularly!
When the upgrade failes, it's supposed to perform a rollback, and reading the setup log it actually do try.  
Unfortunatly, the "rollback" will remove any existing SCOM Roles in the server. O_o

Yes, thats right. Your Management Server is **no longer a Management Server**!

### Workaround

Make sure all SCOM Management Servers have .NET Framework 3.5 installed before attempting an upgrade. 

## Up-to-date Linux/Unix Management Packs (or worse, newer)

Oh, yes. If you have Linux management packs that are newer than what's included in the 1801 setup, this will fail the setup. Causing the same defunct "roll-back" that will **uninstall your Management Server**, but only after it mucks about in your databases for a bit. You'll need to **restore databases from backup** after this. 

### Workaround

There's a few ways to get around this, all done before attempting the upgrade:

- Downgrade your cross-platform management packs (yuck!)
- Import the version shipped with the setup (in the ManagementPack subfolder).
- Remove all Cross-platform management packs. 

## Updated OMS Management Pack (7.2.12026.0, released 2018-07-25)

This is really the same fault as with the cross-platform management packs, but since this is announced without any other notices other than "import if you need to" I decided to put this in a separate part. 

Here's the [release blog](https://blogs.technet.microsoft.com/momteam/2018/07/25/microsoft-system-center-operations-manager-management-pack-to-configure-operations-management-suite/) and the [SCOM 2016 version](https://www.microsoft.com/en-us/download/details.aspx?id=57172) of the updated OMS MP. 

Once again, the setup is unable to handle that already existing management packs is newer than what's provided with the 1801 setup. Instead of skipping, it will fail the installation with a, you guessed it, **uninstalled Management Server** and **semi-upgraded databases** as the result.  
Hello backup, old friend.

In the OpsMgrSetupWizard.log file you'll spot something similar to this:
```
[11:27:09]:	Info:	:Info:FirstManagementServer: Importing Management Pack: Microsoft System Center Advisor
[11:27:09]:	Always:	:ImportManagementPack: Loading management pack C:\install\OM1801\Setup\AMD64\..\..\ManagementPacks\Microsoft.SystemCenter.Advisor.mpb. 11:27:09
[11:27:10]:	Error:	:ImportManagementPack: Error: Unable to load management pack C:\install\OM1801\Setup\AMD64\..\..\ManagementPacks\Microsoft.SystemCenter.Advisor.mpb
[11:27:10]:	Error:	:: Verification failed with 3 errors:
-------------------------------------------------------
Error 1:
Found error in 2|Microsoft.SystemCenter.Advisor|7.2.12026.0|Microsoft.SystemCenter.Advisor|| with message:
Version 7.3.13142.0 of the management pack is not upgrade compatible with older version 7.2.12026.0. Compatibility check failed with 2 errors:

-------------------------------------------------------
Error 2:
Found error in 1|Microsoft.SystemCenter.Advisor/31bf3856ad364e35|1.0.0.0|Microsoft.SystemCenter.Advisor.Settings|| with message:
Publicly accessible ClassProperty (PortalLink) has been removed in the newer version of this management pack.
-------------------------------------------------------
Error 3:
Found error in 1|Microsoft.SystemCenter.Advisor/31bf3856ad364e35|1.0.0.0|Microsoft.SystemCenter.Advisor.Settings|| with message:
Publicly accessible ClassProperty (OmsBladeLink) has been removed in the newer version of this management pack.
-------------------------------------------------------


[11:27:10]:	Error:	:ImportManagementPack: Unknown Error. System.ArgumentException : The requested management pack is not valid. See inner exception for details.
Parameter name: managementPack
[11:27:10]:	Always:	:FirstManagementServer: Failed to load MP C:\install\OM1801\Setup\AMD64\..\..\ManagementPacks\Microsoft.SystemCenter.Advisor.mpb.  We will retry.
```

### Workaround

As with the cross-platform management packs, you basically have two options:

- Downgrade to the setup-provided version of the management pack
- [Remove the OMS/Advisor management packs](https://blogs.technet.microsoft.com/kevinholman/2016/03/26/how-to-remove-oms-and-advisor-management-packs/) alltogether.

## Operations Manager Reporting Upgrade

When the setup checks for existing products to upgrade, it successfully finds your Operations Manager Reporting (OMRS) installation. Great, you are now able to tick that checkbox that allow you to continue the upgrade.  
Unfortunately, the actual upgrade seems to be utterly unable to spot it, fails on upgrade and will "roll back" the installation. Since setup believes that there never was an OMRS on the server, it will return to that state. 

Meaning, **you no longer have an Operations Manager Reporting Server!**
(yay)

This one is not as critical as the others as you can simply install OMRS again, using the 1801 setup. 

### Workaround

Install the SCOM 2016 console on the OMRS before attempting your upgrade.  
Yeah, I know, this is stupid.

## Final thoughts

What the :shit::exclamation::question:  
What the hell is going on at Microsoft right now?

I've been a strong supporter of System Center Operations Manager as one of, if not *the*, best and solid Infrastructure and application monitoring solution currently available. Especially on Windows and Microsoft-heavy platforms. The upgrades and installations have been getting more and more solid and easy to perform. It's often been a case of "verify backups, hit play, wait".  
Up until 1801, that is. And it's not like in the old days, where an upgrade failure resulted in a slight headache and a bit of troubleshooting to find that little bit of config the documentation failed to mention. No, this one actively corrupts and removes your existing SCOM components, leaving you with the only option to restore from backups or start from scratch.

Ugh!
