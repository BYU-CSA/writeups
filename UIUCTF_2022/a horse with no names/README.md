# UIUCTF 2022 - A Horse with No Names Writeup
- Type - jail
- Name - A Horse with No Names
- Points - 117

## Description
```markdown
Can you make it through the desert on a horse with no names?

nc horse.chal.uiuc.tf 1337

author: kmh
```

## Writeup
I want to start off by saying this was one of my favorite challenges, and we ended up getting third blood on the challenge! The challenge provided 2 files, `desert.py` and a Dockerfile. The Dockerfile simply showed us that the flag was stored at `/flag.txt`. `desert.py` looked like this:

```python
#!/usr/bin/python3
import re
import random
horse = input("Begin your journey: ")
if re.match(r"[a-zA-Z]{4}", horse):
    print("It has begun raining, so you return home.")
elif len(set(re.findall(r"[\W]", horse))) > 4:
    print(set(re.findall(r"[\W]", horse)))
    print("A dead horse cannot bear the weight of all those special characters. You return home.")
else:
    discovery = list(eval(compile(horse, "<horse>", "eval").replace(co_names=())))
    random.shuffle(discovery)
    print("You make it through the journey, but are severely dehydrated. This is all you can remember:", discovery)
```

This jail challenge consisted of bypassing 3 roadblocks - two regular expressions, and removing all Python bytecode with a `co_name` (more on that later). If I could get past those three filters, then any Python code I wanted could be run, such as `open('flag.txt').read()` or `os.system('shell command')`. 

### Roadblock 1 - No 4-letter Words
The first `if` statement checked to see if `re.match(r"[a-zA-Z]{4}", horse)` evaluated to True - if it did, no dice. The regular expression `r"[a-zA-Z]{4}"` simply matched any 4-letters in a row inside our input variable, `horse`. There were 2 possible workarounds that came to mind originally - using Unicode characters, and hex encodings. 

Python is unique since it will automatically normalize Unicode characters in certain circumstances. For example, an italicized `𝘦` (Unicode number `0x1d626`) will be normalized to a normal `e` when present in a variable name, global variable, function, or module (with some exceptions). That means that `𝘦𝘹𝘦𝘤` and `exec` functions look the same to Python, except `𝘦𝘹𝘦𝘤` will NOT match the regular expression `r"[a-zA-Z]{4}"` - thus allowing us to use the `exec` function. 

Hex encoding in strings allow us to only use the characters `\x0123456789abcdef`, with each ASCII char represented by it's double-hex number. For example, the string `'a'` and `'\x61'` are the same, and `'\x65\x78\x65x\x63'` is the same as `'exec'`. However, the hex-encoded characters MUST be inside of a string, and not as regular Python code.

(Note - this specific Python line used the `re` function `match` instead of `search`, which means a 5-letter word was not flagged, only 4-letters words. A second version of this challenge was released where this roadblock was changed to "No words with 4+ letters" by using `search` instead.)

### Roadblock 2 - Maximum of 4 Symbols
Our second roadblock checked to see if `len(set(re.findall(r"[\W]", horse)))` was greater than 4, and if it was - no go. The regular expression `r"[\W]"` included all non-word characters (this means alphanumeric and `_` and `:` and Unicode normalized to these ASCII chars, along with probably a few others). Sticking that in the `findall` function simply returned a list of most symbols used in your code. The `set` function filtered out duplicates, so this line was checking to see how many symbols were used in your payload. If you used more than 4, the code wouldn't run. So we had to be conservative with common symbols like `(`, `)`, `+`, `.`, etc.

### Roadblock 3 - No `co_names`
Running arbitrary code with the first two roadblocks would have been fairly simple - it was the third roadblock that made it very difficult. One payload that would've worked with the first two roadblocks is `𝘦𝘹𝘦𝘤('\x70\x72\x69\x6E\x74\x28\x6F\x70\x65\x6E\x28\x27\x2F\x66\x6C\x61\x67\x2E\x74\x78\x74\x27\x29\x2E\x72\x65\x61\x64\x28\x29\x29')` (hex-encoded `print(open('/flag.txt').read())`). To understand the last roadblock, we have to take a look at Python bytecode. 

A good explanation of Python code object, disassembly, and bytecode [can be found here](https://towardsdatascience.com/understanding-python-bytecode-e7edaae8734d). The program would take our input, disassemble it, and clear all `co_names`, which means any Python bytecode that loaded a name would not work. This prevented us from calling functions directly like `print('a')` or attributes, like `().__class__`. This was a huge blow! However, after some trial and error, I discovered that Python functions that used `print()` or attributes like that were okay. For some reason, creating and calling a function never used the `LOAD_NAME` instruction, and when running a function with code like `print('a')` inside, it used `LOAD_GLOBAL` or `LOAD_ATTRIBUTE` instead of `LOAD_NAME`. So if we could call a function, we could bypass the third roadblock.

Creating and calling a custom function, however, didn't work because the code used the `eval` function instead of `exec`. Both of these functions will run Python code passed into it, however `eval` is looking for expressions, not multiline code/modules/functions - `exec` doesn't care. So using `def code: print('a'); code()` or something would not work. However, lambdas are a function-like Python struct designed to not be named and be usable inside of an expression. The normal syntax is `lambda (param1, param2) : print('a')`.

It's important to note that spaces counted as symbols, so I had to remove spaces if possible. I tested and realized I could use the syntax `lambda:print('a')` since I had no parameters, and there were no spaces. To immediately call a lambda after creating it, I just had to wrap it in parentheses like this - `(lambda:print('a'))()`. This was going to be my setup.

### Putting It All Together
My first attempt was this payload - `(lambda:open('/flag.txt'))()`. The problem with this one was too many symbols: `(`, `)`, `:`, `'`, `.`, and `/`. Even if I hex-encoded the string `/flag.txt` to `\x2F\x66\x6C\x61\x67\x2E\x74\x78\x74` (minus 1 symbol), we still had 5. That meant I could use `(lambda:print('aaa'))()`, but only use characters for aaa, not symbols. I wasn't quite sure how to go from here until I went through a list of all the builtin functions for Python and saw `chr()`. `chr()` takes in a number and outputs the ASCII character with that charcode. I would need to use the `+` character in between, but that meant no single quote for a string! So using `(lambda:exec(PAYLOAD))()` with a payload like `chr(1)+chr(2)+chr(3)` would work! I wrote a quick script called `encode.py` that would convert Python code to this `chr()` format, used the payload `print(open('/flag.txt').read())`, and it worked!

```
$ nc horse.chal.uiuc.tf 1337
== proof-of-work: disabled ==
Begin your journey: (lambda:𝘦𝘹𝘦𝘤(chr(112)+chr(114)+chr(105)+chr(110)+chr(116)+chr(40)+chr(111)+chr(112)+chr(101)+chr(110)+chr(40)+chr(39)+chr(47)+chr(102)+chr(108)+chr(97)+chr(103)+chr(46)+chr(116)+chr(120)+chr(116)+chr(39)+chr(41)+chr(46)+chr(114)+chr(101)+chr(97)+chr(100)+chr(40)+chr(41)+chr(41)))()
uiuctf{my_challenges_have_abandoned_any_pretense_of_practical_applicability_and_im_okay_with_that}
```

**Flag:** `uiuctf{my_challenges_have_abandoned_any_pretense_of_practical_applicability_and_im_okay_with_that}`

## Real World Application
Sandboxes are very useful because they teach you how to bypass filters that you may experience in real-world engagements, like Web Application Firewalls (WAFs). It also forces you to be creative with how you program and look into lesser-known aspects of programming languages. Knowing how something works even better than the developer that used it is a surefire way to figuring out how to hack it. For example, if a developer doesn't know that Unicode characters are still parsed as valid Python but bypass regex filters, they may not sanitize user input sufficiently. 