from adafruit_seesaw import seesaw, rotaryio, digitalio
import board

class Encoder:
  global kit
  seesaw = None
  button = None
  button_held = False
  lastEncoder = 0
  lastPos = 0
  increment = 2

  def __init__(self, addr):
    self.seesaw = seesaw.Seesaw(board.I2C(), addr=addr)
    self.addr = addr
    seesawVer = (self.seesaw.get_version() >> 16) & 0xFFFF
    if seesawVer != 4991:
      print("Wrong firmware loaded?  Expected 4991")
    self.seesaw.pin_mode(24, self.seesaw.INPUT_PULLUP)
    self.button = digitalio.DigitalIO(self.seesaw, 24)
    self.button_held = False
    self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
    self.encoder.position = int(90 / self.increment)

  def periodic(self):
    encoder = self.encoder.position
    delta = encoder - self.lastEncoder
    if delta != 0:
        self.lastEncoder = encoder
        pos = self.lastPos + delta * self.increment
        if pos > 179:
          pos = 179
        if pos < 1:
          pos = 0
        #print("Addr:0x%x Pos:%d Delta:%d Actual:%d" % (self.addr, pos, delta, encoder))
        if self.lastPos != pos:
          self.lastPos = pos
          #print("Pos for %x changed:%d" % (self.addr, pos))
          return pos
    if not self.button.value and not self.button_held:
        self.button_held = True
        print("Button pressed on " + hex(self.addr))
        return -1
    if self.button.value and self.button_held:
        self.button_held = False
        print("Button released on "  + hex(self.addr))
    return self.lastPos