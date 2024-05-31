import asyncio
import time
import math
from robotLegs import legs

# Balanced with front right leg lifted
# Servo:0 - 119.9
# Servo:1 - 119.9
# Servo:2 - 90.0
# Servo:4 - 89.9
# Servo:5 - 59.9
# Servo:6 - 89.9
# Servo:8 - 89.9
# Servo:9 - 59.8
# Servo:10 - 90.0
# Servo:12 - 59.9
# Servo:13 - 119.9
# Servo:14 - 89.9


# def testBalanceOS():
#    for servo in [0,8,12,4]:
#       initForward(servo)
#        # Init
#       #setAngle(servo+2, 80)
#    time.sleep(5)
#    for servo in [0,8,12,4]:
#       moveBack(servo)


# def initForward(servo):
#    # Forward
#     setAngle(servo+1, 109)
#     setAngle(servo+0, 68)

# def moveBack(servo):
#     # Back
#     setAngle(servo+1, 131)
#     setAngle(servo+0, 90)

def asyncTestBalance():
     asyncio.run(action([[[0,4],90],[[8,12],68],[[1,9,13,5],109]],.5,normalize=True))
     #await asyncio.sleep(1)
     time.sleep(1)
     asyncio.run(action([[[0,4],130],[[8,12],90],[[1,9,13,5],131]],.5,normalize=True))

def asyncMove(actions, speed):
    asyncio.run(action(actions, speed))

def asyncSit():
  asyncio.run(action([[0,90],[1,90],[12,140],[13,90],[4,90],[5,90],[8,40],[9,90]],.5))
   
def asyncM():
  asyncio.run(action([[1, 70],[5, 70],[9, 70],[13, 70]],1))

def lowerAsync():
  asyncio.run(action([[2,90],[6,90],[10,90],[14,90],[0, 60],[1, 160],[12, 60],[13, 160],[4, 120],[5, 30],[8, 120],[9,30]],2))

def higherAsync():
    asyncio.run(action([[2,90],[6,90],[10,90],[14,90],[0,140],[1,130],[12,90],[13,130],[4,55],[5,50],[8,90],[9,53]],2))

# adjust angle to make right and left angles the same indepentant of servo
def adjustAngle(servo, angle, normalize):
    if normalize:
         group = int(servo / 4)
         if group == 1 or group == 2:
           angle = 180 - angle
    return angle

async def action(actions, speed, normalize=False ):
    tasks = []
    for act in actions:
        print(act)
        if  type(act[0]) is list:
            for a in act[0]:
                angle = adjustAngle(a,act[1],normalize)
                tasks.append(asyncio.create_task(move(a, angle, speed)))
        else:
           angle = adjustAngle(act[0],act[1],normalize)
           tasks.append(asyncio.create_task(move(act[0], angle, speed)))
    for task in tasks:
        await task

async def move(servo, angle, seconds):
    startTime = time.perf_counter()
    startAngle = 90
    startAngle = legs.getAngle(servo)
    period = 0.025  
    delta = (angle - startAngle) * period / seconds
    #print("servo:%d endangle:%.2f sec:%.2f delta:%.2f" % (servo, angle, seconds, delta))
    while ((startAngle >= angle) and delta < 0) or ((startAngle <= angle) and delta > 0 ):
        if abs(startAngle - angle) < .25:
            break
        if servo == 99:
            print("servo:%.2f angle:%.2f time:%.2f" % (servo, startAngle, time.perf_counter() - startTime))
        startAngle += delta
        legs.setAngle(servo,startAngle)
        await asyncio.sleep(period - 0.005)
    print("Complete servo:%d angle:%.2f time:%.2f" % (servo, legs.getAngle(servo), time.perf_counter() - startTime))


# def strToMovements(s, speed):
#    ar = s.split(",")
#    actions = []
#    for i in range(0, len(ar),2):
#        actions.append([int(ar[i]), float(ar[i+1])])
#    servosMove.newServoActions(actions, speed)
