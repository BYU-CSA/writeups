# ASVCTF 2022 - Hack the Hacker Writeup
- Type - Misc
- Name - Hack the hacker!
- Points - 150

## Description
```markdown
We were just attacked and lost our network capture. All we have are access logs from apache.

Can you find the attack and see what the attackers exfiltrated? 

Files:
* access.log
```

([source code](access.log))

## Writeup
First, before I dive into how the problem is solved, it's vital to understand how a boolean-based blind SQL injection attack works. Imagine you have the following SQL query run in the backend: `SELECT * FROM users WHERE username = '$user' AND password = '$password'`. The server-side logic is set up so that if any rows are returned, you are authenticated in the system. If you insert the following payload for `$user`: `admin' AND password LIKE 'a%'--`, the SQL query now effectively becomes `SELECT * FROM users WHERE username = 'admin' AND password LIKE 'a%'`. If you get signed in, then you know that the admin password starts with an `a`. If you don't, then you know that the admin password does *not* start with an `a`. If that's the case, you would try the payload `admin' AND password LIKE 'b%'--`. Again, if you get signed in, then you know the admin password starts with a `b`. If not, you would try with `c`, etc. Once you know it starts with `b`, you would then use the payload `admin' AND password LIKE 'ba%'--` to brute force the second letter. This is the pattern that would happen.

Now think of it in the perspective of what the HTTP access logs would look like.


**Flag:** `ASV{}`