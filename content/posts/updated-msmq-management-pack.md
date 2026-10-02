---
title: Updated MSMQ Management Pack v6.0.6615.0!
date: 2009-12-23 09:57:38
year: "2009"
month: "12"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/updated-msmq-management-pack/
url_encoded: /ms/opsmgr2007/updated-msmq-management-pack/
description: "Microsoft has released an update to the MSMQ (version 3) management pack. System Center Pack for: Message Queuing 3.0Version:      6.0.6615.0Released on:  12&#x2F;14&#x2F;2009Message Queuing (also known as MSMQ"
hexo_slug: updated-msmq-management-pack
excerpt: "Microsoft has released an update to the MSMQ (version 3) management pack. System Center Pack for: Message Queuing 3.0Version: 6.0.6615.0Released on: 12/14/2009Message Queuing (also known as MSMQ) is a server application that enables applications to communicate across heterogeneous networks and systems that may be temporarily offline or otherwise inaccessible. Instead of an application communicating with a service on another computer, it sends its information to Message Queuing, which sends the information to a Message Queuing service on the target computer where it is made available to the other application. Message Queuing provides guaranteed delivery, efficient routing, security, and priority based messaging. Now, what’s really interesting is what you will find in the MP Guide under “Supported Configurations”. The Message Queuing Management Pack for Operations Manager 2007 is designed to monitor Message Queuing version 3 only. The Message Queuing Management Pack supports the following platforms: Windows Server 2003 Windows XP The Message Queuing Management Pack also supports monitoring clustered MSMQ components Emphasis by me. Finally, MSMQ monitoring seems to be cluster aware, which might mean that the home-made pack i did to have those (numerous) queues covered could be passed on to the scrap-heap. This is also confirmed under “Changes in This Update”. The December 2009 update to this management pack includes the following change: Fixed a problem when working with an instance of MSMQ in a Cluster. The MP is now able to discover and monitor public and private queues in a cluster. Fixed a problem when discovering the local and cluster instance of MSMQ. The MP is now able to discover and monitor both instances."
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - Management Pack
  - MSMQ
hexo_id: 251
---

Microsoft has released an update to the MSMQ (version 3) management pack.

```text
System Center Pack for: Message Queuing 3.0
Version:      6.0.6615.0
Released on:  12/14/2009

Message Queuing (also known as MSMQ) is a server application that enables applications to communicate across heterogeneous networks and systems that may be temporarily offline or otherwise inaccessible. Instead of an application communicating with a service on another computer, it sends its information to Message Queuing, which sends the information to a Message Queuing service on the target computer where it is made available to the other application. Message Queuing provides guaranteed delivery, efficient routing, security, and priority based messaging.
```

Now, what’s really interesting is what you will find in the MP Guide under “Supported Configurations”.
> The Message Queuing Management Pack for Operations Manager 2007 is designed to monitor Message Queuing version 3 only.

> The Message Queuing Management Pack supports the following platforms:
> - Windows Server 2003
> - Windows XP

> ***The Message Queuing Management Pack also supports monitoring clustered MSMQ components***

Emphasis by me.

Finally, MSMQ monitoring seems to be cluster aware, which might mean that the home-made pack i did to have those (numerous) queues covered could be passed on to the scrap-heap. This is also confirmed under “Changes in This Update”.

> The December 2009 update to this management pack includes the following change:

> - Fixed a problem when working with an instance of MSMQ in a Cluster. The MP is now able to discover and monitor public and private queues in a cluster.
> - Fixed a problem when discovering the local and cluster instance of MSMQ. The MP is now able to discover and monitor both instances.

The confusing double RunAs profiles seems to have been cleaned up too (you only have to worry about one now) as well as fixing some sloppy mistakes in the previous scripts (no Option Explicit? C’mon Microsoft! You _write_ the best practices, try to stick to them.) and generally improving display and documentation.

Gonna import this to our staging environment today and let it roll during the holidays.

Download and documentation:
[http://www.microsoft.com/downloads/details.aspx?FamilyId=1D2B4398-8BC2-4A43-850C-852EBB0D983B&displaylang=en&displaylang=en](http://www.microsoft.com/downloads/details.aspx?FamilyId=1D2B4398-8BC2-4A43-850C-852EBB0D983B&displaylang=en&displaylang=en "http://www.microsoft.com/downloads/details.aspx?FamilyId=1D2B4398-8BC2-4A43-850C-852EBB0D983B&displaylang=en&displaylang=en")

Cheers! Oh, and happy holidays!
