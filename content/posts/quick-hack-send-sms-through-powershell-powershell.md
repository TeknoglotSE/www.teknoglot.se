---
title: "Quick-Hack: Send SMS through Powershell [#powershell]"
date: 2012-05-15 15:14:00
year: 2012
month: 05
lastmod: 2016-05-25T00:33:26+02:00
url: /code/posh/quick-hack-send-sms-through-powershell-powershell/
url_encoded: /code/posh/quick-hack-send-sms-through-powershell-powershell/
description: Decided to do a quick-hack&#x2F;fast-publish on this one as I have had a bit less time to create a nice clean production-ready version as of yet… and people has been asking about how far off the article is
excerpt: "Decided to do a quick-hack/fast-publish on this one as I have had a bit less time to create a nice clean production-ready version as of yet… and people has been asking about how far off the article is. What this script does is to send a text message using a GSM/GPRS modem connected to a local (or LAN-connected with local drivers) serial port using Powershell. Disclaimer! This script “works” but is not fit for production. See it as an example of the general concept to evolve and adapt into something worthy of production use. What’s missing in the latest iteration is: A working Event-Handler to deal with asynchronous call-backs. Support for AT+MSGW (write to modem memory) Reusing messages in modem memory for multiple recipients. Various error- and exeption-handlers. Actually verifying that the modem is AT-capable. Querying the system for available modems and their ports. The Script So, a short note before digging into the script. Prerequisites for this script is that you have identified which COM-port to use and it’s supported baud-rates and whether it supports DTR or not. If you do not know what the hell I am talking about, you could probably have it work with my preconfigured settings anyway. If you are unsure about if your modem supports AT commands you could open a serial connection to the modem using Hyperterminal or PuTTY and run AT+CMGF=1. If supported, the return should be OK. If it is not supported (you get ERROR instead) you would have to use PDU-mode which require a bit of hex-encoding of your messages. This is nothing I have had to do yet and will not be including in this script. Maybe in the future. Maybe. So, looking a some powershelling then. First thing would be to connect to the modem. # Create your instance of the SerialPort Class$serialPort = new-Object System.IO.Ports.SerialPort# Set various COM-port settings$serialPort.PortName = \"COM1\"$serialPort.BaudRate = 19200$serialPort.WriteTimeout = 500$serialPort.ReadTimeout = 3000$serialPort.DtrEnable = \"true\"# Open the connection$serialPort.Open()"
cats:
  - code
  - code/posh
tags:
  - PoSH
  - GSM
  - Quick-hack
  - SMS
hexo_id: 607
---

Decided to do a quick-hack/fast-publish on this one as I have had a bit less time to create a nice clean production-ready version as of yet... and people has been asking about how far off the article is.

What this script does is to send a text message using a GSM/GPRS modem connected to a local (or LAN-connected with local drivers) serial port using Powershell.

# Disclaimer!

This script "works" but is not fit for production. See it as an example of the general concept to evolve and adapt into something worthy of production use.

What's missing in the latest iteration is:

* A working Event-Handler to deal with asynchronous call-backs.
* Support for AT+MSGW (write to modem memory)
* Reusing messages in modem memory for multiple recipients.
* Various error- and exeption-handlers.
* Actually verifying that the modem is AT-capable.
* Querying the system for available modems and their ports.


# The Script

So, a short note before digging into the script. Prerequisites for this script is that you have identified which COM-port to use and it's supported baud-rates and whether it supports DTR or not. If you do not know what the hell I am talking about, you could probably have it work with my preconfigured settings anyway. If you are unsure about if your modem supports AT commands you could open a serial connection to the modem using Hyperterminal or PuTTY and run AT+CMGF=1\. If supported, the return should be OK. If it is not supported (you get ERROR instead) you would have to use PDU-mode which require a bit of hex-encoding of your messages. This is nothing I have had to do yet and will not be including in this script. Maybe in the future. Maybe.

So, looking a some powershelling then. First thing would be to connect to the modem.

```powershell
# Create your instance of the SerialPort Class
$serialPort = new-Object System.IO.Ports.SerialPort
# Set various COM-port settings
$serialPort.PortName = "COM1"
$serialPort.BaudRate = 19200
$serialPort.WriteTimeout = 500
$serialPort.ReadTimeout = 3000
$serialPort.DtrEnable = "true"
# Open the connection
$serialPort.Open()
```

With the connection established, you the set to modem in AT-mode and start sending the message to the modem.

```powershell
# Tell the modem you want to use AT-mode
$serialPort.Write("AT+CMGF=1`r`n")

# Start feeding message data to the modem
# Begin with the phone number, international
# style and a <CL>... that's the `r`n part
$serialPort.Write("AT+CMGS=`"+46888888888`"`r`n")

# Now, write the message to the modem
$serialPort.Write("This is a test!`r`n")

# Send a Ctrl+Z to end the message.
$serialPort.Write($([char] 26))
```

As you may notice, the message is only stored in the modems memory until you send a Ctrl+z which will end the message and send it. It is possible to add more text to the message before sending it if you would like. Personally, I prefer to store the message into a regular powershell variable and pass that one to the script. The SerialPort library is sort of clever and a local phone number will probably work. For safety, I always use international number with country code as it will work every time.

Only thing left now is to close the serial port connection and end the script. Like this.

```powershell
$serialPort.Close()
```

## The Copy/Paste part

Here's the entire script with some added control-features and check to avoid trying to send text messages with no serial connection.

```powershell
### DISCLAIMER ###
## This script is a quick-hack to demonstrate
## the basics of sending an SMS using an AT-
## compatible GSM modem connected a local
## serial port through PowerShell.
## No error-handling is implemented and this
## is NOT a script fit for production.
##################

# Create your instance of the SerialPort Class
$serialPort = new-Object System.IO.Ports.SerialPort
# Set various COM-port settings
$serialPort.PortName = "COM1"
$serialPort.BaudRate = 19200
$serialPort.WriteTimeout = 500
$serialPort.ReadTimeout = 3000
$serialPort.DtrEnable = "true"
# Open the connection
$serialPort.Open()
# Add variables for phone number and the message.
$phoneNumber = "+46888888888"
$textMessage = "This is a test message!"

try {
 $serialPort.Open()
}
catch {
 # Wait for 5s and try again
 # Told you this is a quick-hack, right?
 Start-Sleep -Seconds 5
 $serialPort.Open()
}
If ($serialPort.IsOpen -eq $true) {
 # Tell the modem you want to use AT-mode
 $serialPort.Write("AT+CMGF=1`r`n")
 # Start feeding message data to the modem
 # Begin with the phone number, international
 # style and a <CL>... that's the `r`n part
 $serialPort.Write("AT+CMGS=`"$phoneNumber`"`r`n")
 # Give the modem some time to react...
 Start-Sleep -Seconds 1
 # Now, write the message to the modem
 $serialPort.Write("$textMessage`r`n")
 # Send a Ctrl+Z to end the message.
 $serialPort.Write($([char] 26))
 # Wait for modem to send it
 Start-Sleep -Seconds 1
}
# Close the Serial Port connection
$serialPort.Close()
if ($serialPort.IsOpen -eq $false) {
 echo "Port Closed!"
}

# That's all folks
# Now, add call-backs, event-handlers, and return-
# message handling.
```

Enjoy!