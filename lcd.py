#!/usr/bin/python
import sys 
import spidev as SPI
import time
#sys.path.append("..")
import LCD_1inch47
# PIL is a great image manipulation library -- can do a lot
from PIL import Image,ImageDraw,ImageFont

class lcd:
  disp = LCD_1inch47.LCD_1inch47()
  disp.Init()
  disp.clear()
  image1 = Image.new("RGB", (disp.width, disp.height ), "WHITE")
  Font3 = ImageFont.truetype("../Font/Font02.ttf",30)

  def showVoltageCurrent(self, voltage, current):
    self.image1 = Image.new("RGB", (self.disp.width, self.disp.height ), "BLACK")
    self.draw = ImageDraw.Draw(self.image1)
    current_time = time.strftime("%I:%M:%S %p")
    self.draw.text((2, 100), current_time, fill = "WHITE",font=self.Font3)
    self.draw.text((5, 130), 'Current:' + str(current), fill = "WHITE",font=self.Font3)
    #draw.rectangle([(0,155),(172,195)],fill = "BLACK")
    self.draw.text((5, 155), 'Voltage:' + str(voltage), fill = "WHITE", font=self.Font3)
    image1=self.image1.rotate(270)
    self.disp.ShowImage(image1)

  def showServoPositions(self, servo, lower, upper):
    self.image1 = Image.new("RGB", (self.disp.width,self.disp.height ), "BLACK")
    self.draw = ImageDraw.Draw(self.image1)
    self.draw.rectangle([(0,120),(140,153)],fill = "GREEN")
    self.draw.text((5, 120), 'Servo:' + str(servo), fill = "WHITE",font=self.Font3)
    #draw.rectangle([(0,155),(172,195)],fill = "BLACK")
    self.draw.text((5, 155), 'Upper:' + str(upper), fill = "WHITE", font=self.Font3)
    self.draw.text((5, 190), 'Lower:' + str(lower), fill = "WHITE",font=self.Font3)
    image1=self.image1.rotate(270)
    self.disp.ShowImage(image1)
    
  def showPosition(self, roll, pitch, yaw):
    self.image1 = Image.new("RGB", (self.disp.width,self.disp.height ), "BLACK")
    self.draw = ImageDraw.Draw(self.image1)
    current_time = time.strftime("%I:%M:%S %p")
    self.draw.text((2, 100), current_time, fill = "GREEN",font=self.Font3)
    self.draw.text((2, 130), "Roll:" + "%.2f" % (roll), fill = "GREEN",font=self.Font3)
    self.draw.text((2, 160), "Pitch:" + "%.2f" % (pitch), fill = "GREEN",font=self.Font3)
    self.draw.text((2, 190), "Yaw:" + "%.2f" % (yaw), fill = "GREEN",font=self.Font3)
    image1=self.image1.rotate(270)
    self.disp.ShowImage(image1)
  
  def showEncoder(self, low, up):
    self.image1 = Image.new("RGB", (self.disp.width,self.disp.height ), "BLACK")
    self.draw = ImageDraw.Draw(self.image1)
    current_time = time.strftime("%I:%M:%S %p")
    self.draw.text((2, 100), current_time, fill = "GREEN",font=self.Font3)
    self.draw.text((2, 130), "Low:" + str(low), fill = "GREEN",font=self.Font3)
    self.draw.text((2, 160), "Up:" + str(up), fill = "GREEN",font=self.Font3)
    image1=self.image1.rotate(270)
    self.disp.ShowImage(image1)
    
  def clear(self):
    self.disp.clear()

  def exit(self):
    self.disp.module_exit()

if __name__ == '__main__':
  print("Init lcd")
  l = lcd()
  l.showServoPositions(4,90,100) 
  time.sleep(1)
  l.showVoltageCurrent(5.6, 4)
  time.sleep(1)
  l.showServoPositions(4,90,80)
  time.sleep(1)
  l.showEncoder(0,0)
  l.exit()