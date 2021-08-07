input = input()

print("'", end="")
for letter in input:
    print(hex(ord(letter)).replace("0x", "\\U000000").upper(), end="")

print("'")