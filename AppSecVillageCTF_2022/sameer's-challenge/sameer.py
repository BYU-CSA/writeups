import base64

from flag import FLAG

s = ""
for i in range(len(FLAG)):
    if (i % 4) == 0:
        s += base64.b64encode(FLAG[i].encode("ascii")).decode("ascii")
    else:
        s += FLAG[i]

print(s)

assert s[0] == "Q"
assert s[1] == "Q"
assert s[20] == "_"
assert s[4] == "S"
assert s[5] == "V"
assert s[29] == "w"
assert s[7] == "d"
assert s[23] == "="
assert s[24] == "="
assert s[25] == "o"
assert s[8] == "w"
assert s[15] == "A"
assert s[16] == "="
assert s[17] == "="
assert s[18] == "m"
assert s[9] == "="
assert s[30] == "="
assert s[31] == "="
assert s[32] == "}"
assert s[10] == "="
assert s[11] == "3"
assert s[12] == "l"
assert s[13] == "c"
assert s[14] == "M"
assert s[2] == "="
assert s[3] == "="
assert s[19] == "3"
assert s[28] == "M"
assert s[21] == "d"
assert s[22] == "A"
assert s[6] == "{"
assert s[26] == "_"
assert s[27] == "R"