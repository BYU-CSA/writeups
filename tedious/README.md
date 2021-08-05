# UIUCTF 2021 - Tedious Writeup
* Type - Reverse Engineering
* Name - Tedious
* Points - 50

## Description
```
Enter the flag and the program will tell you if it is correct!

author: Chief

[challenge]
```

## Writeup
Okay I'm going to be straight up and say - I suck at reverse engineering. I know this was a basic challenge, but it took me a hot second and I didn't even fully reverse it. So this was quite the train wreck, but this is what I did.

The first thing I did with the challenge binary I downloaded was put it in Ghidra, navigate to the main function, and export the assembly into decompiled C code. It still requires a lot of work going through the code and making it readable, but it definitely gives you a good start. I started going through the code, replacing `undefined4` with int, while loops with for loops, and so forth until I felt like I understood what the binary was doing. It was taking your 38-character input, doing a bunch of XORing numbers, and adding or subtracting it from the character code. It then compared it to an array of integer values and told you if you got it right or wrong. You can see how far I got in decompiling this code in manglePassword.c (included in this folder). I went through and (TEDIOUSLY) did all the math by hand, and found it adds 2010 to each character code. This obviously put it way out of the ASCII range in hexadecimal, so I figured some sort of overloading it and going back to the minimum value was going on, and at this point the manual conversion from hex to decimal and addition/subtract had gotten to me and I was frustrated.

I then recompiled the code from Ghidra into C, made some changes to take out errors, and added a print statement on line 241 (of manglePassword2.c) that printed out the decimal value for each character. I made create_array.py, which ran the binary inputting a single, unique character, and outputted the decimal value that the modified binary put out.

```
{'a': 81, 'b': 106, 'c': 11, 'd': 36, 'e': 93, 'f': 102, 'g': 71, 'h': 16, 'i': 57, 'j': 50, 'k': 51, 'l': 44, 'm': 69, 'n': 14, 'o': 79, 'p': 120, 'q': 65, 'r': 90, 's': 123, 't': 84, 'u': 77, 'v': 86, 'w': 55, 'x': 64, 'y': 41, 'z': 98, 'A': 113, 'B': 10, 'C': 43, 'D': 68, 'E': 125, 'F': 6, 'G': 103, 'H': 48, 'I': 89, 'J': 82, 'K': 83, 'L': 76, 'M': 101, 'N': 46, 'O': 111, 'P': 24, 'Q': 97, 'R': 122, 'S': 27, 'T': 116, 'U': 109, 'V': 118, 'W': 87, 'X': 96, 'Y': 73, 'Z': 2, '0': 56, '1': 1, '2': 26, '3': 59, '4': 20, '5': 13, '6': 22, '7': 119, '8': 0, '9': 105, '{': 99, '}': 117, '_': 95, '-': 5, '!': 17, '@': 104, '#': 75, '$': 100, '%': 29, '^': 30, '&': 38, '*': 114, '(': 80, ')': 121}
```

I then created the answer.py file, which had a dictionary of the values above and put the answer in hex into an array, then looped through the array of values and printed out which characters it matches with. So when you run answer.py, it prints out the flag.

**Flag:** `uiuctf{y0u_f0unD_t43_fl4g_w0w_gud_j0b}`

## Real-World Application
Reverse engineering sucks.