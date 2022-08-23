import base64

# initialize s
s = ['?'] * 33
s[0] = "Q"
s[1] = "Q"
s[20] = "_"
s[4] = "S"
s[5] = "V"
s[29] = "w"
s[7] = "d"
s[23] = "="
s[24] = "="
s[25] = "o"
s[8] = "w"
s[15] = "A"
s[16] = "="
s[17] = "="
s[18] = "m"
s[9] = "="
s[30] = "="
s[31] = "="
s[32] = "}"
s[10] = "="
s[11] = "3"
s[12] = "l"
s[13] = "c"
s[14] = "M"
s[2] = "="
s[3] = "="
s[19] = "3"
s[28] = "M"
s[21] = "d"
s[22] = "A"
s[6] = "{"
s[26] = "_"
s[27] = "R"

# prep to reverse operation
s = ''.join(s)
flag = ""
index = 0

while index < len(s):
    # tests to see if the four characters are base64 encoded
    if (index < len(s)-3) and (s[index+2] == '=') and (s[index+3] == '='):
        flag += base64.b64decode(s[index:index+4]).decode("ascii")
        index += 4
    
    # if not base64-encoded, just add to flag
    else:
        flag += s[index]
        index += 1

print(flag)