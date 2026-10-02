---
title: OpsMgr 2012 R2 UR4 - Field Notes [#opsmgr]
date: 2014-10-30 11:41:47
year: "2014"
month: "10"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2012/opsmgr-2012-r2-ur4-field-notes/
description: Quick and unrefined notes on Update Roll-up 4 for System Center 2012 R2 - Operations Manager  Preparation The usual routine applies. Check the KB for instructions and take not of known issues. Check i
excerpt: "Quick and unrefined notes on Update Roll-up 4 for System Center 2012 R2 - Operations Manager Preparation The usual routine applies. Check the KB for instructions and take not of known issues. Check if Kevin Holman has written something about it. As this is an update roll up, I pre-emptively expect that gotchas in UR3 may apply. Remember to open the update catalog in IE as the downloader is not working in other browsers. Download, unpack, toss what languages that does not apply to your organization. It is advised to disable any mail-generating alert subscriptions during the upgrade process to avoid unnecessary spammage. Issues - So Far [updated: 2014-11-03] Got a few problems with cross-platform monitoring templates not working after the update. This was due to missing files in the update package. Make sure you download the updated version! Have not updated a customer using gateways yet, so unless they have fixed the issues in UR3, expect an update to this section soon. Planning"
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - Field Notes
  - Update Rollup
---

_Quick and unrefined notes on Update Roll-up 4 for System Center 2012 R2 -
Operations Manager_

## Preparation

The usual routine applies. Check the [KB](http://support.microsoft.com/kb/2992020) for instructions and take not of
known issues. Check if [Kevin Holman](http://blogs.technet.com/b/kevinholman/) has written something about it. As this
is an update _roll up_, I pre-emptively expect that [gotchas in UR3](http://www.teknoglot.se/ms/opsmgr2012/opsmgr2012r2ur3-field-notes/) may
apply. Remember to open the update catalog in IE as the downloader is not
working in other browsers.

Download, unpack, toss what languages that does not apply to your organization.

It is advised to disable any mail-generating alert subscriptions during the
upgrade process to avoid unnecessary spammage.

## Issues - So Far

[updated: 2014-11-03]

*   Got a few problems with cross-platform monitoring templates not working after the update. This was due to [missing files](https://social.technet.microsoft.com/Forums/en-US/e2378c57-02fb-43ac-b263-f28f26e21161/2012-r2-ur4-missing-files) in the update package. Make sure you download the [updated version](http://www.microsoft.com/en-us/download/details.aspx?id=29696)!

Have not updated a customer using gateways yet, so unless they
have fixed the issues in UR3, expect an update to this section soon.

## Planning

As with all update roll-ups, you've got a number of MSP files to install on
the different server roles, some SQL-scripts for the OpsDB and OpsDW and a few
updated management packs. I've updated the components in the following order.

*   Management Servers (and consoles installed on them)
*   SQL-Scripts
*   Management Packs (might need an updated console for this)
*   Consoles
*   Gateway Servers
*   Web Console
*   Agents

As usual, the first management server update takes the longest as that's
when the process is updating the databases. You absolutely _must_ wait for it to
complete before updating anything else. Feel free to prepare the other
management servers by copying installations files, logging in and starting up
your command prompts as admin. I never update more than one management server at
the time anyway. Less to worry about that way.

## Installation

### Management Servers

Open a command prompt (powershell will work just fine) as Administrator and
execute the MSP-file. First management server will take some time, so be
patient. If a management server has multiple roles, you can update those while
logged in as well.

### SQL-Scripts

The installation package will unpack these scripts under `%SystemDrive%\Program
Files\System Center 2012 R2\Operations Manager\Server\SQL Script for Update
Rollups`. Run the `UR_Datawarehouse.sql` one on the OpsDW first, then the
`Update_rollup_mom_db.sql` on OpsDB. If you're getting deadlocks, try again. If
that don't help, stop the management server services and try again. _Do not
continue with the next script ​until you've succeeded with the first._

If you've installed UR3, the OpsDW-script is pretty quick (not sure if
it's changed at all) and the OpsDB is a bit less prone to deadlocks.

### Management Packs

Just import the management packs from the %SystemDrive%\Program Files\System
Center 2012 R2\Operations Manager\Server\Management Packs for Update Rollups
folder. Might have to retry as the console can do a little poor job of
calculating the dependencies.

### Console

The easiest one, just install the MSP-file.

### Gateway

Installation is a breeze. Make sure to check `%SystemDrive%\Program Files\System
Center Operations Manager\Gateway\AgentManagement\<architecture>` for updated
agent files. If not, copy from same folder on any management server.

### Web Console

Installation is very simple. Install the MSP from an administrative command
prompt. If you're affected by [KB911722](http://support.microsoft.com/kb/911722) and need the web console fixes, you
need to edit `%windir%\Microsoft.NET\Framework64\v2.0.50727\CONFIG\web.config`
by adding the following line:

`<machineKey validationKey="AutoGenerate,IsolateApps"
decryptionKey="AutoGenerate,IsolateApps" validation="3DES" decryption="3DES"/>`

### Agents

Normal update procedure applies. Use "Pending Management", SCCM, manual
installations or whatever method you'd like.

## Summary

If you already have UR3, this one is very quick. If you are updating a fresh
installation, wait a day or your management group may end up uninitialized for
reasons. Remember to enable your subscriptions when done.
 

GLHF!