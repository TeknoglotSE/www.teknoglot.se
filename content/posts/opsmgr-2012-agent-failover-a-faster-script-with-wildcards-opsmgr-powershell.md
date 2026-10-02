---
title: "OpsMgr 2012 Agent Failover – A Faster Script with Wildcards [#opsmgr, #powershell]"
date: 2012-06-28 14:28:36
year: 2012
month: 06
lastmod: 2017-06-05T10:13:43+02:00
url: /ms/opsmgr2012/opsmgr-2012-agent-failover-a-faster-script-with-wildcards-opsmgr-powershell/
url_encoded: /ms/opsmgr2012/opsmgr-2012-agent-failover-a-faster-script-with-wildcards-opsmgr-powershell/
description: Now we’re gonna make things even faster! In the previous post on the subject of Agent Fail-over in Operations Manager 2012 we created a script that will go through a selection of agents and make sure
excerpt: Now we’re gonna make things even faster! In the previous post on the subject of Agent Fail-over in Operations Manager 2012 we created a script that will go through a selection of agents and make sure that they all have up-to-date fail-over settings. We are doing the same thing in this one, but making it go faster. In my lab, it’s about five times faster in fact and I only have about 20 agents to play with. Not really a big deal, but scale it up a bit and add a few thousand agents and the pay-off will be very significant. As usual, the script will work as is, but it really is more to show the concept. You would have to add filtering to make sure you don’t mix agents behind gateway servers and agents behind management servers. Giving an agent behind a gateway a management servers as it’s fail-over server will likely not help you in any way. We will pretty quickly go “advanced” this time, so buckle up. 😉
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - PoSH
  - Script
  - Fail-over
hexo_id: 710
---

Now we're gonna make things even faster! In the [previous post](http://www.teknoglot.se/code/powershell/opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell/ "OpsMgr 2012 Agent Failover – Simple Script with Wildcards [#opsmgr, #powershell]") on the subject of [Agent Fail-over in Operations Manager 2012](http://www.teknoglot.se/series/om2012-failover-mgmt/) we created a script that will go through a selection of agents and make sure that they all have up-to-date fail-over settings. We are doing the same thing in this one, but making it go faster. In my lab, it's about five times faster in fact and I only have about 20 agents to play with. Not really a big deal, but scale it up a bit and add a few thousand agents and the pay-off will be very significant.

As usual, the script will work as is, but it really is more to show the concept. You would have to add filtering to make sure you don't mix agents behind gateway servers and agents behind management servers. Giving an agent behind a gateway a management servers as it's fail-over server will likely not help you in any way.

We will pretty quickly go "advanced" this time, so buckle up. ;)

<!--more-->

Being a slight modification of the script in the last post I am not going to go through those details. Use that post if you need references to the Inputs, the OpsMgr 2012 Modules, Management Group connection and gathering your agents and management servers.

### Why Is It Faster?

We are doing the same thing, on the same agents and with the same servers. And we already did some optimization by loading them all into memory and working from there. How do you make it faster? Basically, I'm cutting the over-head of the cmdlets and how they work. You may have noticed that in the "Do Stuff" section, we are actually calling the `Set-SCOMParentManagementServer` cmdlet twice! Once for the primary Management Server and once for the fail-over Management Servers. In effect, we connect, fire a command, wait for result, and disconnect two times for each agent. And pretty much only because the cmdlet does not offer support to set primary and fail-over management servers at the same time. Any attempt to do so will return an ambiguous parameter error.

I don't like that. A brief look at the agent object class, [Microsoft.EnterpriseManagement.Administration.AgentManagedComputer](http://msdn.microsoft.com/en-us/library/microsoft.enterprisemanagement.administration.agentmanagedcomputer.aspx), revealed a method called [SetManagementServers](http://msdn.microsoft.com/en-us/library/microsoft.enterprisemanagement.administration.agentmanagedcomputer.setmanagementservers "AgentManagedComputer.SetManagementServers Method"). This method takes, or actually "requires", two parameters. One for primary and one for fail-over management servers. Yay!

Using this method saves us a bunch of over-head and a couple of round-trips to the SDK-service.

### The Challenge

Unfortunately, you cannot simply toss an array of management servers at the SetManagementServers method. With a bit of knowledge or keen eyes you will spot the problem right away. I didn't and was pulling my hair for a while until I realized what caused the errors. Looking closer at how the method is defined we see this:

```csharp 
public void SetManagementServers (
 ManagementServer managementServer,
 IList failoverManagementServers
 )
 ```

You see that `IList<ManagementServer>` part?
That's the problem. When you run `Get-SCOMManagementServer` and save the result to a powershell variable, you will get a powershell "Enumerable". In C#, that would be a class that implements the `IEnumerable` interface. Sad part is, it does not also implement `IList`. If you are thinking "IList... IEnumerable... Interface... Whaaaaa...???" right now, don't worry. You don't have to understand this to read the script later on, just think of it as different types of data.

To get around this, we create a new object based on the dotNET List type and populate it with the management servers in our $scomFailOverMS array.

```powershell 
$scomMSList = New-Object 'Collections.Generic.List[Microsoft.EnterpriseManagement.Administration.ManagementServer]'
foreach ($scomMS in $scomFailOverMS) {
 # Loop through the array and add your failover MSs to the list
 $scomMSList.Add($scomMS)
}
```
> Note:We have to do that foreach loop since our $scomMSList object do not implement IEnumerable
Still with me?

### Configuring the Agent

As the method exist on that `AgentManagedComputer` class we will call it on our `$scomAgent` object, like this:

```powershell 
$scomAgent.SetManagementServers($scomPrimaryMS,$scomMSList)
```

And we're done!

I had some doubt that this would be an improvement at first since we have to create our own objects and run an extra foreach-loop, but as we only work on objects in memory and only speak to the SDK service once per agent, we cut a lot of over-head and delays from our execution. On 20-ish agents in a lab, I've measured the execution time drop to barely a fifth.

### The Copy/Paste Part

And here's the entire script with a few added comments for clarity. Read, adapt and try it. In a lab, preferably.

```powershell 
# Input SCOM Management Server to connect to in this session
[string]$inputScomMS = "scomms02.domain.local"
# Input an existing agent you want to modify
[string]$inputTargetAgent = "*.domain.local"

### Connect to SCOM 2012 Management Group ###
If (Get-Module -Name "OperationsManager") {
    try {
        Import-Module -Name "OperationsManager"
    } catch {
        echo "Could not load Operations Manager module"
        exit
    }
}
New-SCOMManagementGroupConnection -ComputerName $inputScomMS
### END ###

$scomAgents = Get-SCOMAgent -DNSHostName $inputTargetAgent | Where {$_.ManuallyInstalled -ne $true}
# Get all of the management servers
# It is ofcourse possible to search by hostname and wildcards using selected
# parameters to the cmdlet.
$scomManagementServers = Get-SCOMManagementServer
# Switch to the following line to only get Gateway Servers
#$scomManagementServers = Get-SCOMGatewayManagementServer
foreach ($scomAgent in $scomAgents) {
    # Get the primary management server for the agent
    $scomPrimaryMS = $scomManagementServers | where {$_.Name -eq $scomAgent.PrimaryManagementServerName}
    # Remove the primary MS from "all MS" array to use it for FailOver servers
    $scomFailOverMS = $scomManagementServers | where {$_.Name -ne $scomPrimaryMS.Name}

    # Create a new IList derived object for the failover MSs
    # You have to do this because the SetManagementServers() method requires an
    # IList and the MS-array is an IEnumerable type. So we basically create
    # a new IList object och the ManagementServer type.
    $scomMSList = New-Object 'Collections.Generic.List[Microsoft.EnterpriseManagement.Administration.ManagementServer]'
    foreach ($scomMS in $scomFailOverMS) {
        # Loop through the array and add your failover MSs to the list
        $scomMSList.Add($scomMS)
    }
    $scomAgent.SetManagementServers($scomPrimaryMS, $scomMSList)
}
```

GLHF!