---
title: NVidia problems in Ubuntu 8.10
date: 2008-11-10 09:20:14
lastmod: 2016-05-25T00:33:26+02:00
url: /linux/ubuntu/nvidia-problems-in-ubuntu-810/
url_encoded: /linux/ubuntu/nvidia-problems-in-ubuntu-810/
cats:
  - linux
  - linux/ubuntu
tags:
  - Drivers
  - NVidia
hexo_id: 98
---

[updated, scroll down if you want to skip some nonsense]

So, I did an upgrade to Ubuntu Studio 8.10 (basically Ubuntu with rt-kernel and lots of nice media-related packages easily accessible and a skin that rocks) from the earlier 8.04\. And the upgrade itself was really easy. I just opened the "Software Sources", set the  _Release upgrade_ to **Normal Releases** (you find it under the _Updates_ tab).
After that you get the option to do a _Distribution Upgrade_, which I did (took some 45 minutes to finish).

I did however run into some serious problems with the NVidia Drivers after the upgrade. Basically, the new drivers dont seem to install correctly under the new kernel. This conclusion took me a day of laborating with settings, installing packages, uninstalling packages, reinstalling packages and a whole lot of googling.

What I have come down to right now is doing the following:
> **sudo apt-get install module-assistant**
This will install the module assistant and it will also make sure that you have all the correct linux headers to install the NVidia drivers.

<span style="text-decoration: line-through;">Going back to the "Software Sources" under i check the "Unsopported updates".</span>
Then i execute
> <span style="text-decoration: line-through;">sudo apt-get autoremove</span>
> <span style="text-decoration: line-through;">sudo apt-get install nvidia-177-kernel-source</span>
> **m-a auto-install nvidia**
**UPDATE!**

After fiddling around with this Laptop (Lenovo Thinkpad T61) I really just needed these three steps to fix the problem. All of them from X using the regular nv-drivers.

1.  In a terminal, run _sudo apt-get install module assistant_
2.  In a terminal, run _sudo m-a auto-install nvidia_
3.  Open the "Hardware Drivers" application and pick the driver you want (177 in my case) and click Activate. If it worked alright, you'll get the green recycle icon and be asked to reboot to activate the settings.
Hopefully, this might help someone. It did work for me and I am now able to work with wobbly windows and all that crap. (Besides some serious 3d stuff ;) )

Anyway. Since I did not save the urls, I cannot give credit to those who have pointed to stuff that did help me on the way, but I've actually not find information anywhere yet that solve the problem totally and, well... that's why I did decide to post in here.

Feel free to leave a comment if you got any more info or if you got any help from this.