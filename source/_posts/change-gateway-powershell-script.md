---
title: Change Gateway Powershell Script
tags:
  - OpsMgr
  - PoSH
  - Script
id: 261
categories:
  - Microsoft
  - OpsMgr 2007
date: 2010-03-31 15:27:08
---

This script has pretty much already been covered in my previous post about [Changing or Replacing an Operations Manager Gateway Server](http://www.teknoglot.se/ms/opsmgr2007/replacechange-a-gateway-server/).

This time I’ve basically put parameter support in it to make it easier to use.

Here’s the script anyway.

```powershell
Param($OldGW,$NewGW)

$OldMS= Get-ManagementServer | where {$_.Name -eq $OldGW}
$NewMS = Get-ManagementServer | where {$_.Name -eq $NewGW}
$agents = Get-Agent | where {$_.PrimaryManagementServerName -eq $OldGW}
$agents = $agents
"Moving " + $agents.count + " agents from " + $OldMS.Name + " to " + $NewMS.Name
Start-Sleep -m 200
Set-ManagementServer -AgentManagedComputer: $agents -PrimaryManagementServer: $NewMS -FailoverServer: $OldMS
```

To use it, create a textfile called ChangeGW.ps1 and paste the code into it. Save the file somewhere neat (maybe C:Scripts) for easy access. If you don't feel like copy/pasting, you can [download the script here](http://www.teknoglot.se/ms/opsmgr2007/change-gateway-powershell-script/attachment/changegw/).

To use it, open the Operations Manager Command Shell and type:
`C:\ScriptsChangeGW.ps1 <old.gatewayserver.dns.name> <new.gatewayserver.dns.name>`

For example:

```powershell
C:\ScriptsChangeGW.ps1 gwserver01.domainname.local gwserver02.domainname.local
```