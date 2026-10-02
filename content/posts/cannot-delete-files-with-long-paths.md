---
title: Cannot Delete Files with Long Paths?
date: 2009-10-21 09:39:17
year: "2009"
month: "10"
lastmod: 2018-08-28T15:29:58+02:00
url: /ms/windows/cannot-delete-files-with-long-paths/
url_encoded: /ms/windows/cannot-delete-files-with-long-paths/
description: What do you do when you cannot delete a file or folder on a windows server? Check the file permissions! And if that doesn’t help? Check the share permissions! Yes, if it is a shared folder. And if tha
hexo_slug: cannot-delete-files-with-long-paths
excerpt: "What do you do when you cannot delete a file or folder on a windows server? Check the file permissions! And if that doesn’t help? Check the share permissions! Yes, if it is a shared folder. And if that doesn’t help? Check the file ownership! Great! But then what? Well, the file could be in use, and then you would have to shut the locking process down and perhaps kick a user out. In a really bad scenario it could also be a symptom of a broken filesystem, a reserved filename (like “lpt1” or “PRN”) or even an invalid name (silly things like a space in the beginning or the end of a filename). Another possible reason could actually be that the path to the file or folder is too long. You won’t actually get an error telling you that the filepath exceeds the 255 characters Windows can handle but a simple “Acces Denied”. There are some, more or less tedious, work-arounds for the problem. Like renaming, starting from the root, all the directories to shorter ones or using the old DOS (8.3, like “dokume~1.doc”) names that windows can auto-generate for you. Personally, I have two favourite ways of handling this. Map the parent-directory of the file/folder you are trying to access/delete as a network drive and access your files that way. This is particularly useful if the folder you are trying to access a DFS-share or perhaps a share on the central fileserver filepaths like \\\\servername01\\Central Projects\\Central Services\\IT Department\\Develop Methods for Automatically Deploying New Central Servers\\2.2.1 Auto-Deploying SQL-Server 2005 Cluster\\Documents\\Preparations\\Whitepapers\\SQL Server 2005 Failover Clustering White Paper.doc Create a new share to a folder further down the hierarchy. This works locally too if you are logged on to, say, SRV01, you create a new share on D:\\\\Central Projects\\Central Services\\IT Department\\Develop Methods for Automatically Deploying New Central Servers\\ called Autodeploymethods and access it from \\\\SRV01\\Autodeploymethods. That way the filepath doesn’t exceed 255 characters. Now. When designing fileservers, you really should think about how deep the filepaths may get. This is especially true on DFS-shares since you might have to deal with the full FQDN too, and not only the actual folder structure. Many big corporations I know uses “codes” for departments and assign a project ID (quite simply a number or maybe an abbreviation) to each project and uses theese for the fileshares too. Another scenario that could lead to similar problems are intranet sites where users can create and manage their own subsites and where filenames and folders are not stored in a database. I have only seen this phenomena on Windows systems so far, and I’ve actually used a linux Live-CD on occasion when admin access is denied. Read More: http://support.microsoft.com/kb/320081"
cats:
  - ms
  - ms/windows
tags:
  - Windows
  - Errors
  - KB
  - Windows 2008
  - Windows Vista
  - Windows XP
hexo_id: 171
---

What do you do when you cannot delete a file or folder on a windows server?

Check the file permissions! And if that doesn’t help?

Check the share permissions! Yes, if it is a shared folder. And if that doesn’t help?

Check the file ownership! Great! But then what?

Well, the file could be in use, and then you would have to shut the locking process down and perhaps kick a user out. In a really bad scenario it could also be a symptom of a broken filesystem, a reserved filename (like “lpt1” or “PRN”) or even an invalid name (silly things like a space in the beginning or the end of a filename).
Another possible reason could actually be that the path to the file or folder is too long. You won’t actually get an error telling you that the filepath exceeds the 255 characters Windows can handle but a simple “Acces Denied”.

There are some, more or less tedious, work-arounds for the problem. Like renaming, starting from the root, all the directories to shorter ones or using the old DOS (8.3, like “dokume~1.doc”) names that windows can auto-generate for you. Personally, I have two favourite ways of handling this.

1. Map the parent-directory of the file/folder you are trying to access/delete as a network drive and access your files that way.
  This is particularly useful if the folder you are trying to access a DFS-share or perhaps a share on the central fileserver filepaths like `\\servername01\Central Projects\Central Services\IT Department\Develop Methods for Automatically Deploying New Central Servers\2.2.1 Auto-Deploying SQL-Server 2005 Cluster\Documents\Preparations\Whitepapers\SQL Server 2005 Failover Clustering White Paper.doc`
2. Create a new share to a folder further down the hierarchy.  
  This works locally too if you are logged on to, say, SRV01, you create a new share on `D:\\Central Projects\Central Services\IT Department\Develop Methods for Automatically Deploying New Central Servers\` called `Autodeploymethods` and access it from `\\SRV01\Autodeploymethods`. That way the filepath doesn’t exceed 255 characters.

Now. When designing fileservers, you really should think about how deep the filepaths may get. This is especially true on DFS-shares since you might have to deal with the full FQDN too, and not only the actual folder structure. Many big corporations I know uses “codes” for departments and assign a project ID (quite simply a number or maybe an abbreviation) to each project and uses theese for the fileshares too. Another scenario that could lead to similar problems are intranet sites where users can create and manage their own subsites and where filenames and folders are not stored in a database.

I have only seen this phenomena on Windows systems so far, and I’ve actually used a linux Live-CD on occasion when admin access is denied.
> Read More:
> [http://support.microsoft.com/kb/320081](http://support.microsoft.com/kb/320081)

*[DFS]: Distributed File System
*[FQDN]: Fully Qualified Domain Name