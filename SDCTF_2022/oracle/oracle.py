import subprocess

flag = "sdctf{"
characters = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
answer = [48, 6, 122, -86, -73, -59, 78, 84, 105, -119, -36, -118, 70, 17, 101, -85, 55, -38, -91, 32, -18, -107, 53, 99, -74, 67, 89, 120, -41, 122, -100, -70, 34, -111, 21, -128, 78, 27, 123, -103, 36, 87]

def plzwork(flag_temp):
    print("Calling plzwork with the flag "+flag_temp)
    for char in characters:
        #print(char)
        # get result
        process = subprocess.Popen(['java', 'flag.java', flag_temp+char+('a'*(40-len(flag_temp)))+"}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        result = out.decode("utf-8").split("\n")[0].split(" ")[:-1]
        #print(result)

        # checking
        same = True
        for i in range(len(flag_temp)+1):
            if int(result[i]) != answer[i]:
                same = False

        if same:
            plzwork(flag_temp+char)

for _ in range(35):
    plzwork(flag)