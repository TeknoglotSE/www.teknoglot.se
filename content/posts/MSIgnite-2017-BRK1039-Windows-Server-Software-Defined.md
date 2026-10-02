---
title: "#MSIgnite 2017: BRK1039 - Windows Server Software Defined"
date: 2017-09-26 10:23:13
year: 2017
month: 09
lastmod: 2017-09-28T18:15:59-04:00
url: /Events/MSIgnite-2017/MSIgnite-2017-BRK1039-Windows-Server-Software-Defined/
url_encoded: /Events/MSIgnite-2017/MSIgnite-2017-BRK1039-Windows-Server-Software-Defined/
description: BRK1039 - Windows Server Software Defined The fastest route to the benefits of hyper-converged infrastructure WinSrv 2016, “Most cloud ready OS”, “Security” etc Talking about how WS2016 makes it poss
excerpt: BRK1039 - Windows Server Software Defined The fastest route to the benefits of hyper-converged infrastructure WinSrv 2016, “Most cloud ready OS”, “Security” etc Talking about how WS2016 makes it possible to define Network, Compute and Storage in software, as virtual machines/Applicances. WSSD Microsoft defines reference architecture, Solution vendors make and certify hardware packages, customers use and get rekommendations from Microsoft and vendors. Benefits Pre-validated Partner validated against reference architecture Time to value Up and running quickly Optimized OOB Less guesswork Tuned for the hardware solution Hardware Choice Select best match from vendors Converged Storage VMs on SMB3 on S2D on SOFS Cluster
cats:
  - Events
  - Events/MSIgnite-2017
tags:
  - MSIgnite
  - Presentation Notes
  - Hyper-Converged
  - WSSD
---

# BRK1039 - Windows Server Software Defined

`The fastest route to the benefits of hyper-converged infrastructure`

WinSrv 2016, "Most cloud ready OS", "Security" etc

Talking about how WS2016 makes it possible to define Network, Compute and Storage in software, as virtual machines/Applicances.

## WSSD

Microsoft defines reference architecture, Solution vendors make and certify hardware packages, customers use and get rekommendations from Microsoft and vendors.

### Benefits

- Pre-validated
    - Partner validated against reference architecture
- Time to value
    - Up and running quickly
- Optimized OOB
    - Less guesswork
    - Tuned for the hardware solution
- Hardware Choice
    - Select best match from vendors

### Converged Storage

VMs on SMB3 on S2D on SOFS Cluster

### Hyper-Converged

VM on S2D SOFS Cluster
Simpler management and deployment, all contained in each "box". 

### Cloud-Inspored Infrastructure

Functionality|Hyper-Converged Standard|Hyper-Converged Premium|Converged SDS
---|---|---|---
Security|Y|Y|Y
SDN|N|Y|N
Networking|Y|Y|Y
Compute|Y|Y|N
Storage|Y|Y|Y
Server|Y|Y|Y

### Key Use Cases

- Low-cost high-performance storage
    - FileServer, Hyper-V, Databases, Media streaming, High-throughput data ingestion
- Infrastructure for VM
    - Enterprise Apps, VDI, Hosting, IT Infrastructure aka Fabric
- SQL Server Databases
- Backup/Archive

>Some of the examples given in this section looks less like Hyper-Converged and more like a tad smarter file clusters.

### WSSD reference architecture

- Design Overview
    - Hardware Requirements
    - Expansion
- Server Hardware
- Server and Cluster Configuration
- Net Configuration
- Storage Configuration
- Security Configuration

Then, from requested or required workload, decide what offering (Hyper-Converged Infrastructure or Converged) and design to use.

### Quality-Assurance - End to End

- Comp and System Certification
    - IHV & Server Vendor
    - Win2016 Logo + SDDC Qualifiers
- Solution Validation
    - Solution Vendor
        - reference architecture
        - Stress
        - Quality-Assurance

### PCS - Private Cloud Simulator

Cool, but can I run it myself?

It is a public tool, but it might need a partner login to access, speaker was unsure. Speaker also suggested that, while it is possible for us to use the tool, it is not developed as a load-tester for any other than the WSSD solution developers. 

*It would probably be better for us to stick to tools like [VMFleet](https://github.com/Microsoft/diskspd/tree/master/Frameworks/VMFleet).*

### Automated Deployment

This is offered by WSSD Partner, although Microsoft has a DSC-kit prepared.

### Customer "demo"

- Moving from Server Cluster + iSCSI
- Mostly File Servers and SQL
- Maxed out at 15000 IOPS
- Latency spikes of 50-100ms (ouch)

Went to:
- S2D
    - Hyper-Converged Infrastructure
    - Hyper-V + Storage on the same node
- Simple
- Fault tolerant
- Good performance
- Lower costs

Opted for DataOn S2d-3216

Tested with VMFleet
- 2225479 IOPS
- 6,6MB/s throughput
- 0.99 Microsoft latency

These tested numbers have held true when in production as well.

## Personal Reflections

Again, very little real world talk. It's all happy-sunshine-candyland.

I have customers that are testing HCI, and from them I know that there is some things you really have to think about to succeed. It would be nice to hear what parts of the WSSD-rollout was super easy and a little on what popped up as "gotchas".

All these IOPS gains; are they from the S2D clusters or mainly from going from SAS/SATA to SSD? Not sure what kind of disks they had before and what performance the could have gotten from simply upgrading their storage. 



