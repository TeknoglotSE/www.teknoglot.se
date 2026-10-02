---
title: "Cloudflare as Dynamic DNS [#cloudflare #mikrotik #script]"
date: 2014-08-25 13:37:36
lastmod: 2018-08-28T15:16:14+02:00
url: /mikrotik/cloudflare-dynamic-dns-mikrotik/
url_encoded: /mikrotik/cloudflare-dynamic-dns-mikrotik/
cats:
  - mikrotik
tags:
  - PoSH
  - Script
  - DNS
  - Invoke-RestMethod
  - Mikrotik
  - RouterOS
hexo_id: 796
---

# Background

I have, for a time, been using [CloudFlare](http://www.cloudflare.com "CloudFlare Website") for CDN, Optimizations and DNS Management for this and a few other domains. At the same time, I've been using [DynDNS](http://www.dyn.com "Dyn DNS") to provide name resolution to my home network/lab. Browsing around the [CloudFlare JSON API](https://www.cloudflare.com/docs/client-api.html "CloudFlare Client Api") I noticed that I can update DNS records through some fairly simple HTTP GET requests, and since the RouterOS (the operating system used by [Mikrotik's](http://www.mikrotik.com/ "Mikrotik Website") routerboards) has support for some pretty decent scripting I decided to let my router update CloudFlare for some custom and free dynamic DNS resolution.

# Attribution

My current script is a modified version of a script developed by Konstantin Antselovich.

Original script: [http://konstant1n.livejournal.com/9759.html](http://konstant1n.livejournal.com/9759.html "Random Journal")

Original Author website: [http://konstantin.antselovich.com/](http://konstantin.antselovich.com/ "Konstantin Antselovich")

Thanks!

# How you do it

## What you need

* RouterOS v6+ for HTTPS support
* Cloudflare API key, aka "Token", found at the [account page](https://www.cloudflare.com/my-account "CloudFlare Account Page")
* Cloudflare DNS Zone name
* Cloudflare Record Id (more on that later)
* Cloudflare subdomain name
* Name of the external router interface

<!--more-->

## Getting the Record Id

To get the record id of the DNS record you want to update, I used the _[rec_load_all](https://www.cloudflare.com/docs/client-api.html#s3.3 "rec_load_all - Get all DNS Records")_ function of the API. And since I'm a windows admin, I use powershell for that.

```powershell
$cfDomain = "homelab"
$cfToken = "<your API Key/Token>"
$cfZone = "example.com"
$cfEmail = "<your CF email address>"
$apiLoadAllRecordsURI = "https://www.cloudflare.com/api_json.html?a=rec_load_all&tkn=$cfToken&email=$cfEmail&z=$cfZone"
$restRequest = Invoke-RestMethod -Uri $apiLoadAllRecordsURI
$restRequest.response.recs.objs | ?{$_.display_name -eq $cfDomain} | fl -Property rec_id,name,display_name,type,ttl,service_mode
```

That should, given that you've replaced all the example variables produce something like this:

```text
rec_id : 16606003
name : homelab.example.com
display_name : homelab
type : A
ttl : 1
service_mode : 0
```

And with that done, you should have everything necessary for the RouterOS script.

## Building the Script

I'm not going to go into the [syntax of ros scripts](http://wiki.mikrotik.com/wiki/Manual:Scripting "RouterOS Scripting Manual"), but I'll try to explain the different building block to some degree.

### Defining our variables

First, we'll define out variables used for the script. The global _$hostname_ variable is actually redundant as I could derive the FQDN from  _$CFDomain_ and _$CFZone_, but it's used in other scripts in my router so it's included for that purpose alone.

```text
######## Set and collect general variables #########
:global hostname "homelab.example.com"
:global resolvedIP ""
:global externalIP ""
:global WANInterface "eth1-ext-internet"

######## Set CloudFlare variables #################
:local CFemail "<same email as in the powershell script"
:local CFtkn "<your API key/token>"
:local CFzone "example.com"
:local CFid "16606003"
:local CFtype "A"
:local CFttl "1"
:local CFservicemode "0"
:local CFDomain "homelab"
:local CFDebug "true"
```

Take care to verify and compare the CFxx variables with the ones used in and received from the previous powershell script, but also the _$hostname_ variable.

* hostname: Used in the script to lookup the currently set IP-address.
* WANInterface: The list name of the external interface, used to find the external IP-address.
* CFemail: Your CloudFlare Login email.
* CFtkn: Your API Key/Token.
* CFzone: Your DNS Zone.
* CFid: The rec_id from the powershell script.
* CFtype: A for IPv4 host records, AAAA for IPv6.
* CFttl: Record time-to-live, use "1" for automatic.
* CFservicemode: Use "0" for direct traffic or "1" to go through their CDN, Optimizations and Security features. I recommend "0" for anything but websites.
* CFDomain: Subdomain or rather hostname for your router.
* CFDebug: Use "True" to print some informational stuff to the router logs.

### Resolve IP-addresses

Next, we resolve two IP-addresses. First one, _$externalIP_, is the routers current external address. And the second, _$resolvedIP_, is the address currently set for our _$hostname_.

```text
######## Resolve and set IP-variables ##########
:local currentIP [/ip address get [/ip address find interface=$WANInterface ] address];
:set externalIP [:pick $currentIP 0 [:find $currentIP "/"]];
:set resolvedIP [:resolve $hostname];
```

### Build CF API Request and log debug info

Now, build the URI for the API call from our variables.

```text
######## Build CF API Url #########################
:local CFurl "https://www.cloudflare.com/api_json.html\3F"
:set CFurl ($CFurl . "a=rec_edit&tkn=$CFtkn&id=$CFid");
:set CFurl ($CFurl . "&email=$CFemail&z=$CFzone&type=$CFtype");
:set CFurl ($CFurl . "&name=$CFDomain&service_mode=$CFservicemode&ttl=$CFttl");
```

And if the _$CFdebug_ variable is set to "true", write a little info to the router log.

```text
######## Write debug info to log #################
:if ($CFDebug = "true") do={
:log info ("CF: hostname = $hostname")
:log info ("CF: resolvedIP = $resolvedIP")
:log info ("CF: currentIP = $currentIP")
:log info ("CF: externalIP = $externalIP")
:log info ("CF: CFurl = $CFurl&content=$externalIP")
};
```

### Compare and Update

Last step is to compare _$externalIP_ with _$resolvedIP_. If they don't match, our external IP-address has been changed and we need to update the DNS record. To execute the HTTP GET request we use a RouterOS tool called [fetch](http://wiki.mikrotik.com/wiki/Fetch "Mikrotik Manual: Fetch") to which we pass the _$CFurl_ variable. The reason this will not work before RouterOS v6+ is that before that there was no support for HTTPS, and CloudFlare does not accept unencrypted traffic for their APIs.

The script block is pretty straight-forward. Compare, update, flush local DNS-cache and write to the log.

```text
######## Compare and update CF if necessary #####
:if ($resolvedIP != $externalIP) do={
:log info ("CF: Updating CF, setting $CFDomain = $externalIP")
/tool fetch mode=https url="$CFurl&content=$externalIP" keep-result=no
/ip dns cache flush
} else={
:log info "CF: No Update Needed!"
}
```

### Permissions/Policies

This part, I'm not entirely sure on. The script needs to do name resolution, read settings and set variables and it works for me with these policies configured:

* Read
* Write
* Test
* Sniff
* Sensitive

It might be over-doing it a bit, but I have not had occasion to fiddle with them yet.

### Scheduling

I have this script scheduled to run once every 20 minutes. As it will only try to update the DNS records if there is a difference between them and the current external IP-address I feel fairly sure that I won't be tagged as a spammer or something by CloudFlare.

The schedule is configured with:

* Start Time: startup
* Interval: 00:20:00
* On Event: `/system script run <Name of your script>`
* Policy: Read,Write, Test, Sniff, Sensitive

This schedule is also a good place for a [hairpin](http://wiki.mikrotik.com/wiki/Hairpin_NAT "Mikrotik Wiki: Hairpin NAT") update if it's needed.

# The Copy-Paste part

Now, obviously, at least make sure you proof-read the script before putting it into production. I am not a network dude, and I rarely dabble with ROS scripts. I am certain that anyone with a bit more experience could create a smarter, prettier version of this script, so **use at your own risk**. Anyway, here's the script in it's entirety.

```text
######## Set and collect general variables #########
:global hostname "homelab.example.com"
:global resolvedIP ""
:global externalIP ""
:global WANInterface "eth1-ext-internet"

######## Set CloudFlare variables #################
:local CFemail "<same email as in the powershell script"
:local CFtkn "<your API key/token>"
:local CFzone "example.com"
:local CFid "16606003"
:local CFtype "A"
:local CFttl "1"
:local CFservicemode "0"
:local CFDomain "homelab"
:local CFDebug "true"

######## Resolve and set IP-variables ##########
:local currentIP [/ip address get [/ip address find interface=$WANInterface ] address];
:set externalIP [:pick $currentIP 0 [:find $currentIP "/"]];
:set resolvedIP [:resolve $hostname];

######## Build CF API Url #########################
:local CFurl "https://www.cloudflare.com/api_json.html\3F"
:set CFurl ($CFurl . "a=rec_edit&tkn=$CFtkn&id=$CFid");
:set CFurl ($CFurl . "&email=$CFemail&z=$CFzone&type=$CFtype");
:set CFurl ($CFurl . "&name=$CFDomain&service_mode=$CFservicemode&ttl=$CFttl");

######## Write debug info to log #################
:if ($CFDebug = "true") do={
:log info ("CF: hostname = $hostname")
:log info ("CF: resolvedIP = $resolvedIP")
:log info ("CF: currentIP = $currentIP")
:log info ("CF: externalIP = $externalIP")
:log info ("CF: CFurl = $CFurl&content=$externalIP")
};

######## Compare and update CF if necessary #####
:if ($resolvedIP != $externalIP) do={
:log info ("CF: Updating CF, setting $CFDomain = $externalIP")
/tool fetch mode=https url="$CFurl&content=$externalIP" keep-result=no
/ip dns cache flush
} else={
:log info "CF: No Update Needed!"
}
```
