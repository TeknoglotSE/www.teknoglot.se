---
title: "OpsMgr 2012 Agent & Gateway Failover - The Basics [#opsmgr, #powershell]"
date: 2012-05-30 14:12:37
year: "2012"
month: "05"
lastmod: 2017-06-05T10:13:43+02:00
url: /ms/opsmgr2012/opsmgr-2012-agent-gateway-failover-the-basics/
url_encoded: /ms/opsmgr2012/opsmgr-2012-agent-gateway-failover-the-basics/
description: I have previously posted a few scripts on managing and configuring fail-over management servers on gateways and agents in System Center Operations Manager 2007 R2. Now that System Center 2012 Operatio
hexo_slug: opsmgr-2012-agent-gateway-failover-the-basics
excerpt: I have previously posted a few scripts on managing and configuring fail-over management servers on gateways and agents in System Center Operations Manager 2007 R2. Now that System Center 2012 Operations Manager is RTM and users are starting to explore the differences between the versions I see more and more questions on how you do, in OpsMgr 2012, what you did in OpsMgr 2007. In a few posts henceforth I will go through Agent and Gateway server fail-over configuration and management. In this first post I’ll look at the very basics of fail-over configuration, the cmdlets to use and some one-liners.
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - PoSH
  - How-To
  - Fail-over
  - Scripts
hexo_id: 659
---

I have [previously](http://www.teknoglot.se/ms/opsmgr2007/replacechange-a-gateway-server/ "Replace/Change a Gateway Server") posted a few [scripts](http://www.teknoglot.se/ms/opsmgr2007/change-gateway-powershell-script/ "Change Gateway Powershell Script") on managing and [configuring fail-over](http://www.teknoglot.se/ms/opsmgr2007/loadbalancing-ps-script-opsmgr/ "“Load Balancing” Powershell Script for Operations Manager") management servers on gateways and agents in System Center Operations Manager 2007 R2.

Now that System Center 2012 Operations Manager is RTM and users are starting to explore the differences between the versions I see more and more questions on how you do, in OpsMgr 2012, what you did in OpsMgr 2007. In a few posts henceforth I will go through Agent and Gateway server fail-over configuration and management. In this first post I'll look at the very basics of fail-over configuration, the cmdlets to use and some one-liners.

<!--more-->

### The cmdlet

First of all, the cmdlets of OpsMgr powershell have all got new names looking like _Verb_-SCOM_noun_ and to list them all in the console you can execute the following command:

```powershell
get-command *SCOM*
```

The cmdlet we are looking for to set and manage primary and fail-over management servers is

```powershell
Get-SCOMParentManagementServer
```

As usual, you can pass the cmdlet as a parameter to get-help for information about its parameters and a few use-cases.
> **SYNOPSIS**
> 
> Changes the primary and failover management servers for an agent or gateway management server.
> 
> 
> **SYNTAX**
> 
> Set-SCOMParentManagementServer -Agent -PrimaryServer [-PassThru ] [-Confirm ] [-WhatIf ] []
> 
> Set-SCOMParentManagementServer -Agent -FailoverServer [-PassThru ] [-Confirm ] [-WhatIf ] []
> 
> Set-SCOMParentManagementServer -GatewayServer -FailoverServer [-PassThru ] [-Confirm ] [-WhatIf ] []
> 
> Set-SCOMParentManagementServer -GatewayServer -PrimaryServer [-PassThru] [-Confirm] [-WhatIf] []
But that's so boring to read the manual is a bit sketchy on how it behaves and the limitations.

#### The One-Liners!

I have compiled a few examples for a few common tasks to better illustrate it's uses.

##### Set Primary Management Server on Agent

```powershell
#Set Primary Management Server on Agent
Set-SCOMParentManagementServer -Agent (Get-SCOMAgent -DNSHostName "AGENT.domain.local") -PrimaryServer (Get-SCOMManagementServer -Name "SCOMMS01.domain.local")
```

##### Set Fail-over Management Server on Agent

```powershell
#Set Fail-over Management Server on Agent
Set-SCOMParentManagementServer -Agent (Get-SCOMAgent -DNSHostName "AGENT.domain.local") -FailoverServer (Get-SCOMManagementServer -Name "SCOMMS02.domain.local")
```

##### Set Primary Management Server on Gateway

```powershell
#Set Primary Management Server on Gateway
Set-SCOMParentManagementServer -GatewayServer (Get-SCOMGatewayManagementServer -Name "SCOMGW01.domain.local") -PrimaryServer (Get-SCOMManagementServer -Name "SCOMMS01.domain.local")
```

##### Set Fail-over Management Server on Gateway

```powershell
#Set Fail-over Management Server on Gateway
Set-SCOMParentManagementServer -GatewayServer (Get-SCOMGatewayManagementServer -Name "SCOMGW01.domain.local") -FailoverServer (Get-SCOMManagementServer -Name "SCOMMS02.domain.local")
```

#### A few reflections

As you may notice, if you have used the OpsMgr 2007 `Set-ManagementServer` cmdlet you actually have to use separate parameters depending on whether you are configuring management servers on an agent or a gateway server. You probably also noticed that to get an object for a gateway server you also have to use `Get-SCOMGatewayManagementServer` in OpsMgr 2012.

For some reason, there's different properties on agent objects compared to management and gateway servers. On an MS or GW, you use `-Name` to select by name, while on an agent you have to use `-DNSHostName`. Both of these parameters take wild-cards making it possible to find all the agents named "*.domain.local".

While `-PrimaryServer` only takes a single object the `-Agent`, `-GatewayServer` and `-FailoverServer` can take an array or collection of objects.

One more "gotcha" I ran into is the fact that trying to set both` -PrimaryServer` and `-FailoverServer` in the same command will fail with an "AmbiguousParameterSet" error. You have to run it once for the Primary Management Server and once for your Fail-over Management Servers.

### Related Snippets

Apart from setting your management servers you might also want to read your agent's current configuration as well.

##### Get current Primary Management Server on Agent

```powershell
#Get current Primary MS on Agent
$agent = Get-SCOMAgent -DNSHostName "AGENT.domain.local"
$primaryMS = $agent.GetPrimaryManagementServer()
write-host "Current Primary ManagementServer: "$primaryMS.Name
```

##### Get current Failover Management Server on Agent

```powershell
#Get current Failover MS on Agent
$agent = Get-SCOMAgent -DNSHostName "AGENT.domain.local"
$failoverMSs = $agent.GetFailoverManagementServers()
write-host "Got"$failoverMSs.Count"failover Management Servers"
foreach($failoverMS in $failoverMSs) {
 $failoverMS.Name
}
```

I think that would be all for this post. Next one will touch on a little more intelligence and a few ways to automatically select "other" management servers as fail-over management servers.

Enjoy!