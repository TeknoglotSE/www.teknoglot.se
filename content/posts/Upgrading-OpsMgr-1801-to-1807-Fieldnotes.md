---
title: "Upgrading #OpsMgr 1801 to 1807 - Fieldnotes"
date: 2018-09-06 14:42:51
lastmod: 2019-07-30T16:15:14+02:00
url: /ms/opsmgr1801/Upgrading-OpsMgr-1801-to-1807-Fieldnotes/
description: My Fieldnotes are quick, unrefined notations and reflections from the field.  Content may be obvious and unnecessary to some, useful to others.The main purpose is for them to be used as a searchable n
excerpt: My Fieldnotes are quick, unrefined notations and reflections from the field. Content may be obvious and unnecessary to some, useful to others.The main purpose is for them to be used as a searchable notebook.These Notes are not to be seen as a manual, a how-to or a set ofinstructions, but rather a collection of thoughts, reflectionsand experiences from my field-work. Abstract Upgrades from OpsMgr (SCOM) 1801 to 1807 is generally a safe operation. Can be done using Windows Update if you want to, but I would suggest only letting Management Servers, Reporting Servers and Web Console servers pre-load the update for a controlled update at a suitable time. I general, the updates goes smooth, but you still have to run the SQL-script(s) and import the updated Management Packs provided with the update. This should be done directly after updating the last Management Server. Links Official Documentation Download Location Announcement Blog What’s New! - Webinar Recording List of fixes Notes Updating the Management Servers Fairly quick update, may need a restart afterwards. On occasion, especially if the patch has to wait on shutting down the management server services (healthservice, omsdk, cshost) due to backlogs or high load, it might fail at replacing the binaries. You will notice this as the management server will go grey in the SCOM Console and you might find connectivity errors in the OperationsManager eventlog. If this happens, can be fixed by simply applying the patch again after a reboot.
cats:
  - ms
  - Fieldnotes
  - Fieldnotes/OpsMgr
  - ms/opsmgr1807
  - ms/opsmgr1801
tags:
  - Fieldnotes
---

```text
My Fieldnotes are quick, unrefined notations and reflections from the field.  
Content may be obvious and unnecessary to some, useful to others.
The main purpose is for them to be used as a searchable notebook.
These Notes are not to be seen as a manual, a how-to or a set of
instructions, but rather a collection of thoughts, reflections
and experiences from my field-work.
```

## Abstract

Upgrades from OpsMgr (SCOM) 1801 to 1807 is generally a safe operation. Can be done using Windows Update if you want to, but I would suggest only letting Management Servers, Reporting Servers and Web Console servers pre-load the update for a controlled update at a suitable time.  

I general, the updates goes smooth, but you still have to run the SQL-script(s) and import the updated Management Packs provided with the update. This should be done directly after updating the last Management Server.

## Links

- [Official Documentation](https://docs.microsoft.com/en-us/system-center/scom/upgrade-1801-to-1807?view=sc-om-1807)
- [Download Location](http://www.catalog.update.microsoft.com/Search.aspx?q=4133779)
- [Announcement Blog](https://blogs.technet.microsoft.com/momteam/2018/07/25/system-center-operations-manager-1807-is-released/)
- [What's New! - Webinar Recording](https://squaredup.com/blog/whats-new-in-scom-1807/)
- [List of fixes](https://support.microsoft.com/en-us/help/4133779/system-center-operations-manager-version-1807)

## Notes

### Updating the Management Servers

Fairly quick update, may need a restart afterwards.

On occasion, especially if the patch has to wait on shutting down the management server services (healthservice, omsdk, cshost) due to backlogs or high load, it might fail at replacing the binaries. You will notice this as the management server will go grey in the SCOM Console and you might find connectivity errors in the OperationsManager eventlog.  
If this happens, can be fixed by simply applying the patch again after a reboot.

### Updating the database(s)

The official documentation say that you should "Apply SQL scripts" (plural) then only mentions the `Update_rollup_mom_db.sql` script. Not entirely sure what gives? I've only applied the mentioned script file, and that's been working so far. The DW-script don't seem to be doing very much anyway.

## Afterthoughts

Apart from the vague instructions regarding the SQL-scripts, the 1807 upgrade is pretty straight-forward. Alhough, given the recent experiences with 1801, I am far more cautious going into these semi-annual updates going forth.

I am a bit dissapointed with the actual update, though. There's *very* little going on between these, supposedly larger, updates compared to what we got with the old Update Rollups.

Not much more to say on that front, perhaps there will be something interesting in SCOM 2019...  
¯\\_(ツ)_/¯
