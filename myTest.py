#!/usr/bin/env python3
import util
import time
import monitorCurrentVoltage
import lcd
import movements as m
import robotLegs
import encoder
from threading import Thread
import imu
from enum import Enum
import robotLegs
import asyncServo
import controlPattern

dispMode = Enum("dispMode", ["Power", "Encoder", "RollPitchYaw"])


def mySleep(_time):
    finishTime = time.monotonic()
    while time.monotonic() < finishTime + _time:
        current, volts = monCurVolt.checkCurrent()
        time.sleep(0.05)

help_ = "0-legs to 90, 1-wiggle legs, \n"
help_ += "2-legs range, 3-lower robot, 4-raise robot, \n"
help_ += "5-raise and lower 10 times, 6-set leg to angle, 7-Test Balance, 8-sit, 9-march h-this help\n"
help_ += "a-move async, b-test balance, e-move servo by encoders, k-kinematics walk, g-show gyro i-init Gyro angles\n"
help_ += "l-lean forward, m-multiple moves, n-multiple moves, s-show status, w-walk keith vers, q-quit"

def task(s):
    global dispMode, fin, servosMove
    if s != "":
        result = s.strip()
        legVal = result.split(",")
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        # Take in an array of 12 angles for setting each of the 12 servos
        # if len(result) > 10:
        #     # print("Got:" + result)
        #     for i in range(4):
        #         # print('leg = '+str(i))
        #         for j in range(3):
        #             robotLegs.legs.setAngle(i * 4 + j, 90 + int(legVal[i * 4 + j]))
        if result == "0":
            robotLegs.legs.setDefaults()
        if result == "1":
            m.wiggle()
            robotLegs.legs.setDefaults()
        if result == "2":
            for i in range(4):
                robotLegs.legs.testLegRange(i)
        if result == "3":
            asyncServo.lowerAsync()
        if result == "4":
            asyncServo.higherAsync()
        if result == "5":
            start = time.time()
            for i in range(5):
                print("Elapsed 0 %.2f" % (time.time() - start))
                asyncServo.lowerAsync()
                print("Elapsed 1 %.2f" % (time.time() - start))
                time.sleep(0.2)
                print("Elapsed 2 %.2f" % (time.time() - start))
                asyncServo.higherAsync()
                print("Elapsed 3 %.2f" % (time.time() - start))
                time.sleep(0.2)
            monCurVolt.showStats()
        if legVal[0] == "6" and len(legVal) == 3:
            print(legVal)
            robotLegs.legs.setAngle(int(legVal[1]), int(legVal[2]))
        if legVal[0] == "7":
            # m.testBalanceOS()
            asyncServo.asyncTestBalance()
        if legVal[0] == "8":
            asyncServo.asyncSit()
        if legVal[0] == "9":
            for i in range(10):
                m.march1()
                time.sleep(0.5)
                m.march2()
                time.sleep(0.5)
            m.higher()
        if result == "a":
            asyncServo.asyncM()
        if result == "b":
            asyncServo.asyncLiftRightLeg()
        if legVal[0] == "c":
            if len(legVal) == 2:
                print(legVal)
                controlPattern.control(int(legVal[1]))
        if legVal[0] == 'f':
            if len(legVal) == 2:
                controlPattern.runFile(legVal[1])
        if result == "d":
            m.dance()
        if len(legVal) == 2 and legVal[0] == "e":
            if enc0 is not None:
                print("Not in Service")
                return
            while True:
                dispMode = dispMode.Encoder
                e0 = enc0.periodic()
                e1 = enc1.periodic()
                if util.checkInput() is not None:
                    break
                robotLegs.legs.setAngle(int(legVal[1]), e1)
                robotLegs.legs.setAngle(int(legVal[1]) + 1, e0)
                print("Low:%.1f Up:%.1f" % (e1, e0))
                # disp.showEncoder(e1, e0)
                time.sleep(0.25)
            dispMode = dispMode.Power
        if result == "g":
            dispMode = dispMode.RollPitchYaw
            while True:
                if util.checkInput() is not None:
                    break
                res = imu.showGyro()
                disp.showPosition(res[0], res[1], res[2])
                time.sleep(1)
            dispMode = dispMode.Power
        if result == "h":
            print(help_)
        if result == "i":
            imu.initGyroAngles()
            imu.showGyro()
        if result == "k":
            asyncServo.walk()
        if result == "l":
            m.leanforward()
        if result == "m":
            s = [[1, 120], [13, 120], [9, 60], [5, 60]]
            asyncServo.asyncMove(s, 0.5)
        if result == "n":
            s = [[1, 90], [13, 90], [9, 90], [5, 90]]
            asyncServo.asyncMove(s, 0.5)
        if result == "q":
            fin = True
            exit()
        if result == "s":
            print("Display Mode:", dispMode, " Fin:", fin)
            util.showI2C()
            monCurVolt.showIna219()
            robotLegs.legs.printServos()
            if enc0 is not None:
                disp.showEncoder(enc0.periodic(), enc1.periodic())
        if result == "w":
            m.legswalkTest()


class DisplayThread(Thread):
    global fin
    fin = False
    count = 0

    def run(self):
        count = 0
        while True:
            if fin:
                return
            if dispMode == dispMode.Power:
                volts = monCurVolt.getVolts()
                current = monCurVolt.getCurrent()
                disp.showVoltageCurrent(volts, current)
                count += 1
            time.sleep(0.25)



monCurVolt = monitorCurrentVoltage.MonitorCurrentVoltage()
print("Ready for input from serial port")

print(help_)
count = 0
startTime = 0
# set objects for the encoder
enc0 = None  # encoder.Encoder(0x36)
enc1 = None  # encoder.Encoder(0x3D)
disp = lcd.lcd()

# create and start the thread
fin = False
thread = DisplayThread()
thread.start()
print("Set default angles")
imu.initGyroAngles()
print("\n>", end="")
time.sleep(0.05)
dispMode = dispMode.Power
while True:
    while True:
        count += 1
        # servosMove.moveServos()
        if time.monotonic() > startTime + 120:
            startTime = time.monotonic()
            current, volts = monCurVolt.checkCurrent()
            print("\nCurrent:%.2f Volts:%.2f" % (current, volts))
            if dispMode == dispMode.Power:
                disp.showVoltageCurrent(volts, current)
            print("\n>", end="")
        if util.charAvailable():
            break
    s = input()
    if len(s) != 0:
        print(ord(s[0:1]))
        task(s)
    print("\n>", end="")
