import pyb
from pyb import Pin, Timer
from oled_938 import OLED_938  # Use various class libraries in pyb

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP) # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP) 
B1 = Pin('X7', Pin.OUT_PP) # Control direction of motor A
B2 = Pin('X8', Pin.OUT_PP) 
PWMA = Pin('X1') # Control speed of motor A
PWMB = Pin('X2') # Control speed of motor B

# Define Potentiometer object as ADC conversion  on X11
pot = pyb.ADC(Pin('X11'))

# Configure timer 2 to produce 1KHz clock for PWM control 
tim = Timer(2, freq=1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

def A_forward():
	A1.low()
	A2.high()
	
def A_backward():
	A1.high()
	A2.low()
	
def B_backward():
	B1.low()
	B2.high()

def B_forward():
	B1.high()
	B2.low()
	
def speedChange(value):
	motorA.pulse_width_percent(value)
	motorB.pulse_width_percent(value)

def forward(value):
	A_forward()
	B_forward()
	speedChange(value)

def backward(value):
	A_backward()
	B_backward()
	speedChange(value)
	
def stop():
	A1.low()
	A2.low()
	B1.low()
	B2.low()
	
# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout = {'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc = False, i2c_devid = 61)
oled.poweron()
oled.init_display()

DEADZONE = 5
while True:
	value = pot.read() # value = 0 to 4095 for voltage 0v to 3.3v
	speed = int((pot.read()-2048)*200/4096)
	oled.draw_text(0, 40, 'Motor Drive:{:5d}%'.format(speed))
	oled.display()
	if (speed >= DEADZONE):
		forward(speed)
	elif (speed <= DEADZONE):
		backward(abs(speed))
	else:
		stop()