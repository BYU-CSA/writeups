# That's Not Crypto
* CTF - [JustCTF 2020](https://ctftime.org/event/1050/)
* Type - Reverse Engineering
* Name - That's Not Crypto

## Description
```
This is very simple RE task, but you may need some other skills as well. :)

https://<REDACTED>/checker.pyc
```

## Writeup
While Python is normally compiled as it's being run, it's also possible to compile it beforehand into machine code and run it. To turn it back into Python, we used [uncompyle6](https://pypi.org/project/uncompyle6/) and turned checker.pyc into checker.py (see below):

```
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.17 (default, Sep 30 2020, 13:38:04) 
# [GCC 7.5.0]
# Warning: this version of Python has problems handling the Python 3 "byte" type in constants properly.

# Embedded file name: checker.py
# Compiled at: 2021-01-30 07:41:40
# Size of source mod 2**32: 50109 bytes
from random import randint

def make_correct_array(s):
    from itertools import accumulate
    s = map(ord, s)
    s = accumulate(s)
    return [x * 69684751861829721459380039 for x in s]


def validate(a, xs):

    def poly(a, x):
        value = 0
        for ai in a:
            value *= x
            value += ai

        return value

    if len(a) != len(xs) + 1:
        return False
    else:
        for x in xs:
            value = poly(a, x)
            if value != 24196561:
                return False

        return True


if __name__ == '__main__':
    a = [insert really big array]
    a = [ai * 4919 for ai in a]
    flag_str = input('flag: ').strip()
    flag = make_correct_array(flag_str)
    if validate(a, flag):
        print('Yes, this is the flag!')
        print(flag_str)
    else:
        print('Incorrect, sorry. :(')
```

We then copied this program into checker2.py and commented out what each line does (see attached file). We found that it takes a large array of numbers, does a bunch of math on it, and then checks to see if that equals the inputted flag. Since the array has 57 values, we know the flag length is 57. 

Because the math is very computationally expensive, we decided to go the brute-forcing route and wrote a script in C++ to do that (I was still learning Python at the time). That script is makeline.cpp (attached). 

To summarize what makeline.cpp does, it loops 57 times and each time it loops, it runs the Python script with each possible character and outputs the result into a text file. It then searches all the text files to see which one has a success message, and recognizes that is the next character. It then adds that on to the flag and then tries the next character. It continues for a few minutes until it verifies each character in the flag, one at a time.