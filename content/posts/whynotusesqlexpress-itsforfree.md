---
title: Why not use SQL Express? It’s for free!
date: 2009-08-21 10:38:55
year: "2009"
month: "08"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/sql/whynotusesqlexpress-itsforfree/
url_encoded: /ms/sql/whynotusesqlexpress-itsforfree/
description: Background I get this question every now and then and every time I find myself completely flabbergasted and having to look things up once again. To avoid wasting my time on the same question once aga
hexo_slug: whynotusesqlexpress-itsforfree
excerpt: Background I get this question every now and then and every time I find myself completely flabbergasted and having to look things up once again. To avoid wasting my time on the same question once again and perhaps help others doing the same, here’s a little guidance. Don’t get me wrong now. SQL Express has it’s applications and for a free database server, it’s not half-bad. Small development sites, minor, not that extremely important systems with lower performance and feature demands, minor website databases et cetera could do well with SQL Express. My Checklist Here’s my list of questions you have to ask to find if SQL Express is the correct choice. 1. Do your applications support SQL Express? If your application developers cannot say “Yes” to this, you’re out of luck. You could probably get their applications to run on SQL Express anyway, but application support if something goes bad will most likely be zilch. 2. Do your applications fit the hardware limitations? SQL Express is limited to 1GB RAM, 1 CPU and 4GB of databases. 1GB of RAM seems a bit tight to me for any production data. Also, on SQL Express 2005, according to Microsoft, you cannot run parallel queries. ”SQL Server Express can install and run on multiprocessor machines, but only a single CPU is used at any time. Internally, the engine limits the number of user scheduler threads to 1 so that only 1 CPU is used at a time. Features such as parallel query execution are not supported because of the single CPU limit.”
cats:
  - ms
  - ms/sql
tags:
  - Checklist
  - SQL Express 2005
  - SQL Express 2008
hexo_id: 195
---

# Background

I get this question every now and then and every time I find myself completely flabbergasted and having to look things up once again. To avoid wasting my time on the same question once again and perhaps help others doing the same, here’s a little guidance.

Don’t get me wrong now.
SQL Express has it’s applications and for a free database server, it’s not half-bad. Small development sites, minor, not that extremely important systems with lower performance and feature demands, minor website databases et cetera could do well with SQL Express.

## My Checklist

Here’s my list of questions you have to ask to find if SQL Express is the correct choice.

### 1. Do your applications support SQL Express?

If your application developers cannot say “Yes” to this, you’re out of luck. You could probably get their applications to run on SQL Express anyway, but application support if something goes bad will most likely be zilch.

### 2. Do your applications fit the hardware limitations?

SQL Express is limited to 1GB RAM, 1 CPU and 4GB of databases. 1GB of RAM seems a bit tight to me for any production data. Also, on SQL Express 2005, [according to Microsoft](http://msdn.microsoft.com/en-us/library/ms345154%28SQL.90%29.aspx#sseover_topic4), you cannot run parallel queries.

> ”SQL Server Express can install and run on multiprocessor machines, but only a single CPU is used at any time. Internally, the engine limits the number of user scheduler threads to 1 so that only 1 CPU is used at a time. Features such as parallel query execution are not supported because of the single CPU limit.”

If this is still true on SQL Express 2008, I don’t know and I haven’t found any information about it (yet).

When answering this question, remember to calculate expected growth and possibly new databases/applications too.

### 2. Do your applications use database replication?

  If, so. Do the new server need to act as a publisher? If, yes, then you’re out of luck. SQL Express do handle database replication, but only as a subscriber. If you need to publish data, then you need a “bigger” SQL Edition.

### 4. Do you need Database Mail?

SQL Express does not have Database Mail. You have to find other ways to code your notifications. This question has raised counter-questions from customers as to “What would I need Database Mail for?”. It is, evidently a feature not used by many. Personally, I find it useful. [Clay McDonald has a nice blog-post](http://claysql.blogspot.com/2009/02/send-database-mail-from-trigger.html) on how to make SQL-triggers send mail on, for instance, inserts into a table using Database Mail. You could of course have it send mail on deletions as well. In my mind, this might come in handy in user-databases in CRM- or HR-systems. Every time an employee gets deleted from the database, the HR-admin could receive a notification.

### 5. Do you need the SQL Agent?

Perhaps not. Maybe you feel comfortable with scheduling your database backups using the windows scheduler and homebrew scripts. Just make sure your monitoring software (or IT-personnel) discover when the script fails. An increasing amount of applications require the SQL Agent to schedule and monitor recurring tasks, like Microsoft's App-V. Without the SQL Agent, the databases would grow ad infinitum. How about index maintenance? This is also possible to go by using your own scripts and the windows scheduler. SQL Express can do most maintenance tasks you would need using scripts and T-SQL. The SQL Agent just makes it simpler and more manageable. Once again, double-check this with the application developer.

### 6. Do you application use SSIS/DTS-jobs?

This is not included in SQL Express. Maybe there’s a work-around, but I haven’t found it and I doubt it is supported by anyone.

### 7. Do you need to be able to troubleshoot performance problems?

You can do this on SQL Express with a great deal of knowledge and timers. The SQL-profiler, the Performance Data Collection and the Database Tuning Advisor makes it easier. Specifically, the SQL-profiler comes in really handy when you suspect the application (not the system) to be the bad guy since you can trace the queries and pin-point where the performance-hit resides. Using the SQL-profiler I have been able to optimise indexes to and thus making database servers go from a 98% CPU Load to 3% CPU Load. I have also been able to pin-point specific queries and use them as “evidence” that the problem is bad/sloppy code rather than problems with the database server. Also, using the SQL-profiler.

There’s more, of course, but these point are the most common pit-falls in my experience. As you can see, there’s three “do you need”-questions  and there are highly optional. Far from everyone use them and often because of lacking SQL Server knowledge. You don’t know what you can do. Still, the most important question is #1\. Is SQL Express a supported database server for your applications. Hopefully, the developer knows the answer to this directly. No maybe’s. Yes or No.

Personally, I find that If you need a database server for production data, don’t go for SQL Express. Many customers have gone that way because “it’s free!” just to find themselves in the midst of a SQL Server upgrade and database migration a year later.