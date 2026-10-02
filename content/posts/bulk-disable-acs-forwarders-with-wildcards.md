---
title: Bulk disable ACS Forwarders (with wildcards)
date: 2011-07-07 10:59:24
lastmod: 2017-06-05T10:13:43+02:00
url: /ms/opsmgr2007/bulk-disable-acs-forwarders-with-wildcards/
url_encoded: /ms/opsmgr2007/bulk-disable-acs-forwarders-with-wildcards/
cats:
  - ms
  - ms/opsmgr2007
tags:
  - ACS
  - OpsMgr
  - PoSH
  - Script
hexo_id: 558
---

Here's a little something-something for the wicked.

Me and my apprentice is currently decommissioning an entire Management Group with a thousand (-ish) agents. Long story short, we got a new Management Group, migrated all the agents, added a couple of hundreds more, deployed a bunch of gateways and now we are shutting down the old one.

Now, uninstalling the old Management Group from all the agents is a breeze using SCCM and handling the few 20-ish servers that are left is not a biggie either. Shutting down ACS, however, is a different matter.

<!--more-->

Although you do configure your forwarders using Operations Manager, removing the management group you were running ACS in does not mean the agents will shut down and disable the AdtAgent service or stop trying to forward audit events to your collector. Now, selecting 10 agents at the time and running the "Disable Audit Collection" task--in case you did not know, there's a limitation on how many agents you can run a task on in the Operations Console--is not my idea of a jolly good day and since Powershell is a bucket of joy in comparison; here's a script for you all!

[DisableACSForwarders](http://teknoglotse.nfshost.com/wp-content/uploads/2011/07/DisableACSForwarders.zip)

It is zipped to avoid security alerts, but as with any script found on the internet I implore to to read the code before actually running it.

Anyway, you can use it in a couple of ways.

To run it interactively, just go to the directory where you unpacked it and run it. You will be requested to enter the FQDN of you Root Management Server and a wildcard search for ACS Forwarders.
For example:

```bat 
C:\..\Scripts> .\DisableACSForwarders.ps1
Root Management Server: rms.teknoglot.local
ACS Forwarder name (wildcard): *.teknoglot.local
```

You can also run it with parameters (for scheduling?) like this:

```bat 
C:\..\Scripts> .\DisableACSForwarders.ps1 rms.teknoglot.local *.teknoglot.local
```

If you need to run the task with different credentials there's a switch for that. Just add -UseCredentials to the command and you will be prompted for it.
Like this:

```bat 
C:\..\Scripts> .\DisableACSForwarders.ps1 -UseCredentials
```

As you might already have realized, the wildcard search does not require actual wildcards. If you only want to disable the ACS forwarder on a single machine, just enter it's FQDN. As for what wildcards it will accept; [anything supported by the powershell -like operator](http://msdn.microsoft.com/en-us/library/aa717088%28VS.85%29.aspx "Supporting Wildcard Characters in Cmdlet Parameters") is valid.

[UPDATE!] You might get false failures when running the script on clustered machines because of a [bug in the AC Management Pack](https://connect.microsoft.com/OpsMgr/feedback/details/523453/bug-with-microsoft-audit-collection-services-management-pack "Bug with Microsoft Audit Collection Services Management Pack")

For the source code, read on!

<!--more-->

```powershell
## Using parameters for RMS and wildcard search
param(
    [string]$rootManagementServer = $(Read-Host -Prompt "Root Management Server" ),
    [string]$filterAgents = $(Read-Host -Prompt "ACS Forwarder name (wildcard)" ),
    [switch]$UseCredentials
)

## Make sure the $rootManagementServer variable is defined
while (-not $rootManagementServer) {
    Write-Host "`nRoot Management Server MUST be defined!" -ForegroundColor Red
    [string]$rootManagementServer = $(Read-Host -Prompt "Root Management Server" )
}

if ($UseCredentials -eq $true) {
    $taskCredentials = Get-Credential
}

$startLocation = Get-Location
$checkPSSnapin = Get-PSSnapin | where {$_.Name -eq "Microsoft.EnterpriseManagement.OperationsManager.Client" }
if ($checkPSSnapin -eq $null) {
    Add-PSSnapin "Microsoft.EnterpriseManagement.OperationsManager.Client"
}
$result = Set-Location "OperationsManagerMonitoring::"
$result = New-ManagementGroupConnection -ConnectionString:$rootManagementServer
$result = Set-Location $rootManagementServer

$acsForwarderClass = Get-MonitoringClass -Name "Microsoft.SystemCenter.ACS.Forwarder"
$agentNames = Get-MonitoringObject -monitoringclass:$acsForwarderClass | where {$_.Path -like $filterAgents} | Select Path
$successfulTasks = @()
$skippedTasks = @()
$failedTasks = @()

$monitoringClass = Get-MonitoringClass -Name "Microsoft.SystemCenter.Agent"
if ($agentNames -ne $null) {
    Write-Host "`nFound" $agentNames.Count"ACS forwarders with wildcard $filterAgents"
    Write-Host "`n`nWaiting for 5 seconds to give you a chance to abort!`n"
    Start-Sleep -Seconds 5
    Write-Host "Time's UP!`n`n"
    $agentNames | ForEach-Object {
        $agentName = $_.Path
        Write-Host "Disabling Audit Collection on" $agentName
        $monitoringObject = Get-MonitoringObject -monitoringclass:$monitoringClass | where {$_.DisplayName -like $agentName}
        $agentTask = $monitoringObject | Get-Task | where {$_.Name -eq "Microsoft.SystemCenter.DisableAuditCollectionService" }
        if ($monitoringObject.IsAvailable -eq $true) {
            if ($credentials -eq $null) {
                $result = Start-Task -Task $agentTask -TargetMonitoringObject $monitoringObject
            }
            else {
                $result = Start-Task -Task $agentTask -TargetMonitoringObject $monitoringObject -Credential $taskCredentials
            }
  
            if ($result.Status -eq "Succeeded" ) {
                Write-Host "Operation Successful!" -ForegroundColor Green
                Write-Host `n
                $successfulTasks += $agentName
            }
            else {
                Write-Host "Operation failed." -ForegroundColor Red
                Write-Host $result.ErrorMessage
                Write-Host `n
                $failedTasks += $agentName
            }
        }
        else {
            Write-Host "The agent is unavailable, Skipping!"
            Write-Host `n
            $skippedTasks += $agentName
        }
    }
    Write-Host "Summary"
    Write-Host "`tSuccessful:`t" $successfulTasks.count
    Write-Host "`tFailed:`t`t" $failedTasks.count
    Write-Host "`tSkipped:`t" $skippedTasks.count
}
else {
    Write-Host "`nNo ACS Forwarders found using wildcard $filterAgents"
}

Set-Location $startLocation
```

Enjoy!