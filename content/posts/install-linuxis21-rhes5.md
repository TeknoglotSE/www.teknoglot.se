---
title: Installing Linux Integration Services v2.1 on Red Hat ES 5
date: 2010-08-31 12:06:04
year: "2010"
month: "08"
lastmod: 2018-08-28T15:16:14+02:00
url: /linux/rhes/install-linuxis21-rhes5/
url_encoded: /linux/rhes/install-linuxis21-rhes5/
description: Ok, so I got the task to install the Linux Integration Service for Hyper-V R2 on a RedHat Enterprise Server 5. Something that turned out to be a bit more to handle than I would have thought. So here’s
hexo_slug: install-linuxis21-rhes5
excerpt: "Ok, so I got the task to install the Linux Integration Service for Hyper-V R2 on a RedHat Enterprise Server 5. Something that turned out to be a bit more to handle than I would have thought. So here’s a little How-To. Preparations Read the documentation provided in the Linux Integration Services download. Much of the information in this article is in there, but some parts are not. Otherwise I would not have bothered writing about it. 😉 I’m not going to go through the OS installation process here, but make sure to select the “Software Development” packages since you will be needing it. In case you missed it, you can install them later by running these commands. # yum groupinstall \"Development Tools\"# yum install kernel-headers I’m not actually sure that you need to run the kernel-headers install manually or if it’s included in the “Development Tools” package. The first gotcha i ran into was the fact that the link to the Linux Integration Services–previously known as Linux Integration Components or LinuxIC–on RedHat’s information pages gave me a 404 and a redirect to a bing-search that returned the exact same 404. The page have simply been removed by Microsoft without any form of redirection to the new page. Anyway, a search on http://download.microsoft.com for “Linux Integration Components” do return the new page, and that’s where I learned about the new name. Thank you for making it easy for us Microsoft! Here’s a direct link to the search on the current name. And here’s a direct link to the actual download page. This download contains an ISO file that you can mount using the Hyper-V- or VMM-console, or you can do as I did and download the ISO to the virtual machine, mount it locally, copy the files and unmount it. Like this. # mkdir /mnt/ISO# mount -o loop /root/LinuxIC v21.iso /mnt/ISO# mkdir /opt/linux_ic_v21_rtm# cp /mnt/ISO/* -R /opt/linux_ic_v21_rtm/# umount /mnt/ISO"
cats:
  - linux
  - linux/rhes
tags:
  - How-To
  - Hyper-V
  - Linux
  - RedHat
  - RHES5
hexo_id: 291
---

Ok, so I got the task to install the Linux Integration Service for Hyper-V R2 on a RedHat Enterprise Server 5\. Something that turned out to be a bit more to handle than I would have thought. So here's a little How-To.

# Preparations

Read the documentation provided in the Linux Integration Services download. Much of the information in this article is in there, but some parts are not. Otherwise I would not have bothered writing about it. ;)

I'm not going to go through the OS installation process here, but make sure to select the "Software Development" packages since you will be needing it. In case you missed it, you can install them later by running these commands.

```bash
# yum groupinstall "Development Tools"
# yum install kernel-headers
```

I'm not actually sure that you need to run the kernel-headers install manually or if it's included in the "Development Tools" package.

The first gotcha i ran into was the fact that the link to the Linux Integration Services--previously known as Linux Integration Components or LinuxIC--on RedHat's information pages gave me a 404 and a redirect to a bing-search that returned the exact same 404\. The page have simply been removed by Microsoft without any form of redirection to the new page. Anyway, a search on [http://download.microsoft.com](http://download.microsoft.com) for "Linux Integration Components" do return the new page, and that's where I learned about the new name.  
Thank you for making it easy for us Microsoft!

- Here's a [direct link to the search on the current name.](http://www.microsoft.com/downloads/en/results.aspx?freetext=linux+integration+services&displaylang=en&stype=s_basic)
- And here's a [direct link to the actual download page.](http://www.microsoft.com/downloads/details.aspx?displaylang=en&FamilyID=eee39325-898b-4522-9b4c-f4b5b9b64551)

This download contains an ISO file that you can mount using the Hyper-V- or VMM-console, or you can do as I did and download the ISO to the virtual machine, mount it locally, copy the files and unmount it. Like this.

```bash
# mkdir /mnt/ISO
# mount -o loop /root/LinuxIC v21.iso /mnt/ISO
# mkdir /opt/linux_ic_v21_rtm
# cp /mnt/ISO/* -R /opt/linux_ic_v21_rtm/
# umount /mnt/ISO
```

You probably have to be root to do this by the way.
With that done, let's get to the installation.

# Installation

As root, do the following:

```bash
# export PATH=$PATH:/sbin
# cd /opt/linux_ic_v21_rtm/
# make
 make install
# reboot
```

Why the export PATH command? Apparently, on RHES5, /sbin is not in the PATH by default and this is something that the make scripts are completely unaware of. The `make install` will try to run `depmod` which will fail since it's not in the default path.  
You could also add `PATH=$PATH/sbin` to the root users ~/.bashrc which will put it back in the PATH but only for the root user, but I don't know if that's recommended.
And, yes. You DO have to reboot after the install.

If you are running RHES5 64bit you also have to install the `adjtimex` package. It is in the RHN repository but also on the RHES5 Installation CD in case you have no internet connection. Install it with yum like this:

```bash
# yum install adjtimex
```

And from the CD (mount it first) like this:

```bash
# rpm –ivh /mnt/cdrom/Server/adjtimex-1.20-2.1.x86_64.rpm
```

And that's basically it for the installation.

# Verification

How do you know that the driver are installed?

Aftr the reboot, try running `modinfo vmbus` which should return something like this:

```bash
# modinfo vmbus
filename:       /lib/modules/2.6.18-194.11.1.el5/kernel/drivers/vmbus/vmbus.ko
verion:        2.1.25
licnse:        GPL
srcversion:     3C1899C419665CB2514F2D0
depends:
vermagic:       2.6.18-194.11.1.el5 SMP mod_unload gcc-4.1
parm:           vmbus_irq:int
par:           vmbus_loglevel:int
```

Try that with netvsc, storvsc and blkvsc too (replace the _vmbus_ part) and you should get something similar. If you don't, the installation did not succeed.
The documentation also tells us to check that the components are running with `/sbin/lsmod | grep vsc` which should return:

```bash
# /bin/lsmod | grep vsc
blkvsc                 70184  3
storvsc                64264  0
netvsc                 73504  0
vmbus                  88304  3 blkvsc,storvsc,netvsc
scs_mod              196953  6 scsi_dh,sg,blkvsc,storvsc,libata,sd_mod
```

The numbers will probably differ from installation to installation depending on blocksizes and allocation.

# Configuration

Configuration is pretty straight-forward so I'll keep this short.

When you install the drivers you will get a new network card called `seth0`, which I presume stands for **S**ynthetic **ETH**ernet. There's nothing magic about it regarding configuration and `system-configuration-network` will work just fine.
The drivers will also give you a couple of SCSI-devices (if you have one attached) with the regular `/dev/sd*` naming. Simply configure these using fdisk or whatever GUI you might prefer.

There is also a note in the documentation about changing the grub configuration in the "Additional Information..." section. Do read that section.

# Additional Comments

One thing I tend to do now that disk space is dirt cheap is to copy all ISO-files I use locally instead of mounting them when needed through Hyper-V. Simply because you can bet your insert-shorter-word-for-buttocks that the day you need it again, someone has been kind enough to have done som spring-cleaning or it's locked by another machine in the cluster. If you have it locally and followed my instructions in the "Preparation" section, you will allready have a /mnt/ISO directory. Only thing you'll have to do is

```bash
# mount -o loop /path/to/your.iso /mnt/ISO
```

And there you have it. Just remember to unmount it when you're done.

I also almost never use the Hyper-V remote connection interface thingy since it will give you a GUI and the mouse just won't work. If you haven't configured a network card yet though, you could connect through Hyper-V and hit _Ctrl+Alt+F1_ to get a command prompt. Unfortunatly cut/paste don't work here, but you could run `system-configuration-network`, assign an IP-address and then connect with an SSH client. I prefer PuTTY to a degree that I usually install the ported version on my Linux desktops as well.

And I never logon using root. People should know this, but it should be stressed anyway. Always logon as regular user and `su` or `sudo` when needed. I can't understand why RHES has root-login enabled by default in the SSH-server config.

Good luck!