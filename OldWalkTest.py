import Kinematics as kin
import Config as conf
import numpy as np
import math
from robotLegs import legs
import time


def radToDegrees(ar):
    r = []
    for a in ar:
        d = round(math.degrees(a), 2)
        r.append(d)
    return r


def arToStr(ar, fmt="%7.2f"):
    s = "["
    for a in ar:
        s += fmt % (float(a)) + ", "
    return s[0:-2] + "]"


def showInfo(initPos, idx, endVal, delta, legIndex=0):
    print("Show idx:", idx, arToStr(initPos))
    while initPos[idx] < endVal:
        legIndex = 0
        angles = kin.leg_explicit_inverse_kinematics(initPos, legIndex, config)
        d = radToDegrees(angles)
        xyz = kin.forward_kinematics(angles, config, legIndex)
        print(
            "pos: %s Angles = %s XYZ = %s"
            % (arToStr(initPos), arToStr(d), arToStr(xyz))
        )
        initPos[idx] += delta
    print()


x = 0
config = conf.Configuration()
# showInfo([0, 0, 0.05], 0, 0.2, 0.02)
# showInfo([0, 0, 0.05], 1, 0.2, 0.02)
# showInfo([0, 0, 0.05], 2, 0.2, 0.02)


def testWalk(leg):
    prt = True
    legIndex = int(leg / 4)
    print("\nTest Walk leg:", leg, legIndex)
    initPos = [0, 0, 0.05]
    idx = 2
    endVal = 0.1
    delta = 0.0025
    while initPos[idx] < endVal:
        angles = kin.leg_explicit_inverse_kinematics(initPos, legIndex, config)
        d = radToDegrees(angles)
        # Check for servo on Left side
        if legIndex == 1 or legIndex == 2:
            # Left Side
            legs.setAngle(leg + 1, 90 + d[1])
            legs.setAngle(leg, d[1])
        else:
            # Right Side
            legs.setAngle(leg + 1, -d[1] + 90)
            legs.setAngle(leg, -d[1] + 90)
        xyz = kin.forward_kinematics(angles, config, legIndex)
        if prt:
            print(
                "pos: %s Angles = %s XYZ = %s"
                % (arToStr(initPos), arToStr(d), arToStr(xyz))
            )
            # prt = False
        initPos[idx] += delta
        time.sleep(0.02)
