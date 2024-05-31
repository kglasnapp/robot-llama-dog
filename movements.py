import time
import math
from robotLegs import legs
from adafruit_motor import servo
import myServo

def strToMovements(s, speed):
   ar = s.split(",")
   actions = []
   for i in range(0, len(ar),2):
       actions.append([int(ar[i]), float(ar[i+1])])
   legs.servosMove.newServoActions(actions, speed)

def wiggle():
    # Move the lower leg servo through a range of motion
    for angle in range(70, 110, 5):
        print("Move all lower legs angle:", angle)
        legs.setAngle(1, angle)
        legs.setAngle(5, angle)
        legs.setAngle(9, angle)
        legs.setAngle(13, angle)
        time.sleep(0.1)


# march1 and march2 by Elie
def march1():
    legs.setAngle(0, 140)
    legs.setAngle(1, 150)
    legs.setAngle(12, 180)
    legs.setAngle(13, 130)
    legs.setAngle(4, 0)
    legs.setAngle(5, 50)
    legs.setAngle(8, 40)
    legs.setAngle(9, 16)


def march2():
    legs.setAngle(0, 180)
    legs.setAngle(1, 130)
    legs.setAngle(12, 150)
    legs.setAngle(13, 150)
    legs.setAngle(4, 40)
    legs.setAngle(5, 30)
    legs.setAngle(8, 0)
    legs.setAngle(9, 36)


# Move All legs 4.5" from bottom and 0" from back of Robot
def test1():
    legs.setAngle(0, 102)
    legs.setAngle(1, 160)
    legs.setAngle(12, 102)
    legs.setAngle(13, 160)

    legs.setAngle(8, 85)
    legs.setAngle(9, 37)
    legs.setAngle(4, 75)
    legs.setAngle(5, 37)


# Move All legs 4.5" from bottom and 4.5" from back of Robot
def test2():
    legs.setAngle(0, 45)
    legs.setAngle(1, 127)
    legs.setAngle(12, 45)
    legs.setAngle(13, 127)

    legs.setAngle(8, 130)
    legs.setAngle(9, 75)
    legs.setAngle(4, 130)
    legs.setAngle(5, 75)


frf = [12, 45, 13, 127]
frb = [12, 102, 13, 160]
rrf = [0, 45, 1, 127]
rrb = [0, 102, 1, 160]
frz = [12, 90, 13, 90]
rrz = [0, 90, 1, 90]
d5 = [0.5]

flf = [8, 135, 9, 90 - (127 - 90)]
flb = [8, 90 - 12, 9, 90 - (160 - 90)]
rlf = [4, 135, 5, 90 - (127 - 90)]
rlb = [4, 90 - 12, 5, 90 - (160 - 90)]
flz = [8, 90, 9, 90]
rlz = [4, 90, 5, 90]


def move(actions):
    for a in actions:
        print(len(a), a)
        if len(a) == 1:
            time.sleep(a[0])
        if len(a) == 4:
            legs.setAngle(a[0], a[1])
            legs.setAngle(a[2], a[3])


def moveWithTime(actions, duration):
    startTime = round(time.time() * 1000)
    currentTime = startTime
    startAngles = legs.getAngles()
    elapsedTime = currentTime - startTime

    while elapsedTime < duration:
        currentTime = round(time.time() * 1000)
        elapsedTime = currentTime - startTime
        print("currentTime: " + str(currentTime))

        print("elapsed time: " + str(elapsedTime))
        for a in actions:
            currentTime = round(time.time() * 1000)
            elapsedTime = currentTime - startTime
            percentCompleted = elapsedTime / duration
            newAngle = startAngles[math.floor(a[0])] + (
                (a[1] - startAngles[math.floor(a[0])]) * percentCompleted
            )
            legs.setAngle(a[0], newAngle)
            currentTime = round(time.time() * 1000)
            elapsedTime = currentTime - startTime
            percentCompleted = elapsedTime / duration
            newAngle = startAngles[math.floor(a[2])] + (
                (a[3] - startAngles[math.floor(a[2])]) * percentCompleted
            )
            legs.setAngle(a[2], newAngle)

    for a in actions:
        legs.setAngle(a[0], a[1])
        legs.setAngle(a[2], a[3])


def dance1():
    frf = [12, 45, 13, 127]
    frb = [12, 102, 13, 160]
    rrf = [0, 45, 1, 127]
    rrb = [0, 102, 1, 160]
    frz = [12, 90 - 20, 13, 90]
    rrz = [0, 90, 1, 115]
    d5 = [0.5]

    flf = [8, 135, 9, 90 - (127 - 90)]
    flb = [8, 90 - 12, 9, 90 - (160 - 90)]
    rlf = [4, 135, 5, 90 - (127 - 90)]
    rlb = [4, 90 - 12, 5, 90 - (160 - 90)]
    flz = [8, 90 + 20, 9, 90]
    rlz = [4, 90, 5, 90 - 25]
    for i in range(5):
        moveWithTime([frf, rrb, flf, rlb], 550)
        moveWithTime([frb, rrf, flb, rlf], 350)

    moveWithTime([frz, rrz, flz, rlz], 500)

def setAngle(servo, angle):
    group = int(servo / 4)
    if group == 1 or group == 2:
        angle = 180 - angle
    print("Servo:%d angle:%.2f g:%d" % (servo, angle, group))
    legs.setAngle(servo, angle)

def testBalanceOS1():
   for servo in [0,8,12,4]:
     print("Move leg %d" % (servo))
     moveLeg(servo)
     time.sleep(.5)

def testBalanceOS():
   for servo in [0,8,12,4]:
      initForward(servo)
       # Init
      #setAngle(servo+2, 80)
   time.sleep(5)
   for servo in [0,8,12,4]:
      moveBack(servo)


def initForward(servo):
   # Forward
    setAngle(servo+1, 109)
    setAngle(servo+0, 68)

def moveBack(servo):
    # Back
    setAngle(servo+1, 131)
    setAngle(servo+0, 90)

def moveLeg(servo):
    # Init
    setAngle(servo+2, 70)
    # Floor
    setAngle(servo+1, 131)
    setAngle(servo+0, 90)
    time.sleep(0.5)
    # UP
    setAngle(servo+1, 134)
    setAngle(servo+0, 95)
    time.sleep(0.05)
    # Forward
    setAngle(servo+1, 109)
    setAngle(servo+0, 68)
    time.sleep(0.15)
    # Down
    setAngle(servo+1, 107)
    setAngle(servo+0, 70)
    time.sleep(0.05)
    # Back
    setAngle(servo+1, 131)
    setAngle(servo+0, 90)
    time.sleep(0.15)


def testBalance():
    for i in range(20):
        legs.setAngle(2, 90)
        legs.setAngle(10, 90)
        time.sleep(0.5)
        d = 1
        legs.setAngle(0, 50)  # up
        time.sleep(d)
        legs.setAngle(1, 90)  # forward
        time.sleep(d)
        legs.setAngle(0, 90)  # down
        time.sleep(d)
        legs.setAngle(1, 130)  # back
        time.sleep(d)
        return
        legs.setAngle(9, 60)
        time.sleep(0.02)
        legs.setAngle(8, 140)
        time.sleep(0.04)
        legs.setAngle(9, 50)
        time.sleep(0.02)
        legs.setAngle(8, 90)

        time.sleep(0.3)

    return

    # legs.setAngle(4,140)
    # time.sleep(.04)
    # legs.setAngle(4,90)

    # legs.setAngle(12,60)
    # time.sleep(.04)
    # legs.setAngle(12,90)


def walkTest():
    leanforward()
    bls1 = [[4, 145, 5, 65]]
    frs1 = [[12, 25, 13, 135]]
    frs2 = [[12, 25, 13, 115]]
    speed = 300
    moveWithTime(bls1, speed)
    moveWithTime(frs1, speed)
    moveWithTime(frs2, speed)


def leanforward():
    speed = 300
    leanForward = (
        [[1, 135, 0, 80]] + [[13, 135, 12, 80]] + [[9, 45, 8, 100]] + [[5, 45, 4, 100]]
    )
    moveWithTime(leanForward, speed)


def walkTestOld():
    legs.setAngle(2, 60)
    legs.setAngle(14, 110)
    legs.setAngle(6, 110)
    legs.setAngle(10, 60)
    brs1 = [[0, 135, 1, 180]]
    brs2 = [[0, 90, 1, 180]]
    brs3 = [[0, 45, 1, 105]]
    brs4 = [[0, 150, 1, 140]]
    frs1 = [[12, 135, 13, 180]]
    frs2 = [[12, 90, 13, 180]]
    frs3 = [[12, 25, 13, 90]]
    frs4 = [[12, 90, 13, 90]]

    bls1 = [[4, 90 - (135 - 90), 5, 90 - (180 - 90)]]
    bls2 = [[4, 90, 5, 0]]
    bls3 = [[4, 90 - (45 - 90), 5, 90 - (90 - 105)]]
    bls4 = [[4, 90 - (150 - 90), 5, 90 - (140 - 90)]]
    fls1 = [[8, 90 - (135 - 90), 9, 90 - (180 - 90)]]
    fls2 = [[8, 90, 9, 90 - (180 - 90)]]
    fls3 = [[8, 90 - (25 - 90), 9, 90]]
    fls4 = [[8, 90 - (90 - 90), 9, 90 - (90 - 90)]]
    speed = 300
    for i in range(5):
        moveWithTime(bls1 + brs1, speed)
        moveWithTime(bls2 + brs2, speed)
        moveWithTime(bls3 + brs3, speed)
        moveWithTime(frs1 + fls1, speed)
        moveWithTime(bls4 + brs4, speed)
        moveWithTime(frs3 + fls3, speed)
        moveWithTime(frs4 + fls4, speed)

    moveWithTime([frz, rrz, flz, rlz], 500)


def dance():
    legs.setAngle(2, 60)
    legs.setAngle(14, 110)
    legs.setAngle(6, 110)
    legs.setAngle(10, 60)
    brs1 = [[0, 135, 1, 190]]
    brs2 = [[0, 90, 1, 190]]
    brs3 = [[0, 45, 1, 105]]
    brs4 = [[0, 150, 1, 140]]
    frs1 = [[12, 135, 13, 180]]
    frs2 = [[12, 90, 13, 180]]
    frs3 = [[12, 25, 13, 90]]
    frs4 = [[12, 90, 13, 90]]

    bls1 = [[4, 90 - (135 - 90), 5, 90 - (190 - 90)]]
    bls2 = [[4, 180, 5, 0]]
    bls3 = [[4, 90 - (45 - 90), 5, 90 - (90 - 105)]]
    bls4 = [[4, 90 - (150 - 90), 5, 90 - (140 - 90)]]
    fls1 = [[8, 90 - (135 - 90), 9, 90 - (180 - 90)]]
    fls2 = [[8, 90, 9, 90 - (180 - 90)]]
    fls3 = [[8, 90 - (25 - 90), 9, 90]]
    fls4 = [[8, 90 - (90 - 90), 9, 90 - (90 - 90)]]
    speed = 300
    for i in range(5):
        moveWithTime(brs1 + frs4 + bls4 + fls1, speed)
        moveWithTime(brs2 + fls2, speed)
        moveWithTime(brs3 + fls3, speed)

        moveWithTime(brs4 + frs1 + bls1 + fls4, speed)
        moveWithTime(frs2 + bls2, speed)
        moveWithTime(frs3 + bls3, speed)

    moveWithTime([frz, rrz, flz, rlz], 500)


def walkTest1():
    for i in range(5):
        moveWithTime([frf, rrb, flf, rlb], 550)
        moveWithTime([frb, rrf, flb, rlf], 350)

    moveWithTime([frz, rrz, flz, rlz], 500)


def higher():
    legs.setAngle(0, 90)
    legs.setAngle(1, 130)
    legs.setAngle(12, 90)
    legs.setAngle(13, 130)

    legs.setAngle(4, 90)
    legs.setAngle(5, 50)
    legs.setAngle(8, 90)
    legs.setAngle(9, 50)

    legs.setAngle(2, 85)
    legs.setAngle(14, 100)
    legs.setAngle(6, 100)
    legs.setAngle(10, 85)


def higherAction():
    hipsOut = ",2,80,6,100,10,80,14,100"
    return "0,90,1,130,12,90,13,130,4,90,5,50,8,90,9,50" + hipsOut


def lower():
    legs.setAngle(0, 60)
    legs.setAngle(1, 160)
    legs.setAngle(12, 60)
    legs.setAngle(13, 160)

    legs.setAngle(4, 120)
    legs.setAngle(5, 30)
    legs.setAngle(8, 120)
    legs.setAngle(9, 30)

    legs.setAngle(2, 85)
    legs.setAngle(14, 100)
    legs.setAngle(6, 100)
    legs.setAngle(10, 85)


def lowerAction():
    return "0, 60, 1, 160, 12, 60,13, 160,4, 120,5, 30,8, 120,9,30"


def sit():
    legs.setAngle(0, 90)
    legs.setAngle(1, 90)
    legs.setAngle(12, 140)
    legs.setAngle(13, 90)
    legs.setAngle(4, 90)
    legs.setAngle(5, 90)
    legs.setAngle(8, 40)
    legs.setAngle(9, 90)



def relaxServos():
    print("Relax all Servos")
    for i in range(16):
        if i % 4 != 3:
            angle = legs.getAngle(i)
            print("Relax servo:%d angle:%.2f" % (i, angle))
            # if angle is not None:
            #     legs.relaxServo(servo)


def moveSlow(low, high, delay, channel):
    print("Low:%d High:%d channel:%d" % (low, high, channel))
    for i in range(low, high):
        legs.setAngle(channel, i)
        time.sleep(delay)
    for i in range(high, low, -1):
        legs.setAngle(channel, i)
        time.sleep(delay)


def moveSlowStop(low, high, stop, delay, channel):
    print("moveSlowStop Low:%d High:%d channel:%d" % (low, high, channel))
    for i in range(stop, low, -1):
        legs.setAngle(channel, i)
        time.sleep(delay)
    for i in range(low, high):
        legs.setAngle(channel, i)
        time.sleep(delay)
    for i in range(high, low, -1):
        legs.setAngle(channel, i)
        time.sleep(delay)
    for i in range(low, stop):
        legs.setAngle(channel, i)
        time.sleep(delay)
