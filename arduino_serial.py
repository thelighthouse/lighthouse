import serial
from random import randint
from cobs import cobs
from time import sleep
import array


class SerialCOBS(object):

  def __init__(self, ser):
    ser.close()
    ser.open()
    sleep(1)
    self.ser = ser

  def get(self):
    outBuffer = ""
    while 1:
      read = self.ser.read(1000)
      if len(read) == 0:
        print "timeout"
        break
      outBuffer += read

      if outBuffer[-1] == '\x00':
        break
    return cobs.decode(bytes(outBuffer[:-1]))

  def init(self):
    res = ""
    while res != "ok":
      null = chr(0)
      self.ser.write(null)
      res = self.get()

  def send(self, data):
    self.init()
    enc = cobs.encode(bytes(data)) + chr(0)
    return self.ser.write(enc)


def byteArray(x):
  return array.array('B', x).tostring()


def set_speed(serialCOBS):
  serialCOBS.send(byteArray([1, 0]))
  # print repr(serialCOBS.get())  # Should be 'egassem tset'


def test_solid(serialCOBS):
  offset = 0
  while True:
    offset = (offset+1) % 256
    try:
      serialCOBS.send(byteArray([1, offset, 255, 255]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)


def test_gradient(serialCOBS):
  offset = 0
  while True:
    offset = (offset+1) % 256
    hue_from = offset
    hue_to = (offset-1) % 256
    try:
      serialCOBS.send(byteArray([2, hue_from, 255, 255, hue_to, 255, 255]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)


def test_gradient_pulse(serialCOBS):
  offset = 0
  while True:
    offset = (offset+1) % 256
    sat = 2*abs(offset-128)
    try:
      serialCOBS.send(byteArray([2, 0, sat, 128, 255, sat, 128]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)

# serialCOBS = SerialCOBS(serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.01))


def test_gradient_pulse_random(serialCOBS):
  offset = 0
  offset2 = 0
  while True:
    offset = (offset+1) % 256
    sat = 2*abs(offset-128)
    offset2 = (offset2+1) % 256
    hue_from = offset2
    hue_to = (offset2-1) % 256
    try:
      serialCOBS.send(byteArray([2, hue_from, sat, 128, hue_to, sat, 128]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)

# serialCOBS = SerialCOBS(serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.01))


def test_chase(serialCOBS):
  serialCOBS.send(byteArray([1, 0, 0, 0]))
  print repr(serialCOBS.get())  # Should be 'egassem tset'
  sleep(0.5)
  offset = 1120
  # serialCOBS.send(byteArray([4, 0, 255, 0, 1, 0, 255, 128]))
  while True:
    try:
      prev = offset
      offset = ((offset+1) % (240*5-1))
      print offset
      serialCOBS.send(byteArray([4, (prev >> 8), (prev & 0xFF), 0, 1, 0, 0, 0]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
      sleep(0.5)
      serialCOBS.send(byteArray([4, (offset >> 8), (offset & 0xFF), 0, 1, 0, 255, 128]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'

    except:
      pass
    sleep(0.5)


def test_blink(serialCOBS):
  serialCOBS.send(byteArray([1, 0, 0, 0]))
  print repr(serialCOBS.get())  # Should be 'egassem tset'
  sleep(0.5)
  offset = 1118
  # serialCOBS.send(byteArray([4, 0, 255, 0, 1, 0, 255, 128]))
  while True:
    try:
      prev = offset
      # offset = ((offset+1) % (240*5-1))
      print offset
      serialCOBS.send(byteArray([4, (prev >> 8), (prev & 0xFF), 0, 1, 0, 0, 0]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
      sleep(0.5)
      serialCOBS.send(byteArray([4, (offset >> 8), (offset & 0xFF), 0, 1, 0, 255, 128]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'

    except:
      pass
    sleep(0.5)


def test_wire(serialCOBS):
  serialCOBS.send(byteArray([1, 0, 0, 0]))
  print repr(serialCOBS.get())  # Should be 'egassem tset'
  sleep(0.5)
  num_per = 240
  for wire in xrange(5):
    offset = wire*num_per
    serialCOBS.send(byteArray([4, (offset >> 8), (offset & 0xFF), 0, num_per, wire*48, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
    sleep(0.05)


def test_random(serialCOBS):
  serialCOBS.send(byteArray([1, 255, 0, 255]))
  print repr(serialCOBS.get())  # Should be 'egassem tset'
  sleep(0.5)
  num = 240*5-10
  while True:
    try:
      offset = randint(0, num)
      hue = randint(0, 255)
      serialCOBS.send(byteArray([4, (offset >> 8), (offset & 0xFF), 0, 10, hue, 255, 128]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.1)


def test_noop(serialCOBS):
  while True:
    try:
      serialCOBS.send(byteArray([]))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.1)

# serialCOBS = SerialCOBS(serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.01))


def test_pattern(serialCOBS):
  test = [0, 255, 128, 128, 255, 128, 128, 255, 128]  # *160  # , 0, 255, 255, 192, 255, 255]
  test2 = [128, 255, 128, 0, 255, 128, 128, 255, 128]  # *160  # , 0, 255, 255, 192, 255, 255]
  test3 = [128, 255, 128, 128, 255, 128, 0, 255, 128]  # *160  # , 0, 255, 255, 192, 255, 255]

  while True:
    try:
      serialCOBS.send(byteArray([3]+test))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)

    try:
      serialCOBS.send(byteArray([3]+test2))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)

    try:
      serialCOBS.send(byteArray([3]+test3))
      print repr(serialCOBS.get())  # Should be 'egassem tset'
    except:
      pass
    sleep(0.05)


def set_clut(serialCOBS):
  try:
    print "setting"
    serialCOBS.send(byteArray([5, 0, 0, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
  except:
    pass
  # sleep(0.5)
  try:
    print "setting"
    serialCOBS.send(byteArray([5, 1, 32, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
  except:
    pass
  # sleep(0.5)
  try:
    print "setting"
    serialCOBS.send(byteArray([5, 2, 64, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
  except:
    pass
  # sleep(0.5)
  try:
    print "setting"
    serialCOBS.send(byteArray([5, 3, 96, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
  except:
    pass
  # sleep(0.5)
  try:
    print "setting"
    serialCOBS.send(byteArray([5, 4, 128, 255, 128]))
    print repr(serialCOBS.get())  # Should be 'egassem tset'
  except:
    pass
  # sleep(0.5)

if __name__ == '__main__':
  serialCOBS = SerialCOBS(serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.5))
  # test_pattern(serialCOBS)
  # while True:
  # set_clut(serialCOBS)
  set_speed(serialCOBS)
  # test_noop(serialCOBS)

# data scheme:
# cmd (1-byte)
# data (variable)
# CRC (for cmd+data) (1-byte)

# "ack" and "nack" commands with retries on nack

# modes
# scroll
# solid fade
# random fade
# gradient
# solid
# twinkle


# objects
# color array (hsv or just h?)
# animation speed
# s/v if separate from color array
# mode
# look at rainbow code

# commands
