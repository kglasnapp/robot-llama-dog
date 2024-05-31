# from myTest import servos
import util
from adafruit_servokit import ServoKit
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

print("Show I2C Addresses")
util.showI2C()
# Create a simple PCA9685 class instance for the Motor FeatherWing's default address.
kit = PCA9685(util.i2c, address=0x40,  reference_clock_speed=25630710)
#kit.frequency = 100

#kit = PCA9685(util.i2c, address=0x40,  reference_clock_speed=25000000)
kit.frequency = 100

# Create a list of sevos
servos = list()
for i in range(16):
    # Create servo with a min pulse rate and a max pulse rate
    servos.append(servo.Servo(kit.channels[i], min_pulse=500, max_pulse=2300))

def reset():
    kit.reset()

def relax(servo):
   kit.channels[i].angle(None)
