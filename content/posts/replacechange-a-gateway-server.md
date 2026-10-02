---
title: Replace/Change a Gateway Server
date: 2009-09-24 12:32:35
year: "2009"
month: "09"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/replacechange-a-gateway-server/
description: Description of problem If you are looking into replacing an (or just switching to another primary) Operations Manager 2007 Gateway Server for any reason, there’s a little more to consider than just r
excerpt: "Description of problem If you are looking into replacing an (or just switching to another primary) Operations Manager 2007 Gateway Server for any reason, there’s a little more to consider than just right-clicking the clients and selecting “Change Primary Management Server” in the Operations Console. You could end up with agents not being able to connect to the Management Group at all due to a small problem with the order in which Operations Manager do things. Here’s basically what happens: You tell Operations Manager to change Primary Management Server for AGENTX from GW1 to GW2. The SDK Service (i guess) tells GW1 that “You’re no longer the Primary Management Server for AGENTX” GW1 acknowledges this and stops talking to AGENTX. And I mean Completely stops talking to AGENTX. OpsMgr then tells GW2 to start accepting communication from AGENTX. OpsMgr tries to tell AGENTX that it should talk to GW2 since GW1 won’t listen. Spotted the problem? This modus operandi probably works when agents are on the same network and in the same domain where fail-over is sort of automatic. The problem we are facing now is that the server are telling the Gateway to stop accepting communications to and from the agent before the agent is notified that there is a new Gateway server to talk to. The agent will continue to talk to GW1 but will be completely ignored and you will probably start seeing events in the Operations Manager eventlog on GW1 with EventID 20000. How do I get around this little feature then? No matter if you found this article after running into the mentioned troubles or if you are googling ahead of time to be prepared, the fix is the same and consists of a few powershell scripts. These scripts are out there allready, but in different contexts, hence this post. First step: Install the new Gateway Documentation on this from Microsoft is good enough, but here’s the short version. Verify name resolution to and from Gateway server and Management Server Create certificate for the Gateway server Approve the Gateway server Install Gateway server Import certificates on Windows system Run MOMCertImport.exe on Gateway server to add the certificate into Gateway server configuration Wait"
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - PoSH
  - Script
  - How-To
---

# Description of problem

If you are looking into replacing an (or just switching to another primary) Operations Manager 2007 Gateway Server for any reason, there's a little more to consider than just right-clicking the clients and selecting "Change Primary Management Server" in the Operations Console.
You could end up with agents not being able to connect to the Management Group at all due to a small problem with the order in which Operations Manager do things.

Here's basically what happens:

1. You tell Operations Manager to change Primary Management Server for AGENTX from GW1 to GW2.
1. The SDK Service (i guess) tells GW1 that "You're no longer the Primary Management Server for AGENTX"
1. GW1 acknowledges this and stops talking to AGENTX.  And I mean _Completely_ stops talking to AGENTX.
1. OpsMgr then tells GW2 to start accepting communication from AGENTX.
1. OpsMgr tries to tell AGENTX that it should talk to GW2 since GW1 won't listen.

Spotted the problem?
This modus operandi probably works when agents are on the same network and in the same domain where fail-over is sort of automatic.  The problem we are facing now is that the server are telling the Gateway to stop accepting communications to and from the agent _before_ the agent is notified that there is a new Gateway server to talk to. The agent will continue to talk to GW1 but will be completely ignored and you will probably start seeing events in the Operations Manager eventlog on GW1 with EventID 20000.

How do I get around this little _feature_ then?

No matter if you found this article after running into the mentioned troubles or if you are googling ahead of time to be prepared, the fix is the same and consists of a few powershell scripts. These scripts are [out there](http://www.systemcentercentral.com/Forums/tabid/60/IndexID/19305/Default.aspx#vwcComments19305 "System Center Central") allready, but in different contexts, hence this post.

## First step:  Install the new Gateway

[Documentation on this](http://technet.microsoft.com/en-us/library/bb432149.aspx "Deploying Gateway Server in the Multiple Server, Single Management Group Scenario") from Microsoft is good enough, but here's the short version.

1. Verify name resolution to and from Gateway server and Management Server
1. [Create certificate](http://technet.microsoft.com/en-us/library/bb735408.aspx "Authentication and Data Encryption for Windows Computers in Operations Manager 2007") for the Gateway server
1. Approve the Gateway server
1. Install Gateway server
1. Import certificates on Windows system
1. Run MOMCertImport.exe on Gateway server to add the certificate into Gateway server configuration
1. Wait

The wait is for the gateway server to get all needed configuration from RMS and to download all neccesary management packs, run all the discovery scripts and so on. When the Operations Manager event log has calmed down a bit, move to step two.

## Second step: Configure Agent Failover

Connect to an Operations Manager Command Shell. Any will do, as long as it's connected to the correct Management Group.
Then run the following script:

```powershell
$primaryGW= Get-ManagementServer | where {$_.Name -eq 'GW2.domain.local'}
$failoverGw = Get-ManagementServer | where {$_.Name -eq 'GW1.domain.local'}
$agents = Get-Agent | where {$_.primarymanagementservername -eq 'GW1.domain.local'}
Set-ManagementServer -AgentManagedComputer: $agents -PrimaryManagementServer: $primaryGW -FailoverServer: $failoverGw
```

Remember to change "GW1.domain.local" to you OLD Gateway servername and "GW2.domain.local" to your NEW Gateway servername.

If you don't know powershell, this script basically configures all agents using the old Gateway to use the new one as primare, but keep the old one as a fail-over server. The Gateways will still get to know the changes before the agents, but since the old on is still listening to the agents (though, as the fail-over host) it will be able to tell them to go to the new one, GW2.