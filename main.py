import Kinematics as kin
import Config as conf
import numpy as np
import math


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
showInfo([0, 0, 0.05], 0, 0.2, 0.02)
showInfo([0, 0, 0.05], 1, 0.2, 0.02)
showInfo([0, 0, 0.05], 2, 0.2, 0.02)
