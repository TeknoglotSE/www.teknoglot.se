---
title: In transit, again
date: 2016-06-01 21:03:35
year: "2016"
month: "06"
lastmod: 2016-06-02T01:29:59+02:00
url: /tb/in-transit-again/
url_encoded: /tb/in-transit-again/
description: We’re moving! Yep. Again. Although, it’s been a year or two since the last time.  The reason(s) Ok, so I’ve using Wordpress for quite a long time now and it’s been good. Mostly. It’s a fairly solid p
hexo_slug: in-transit-again
excerpt: We’re moving! Yep. Again. Although, it’s been a year or two since the last time. The reason(s) Ok, so I’ve using Wordpress for quite a long time now and it’s been good. Mostly. It’s a fairly solid platform and has a whole slew of feautures that work nicely. Before Wordpress I used Textpattern, a very slimmed, minimalistic authoring experience and my first contact with textile and similar markup/writing/notation languages. For those unaware, textile is not unlike markdown. Or should we say that markdown is not unlike textile? Considering that textile was invented by Dean Allen two years before markdown. Anyhow. Both work pretty much as good as the other, allowing the author to write in any text-editor, using easily readable and fairly logical formatting. Before that I used Movable Type, and prior to that either Dreamweaver or… well, notepad or vim. Problem with all of those platforms, however, is that they require dynamically generated webpages and technologies like PHP, Perl, .NET, Java and whatnot. That, in itself, has been a very minor issue until lately. Sure, it requires servers with logics, engines, add-ons, execution rights to the local filesystem etc, but still a minor nuisance. Mostly a financial nuisance really as active servers tend to cost money while finding static hosting for free is still pretty easy. Hell! I could put a webserver on a RaspberryPi and get good performance for a small-ish blog like mine if all I am using is static content. But, again. Not a major problem in itself. The main instigating factors to move away from Wordpress are the increasing size of the package, the lack of personal control, the lack of ease to extend my platform due to ever-expanding APIs and the fact that it is so popular that every “hacker” and it’s mother knows how to find exploits on it. My webhost, NFSN has been very good at detecting probing and brute-force attempts and automatically block public access to stuff like the login-pages and XML-RPC interfaces when that happens. I am just so sick and tired of having to constantly be on top of it with software updates, plugin updates, theme updates, security updates, spam-filtering, re-enabling the login page… Back to the basics Teknoglot.se will be served statically from now on, and it will be hosted for free on Github Pages. Using Hexo.io I can write my posts using markdown, then with a simple hexo generate --deploy generate and update the static files and publish them. No login pages to hack, no dynamic pages to exploit, no server security to worry about.
cats:
  - tb
tags:
  - Teknoglot
  - Hexo
  - Wordpress
---

# We're moving!

Yep. Again. Although, it's been a year or two since the last time.

## The reason(s)

Ok, so I've using [Wordpress][1] for quite a long time now and it's been good. Mostly.
It's a fairly solid platform and has a whole slew of feautures that work nicely.

Before Wordpress I used Textpattern, a very slimmed, minimalistic authoring experience and my first contact with [textile][2] and
similar markup/writing/notation languages. For those unaware, textile is not unlike [markdown][4].
Or should we say that markdown is not unlike textile? Considering that textile was invented by Dean Allen two years before markdown.
Anyhow. Both work pretty much as good as the other, allowing the author to write in any text-editor, using easily readable and fairly logical formatting.

Before that I used Movable Type, and prior to that either Dreamweaver or... well, notepad or vim.

Problem with all of those platforms, however, is that they require dynamically generated webpages and technologies like PHP, Perl, .NET, Java and whatnot.
That, in itself, has been a very minor issue until lately. Sure, it requires servers with logics, engines, add-ons, execution rights to the local filesystem etc, but
still a minor nuisance. Mostly a financial nuisance really as active servers tend to cost money while finding static hosting for free is still pretty easy.
Hell! I could put a webserver on a RaspberryPi and get good performance for a small-ish blog like mine if all I am using is static content.

But, again. Not a major problem in itself. The main instigating factors to move away from Wordpress are the increasing size of the package, the lack of personal control, 
the lack of ease to extend my platform due to ever-expanding APIs and the fact that it is so popular that every "hacker" and it's mother knows how to find exploits on it.
My webhost, [NFSN][5] has been very good at detecting probing and brute-force attempts and automatically block public access to stuff like the login-pages and XML-RPC interfaces when that happens.
I am just so sick and tired of having to constantly be on top of it with software updates, plugin updates, theme updates, security updates, spam-filtering, re-enabling the login page...

## Back to the basics

Teknoglot.se will be served statically from now on, and it will be hosted for free on [Github Pages][6].
Using [Hexo.io][7] I can write my posts using markdown, then with a simple `hexo generate --deploy` generate and update the static files and publish them.
No login pages to hack, no dynamic pages to exploit, no server security to worry about.

Hexo is built using node.js, which I have installed for other reasons anyway, and since the actual website is build from a git repository I obviously have proper versioning on everything I do per default.

There's obviously not as many plugins, helpers, themes and features available as in Wordpress. And blogging will require some command-line stuff.
But I am totally fine with that. I means I can write offline, generate offline to preview. And when finished, push to the public repo.

## But, comments?

Using Disqus. All client-side.
You need javascript, obviously, but I don't see me losing many readers for that to be frank. ;)

## The kinks

No, not [the band][8]. The stuff I have missed while migrating the posts from Wordpress to Hexo.
Here's what to expect.

### Permalinks may not work

I have done my best to ensure that my old permalink structure from the old site is intact.
Hexo have some limitations to categories though, meaning that I cannot yet have two main categories on the same post.
This do affect those articles that were available through both /code/posh/my-post, /ms/scom2012/my-post.
For those, I have had to pick one to be main and rely on tags to group stuff more freely. 

### Code-highlight artefacts

Wordpress highlight plugins and markdown have different syntax, and the migration plugin did not handle that.
This means that you might find a few `[powershell]`, `[sql]` or `[plain]` tags littered throughout the post for a while.
If you spot one, do comment to let me know. But I will try to convert them all as I find them.

### Images and galleries

Not sure I ever used a gallery, but some images may be missing as I have to migrate them manually and I am absolutely certain that I have missed at least one. Maybe two. ^That's ^a ^joke.

Once again, if you find a missing one you are welcome to post a comment to let me know.

### Series

Nope, no such thing in Hexo at the moment.
May be able to use some other structure, but for now it will be normal posts with links. Probably missing a few there as well.

### Post tabs

Also not available in Hexo.
I have converted those posts to regular posts. I am working on a proper TOC to make them easier to browse.

### Links

As with the images, links I have created manually may point to old wordpress folders and have to be redirected.
I know for a fact that I have missed a few.

### Graphics

Using a new theme will take a few adaptations to logos and other graphics.
This will change over time, so don't laugh too hard. 

# The Last Word

Things be wonky. Have patience. Thanks!



[1]: https://www.wordpress.org
[2]: https://en.wikipedia.org/wiki/Textile_(markup_language)
[3]: http://textpattern.com/
[4]: https://en.wikipedia.org/wiki/Markdown
[5]: https://www.nearlyfreespeech.net/
[6]: https://pages.github.com/
[7]: https://hexo.io/
[8]: https://en.wikipedia.org/wiki/The_Kinks
