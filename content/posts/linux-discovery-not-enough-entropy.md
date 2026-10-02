---
title: Linux Discovery – Not Enough Entropy
date: 2009-12-02 12:37:08
lastmod: 2016-05-25T00:33:26+02:00
url: /linux/sles/linux-discovery-not-enough-entropy/
url_encoded: /linux/sles/linux-discovery-not-enough-entropy/
cats:
  - linux
  - linux/sles
tags:
  - OpsMgr
  - How-To
  - Linux
  - TroubleShooting
  - X-Plat
hexo_id: 243
---

# Error Description

Here’s a little trouble-shooting guide for discovering Linux systems from OpsMgr R2 when getting the following error from the wizard:

```xml
<stdout>Generating certificate with hostname="COMPUTERNAME"

[/home/serviceb/TfsCoreWrkSpcRedhat/source/code/tools/scx_ssl_config/scxsslcert.cpp:198]

Failed to allocate resource of type random data: Failed to get random data - not enough entropy

</stdout><stderr>error: %post(scx-1.0.4-248.i386) scriptlet failed, exit status 1

</stderr><returnCode>1</returnCode>

<DataItem type="Microsoft.SSH.SSHCommandData" time="2009-08-05T11:15:01.5800358-04:00" sourceHealthServiceId="0EB1D6DA-202C-7FC5-3D46-BDBB9208547D"><SSHCommandData><stdout>Generating certificate with hostname="COMPUTERNAME"

[/home/serviceb/TfsCoreWrkSpcRedhat/source/code/tools/scx_ssl_config/scxsslcert.cpp:198]

Failed to allocate resource of type random data: Failed to get random data - not enough entropy

</stdout><stderr>error: %post(scx-1.0.4-248.i386) scriptlet failed, exit status 1

</stderr><returnCode>1</returnCode></SSHCommandData></DataItem>
```

But first, a little background on the actual “problem”. To generate the certificate, the _entropy_ needs to be high enough to generate random data for the certificate creation. Without the certificate, the OpsMgr agent won’t be able to open up communications with the <acronym title="Management Server">MS</acronym>. So, what creates this entropy we need? Bluntly put, a selection of hardware components that are likely to produce non-predictable data. Like a keyboard, mouse and a monitor or videocard. Of course, there’s a lot more to it, but we really don’t need to know this. What _we_ need to know is that there has to be a “bit bucket” of more than 256bytes of entropy for the certificate creation process to succeed. We also need to know that more enterprise-ish servers, like rack- or blade-servers tend to be void of things like directly attached keyboards, mouses and monitors that the linux kernel needs to be able to generate entropy. And herein lies the problem. If you have a new server that is not in full service (likely since we are trying to deploy the monitoring on it) which means that there’s not much random data flowing through the hardware and there’s no keyboard or mouse or monitor connected to it there is quite the risk that the system entropy is going to be very low. Of the linux systems that I have been deploying OpsMgr agents to, about half have failed because of “Not enough entropy”. So, here’s the steps I usually takes to ensure that discovery works. I use [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) to connect to the soon-to-be-monitored servers. This guide also assumes that you have SU rights on the system since all of these steps (except #1) needs it.

# Workaround

## 1. Check you current entropy

```text
cat /proc/sys/kernel/random/entropy_avail
```

Is it less than, or close to, 256? It probably is. If you don’t feel like connecting a mouse and start wiggling it around—not really feasible in a data center—and see if the entropy increases, you can generate your own random data.

## 2. Generate you own random data.
Be advised that this forced entropy will not be as random as the system-created on and thus not as secure. How much more insecure it is, I don’t know, and quite frankly I prefer to have my systems monitored yet slightly less secure than not monitored at all. Anyway, you can force your own random data by running:

```text
dd if=/dev/urandom of=~/.rnd bs=1 count=1024
```

This creates a .rnd file with 1024B of random data that the certificate creation process will use instead of the system entropy if the file exists.

## 3. Uninstall and re-discover

The first failed attempt of discovery will most likely leave a non-working agent installation that we have to remove. Otherwise we will just be stuck with an “Access Denied” error. Run:

```text
rpm –e scx
```

Now, try to discover the system again.

## 4. Failed again?

Try generating the certificate manually by running:

```text
/opt/microsoft/scx/bin/tools/scxsslconfig -f –v
/opt/microsoft/scx/bin/tools/scxadmin –restart
```

Retry discovery again.

## 5. Still fails?

Uninstall the agent once more as instructed in step 3.
Stese steps have solved my problems 100% on both SUSE and RedHat and hopefully they will help you too.

Interestingely enough, these problems seems to be connected to some changes in the 2.6 kernel and basically everything that uses SSL-ish certificates will be affected. Even though the symptoms may be a bit more subtle, like time-outs and disconnects. For “headless” servers like those I usually to administer where the random data tend to be much lower, there’s even specialised hardware whose sole purpose is to generate random data, like the [Entropy Key](http://www.entropykey.co.uk/). I have also been told that new servers is likely to be equipped with entropy chipsets to make sure that there’s chaos enough to avoid these new-found oddities.

> Sources:
> [http://social.technet.microsoft.com/Forums/en-US/crossplatformsles/thread/f94ec905-23ac-4444-b9f8-644fec3ae357](http://social.technet.microsoft.com/Forums/en-US/crossplatformsles/thread/f94ec905-23ac-4444-b9f8-644fec3ae357 "http://social.technet.microsoft.com/Forums/en-US/crossplatformsles/thread/f94ec905-23ac-4444-b9f8-644fec3ae357")

> [http://www.askrenzo.com/oracle/SCOM/SCOM_discovering_nodes.html
> ](http://www.askrenzo.com/oracle/SCOM/SCOM_discovering_nodes.html "http://www.askrenzo.com/oracle/SCOM/SCOM_discovering_nodes.html")