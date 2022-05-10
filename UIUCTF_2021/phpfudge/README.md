# UIUCTF 2021 - PHPFudge (Beginner) Writeup
* Type - Jail
* Name - PHPFudge
* Points - 50

## Description
```
i hate php

http://phpfuck.chal.uiuc.tf

author: arxenix
```

## Writeup
This was a fairly simple challenge to complete. When you navigate to the URL in the description, the page you'll see has this text followed by the output of phpinfo():

```
<?php
// Flag is inside ./flag.php :)
($x=str_replace("`","",strval($_REQUEST["x"])))&&strlen(count_chars($x,3))<=5?print(eval("return $x;")):show_source(__FILE__)&&phpinfo();
```

So, I followed the advice of the comment, went to /flag.php, and when you look at the source code, you find the flag!

<img src="phpflag.png" width="600px">

**Flag:** `uiuctf{pl3as3_n0_m0rE_pHpee}`

## Real-World Application
There's not a whole lot here to go off of, but always look at the source code! Before delving deep into any challenges, always do recon first! Just as in pentesting, the first step (after prep) is [Information Gathering/Discovery](https://www.coresecurity.com/blog/six-stages-penetration-testing)! It's always easier to increase your attack surface first before probing for vulnerabilities. Before getting deep into any CTF challenges, poke around first!