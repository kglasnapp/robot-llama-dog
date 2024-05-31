from adafruit_bno08x import (
  BNO_REPORT_ACCELEROMETER,
  BNO_REPORT_GYROSCOPE,
  BNO_REPORT_MAGNETOMETER,
  BNO_REPORT_ROTATION_VECTOR,
  BNO_REPORT_GAME_ROTATION_VECTOR,
)

from adafruit_bno08x.i2c import BNO08X_I2C
from util import i2c
from math import atan2, sqrt, pi, asin


bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

initYaw = 0
initPitch = 0
initRoll = 0

def initGyroAngles():
    global initYaw, initPitch, initRoll
    res = getRawGyro()
    initYaw = res[0]
    initPitch = res[1]
    initRoll = res[2]
    showGyro()
    
def getRawGyro():
    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
    res = quaternionToEuler(quat_real,quat_i, quat_j, quat_k)
    return res

def getAdjustedGyro():
    global initYaw, initPitch, initRoll
    res = getRawGyro()
    yaw = -norm(res[0] - initYaw)
    pitch = -norm(res[1] - initPitch)
    roll = -norm(res[2] - initRoll)
    return (yaw, pitch, roll)

def showGyro():
    res = getAdjustedGyro()
    f = "Yaw:%.1f Pitch:%.1f Roll:%.1f" % res
    print(f)
    return res

def norm(angle):
  angle = angle % 360
  if angle > 180:
    angle = angle - 360
  return angle

def quaternionToEuler( qr,  qi, qj,  qk):
  sqr = qr * qr
  sqi = qi * qi
  sqj = qj * qj
  sqk = qk * qk
  yaw = atan2(2.0 * (qi * qj + qk * qr), (sqi - sqj - sqk + sqr));
  pitch = asin(-2.0 * (qi * qk - qj * qr) / (sqi + sqj + sqk + sqr));
  roll = atan2(2.0 * (qj * qk + qi * qr), (-sqi - sqj + sqk + sqr));
  RAD_TO_DEG = 180 / 3.14159
  yaw *= RAD_TO_DEG;
  pitch *= RAD_TO_DEG;
  roll *= RAD_TO_DEG;
  return (yaw, pitch, roll)