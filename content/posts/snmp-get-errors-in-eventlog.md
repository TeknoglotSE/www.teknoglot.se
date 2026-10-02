---
title: SNMP GET Errors in OpsMgr EventLog
date: 2010-09-02 22:28:07
year: 2010
month: 09
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/snmp-get-errors-in-eventlog/
url_encoded: /ms/opsmgr2007/snmp-get-errors-in-eventlog/
description: I’ve been building a little SNMP Management Pack in the past few days to discover and monitor a bunch of PowerWare UPS’s, which turned out to take quite a lot more energy and time than expected. Mostl
excerpt: "I’ve been building a little SNMP Management Pack in the past few days to discover and monitor a bunch of PowerWare UPS’s, which turned out to take quite a lot more energy and time than expected. Mostly due to the facts that I am really bad with SNMP and how it works, I’ve never really looked into the inner working of building an SNMP management pack and also because we ran into a couple of errors preventing the discovery process to work alright. To make it clear right away, this is not going to be a “Building an SNMP Management Pack Tutorial” since there’s plentiful good ones out there already, and to be extra helpful I’m gonna include a few links right away: SNMP Setup and Simple Custom SNMP Discovery - Pretty much the basics SNMP Management Pack Example: NetApp Management Pack - Part 4 actually, but has the links to the other parts Creating SNMP Probe Based Monitors - No custom discovery, but a good and simple guide to SNMP Probes It’s the second, the NetApp one, I’ve used as a guide to building the UPS management pack since it goes through the process of building your own filtered discovery using SystemOID to identify your hardware-classes and then building the monitors on top of those. Let’s get to it When building the discovery of my hardware classes I ran into problems. The discovery simply did not work. At first I got some strange errors about “invalid queries”, something that turned out to be related to me reading two guides–seriously though, pick one guide that is closest to what you want to achieve and stick to it–and mixing up the XPathQuery variables. Silly me. I got those errors to go away and I was able to get a few objects to my base-class, but none of the hardware classes who was populated through the return value of an SNMP OID got discovered. The only error I got this time was the following: Log Name: Operations ManagerSource: Health Service ModulesDate: 2010-09-02 11:19:12Event ID: 11001Task Category: NoneLevel: ErrorKeywords: ClassicUser: N/AComputer: CENSOREDDescription:Error sending an SNMP GET message to IP Address XX.XX.XX.XX, Community String:=CENSORED, Status 0x6c.One or more workflows were affected by this.Workflow name: CENSORED.MP.CLASS.DISCOVERYInstance name: CENSORED_DEVICENAMEInstance ID: {5C7EFB30-D885-8843-0DD7-EA86B4FD2311}Management group: CENSORED I went through all the other logical steps of troubleshooting an error like that which include double-checking firewall settings, OIDs, IP-addresses, allowed hosts and so forth. It wasn’t until I loaded the PowerMIB into a MIB Browser installed on the proxy machine (in this case a Management Server) I realized that there was no problem sending an SNMP GET to the UPS from that server. I launched Wireshark and had it listen to SNMP traffic between the UPS and the Management Server. The thing that struck me right-away was the fact that I could see the a bunch of “SNMP Get-Request” but no “SNMP Get-Response” which means that Operations Manager did send an SNMP GET but there was no response. After a bit of intense staring i noticed what you see in the screenshot."
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Errors
  - Management Pack
  - TroubleShooting
hexo_id: 306
---

I've been building a little SNMP Management Pack in the past few days to discover and monitor a bunch of PowerWare UPS's, which turned out to take quite a lot more energy and time than expected. Mostly due to the facts that I am really bad with SNMP and how it works, I've never really looked into the inner working of building an SNMP management pack and also because we ran into a couple of errors preventing the discovery process to work alright.

To make it clear right away, this is not going to be a "Building an SNMP Management Pack Tutorial" since there's plentiful good ones out there already, and to be extra helpful I'm gonna include a few links right away:

* [SNMP Setup and Simple Custom SNMP Discovery](http://www.systemcentercentral.com/BlogDetails/tabid/143/IndexID/66140/Default.aspx "SNMP Setup and Simple Custom SNMP Discovery") - Pretty much the basics
* [SNMP Management Pack Example: NetApp Management Pack](http://www.systemcentercentral.com/BlogDetails/tabid/143/IndexID/58919/Default.aspx "SNMP Management Pack Example: NetApp Management Pack for SCOM 2007 R2 part 4") - Part 4 actually, but has the links to the other parts
* [Creating SNMP Probe Based Monitors](http://www.systemcentercentral.com/Details/tabid/147/IndexID/58815/Default.aspx "Creating SNMP Probe Based Monitors") - No custom discovery, but a good and simple guide to SNMP Probes

It's the second, the NetApp one, I've used as a guide to building the UPS management pack since it goes through the process of building your own filtered discovery using SystemOID to identify your hardware-classes and then building the monitors on top of those.

# Let's get to it

When building the discovery of my hardware classes I ran into problems. The discovery simply did not work. At first I got some strange errors about "invalid queries", something that turned out to be related to me reading two guides--seriously though, pick one guide that is closest to what you want to achieve and stick to it--and mixing up the XPathQuery variables. Silly me.
I got those errors to go away and I was able to get a few objects to my base-class, but none of the hardware classes who was populated through the return value of an SNMP OID got discovered.
The only error I got this time was the following:

```text
Log Name:      Operations Manager
Source:        Health Service Modules
Date:          2010-09-02 11:19:12
Event ID:      11001
Task Category: None
Level:         Error
Keywords:      Classic
User:          N/A
Computer:      CENSORED
Description:
Error sending an SNMP GET message to IP Address XX.XX.XX.XX, Community String:=CENSORED, Status 0x6c.

One or more workflows were affected by this.

Workflow name: CENSORED.MP.CLASS.DISCOVERY
Instance name: CENSORED_DEVICENAME
Instance ID: {5C7EFB30-D885-8843-0DD7-EA86B4FD2311}
Management group: CENSORED
```

I went through all the other logical steps of troubleshooting an error like that which include double-checking firewall settings, OIDs, IP-addresses, allowed hosts and so forth. It wasn't until I loaded the [PowerMIB](http://www.networkupstools.org/protocols/eaton/ "EATON Protocol Library") into a MIB Browser installed on the proxy machine (in this case a Management Server) I realized that there was no problem sending an SNMP GET to the UPS from that server. I launched Wireshark and had it listen to SNMP traffic between the UPS and the Management Server. The thing that struck me right-away was the fact that I could see the a bunch of "SNMP Get-Request" but no "SNMP Get-Response" which means that Operations Manager did send an SNMP GET but there was no response.

After a bit of intense staring i noticed what you see in the screenshot.


![SNMP Error in Wireshark](http://teknoglotse.nfshost.com/wp-content/uploads/2010/09/snmp_error_wireshark.png "SNMP Error in Wireshark")

For some reason Operations Manager does not care about what SNMP version you configure when you do the initial discovery of a network device. Even if you do specify SNMP v1, you probes may very well be using SNMP v2c instead and in many cases that will result in these SNMP GET errors in the Operations Manager event log.

To avoid this, you haves to specify which SNMP version to use in your System.SnmpProbe according to the information provided here: [http://msdn.microsoft.com/en-us/library/ee809331.aspx](http://msdn.microsoft.com/en-us/library/ee809331.aspx)

Since I am such a nice guy, here's an example of the working probe with the added line highlighted.

```xml
<IsWriteAction>false</IsWriteAction>
<IP>$Config/IP$</IP>
<CommunityString>$Config/CommunityString$</CommunityString>
<Version>1</Version>
<SnmpVarBinds>
	<SnmpVarBind>
	<OID>1.3.6.1.4.1.534.1.1.1.0</OID>
		<Syntax>0</Syntax>
		<Value VariantType="8"></Value>
	</SnmpVarBind>
	<SnmpVarBind>
		<OID>1.3.6.1.4.1.534.1.1.2.0</OID>
		<Syntax>0</Syntax>
		<Value VariantType="8"></Value>
	</SnmpVarBind>
	<SnmpVarBind>
		<OID>1.3.6.1.4.1.534.1.1.3.0</OID>
		<Syntax>0</Syntax>
		<Value VariantType="8"></Value>
	</SnmpVarBind>
</SnmpVarBinds>
```

That's it. Working perfectly now.

Best of luck!