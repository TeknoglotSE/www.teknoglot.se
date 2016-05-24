---
title: w3Socket in VBScript
tags:
  - Script
id: 59
categories:
  - Code
  - VBS
date: 2007-04-21 16:10:05
---

I've been doing quite a lot of VBScripting in a couple of projects lately. The current one requires med to connect to a couple of telnet servers and look for... stuff.
Since we're not in VB6 och .Net i cannot simply user Winsock as normally due to the lack of licensing features in <acronym title="VisualBasic Script">VBS</acronym>/<acronym title="Windows Scripting Host">WSH.</acronym>

Thankfully for me, [Dimac](http://www.dimac.com/ "Dimac") has release a [nifty little component](http://www.dimac.com/default3.asp?M=FreeDownloads/Menu.asp&amp;P=FreeDownloads/FreeDownloadsstart.asp "Dimac - Free Downloads") for free that makes talking telnet in VBS very simple.

I thought that, hey! I must share this!
So here's an example in Classic VBS:

```vbs
Dim oTelnet
oTelnet = CreateObject(Socket.Tcp)

With oTelnet
.DoTelnetEmulation = True
.TelnetEmulation = TTY
.Host = 192.168.242.1:23
.Open
.WaitFor SLUSSEN login:
.SendLine ANiftyUsename
.WaitFor Password:
.SendLine TEHP@ssw0rd
.WaitFor ~ #
.SendLine ifconfig
MsgBox .Buffer
.Close
End With

Set oTelnet = Nothing
```

Not very hard at all. This one is connecting to my router (with fake user/pwd... DUH!) and there's no support for setting the prompt type there, thus the "~ #".
The result of running this script with correct login info gives me a popup with the routers <acronym title="Network Interface Card">NIC</acronym>-configuration.