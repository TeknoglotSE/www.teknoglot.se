---
title: "Resize all images in a Word document with #vbs #macro"
date: 2016-07-05 22:08:26
year: 2016
month: 07
lastmod: 2016-07-05T23:26:16+02:00
url: /code/vbs/Resize-all-images-in-a-Word-document-with-vbs-macro/
url_encoded: /code/vbs/Resize-all-images-in-a-Word-document-with-vbs-macro/
description: TLDR Quick and dirty macro to resize all images in a word document to 145 mm. I am lazy like that. Get the gist of it here.  The “Why” Ok, so. I am a consultant, as you may know. And as a consultant,
excerpt: TLDR Quick and dirty macro to resize all images in a word document to 145 mm. I am lazy like that. Get the gist of it here. The “Why” Ok, so. I am a consultant, as you may know. And as a consultant, people pay me to do stuff and expect me to be efficient and deliver with high quality. Part of that entails writing documentation containing how I do stuff, where I do it and often why I do it. This documentation is expected to be detailed enough to make sure my customers will be able to follow the steps and produce a copy of my work. Most of the time these document are a big part of the disaster recovery processes and might have to be executed by the on-call staff with no previous knowledge of the product. This means screenshots. Lots of screenshots. And while templates are nice and help me out a lot, the screenshots have to be from the actual installation and not some copy-pasta from a previous assignment. To help me out, I use the excellent free program Greenshot to quickly generate screenshots into a WIP-folder (or directly into Word if that is appropriate) and that makes it possible to grab snapshots of the process without having to pause all the time to PrtScn-Alt+Tab-Ctrl+V-Crop-Ctrl+C-Alt+Tab-Ctrl+C. I simply press PrtScn and go on with the installation. Being a bit pedantic, doesn’t help me out here though as I find myself selecting and resizing all the images in the Word document I have produced. This is a very time-consuming process and not the most exact one either. I want all images to be of scaled, if necessary, to an equal maximum width that fits comfortably withing the margins of the document template my company has prepared for me. So I created a fairly simple macro to do it for me. The “How” If you are un-familiar with macros in Word, you will find them under the “View” tab. Clicking on “Macros” will give you the option to execute the ones you have, or you can create your own using VBA (Visual Basic for Applications). To create one, select where you want it saved (normal.dotx in my case, as I want it readily available) and enter a name for it. This will bring up the Visual Basic for Applications IDE, where you can write your own fun stuff.
cats:
  - code
  - code/vbs
tags:
  - VBScript
  - Macro
  - Word
  - Office
---

# TLDR

Quick and dirty macro to resize all images in a word document to 145 mm. I am lazy like that.

Get the gist of it [here][1].

# The "Why"

Ok, so. I am a consultant, as you may know. And as a consultant, people pay me to do stuff and expect me to be efficient and deliver with high quality.
Part of that entails writing documentation containing how I do stuff, where I do it and often why I do it.
This documentation is expected to be detailed enough to make sure my customers will be able to follow the steps and produce a copy of my work. Most of the time
these document are a big part of the disaster recovery processes and might have to be executed by the on-call staff with no previous knowledge of the product.

This means screenshots. Lots of screenshots.
And while templates are nice and help me out a lot, the screenshots have to be from the actual installation and not some copy-pasta from a previous assignment.
To help me out, I use the excellent free program [Greenshot][2] to quickly generate screenshots into a WIP-folder (or directly into Word if that is appropriate) and that makes it possible to
grab snapshots of the process without having to pause all the time to `PrtScn-Alt+Tab-Ctrl+V-Crop-Ctrl+C-Alt+Tab-Ctrl+C`. I simply press `PrtScn` and go on with the installation.

Being a bit pedantic, doesn't help me out here though as I find myself selecting and resizing all the images in the Word document I have produced. This is a *very* time-consuming process and not the most exact one either.
I want all images to be of scaled, if necessary, to an equal maximum width that fits comfortably withing the margins of the document template my company has prepared for me. 

So I created a fairly simple macro to do it for me.

# The "How"

If you are un-familiar with macros in Word, you will find them under the "View" tab.
Clicking on "Macros" will give you the option to execute the ones you have, or you can create your own using VBA (Visual Basic for Applications).
To create one, select where you want it saved (normal.dotx in my case, as I want it readily available) and enter a name for it.
This will bring up the Visual Basic for Applications IDE, where you can write your own fun stuff.

This little macro of mine is saved as a .bas file, which means I can import it into VBA by right-clicking the navigation and selecting "Import file...".
By doing that, and saving my changes, it is now available to me in any other word document, given that I saved it into the global template.

# The Macro

I've put it up on a [public gist][1] for anyone interested.
It is, currently, very specific for my templates but it's very easy to modify it to set images to a different size than 145 mm wide.
Give it a little love, and we could add options for width as well, but I dont need that right now.

And for those who don't want to travel all the way to Github, here's the script in it's current form.
<script src="https://gist.github.com/stegenfeldt/5d81ab5c57a3d20397a6b04a75b882e0.js"></script>



[1]: https://gist.github.com/stegenfeldt/5d81ab5c57a3d20397a6b04a75b882e0
[2]: http://getgreenshot.org/