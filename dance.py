import pyb
from pyb import Pin, Timer, UART
from oled_938 import OLED_938  # Use various class libraries in pyb
import random

# ----- SETTING UP ------
# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP) # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP) 
B1 = Pin('X7', Pin.OUT_PP) # Control direction of motor A
B2 = Pin('X8', Pin.OUT_PP) 
PWMA = Pin('X1') # Control speed of motor A
PWMB = Pin('X2') # Control speed of motor B

# Define Potentiometer object as ADC conversion  on X11
pot = pyb.ADC(Pin('X11'))

# Define UART
uart = UART(6)
uart.init(9600, bits = 8, parity = None, stop = 2)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout = {'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc = False, i2c_devid = 61)
oled.poweron()
oled.init_display()

# Configure timer 2 to produce 1KHz clock for PWM control 
tim = Timer(2, freq=1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# Setting motor direction
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

# ------ DRIVE ------
# drive parameters
deadzone = 5
speed = 50

# Changing speed of motors
def speedChange(value):
	motorA.pulse_width_percent(value)
	motorB.pulse_width_percent(value)

def slower(change):
	global deadzone
	global speed
	if speed >= (change + deadzone):
		speed = speed - change

def faster(change):
	global deadzone
	global speed
	if speed <= (100 - change + deadzone):
		speed = speed + change

# drive functions
def forward(value):
	A_forward()
	B_forward()
	speedChange(value)

def backward(value):
	A_backward()
	B_backward()
	speedChange(value)

def rightturn(value):
	A_forward()
	B_backward()
	speedChange(value)

def leftturn(value):
	A_backward()
	B_forward()
	speedChange(value)

def stop():
	A1.low()
	A2.low()
	B1.low()
	B2.low()

# routine string --> dance
def dancethis(routine):
	for char in routine:
		if char.isalpha(): #if it's an alphabet
			if ord(char)==ord("u"):
				forward(speed)
			elif ord(char)==ord("d"):
				backward(speed)
			elif ord(char)==ord("r"):
				rightturn(speed)
			elif ord(char)==ord("l"):
				leftturn(speed)
			elif ord(char) == ord("s"):
				slower(5)
			elif ord(char) == ord("f"):
				faster(5)
			elif ord(char) == ord("x"):
				stop()
			else:
				stop()
		else:
			try: #changing numbers to wait time
				wait = int(char)
				time.sleep(wait)
			except:
				pass

def randomMove():
	moves = ["u", "d", "r", "l", "s"]
	dancethis(random.choice(moves))




	