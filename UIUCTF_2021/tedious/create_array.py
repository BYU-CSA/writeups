import pexpect

values = {}
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!@#$%^&*()"
answer = ""

for letter in characters:
    terminal = pexpect.spawn("/home/justin/tmp/uiuctf/writeup_tedious/mangle")
    terminal.expect("flag:")
    terminal.sendline(letter)
    terminal.readline()
    terminal.readline()
    terminal.readline()
    integer = int(terminal.before.decode("utf-8"))
    if integer < 0: integer += 128
    values[letter] = integer

    terminal.expect(pexpect.EOF, timeout=2)

print(values)