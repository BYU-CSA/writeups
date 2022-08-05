import pexpect

s = pexpect.spawn("ssh ctf@easy-math.chal.uiuc.tf")


# sign into server and start program
s.expect("password.*")
s.sendline("ctf")
s.expect("=.*")
s.expect("ctf.*")
s.sendline("./easy-math")
s.expect("W.*")


index = 0
while index == 0:
    # respond to question
    index = s.expect(['Question.*', 'You failed.*', 'uiuc.*', pexpect.EOF, pexpect.TIMEOUT])

    if index == 0:
        response = s.after.decode("utf-8")
        num1 = response.split(" ")[2]
        num2 = response.split(" ")[4]
        answer = str(eval(num1+"*"+num2))
        print(response+answer)
        s.sendline(answer)

    elif index == 1:
        print("You failed the test...")
        print(s.before)
        print(s.after)
    elif index == 2:
        print("Flag!")
        print(s.before)
        print(s.after)
        s.interact()
    elif index == 3:
        print("EOF error",s.after)
    elif index == 4:
        print("Timeout error",s.after)