---
title: NetworkAdapterCheck.vbs fails on Windows 2000
date: 2009-04-26 11:21:18
year: 2009
month: 04
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/networkadaptercheck-fails-on-win2k/
url_encoded: /ms/opsmgr2007/networkadaptercheck-fails-on-win2k/
description: Problem Here’s my summary of the problems with the NetworkAdapterCheck.vbs script in the Windows Server 2000 Operating System Management Pack för Operations Manager 2007 that is causing the failed to
excerpt: "Problem Here’s my summary of the problems with the NetworkAdapterCheck.vbs script in the Windows Server 2000 Operating System Management Pack för Operations Manager 2007 that is causing the failed to create System.PropertyBagData error i wrote about earlier. This information in also available on https://connect.microsoft.com/feedback/ViewFeedback.aspx?FeedbackID=432627&SiteID=446 Symptoms This “research” comes from getting an obscene amounts of Script or Executable Failed to run in the Operations Console. Each time it was the NetworkAdapterCheck.vbs script that could not create PropertyBagData. The error message copied from one of the alerts looks like this: The process started at 14:29:26 failed to create System.PropertyBagData, no errors detected in the output. The process exited with 0Command executed: \"C:WINNTsystem32cscript.exe\" /nologo \"NetworkAdapterCheck.vbs\" MASKEDCOMPUTERNAME 0 false true falseWorking Directory: C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 2882781One or more workflows were affected by this.Workflow name: Microsoft.Windows.Server.2000.NetworkAdapter.NetworkAdapterConnectionHealthInstance name: 0Instance ID: {F4C478D3-38E5-8C29-3957-E3B7F486216E}Management group: MASKED This error repeats almost as often as the script is scheduled to run and appears on almost every Windows 2000 server."
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Script
  - Errors
  - Management Pack
hexo_id: 125
---

# Problem

Here's my summary of the problems with the NetworkAdapterCheck.vbs script in the Windows Server 2000 Operating System Management Pack för Operations Manager 2007 that is causing the [failed to create System.PropertyBagData](http://www.teknoglot.se/ms/opsmgr2007/failed-to-create-propertybagdata-opsmgr/ "failed to create System.PropertyBagData") error i wrote about earlier.
This information in also available on [https://connect.microsoft.com/feedback/ViewFeedback.aspx?FeedbackID=432627&SiteID=446](https://connect.microsoft.com/feedback/ViewFeedback.aspx?FeedbackID=432627&SiteID=446)

# Symptoms

This "research" comes from getting an obscene amounts of Script or Executable Failed to run in the Operations Console. Each time it was the NetworkAdapterCheck.vbs script that could not create PropertyBagData. The error message copied from one of the alerts looks like this:

```text
The process started at 14:29:26 failed to create System.PropertyBagData, no errors detected in the output. The process exited with 0

Command executed: "C:WINNTsystem32cscript.exe" /nologo "NetworkAdapterCheck.vbs" MASKEDCOMPUTERNAME 0 false true false
Working Directory: C:Program FilesSystem Center Operations Manager 2007Health Service StateMonitoring Host Temporary Files 2882781

One or more workflows were affected by this.

Workflow name: Microsoft.Windows.Server.2000.NetworkAdapter.NetworkAdapterConnectionHealth
Instance name: 0
Instance ID: {F4C478D3-38E5-8C29-3957-E3B7F486216E}
Management group: MASKED
```

This error repeats almost as often as the script is scheduled to run and appears on almost every Windows 2000 server.

<!--more-->

# Probable Cause

I am not really sure, but after a quite a bit of troubleshooting I am pretty sure it all boils down to a malformed WMI-query. What I basically did was to extract the script from the MP and dry-run it to see if I could find anything obvious, which I didn't.
Since I didn't have a good debugging too available, like in PrimalScript, I added the VBS equivalent of old-school printf debugging. I basically added

```vbs
wscript.echo "Line XX:" & Err.Number
```

after each object/function call in the Main Sub.
The problem seems to be at line 118:

```vbs
Set WMISet = WMIGetInstance("winmgmts:" + TargetComputer + "rootcimv2", query)
```

At line 119 I had a debug line that never executes and it would seem like the script is unable to process the query and exits without any error codes.

The query variable contains the following:

```sql
Win32_NetworkAdapter Where DeviceID='0' And ( NetConnectionStatus = '0' )
```

When I was debugging this I started the script like this:

```cmd
cscript.exe /nologo "NetworkAdapterCheck.vbs" MASKED 0 false true false
```

I did find that if I change the parameters to this:

```cmd
cscript.exe /nologo "NetworkAdapterCheck.vbs" MASKED 0 false false false
```

Then the script runs smoothly and produces an XML-output like this:

```xml
<Collection>
  <DataItem type="System.PropertyBagData" time="2009-04-22T15:03:44.6495202+02:00" sourceHealthServiceId="C9F5A9F7-00A3-8A86-57B5-34FB634471A8">
  <Property Name="State" VariantType="8">GOOD</Property>
  </DataItem>
</Collection>
```

# Comments

There's quite the lot of similar errors posted on various forums on the internet but most of them ends up pointing towards the Antivirus Software as the perp and we have tried various exceptions on the server like excluding HealthExplorer.exe, MonitoringHost.exe and also the entire Health Service State folder with no improvement. But since I was able to run the scripts from other locations (not excluded) on the same server I find it hard to believe that the AV would be blocking it.
