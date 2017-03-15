'''
-----------------------------------------------------------
Name: Lab 4 Exercise 5
-----------------------------------------------------------
Draw Pendulum reflecting pitch angles (raw and filtered)
-----------------------------------------------------------
'''
from mpu6050 import MPU6050
import pyb
from pyb import LED, ADC, Pin  # Pyboard basic library
from oled_938 import OLED_938  # Use various class libraries in pyb

# Define LEDs
b_LED = LED(4)
pot = ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout = {'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc = False, i2c_devid = 61)

oled.poweron()
oled.init_display()

# IMU connected to X9 and X10
imu = MPU6050(1,False) # Use I2C port 1 on Pyboard

def read_imu(dt):
  global g_pitch
  alpha = 0.7 # larger = longer time constant 
  pitch = imu.pitch()
  roll = imu.roll()
  gy_dot = imu.get_gy()
  gx_dot = imu.get_gx()
  g_pitch = alpha*(g_pitch + gy_dot*dt*0.001) + (1-alpha)*pitch
  #show graphics 
  oled.clear()
  oled.line(96, 26, pitch, 24, 1)
  oled.line(32, 26, g_pitch, 24, 1)
  oled.draw_text(0,0, "Raw | PITCH |")
  oled.draw_text(83,0, "filtered")
  oled.display()
  
g_pitch = 0
tic = pyb.millis()
while True:
  b_LED.toggle()
  toc = pyb.millis()
  read_imu(toc-tic)
  tic = pyb.millis()

