---
title: PoSH Grid Dashboard for RDSH [#opsmgr]
date: 2016-06-14 00:01:27
year: 2016
month: 06
lastmod: 2016-07-05T22:00:35+02:00
url: /ms/opsmgr2012/PoSH-Grid-Dashboard-for-RDSH/
url_encoded: /ms/opsmgr2012/PoSH-Grid-Dashboard-for-RDSH/
description: "TLDR Customer wanted to see all RDS Host servers in a view with their current total session count. Decided to use a powershell grid dashboard, and share the script. Here’s the gist of it: SCOM_RDSH_T"
excerpt: "TLDR Customer wanted to see all RDS Host servers in a view with their current total session count. Decided to use a powershell grid dashboard, and share the script. Here’s the gist of it: SCOM_RDSH_TotalSession_PoSHWidget.ps1 How To Keeping it fairly short this time. Pre-requisites are: System Center 2012 R2 with UR2 or later Microsoft RDS Management Pack Microsoft Windows Core OS Management Pack Create a dashboard Rightclick and create a new view somewhere, make it a Dashboard View Enter Name and Description Select Grid type, and layout"
cats:
  - ms
  - ms/opsmgr2012
tags:
  - Powershell
  - OpsMgr 2012 R2
  - HowTo
---


# TLDR

Customer wanted to see all RDS Host servers in a view with their current total session count.

Decided to use a powershell grid dashboard, and share the script.

Here's the gist of it: [SCOM_RDSH_TotalSession_PoSHWidget.ps1][1]

# How To

Keeping it fairly short this time.

Pre-requisites are:

* System Center 2012 R2 with UR2 or later
* Microsoft RDS Management Pack
* Microsoft Windows Core OS Management Pack

## Create a dashboard

1. Rightclick and create a new view somewhere, make it a Dashboard View
1. Enter Name and Description
1. Select Grid type, and layout

## Add a widget

1. Click cog on grid view
1. Select Powershell Grid Widget
1. Set Name and Description
1. Paste your [script](#The-Script) into the script box
1. Save

## The Script

```powershell
# Based on https://gallery.technet.microsoft.com/Retrieve-Performance-Data-c4595e2a#content
function Add-Criteria()
{
    param($criteria,$clause)
    if ($criteria -ne $null)
        {$criteria += " AND $clause"}
    else
        {$criteria = $clause}
    return($criteria)
}

$rdsClass = Get-SCOMClass -Name "Microsoft.Windows.Server.2012.R2.RemoteDesktopServicesRole.Service.RDSessionHost"
$rdsHosts = Get-SCOMMonitoringObject -Class $rdsClass | Sort-Object -Property '[Microsoft.Windows.Computer].PrincipalName'
$rdsTotalSessionRule = Get-SCOMRule -Name "Microsoft.Windows.Server.2012.R2.RemoteDesktopServicesRole.Service.RDSessionHost.PerformanceCollection.TotalSessions"
$objectName = "Terminal Services"
$counterName = "Total Sessions"
$InstanceName = ""


$i=0
foreach ($rdsHost in $rdsHosts) {
    # Build performance criteria
    if ($rdsClass -ne $null) { $criteria = Add-Criteria -criteria $criteria -clause "MonitoringClassId = '{$($rdsClass.Id)}'" }
    if ($rdsHost -ne $null) { $criteria = Add-Criteria -criteria $criteria -clause "MonitoringObjectFullName = '$($rdsHost.FullName)'" }
    if ($objectName -ne $null) { $criteria = Add-Criteria -criteria $criteria -clause "ObjectName = '$objectName'" }
    if ($counterName -ne $null) { $criteria = Add-Criteria -criteria $criteria -clause "CounterName = '$counterName'" }

    #$criteria
    # Get Performance reader object.
    $perfReader = (Get-SCOMManagementGroup).GetMonitoringPerformanceDataReader($criteria)
    while ($perfReader.Read()) {
        $perfData = $perfReader.GetMonitoringPerformanceData()
        $perfValueReader = $perfData.GetValueReader(((Get-Date).AddMinutes(-180)),(Get-Date))

        $perfValues = @()
        while ($perfValueReader.Read()) {
            $perfValues += $perfValueReader.GetMonitoringPerformanceDataValue()
        }
        $perfValue = $perfValues | Sort-Object -Property TimeSampled | select -Last 1

        $dataObject = $ScriptContext.CreateInstance("xsd://stegenfeldt/nullschema")
        $dataObject = $ScriptContext.CreateFromObject($rdsHost, "Id=Id,Health=HealthState,Host=Path", $null)
        $dataObject["Time Sampled"] = $perfValue.TimeSampled
        $dataObject["Total Sessions"] = $perfValue.SampleValue
        $ScriptContext.ReturnCollection.Add($dataObject)
    }
    $criteria = $null
    ++$i
}
```



[1]: https://gist.github.com/stegenfeldt/112c6d3dd513f9659298d1321c98ebd1
