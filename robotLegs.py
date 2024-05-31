import time
import movements
from myServo import servos


class Legs:
    # Servo Ranges -> {low value, high value, default value, offsets for each leg}
    lowServo = [0, 175, 90, 0, 0, 0, 0]
    highServo = [0, 175, 90, 0, 0, 3, 0]
    hipServo = [70, 110, 90, 8, 12, 9, 14]
    ranges = [lowServo, highServo, hipServo]
    angles = []

    """
  BRLow = 0
  BRUp = 1
  BRHip = 2
  
  right_back = 0
  left_back  = 1
  left_front = 2
  right_front= 3
  
  """

    def getOffset(self, servo):
        if servo % 4 != 3:
            servoValues = self.ranges[servo % 4]
            offset = servoValues[int(servo / 4) + 3]
            return offset
        return None

    def getAngle(self, servo):
        angle = servos[servo].angle
        if angle is None:
            # Get the default angle
            angle = self.ranges[servo % 4][2]
        return angle - self.getOffset(servo)

    def angleOk(self, servo, angle):
        if servo % 4 != 3:
            servoValues = self.ranges[servo % 4]
            if angle < servoValues[0]:
                print("angle too low for servo:%d angle:%.2f" % (servo, angle))
                return False
            if angle > servoValues[1]:
                print("angle too high for servo:%d angle:%.2f" % (servo, angle))
                return False
            return True
        print("Invalid servo:", servo)
        return False

    def setAngle(self, servo, angle):
        if servo % 4 != 3:
            servoValues = self.ranges[servo % 4]
            if angle < servoValues[0]:
                print("setAngle to low servo:%d angle:%.2f" % (servo, angle))
                angle = servoValues[0]
            if angle > servoValues[1]:
                print("setAngle to high servo:%d angle:%.2f" % (servo, angle))
                angle = servoValues[1]
            angle += self.getOffset(servo)
            if angle >= 180:
                print("Set angle outside range for servo:%d force angle to 180" % (servo, angle))
                angle = 180
            try:
              servos[servo].angle = angle 
            except:
              print("Tried to set angle to %.2f actual %.2f for servo:%d" % (angle, angle + self.getOffset(servo), servo))

    def relaxServo(self, servo):
        servos[servo].angle = None
        # servo.relaxServo(servo)

    def setAngleC(self, servo, angle):
        self.setAngle(servo, 180 - angle)

    def setDefaults(self):
        for servo in range(0, 15):
            if servo % 4 != 3:
                actual = self.ranges[servo % 4][2] + self.getOffset(servo)
                default = self.ranges[servo % 4][2]
                legs.setAngle(servo, default)
                print("Servo:%2d Default:%.2f Actual:%.2f" % (servo, default, actual))
                time.sleep(0.1)

    def testLegRange(self, leg):
        servo = leg * 4
        if servo % 4 != 3:
            for i in range(3):
                s = self.ranges[i]
                movements.moveSlowStop(s[0], s[1], s[2], 0.005, servo + i)
                time.sleep(0.1)

    def getAngles(self):
        angles = []
        for i in range(16):
            angle = servos[i].angle
            if angle is None:
                angles.append(99)
            else:
                angles.append(angle - int(self.getOffset(i)))
        return angles

    def printServos(self):
        angles = self.getAngles()
        s = "["
        for i in range(len(angles)):
            if i % 4 != 3:
                print("Servo:%d - %.1f" % (i, angles[i]))
                s += "[%d,%f]," % (i,round(angles[i]),1)
        s = s[:-1] + "]"
        print(s)

legs = Legs()

