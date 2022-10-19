#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

  def __init__(self, address, debug=False):
    self.bus = smbus.SMBus(1)
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting PCA9685")
    self.write(self.__MODE1, 0x00)

  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.bus.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result

  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print("Setting PWM frequency to %d Hz" % freq)
      print("Estimated pre-scale: %d" % prescaleval)
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print("Final pre-scale: %d" % prescale)

    oldmode = self.read(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    self.write(self.__MODE1, newmode)        # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.write(self.__LED0_ON_L + 4*channel, on & 0xFF)
    self.write(self.__LED0_ON_H + 4*channel, on >> 8)
    self.write(self.__LED0_OFF_L + 4*channel, off & 0xFF)
    self.write(self.__LED0_OFF_H + 4*channel, off >> 8)
    if (self.debug):
      print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))

  def setDutycycle(self, channel, pulse):
    self.setPWM(channel, 0, int(pulse * (4096 / 100)))

  def setLevel(self, channel, value):
    if (value == 1):
      self.setPWM(channel, 0, 4095)
    else:
      self.setPWM(channel, 0, 0)

# pwm = PCA9685(0x5f, debug=False)
# pwm.setPWMFreq(50)
# pwm.setDutycycle(0,100)
# pwm.setLevel(1,0)
# pwm.setLevel(2,1)

import traitlets
import atexit
from traitlets.config.configurable import Configurable

class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets
        self._driver = driver
        self._driver.setPWMFreq(1000)
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4
        self._motor = channel
        atexit.register(self._release)
        
    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        mapped_value = int(100.0 * (self.alpha * value + self.beta))
        speed = min(max(abs(mapped_value), 0), 99)
        if speed != 0:
            if(self._motor == 1):
                self._driver.setDutycycle(self.PWMB, speed)
                if(mapped_value > 0):
                    self._driver.setLevel(self.BIN1, 0)
                    self._driver.setLevel(self.BIN2, 1)
                else:
                    self._driver.setLevel(self.BIN1, 1)
                    self._driver.setLevel(self.BIN2, 0)
            elif(self._motor == 2):
                self._driver.setDutycycle(self.PWMA, speed)
                if(mapped_value < 0):
                    self._driver.setLevel(self.AIN1, 0)
                    self._driver.setLevel(self.AIN2, 1)
                else:
                    self._driver.setLevel(self.AIN1, 1)
                    self._driver.setLevel(self.AIN2, 0)
            elif(self._motor == 3):
                self._driver.setDutycycle(self.PWMA, speed)
                if(mapped_value > 0):
                    self._driver.setLevel(self.AIN1, 0)
                    self._driver.setLevel(self.AIN2, 1)
                else:
                    self._driver.setLevel(self.AIN1, 1)
                    self._driver.setLevel(self.AIN2, 0)            
            elif(self._motor == 4):
                self._driver.setDutycycle(self.PWMB, speed)
                if(mapped_value < 0):
                    self._driver.setLevel(self.BIN1, 0)
                    self._driver.setLevel(self.BIN2, 1)
                else:
                    self._driver.setLevel(self.BIN1, 1)
                    self._driver.setLevel(self.BIN2, 0)
            else:
                return
        else:
            if ((self._motor == 1) or (self._motor == 4)):
                self._driver.setDutycycle(self.PWMB, 0)
            elif ((self._motor == 3) or (self._motor == 2)):
                self._driver.setDutycycle(self.PWMA, 0)
            else:
                return

    def _release(self):
        """Stops motor by releasing control"""
        self._driver.setDutycycle(self.PWMA, 0)
        self._driver.setDutycycle(self.PWMB, 0)