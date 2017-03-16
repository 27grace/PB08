import pyb
from pyb import Pin, Timer

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP) # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1') # Control speed of motor A

def A_forward(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

A_forward(0)
sys.exit()