---
title: Parameter Replacement in AlertName
date: 2012-04-09 22:04:48
year: "2012"
month: "04"
lastmod: 2016-05-25T00:33:26+02:00
url: /ms/opsmgr2007/parameter-replacement-in-alertname/
url_encoded: /ms/opsmgr2007/parameter-replacement-in-alertname/
description: …and why you should not use it  A Disclaimer I have had serious doubts about actually writing this article for almost a year now for reasons that I will explain further on. But as others have discove
hexo_slug: parameter-replacement-in-alertname
excerpt: …and why you should not use it A Disclaimer I have had serious doubts about actually writing this article for almost a year now for reasons that I will explain further on. But as others have discovered this “feature” as well–maybe “hack” would be a better name for it–I feel the need to explain how it works and also why you should not use it. Knowledge is power, and even if I advice against using this technique it is also a good way to understand how SCOM uses display-strings in management packs. The Good News Yes, you can use parameter replacement in you AlertName. With “parameter replacement” i mean using some kind of substitute text, or mnemonic if you like, that at run-time get translated into something useful. If you have written any kind of alert generating rules or monitors, you most like included something like Data/Context/Property[@Name=′SomeDataFromAPropertyBag′]Data/Context/Property[@Name='SomeDataFromAPropertyBag']Data/Context/Property[@Name=′SomeDataFromAPropertyBag′] into your alert description. In this dialog, you also have the possibility to set the Alert Name. And if you are lazy, like I am, you probably also noticed that it is impossible to insert any kind of dynamic data into that field as well. This is especially annoying when you are writing a management pack that needs to look different in the Alert Views in the console, and you want to monitor 50 different Events or Performance counters or Log entries that are pretty much the same apart from a Name or ID. Of course I could not refrain from copy-pasting a Data/Context...Data/Context...Data/Context... into the alert name only to realize that it simply is not being parsed and translated into the value of the specified parameter. Over time I have settled for a stand-point that it’s probably a performance issue and I have also used that as an argument for this apparent lack of simplicity that some of my customers have been questioning. Two, maybe three, years later. Microsoft releases an update to the core agent monitoring packs. Much to my surprise, one performance monitor suddenly generated alerts with a dynamic performance value in the Alert Name. You know, that field that is not gettingt parsed I was mentioning in the earlier paragraph. It actually looked pretty bad and made it very much impossible to practice any kind of alert supression, but still. It actually had a parsed value in the Alert Name. As the lack of this feature had me irked before, I exported the core MP and started reading through the XML to find out how they did it. To my surprise, it was actually pretty simple if you ditched the Authoring Console and used your trusty text-editor instead. How To Do It In simple terms, if you know your SCOM XML out-side-in, you add the parameters to your “Alert” and modify your DisplayString, the one under LanguagePacks, to call that parameter by it’s relative ID.
cats:
  - ms
  - ms/opsmgr2007
tags:
  - OpsMgr
  - MP Development
hexo_id: 586
---

# ...and why you should not use it

## A Disclaimer

I have had serious doubts about actually writing this article for almost a year now for reasons that I will explain further on. But as others have discovered this "feature" as well--maybe "hack" would be a better name for it--I feel the need to explain how it works and also why you should not use it. Knowledge is power, and even if I advice against using this technique it is also a good way to understand how SCOM uses display-strings in management packs.

## The Good News

Yes, you can use parameter replacement in you AlertName.

With "parameter replacement" i mean using some kind of substitute text, or mnemonic if you like, that at run-time get translated into something useful. If you have written any kind of alert generating rules or monitors, you most like included something like _$Data/Context/Property[@Name='SomeDataFromAPropertyBag']$_ into your alert description.

In this dialog, you also have the possibility to set the Alert Name. And if you are lazy, like I am, you probably also noticed that it is impossible to insert any kind of dynamic data into that field as well. This is especially annoying when you are writing a management pack that needs to look different in the Alert Views in the console, and you want to monitor 50 different Events or Performance counters or Log entries that are pretty much the same apart from a Name or ID.
Of course I could not refrain from copy-pasting a _$Data/Context...$_ into the alert name only to realize that it simply is not being parsed and translated into the value of the specified parameter. Over time I have settled for a stand-point that it's probably a performance issue and I have also used that as an argument for this apparent lack of simplicity that some of my customers have been questioning.

Two, maybe three, years later. Microsoft releases an update to the core agent monitoring packs. Much to my surprise, one performance monitor suddenly generated alerts with a dynamic performance value in the Alert Name. You know, that field that is not gettingt parsed I was mentioning in the earlier paragraph. It actually looked pretty bad and made it very much impossible to practice any kind of alert supression, but still. It actually had a parsed value in the Alert Name.
As the lack of this feature had me irked before, I exported the core MP and started reading through the XML to find out how they did it. To my surprise, it was actually pretty simple if you ditched the Authoring Console and used your trusty text-editor instead.

## How To Do It

In simple terms, if you know your SCOM XML out-side-in, you add the parameters to your "Alert" and modify your DisplayString, the one under LanguagePacks, to call that parameter by it's relative ID.

Just in case you happen to be a regular mortal, here's the step-by-step guide. ;)

In this example I have created a silly-simple Alert Generating EventLog rule in wich I have added some parameters to the description. It pretty much looks like this:

![Alert Description Dialog](/wp-content/uploads/2012/04/ParamReplacement_AlertDescriptionDialog.png)

Saving the MP at this point I will have a new WriteAlert action with a bunch of parameters and a displaystring with a unique ID.
The resulting XML-code for the WriteAlert action looks like this:

```xml
[xml highlight="7,8,9,10,11,12,13"]
<WriteAction ID="Alert" TypeID="Health!System.Health.GenerateAlert">
  <Priority>1</Priority>
  <Severity>2</Severity>
  <AlertName />
  <AlertDescription />
  <AlertOwner />
  <AlertMessageId>$MPElement[Name="TestMP.MyEventlogAlertRule.AlertMessage"]$</AlertMessageId>
  <AlertParameters>
    <AlertParameter1>$Data/EventDescription$</AlertParameter1>
    <AlertParameter2>$Data/LoggingComputer$</AlertParameter2>
    <AlertParameter3>$Data/UserName$</AlertParameter3>
    <AlertParameter4>$Data/EventNumber$</AlertParameter4>
  </AlertParameters>
  <Suppression />
  <Custom1 />
  <Custom2 />
  <Custom3 />
  <Custom4 />
  <Custom5 />
  <Custom6 />
  <Custom7 />
  <Custom8 />
  <Custom9 />
  <Custom10 />
</WriteAction>
```

In this slab of code, you've got the Parameters, their "relative ID" (the number in the Tag), and also the which is what you would need to search for among the displaystrings. Take note of the you want to use in your AlertName since you are going to need it later. A quick search for "TestMP.MyEventlogAlertRule.AlertMessage" will lead you to the actual message, which should looke similar to this:

```xml
<DisplayString ElementID="TestMP.MyEventlogAlertRule.AlertMessage">
  <Name>I want Parameter Replacement here:</Name>
  <Description>Event Description: {0}
{1}
{2}
{3}
  </Description>
</DisplayString>
```

You should have one of these for every language you have configured in your management pack.
As you may notice, the Description does not contain any XPaths of any kind but rather references to the parameters defined in the WriteAction. That would be the {X} thingies within the description tags. You may also notice that the AlertParameters starts from "1" while the parameter references begin with "0". In practice, that means that _{0}_ in the displaystring definition equals to _AlertParameter1_ and so forth.

Now, with this in mind, adding a Parameter to AlertName if very simple and straight-forward. Simply decide which parameter your want to use and add it's reference to the Name definition.
So, let's say I have the above alert message and I want to include _UserName_ in the Alert Name, I would change the <Name> tag to:

```xml
<Name>I want Parameter Replacement here:{2}</Name>
```

That's it folks!
Save the XML, make sure you verify it and import it into your Operations Manager LAB and watch the magic. Just make sure you continue reading this post as the next part about the downsides is pretty important.

## The Downside

The negative effects of using Parameter Replacement in AlertName really boils down to two main perspectives. These are, if I may say to, pretty major and is the reason I have been reluctant on posting this, sort of, how-to.

### You are breaking your subscriptions and connectors

Apparently, parameter replacement is not working in subscriptions and connectors, be it 3:rd-party, Universal, Orchestrator IPs et.c. Basically anything other than the Operations Console will not be able to handle your parameters in AlertName. This will give you a _"{1} in {2} has received an error"_ instead of _"veryimportant.log in C:\Logs\ImportantSystem\ has received an error"_ in anything except the Operations Console. Now, this might not be a bad thing if the Operations Console is your only interface to Operations Manager, but if you would like to forward these alerts to a mobile phone, IM user or a mail recipient it will be utterly useless. I have not verified this, but I am not sure if Alert Suppression is actually parsing the parameters as well. Also. If you, by means of connectors or System Center Orchestrator, are generating incidents from alerts the AlertName forwarded will be equally useless for anyone receiving it.

### It's killing your health perspective

Might sound drastic, but I'm quite serious about this. Using Parameter Replacement in AlertName might be useful for alert generating rules, but should never be used in a monitor. The reason is pretty simple actually. If you are using a monitor, you are without a doubt interested in it's state. Otherwise, you would not use a monitor, am I right? I cannot see how it would make sense to create a monitor that does not reflect the health of a specific checkpoint. Much less having a monitor generating alerts that might confuse any service desk operator about what monitor that caused the alert. Also--I have not tested this--I assume that a monitor would not update it's AlertName once the alert are generated making it more difficult to troubleshoot. Alert generating rules are, to me, something I tend to use only when all other options fail for some reason and I do not like to monitor things to cannot have health. And since parameters in AlertName is nothing for monitors I also question whether it actually is usable at all.

## The Conclusion

While this is an interesting techique and a good way to enjoy MP Authoring and learn about the behaviour of display strings and languages in you Management Packs, I would definitely consider it a mostly academical exercise. Only in <span style="text-decoration: underline;">extreme</span> use-cases and situations would I consider it a viably option and while it might look good in the console, do be aware of the limitations. I have also not seen anything about it on MSDN, and I have serious doubts about it being a supported feature. I have personally been using it in transition to a "better" management pack to get alerting running quickly, yet a prefered solution would actually be using a custom datasouce and a decent macro-enabled text-editor--not to mention snippets--to bulk-generate your monitors and/or rules.

> MP Authoring

> is fun and powerful

> -- be resposible
