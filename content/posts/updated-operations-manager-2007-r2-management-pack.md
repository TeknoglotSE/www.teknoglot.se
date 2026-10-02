---
title: "Updated: Operations Manager 2007 R2 Management Pack"
date: 2009-10-14 11:29:00
year: "2009"
month: "10"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/updated-operations-manager-2007-r2-management-pack/
url_encoded: /ms/opsmgr2007/updated-operations-manager-2007-r2-management-pack/
description: "Microsoft released an updated MP (v6.1.7533.0, released on 10&#x2F;8&#x2F;2009) for monitoring the health the Operations Manager components. Most significant updates, according to me, would seem to be:  Fixed a"
hexo_slug: updated-operations-manager-2007-r2-management-pack
excerpt: "Microsoft released an updated MP (v6.1.7533.0, released on 10/8/2009) for monitoring the health the Operations Manager components. Most significant updates, according to me, would seem to be: Fixed an issue that was previously preventing all rules related to agentless exception monitoring from generating alerts. Added the rule “Collects Opsmgr SDK ServiceClient Connections” to collect the number of connected clients for a given management group. This data is shown in the view “Console and SDK Connection Count” under the folder “Operations ManagerManagement Server Performance”. Updated a number of monitors and rules to ensure that data is reported to the correct management group for multihomed agents. Fixed the configuration of the rule “IIS Discovery Probe Module Execution Failure” to so that the parameter replacement will now work correctly for alert suppression and generating the details of the alert’s description. The rest is mostly polishing, fine-tuning and complementary updates. Nothing really ground-breaking here, but still a welcome update. Download at: http://www.microsoft.com/downloads/details.aspx?FamilyID=61365290-3c38-4004-b717-e90bb0f6c148"
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Management Pack
hexo_id: 225
---

Microsoft released an updated <acronym title="Management Pack">MP</acronym> (v6.1.7533.0, released on 10/8/2009) for monitoring the health the Operations Manager components.

Most significant updates, according to me, would seem to be:
  > Fixed an issue that was previously preventing all rules related to agentless exception monitoring from generating alerts.
  > Added the rule “Collects Opsmgr <acronym title="Software Development Kit">SDK</acronym> ServiceClient Connections” to collect the number of connected clients for a given management group. This data is shown in the view “Console and SDK Connection Count” under the folder “Operations ManagerManagement Server Performance”.
  > Updated a number of monitors and rules to ensure that data is reported to the correct management group for multihomed agents.
  > Fixed the configuration of the rule “IIS Discovery Probe Module Execution Failure” to so that the parameter replacement will now work correctly for alert suppression and generating the details of the alert’s description.

The rest is mostly polishing, fine-tuning and complementary updates. Nothing really ground-breaking here, but still a welcome update.

Download at: [http://www.microsoft.com/downloads/details.aspx?FamilyID=61365290-3c38-4004-b717-e90bb0f6c148](http://www.microsoft.com/downloads/details.aspx?FamilyID=61365290-3c38-4004-b717-e90bb0f6c148 "http://www.microsoft.com/downloads/details.aspx?FamilyID=61365290-3c38-4004-b717-e90bb0f6c148")