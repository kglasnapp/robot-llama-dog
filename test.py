from enum import Enum
import time
import sys
import select

dispMode = Enum("dispMode", ["Power", "Encoder", "RollPitchYaw"])
dispMode = dispMode.Encoder
print(dispMode)
dispMode = dispMode.Power
print(dispMode, dispMode == dispMode.Power, dispMode == dispMode.Encoder)

def check():
    return select.select([sys.stdin], [], [], 0)[0]

def checkInput():
    if select.select([sys.stdin,], [], [], 0)[0]:
        return sys.stdin.readline()
    else:
        return None

count = 0
print("\n>", end="")
#time.sleep(.1)
while True:
    while True:
      count += 1
      if check():
        s = input()
        print("Do:", s, count, "\n>", end="")
        break
startTime = time.monotonic()
while True:
    print(">", end="k")
    while True:
        count += 1
        if time.monotonic() > startTime + 30:
            startTime = time.monotonic()
            print("Refresh", count)
            count = 0
        chk = check()
        if chk:
            break
    s = input()
    print("S:", s)
    print("<", end="")
