---
title: "Load-balanced SCOM2012 SDK Services for Network Illiterates [#opsmgr, #nlb]"
date: 2012-05-18 13:16:51
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2012/load-balanced-scom2012-sdk-services-for-network-illiterates-opsmgr-nlb/
description: Prelude Now that System Center Operations Manager no longer has that pesky Root Management Server role; a server role that in larger environments quickly became the choking point and made creating a
excerpt: Prelude Now that System Center Operations Manager no longer has that pesky Root Management Server role; a server role that in larger environments quickly became the choking point and made creating a fully Highly Available SCOM-environment both complex and frustrating to support and with little gain at that. With that gone and the SDK Service, or Data Access Service, thriving on all the Management Servers HA suddenly became pretty simple. All you have to do in SCOM2012 to make sure your management groups keep on kicking is to have at-least two Management Servers and your databases clustered. This new distributed architecture does not only give easy HA, it also makes it possible to connect to the SDK-service—be it using the Operations Console or powershell to name two options—on any Management Server. This, in turn, provides for a completely new level of scalability. Choked on sessions? Deploy a new Management Server! Anyway… given all this scalability and HA, would it not be nice if you could load-balance all these SDK-sessions you will be running from System Center Virtual Machine Manager, System Center Service Manager, System Center Orchestrator, regular scheduled powershell scripts and what-not? Of course it would! And you can! The simple solution is to use the built-in Network Load Balancer (NLB for short) feature in Windows Server and that’s what we’re going to discuss in this post. Before we go, I’d like to point to a great article written by Justin Cook that is covering most bases but in a less for-dummies way. So, yeah… I suppose this is the for-dummies version then. 😉 Enjoy!
cats:
  - ms
  - ms/opsmgr2012
tags:
  - OpsMgr
  - How-To
  - Highly-Available
  - NLB
  - Tutorial
---

# Prelude

Now that System Center Operations Manager no longer has that pesky Root Management Server role; a server role that in larger environments quickly became the choking point and made creating a fully Highly Available SCOM-environment both complex and frustrating to support and with little gain at that. With that gone and the SDK Service, or Data Access Service, thriving on all the Management Servers HA suddenly became pretty simple. All you have to do in SCOM2012 to make sure your management groups keep on kicking is to have at-least two Management Servers and your databases clustered.

This new distributed architecture does not only give easy HA, it also makes it possible to connect to the SDK-service—be it using the Operations Console or powershell to name two options—on _any_ Management Server. This, in turn, provides for a completely new level of scalability. Choked on sessions? Deploy a new Management Server!

Anyway… given all this scalability and HA, would it not be nice if you could load-balance all these SDK-sessions you will be running from System Center Virtual Machine Manager, System Center Service Manager, System Center Orchestrator, regular scheduled powershell scripts and what-not?

Of course it would! And you can! The simple solution is to use the built-in Network Load Balancer (NLB for short) feature in Windows Server and that's what we're going to discuss in this post.
Before we go, I'd like to point to a [great article](http://systemcentertech.com/2012/02/07/load-balance-scom-2012-operations-console-connections/) written by [Justin Cook](http://systemcentertech.com/) that is covering most bases but in a less for-dummies way. So, yeah… I suppose this is the for-dummies version then. ;)

Enjoy!



<a id="more"></a>



# Prerequisites

We need to have the Network Load Balancing feature installed on all our targeted Management servers. The quick way to do this is using command-line (Windows Server 2008 R2 or later?).

```text
dism /online /enable-feature /featurename:NetworkLoadBalancingFullServer
```

You also need a plan and some information about your new cluster. Make sure you have identified the following parameters before starting the configuration:
<div>
<table style="border-collapse: collapse;" border="0"><colgroup> <col style="width: 307px;" /> <col style="width: 307px;" /></colgroup>
<tbody valign="top">
<tr>
<td style="padding-left: 7px; padding-right: 7px; border: solid 0.5pt;">A Dedicated Cluster IP-Address:</td>
<td style="padding-left: 7px; padding-right: 7px; border-top: solid 0.5pt; border-left: none; border-bottom: solid 0.5pt; border-right: solid 0.5pt;"></td>
</tr>
<tr>
<td style="padding-left: 7px; padding-right: 7px; border-top: none; border-left: solid 0.5pt; border-bottom: solid 0.5pt; border-right: solid 0.5pt;">A Dedicated Cluster DNS Name:</td>
<td style="padding-left: 7px; padding-right: 7px; border-top: none; border-left: none; border-bottom: solid 0.5pt; border-right: solid 0.5pt;"></td>
</tr>
<tr>
<td style="padding-left: 7px; padding-right: 7px; border-top: none; border-left: solid 0.5pt; border-bottom: solid 0.5pt; border-right: solid 0.5pt;">A list of SCOM2012 Management Servers:</td>
<td style="padding-left: 7px; padding-right: 7px; border-top: none; border-left: none; border-bottom: solid 0.5pt; border-right: solid 0.5pt;"></td>
</tr>
</tbody>
</table>
</div>
You can use this pre-flight table to take note of your IP-address, DNS Name and Server List.

# Create a New Cluster

Open the Network Load Balancing Manager and create a new cluster.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance1.png)

In the "New Cluster" dialogue, connect to one of your Management Servers.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance2.png)

1. Enter the name of a management server
2. Click Connect
3. Select the network interface to use
4. Click Next

Select the settings on your first host in the cluster.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance3.png)

1. Make sure it's the correct IP-address.
2. Click Next

Set the Cluster IP-address.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance4.png)

1. Click Add
2. Enter your Dedicated Cluster IP-Address and Subnet mask
3. Click OK
4. Click Next

If need additional IP-addresses, like an IPv6 address, you simply repeat step 1-3 before proceeding to step 4.

Edit DNS Names and Cluster Operation Mode.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance5.png)

1. Select your Dedicated Cluster IP-address
2. Enter your chosen Dedicated Cluster DNS Name
3. Select Multicast mode
4. Click Next

> Note: We are not going to delve into the Cluster Operation Mode in this guide, but this is what I use for Operations Manager 2012.

> If you want to learn more about these settings, here's the KB on the various settings: [http://support.microsoft.com/kb/323437](http://support.microsoft.com/kb/323437)
Set your Port Rules and Affinity Settings.

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance6.png)

1. Verify that Affinity is set to "Single". If not, Click "Edit…" and adjust.
2. Click Finish

> Note: "Single" affinity tells the cluster to always direct the same client to the same host if possible. This is required to be able to support sessions.

> In the world of NLB, a "client" is an IP-address.

## Post-Configuration

Now that you have a cluster configured you have to make sure your SDK-clients are able to resolve the dedicated cluster DNS-name. The one you picked in the pre-flight table.

To enable name resolution you have to add your cluster DNS-name to your DNS-zone and point it to your dedicated cluster IP-address. Make it an A-record and it should work.

If you intend to use the cluster name from outside the local network or subnet—Operation Consoles or Powershell sessions for example—you would also need to verify that the router is able to handle the multicast packages. I am by no means a network guy, but asking the person behind that "Don't blame the network" sign to help you access a NLB cluster on network _X _from network _Y_ usually works. One way to troubleshoot this is to ping the cluster DNS-name from one of the hosts. If that works but you are still unable to ping from another network or subnet, then it might be a router setting.



<a id="more"></a>



# Adding Hosts to the Cluster

With the cluster configured and up-and-running you need to add the rest of the Management Servers. Repeat this section for each Management Server you wish to add to the load-balancing cluster.

In the Network Load Balancing Manager, right-click your cluster and select "Add Host To Cluster".

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance7.png)

Connect to your next Management Server to be added

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance8.png)

1. Enter the server name of the Management Server ("host" in cluster terminology)
2. Click Connect
3. Select the IP-address of the host
4. Click Next

Verify your Host Parameters

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance9.png)

1. Doublecheck the IP-address
2. Click Next

Verify the Port Rules

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance10.png)

1. Make sure that Load is Equal and Affinity is Single
2. Click Finish

# Final Verification

After each added host it would be proper to check if it was added correctly. The easiest way is to check their statuses in the Network Load Balancing Manager. Green is generally considered good and you want your hosts to be "Converged".

![](/wp-content/uploads/2012/05/051812_1216_Loadbalance11.png)

Another way to verify functionality is to point your Operations Manager console to the Cluster DNS-name instead and connect. If you are in a lab or in an environment where it is OK to shut down Management Servers you could try that as well.

Considering my note on routers in the Cluster Post-Configuration I guess it would be prudent to point out that you should try launching SDK-sessions from all networks you intend to connect from. Just to make sure that your routers are correctly configured to handle these kinds of sessions.



<a id="more"></a>



# Postlude

Now; as easy this may be I would personally argue that you should involve your network team _before_ starting to deploy your load-balanced clusters. A little heads-up is always a good thing—I have noticed that network people rarely like surprises—and they might actually be able to help you all the way is you ask nicely. And maybe they'll tell you right away that some configuration is required before-hand instead of giggling frantically in a corner at your feeble attempts to troubleshoot your fresh little cluster.

Soooo… have fun!

And remember; with great powers come great responsibility.

*Sheesh! This post got out of hand!*
