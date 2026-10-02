---
title: "OpsMgr 2012 Agent Failover - Simple Script with Wildcards [#opsmgr, #powershell]"
date: 2012-06-21 10:58:13
year: "2012"
month: "06"
lastmod: 2017-06-05T10:13:43+02:00
url: /ms/opsmgr2012/opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell/
url_encoded: /ms/opsmgr2012/opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell/
description: In the last post, OpsMgr 2012 Agent &amp; Gateway Failover – The Basics, we looked at the basics of the Agent and Gateway fail-over configuration cmdlets and how to use them in a direct and interactiv
hexo_slug: opsmgr-2012-agent-failover-simple-script-with-wildcards-opsmgr-powershell
excerpt: In the last post, OpsMgr 2012 Agent & Gateway Failover – The Basics, we looked at the basics of the Agent and Gateway fail-over configuration cmdlets and how to use them in a direct and interactive setting. This is absolutely useful when you got this specific agent that you need to configure with a specific fail-over management server. To spice it up a little, we are going to add a little intelligence to it and enable wild-card selections while at it. The scenario we are building this script for is that now and then you want to make sure that certain agents have fail-over management servers configured. You also want to make sure that all management servers that are not the primary management server of any selected agent will be in that list of fail-over servers. This would include any new management servers as well as exclude any removed ones. In short, make sure your agent fail-over settings are up-to-date with the current environment.
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - PoSH
  - Fail-over
hexo_id: 685
---

In the last post, [OpsMgr 2012 Agent & Gateway Failover – The Basics](http://www.teknoglot.se/code/powershell/opsmgr-2012-agent-gateway-failover-the-basics/ "OpsMgr 2012 Agent & Gateway Failover – The Basics [#opsmgr, #powershell]"), we looked at the basics of the Agent and Gateway fail-over configuration cmdlets and how to use them in a direct and interactive setting. This is absolutely useful when you got this specific agent that you need to configure with a specific fail-over management server.

To spice it up a little, we are going to add a little intelligence to it and enable wild-card selections while at it. The scenario we are building this script for is that now and then you want to make sure that certain agents have fail-over management servers configured. You also want to make sure that all management servers that are not the primary management server of any selected agent will be in that list of fail-over servers. This would include any new management servers as well as exclude any removed ones. In short, make sure your agent fail-over settings are up-to-date with the current environment.

<!--more-->

### Inputs

To use this script you need to know which management server you should connect your powershell session to and which agent, or agents, you want to check and configure.

```powershell 
# Input SCOM Management Server to connect to in this session
[string]$inputScomMS = "scomms01.domain.local"
# Input an existing agent you want to modify
[string]$inputTargetAgent = "*.domain.local"
```

> Note: If you are using load-balanced SDK-services, or "Data Access Services", pointing `$inputScomMS` to that virtual host-name will work perfectly fine.
This example uses a wild-card for the agent selection and I guess it's the most likely scenario for this script, but a single host-name obviously works fine as well. Supported wildcard selections are [documented at TechNet](http://technet.microsoft.com/en-us/library/ee692793.aspx). An array of computer-names or a comma-separated list, however, will not work. You could easily add that functionality but it's out of scope for this example.

### Connect to Your Management Group

To run any script against an Operations Manager 2012 Management Group we need a connection to one. To connect to a management group we have to load the OperationsManager module. Lets check for a loaded module, load it if necessary and connect to the Management Server from the `$inputScomMS` setting. If loading the module fails--maybe it is not installed--we will exit the script.

```powershell 
# Check if OperationsManager module is loaded
If (Get-Module -Name "OperationsManager") {
    try {
        # Try to load the module
        Import-Module -Name "OperationsManager"
    } catch {
        # Did not work, exit the script
        Write-Output "Could not load Operations Manager module"
        exit
    }
}
# Module is loaded, connect to Management Group/Server
New-SCOMManagementGroupConnection -ComputerName $inputScomMS
```

A good idea would, of course, be to first check if we already have an existing management group connection before creating a new one. But that's up to you.

### Rally Your Agents (and Management Servers)

Since we cannot manage manually installed agents--that would be AD-integrated or installed locally using Configuration Manager or maybe the wizard--through powershell we don't even want to try. So we'll exclude them.

We also need all the available management servers. <del>This will not handle Gateway servers as they have their own cmdlet, `Get-SCOMGatewayManagementServer`, in Operations Manager 2012.</del> Strike that! There is a specific cmdlet for Gateway Servers in OpsMgr 2012, but the regular `Get-SCOMManagementServer` actually don't care whether it's a normal Management Server or a Gateway Server. The `Get-SCOMGatewayManagementServer`, however, only return real Gateway Servers. That means that this script will not care if it is a Management Server or a Gateway Server, so be sure to add some kind of filtering before running it in a Management Group containing management servers.

```powershell 
# Select matching remotely manageable agents
$scomAgents = Get-SCOMAgent -DNSHostName $inputTargetAgent | Where-Object {$_.ManuallyInstalled -ne $true}
# Get all management servers
$scomManagementServers = Get-SCOMManagementServer
```

The reason I like to store all matching agents in a variable is that we will save ourselves a lot of trips to the Data Access Service later on, and we also get a nice collection to run our foreach-loop on. This method is much faster than running `Get-SCOMAgent` inline as we did in "The Basics".
> Note: It would probably be a good idea to check that `$scomAgents` actually contains anything; checking for `$null` with a simple `if() `would be enough.

### Do Stuff

We have our connection to the management group, we have collected our agents, and we have our management servers. It's time to loop through the agents and set their Primary and Fail-over management servers.

```powershell 
foreach ($scomAgent in $scomAgents) {
    # Get the primary management server for the agent
    $scomPrimaryMS = $scomManagementServers | Where-Object {$_.Name -eq $scomAgent.PrimaryManagementServerName}
    # Remove the primary MS from "all MS" array to use it for FailOver servers
    $scomFailOverMS = $scomManagementServers | Where-Object {$_.Name -ne $scomPrimaryMS.Name}
    # Set Primary Management Server
    Set-SCOMParentManagementServer -Agent $scomAgent -PrimaryServer $scomPrimaryMS
    # Set Fail-over Management Server
    Set-SCOMParentManagementServer -Agent $scomAgent -FailoverServer $scomFailOverMS
}
```

The nice thing about loading the agents and the management servers into variables is that all the information you need for this script is pre-cached in memory. You don't have to connect to the management group to find out which management server happens is the primary for each agent. And you don't have to run `Get-SCOMManagementServer` for each agent to select which ones that will be fail-over management servers. All that information is in memory, and memory is fast.

### The Copy/Paste Part

As usual, here's the entire script for you to copy. Read it, try it, adapt it...

```powershell 
# Input SCOM Management Server to connect to in this session
[string]$inputScomMS = "scomms02.domain.local"
# Input an existing agent you want to modify
[string]$inputTargetAgent = "*.domain.local"

### Connect to SCOM 2012 Management Group ###
# Check if OperationsManager module is loaded
If (Get-Module -Name "OperationsManager") {
    try {
        # Try to load the module
        Import-Module -Name "OperationsManager"
    } catch {
        # Did not work, exit the script
        Write-Output "Could not load Operations Manager module"
        exit
    }
}
# Module is loaded, connect to Management Group/Server
New-SCOMManagementGroupConnection -ComputerName $inputScomMS
### END ###

# Select matching remotely manageable agents
$scomAgents = Get-SCOMAgent -DNSHostName $inputTargetAgent | Where-Object {$_.ManuallyInstalled -ne $true}
# Get all management servers
$scomManagementServers = Get-SCOMManagementServer
foreach ($scomAgent in $scomAgents) {
    # Get the primary management server for the agent
    $scomPrimaryMS = $scomManagementServers | Where-Object {$_.Name -eq $scomAgent.PrimaryManagementServerName}
    # Remove the primary MS from "all MS" array to use it for FailOver servers
    $scomFailOverMS = $scomManagementServers | Where-Object {$_.Name -ne $scomPrimaryMS.Name}
    # Set Primary Management Server
    Set-SCOMParentManagementServer -Agent $scomAgent -PrimaryServer $scomPrimaryMS
    # Set Fail-over Management Server
    Set-SCOMParentManagementServer -Agent $scomAgent -FailoverServer $scomFailOverMS
}
### Done!
```

GLHF!