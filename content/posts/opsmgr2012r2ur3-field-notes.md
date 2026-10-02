---
title: OpsMgr 2012 R2 UR3 - Field Notes [#opsmgr]
date: 2014-09-02 11:30:18
year: "2014"
month: "09"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2012/opsmgr2012r2ur3-field-notes/
description: Quick and unrefined notes on Update Roll-up 3 for System Center 2012 R2 - Operations Manager.  Preparation Usual routine, check the KB for instructions and known issues. Double-check with Holman’s blo
excerpt: Quick and unrefined notes on Update Roll-up 3 for System Center 2012 R2 - Operations Manager. Preparation Usual routine, check the KB for instructions and known issues. Double-check with Holman’s blog and take note of any irregularities. Download, curse your favourite deity and re-try in IE. Unpack the CAB-files (why do you keep putting them in CAB-files?) and throw away all the unnecessary language-specific console patches. Notify affected parts of the organisation, I’ve had the benefit to work with good release managers at all clients so far, so no biggie. Then try to close as many consoles as possible to avoid any blocks in database. Make sure you have the credentials for the Data Access service account at hand. Issues - So Far (updated 2014-09-02) The SQL Script for the OpsDW was deadlocked at all sites and customers without exception. It’s easily fixed by stopping the management server services. A few dashboards (the 2012 versions) went blank. Self-healed after some aggregation job over night. From what I’ve noticed, only the SLA Dashboards are affected but never all of them. Agents behind daisy-chained Gateways is not identified as in need of an update. “Repairing” them from the Console is one work-around that seems to work consistently. A few agents that was updated using Windows Update did not report as updated. Repair fixed that nuisance. Had to flush the cache on a few Gateways to avoid heartbeat failures from their agents. Only daisy-chained ones if I recall correctly.
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - Field Notes
  - Update Rollup
---

_Quick and unrefined notes on Update Roll-up 3 for System Center 2012 R2 - Operations Manager._

## Preparation

Usual routine, check the [KB](http://support.microsoft.com/kb/2965445 "Update Roll-up 3 for System Center 2012 R2 Operations Manager") for instructions and known issues. Double-check with [Holman's](http://blogs.technet.com/b/kevinholman/archive/2014/08/07/ur3-for-scom-2012-r2-step-by-step.aspx "UR3 for SCOM 2012 R2 – Step by Step") blog and take note of any irregularities. 
[Download](http://catalog.update.microsoft.com/v7/site/Search.aspx?q=2965445 "Hell-spawn"), curse your favourite deity and re-try in IE. Unpack the CAB-files (why do you keep putting them in CAB-files?) and throw away all the unnecessary language-specific console patches.

Notify affected parts of the organisation, I've had the benefit to work with good release managers at all clients so far, so no biggie. Then try to close as many consoles as possible to avoid any blocks in database.

Make sure you have the credentials for the Data Access service account at hand.

### Issues - So Far

_(updated 2014-09-02)_

*   The SQL Script for the OpsDW was deadlocked at all sites and customers without exception. It's easily fixed by stopping the management server services.</p>
*   A few dashboards (the 2012 versions) went blank. Self-healed after some aggregation job over night. From what I've noticed, only the SLA Dashboards are affected but never all of them.

*   Agents behind daisy-chained Gateways is not identified as in need of an update. "Repairing" them from the Console is one work-around that seems to work consistently.

*   A few agents that was updated using Windows Update did not report as updated. Repair fixed that nuisance.

*   Had to flush the cache on a few Gateways to avoid heartbeat failures from their agents. Only daisy-chained ones if I recall correctly.


<a id="more"></a>



## Planning

<p>UR3 is like most update roll-ups you've seen so far. There's a bunch of <abbr title="Microsoft Patch">msp</abbr> files you install on the different server roles, a few SQL-scripts for the OpsDB and the OpsDW and some updated core management packs. I have used the following order and that has worked quite nicely.

*   Management Servers (and locally installed consoles)
*   SQL-Scripts
*   Management Packs<sup id="fnref-818-2">[1](#fn-818-2)</sup>
*   Consoles<sup id="fnref-818-1">[2](#fn-818-1)</sup>
*   Gateway Servers<sup id="fnref2:818-1">[2](#fn-818-1)</sup>
*   Web Console<sup id="fnref3:818-1">[2](#fn-818-1)</sup>
*   Agents<sup id="fnref4:818-1">[2](#fn-818-1)</sup>

The first management server takes the longest time as it will update the databases as well and you _must_ wait for it to complete before hitting any extra management servers. Otherwise the databases isn't marked as updated and multiple installations will try to update the same stuff at the same time, and that's generally bad. I'd recommend to never update more than one management server at the same time, although it is possible.

## Installation

### Management Servers

Fairly straight-forward. Run the <abbr title="Microsoft Patch">msp</abbr>-file for the server update in an administrative command prompt and follow the wizard. First server takes a while (anything from 10-40 minutes depending on management group size and load in my experience). When that's done, move on to the next management server. If your management servers have multiple roles, like Console, Web Console or Reporting, go ahead and update those at once.

### SQL-Scripts

The scripts are unpacked by the setup. You will find them under `%SystemDrive%\Program Files\System Center 2012 R2\Operations Manager\Server\SQL Script for Update Rollups`. Do OpsDW first using the `UR_Datawarehouse.sql` script, then go for OpsDB using `Update_rollup_mom_db.sql`. I've gotten the deadlock error on all installations so far and the best way to avoid that is to stop the management server services for this part. It's _absolutely crucial_ to have the scripts run to successful completion before running the next or moving on to any other server roles.

### Console

Nothing out of the ordinary here, make sure you run the Console <abbr title="Microsoft Patch">msp</abbr> in an administrative command prompt.

### Management Packs

The updated core management packs are unpacked into `%SystemDrive%\Program Files\System Center 2012 R2\Operations Manager\Server\Management Packs for Update Rollups`. Import them using one of the updated consoles.

### Gateway

Next-next-next if running as administrator. Take effort to verify that the agent updates has been distributed into the `%SystemDrive%\Program Files\System Center Operations Manager\Gateway\AgentManagement\<architecture>` folder. If not, copy them from the same folder from any of the management servers.

### Web Console

No problems so far as long as you run the Web Console <abbr title="Microsoft Patch">msp</abbr> as administrator.

### Agents

Update them as usual, using "Pending Management", windows update, manual installation, <abbr title="System Center Configurations Manager">SCCM</abbr> or whatever method you usually employ. Agent version will not be updated in the Console, but it will be visible under `Monitoring/Operations Manager/Agent Management/Agents by Version`.

## Summary

Fairly simple update, the SQL Scripts can catch your off-guard if you do not know about them. Had some issues with Gateways, but it's a pretty quick update in most environments. Have not experienced any reboots or service outages on updated systems.

GLHF!

<div class="footnotes">

* * *

1.  You're going to need at least one updated console to import the MP-updates. [↩](#fnref-818-2)

2.  These can all be executed in parallel, agents behind Gateways will obviously need to be updated _after_ the gateway. [↩](#fnref-818-1) [↩](#fnref2:818-1) [↩](#fnref3:818-1) [↩](#fnref4:818-1)
</div>