'''
-----------------------------------------------------------
Name: Lab 4 Exercise 4
-----------------------------------------------------------
Learning to use rhe OLED deisplay driver
-----------------------------------------------------------
'''
import pyb
from pyb import LED, ADC, Pin  # Pyboard basic library
from oled_938 import OLED_938  # Use various class libraries in pyb

# Create peripheral objects
b_LED = LED(4)
pot = ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout = {'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc = False, i2c_devid = 61)
oled.poweron()
oled.init_display()

# Simple Hello world message
oled.draw_text(0, 0, 'Hello, world!')  # each character is 6x8 pixels

tic = pyb.millis()  # store starting time
while True:
  b_LED.toggle()
  toc = pyb.millis() # read elapsed time
  oled.draw_text(0, 20, 'Delayed time:{:6.3f}sec'.format((toc-tic)*0.001))
  oled.draw_text(0, 40, 'POT5K reading:{:5d}'.format(pot.read()))
  tic = pyb.millis() # start time
  oled.display()
  delay = pyb.rng()%1000 # Generate a random number btw 0 and 999
  pyb.delay(delay)       # Delay in milliseconds
