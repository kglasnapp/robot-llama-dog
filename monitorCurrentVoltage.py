from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from util import i2c

class MonitorCurrentVoltage:
  overCurrentCount = 0
  maxCurrent = 0
  averageCurrent = 0
  currentCount = 0
  
  def __init__(self):
    
    self.ina219 = INA219(i2c, 0x41)
    # optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
    self.ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    self.ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    # optional : change voltage range to 16V
    self.ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

  def showIna219(self):
    bus_voltage = self.ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = self.ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = self.ina219.current / 132 # current in mA
    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    print("Voltage (VIN+) : {:6.3f} V".format(bus_voltage + shunt_voltage))
    print("Voltage (VIN-) : {:6.3f} V".format(bus_voltage))
    print("Shunt Voltage  : {:8.5f} V".format(shunt_voltage))
    print("Shunt Current  : {:7.4f} A".format(current ))
    print("Power Calc.    : {:8.5f} W".format(bus_voltage * current ))

  def checkCurrent(self):
    current = self.ina219.current / 132
    volts = self.ina219.bus_voltage
    maxCurrent = max(self.maxCurrent, current)
    self.currentCount += 1
    self.averageCurrent += current
    if current > 5:
      self.overCurrentCount += 1
    else:
      self.overCurrentCount = 0
    if current > 10 and self.overCurrentCount > 10:
      print("Over current of " + str(current) + " detected count:", self.overCurrentCount)
      while True:
        pass
    return round(current,2), round(volts,2)
  
  def getVolts(self):
      return round(self.ina219.bus_voltage,1)
    
  def getCurrent(self):
      return round(self.ina219.current / 132, 1)
      
  def showStats(self):
      if self.currentCount == 0:
          self.currentCount = 1
      print("Current Max:%.2f Average:%.2f" % (self.maxCurrent,  self.averageCurrent / self.currentCount))
         