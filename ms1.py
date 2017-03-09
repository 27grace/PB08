import pyb
from pyb import Pin, Timer, UART
from oled_938 import OLED_938  # Use various class libraries in pyb

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP) # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP) 
B1 = Pin('X7', Pin.OUT_PP) # Control direction of motor A
B2 = Pin('X8', Pin.OUT_PP) 
PWMA = Pin('X1') # Control speed of motor A
PWMB = Pin('X2') # Control speed of motor B

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

# USe keypad U, D, L, R keys to control direction
DEADZONE = 5
speed = 50
status = ""
oled.draw_text(0, 40, "working")
oled.display()
while True:
	while (uart.any()!=10):
		pass
	command = uart.read(10)
	if (command[2]==ord('5') and command[3]==ord('1')): # U
		forward(speed)
		status = "forward"
	elif (command[2] == ord('6') and command[3]==ord('1')): # D
		backward(speed)
		status = "backward"
	elif (command[2] == ord('7') and command[3]==ord('1')): # L
		leftturn(speed)
		status = "leftturn"
	elif (command[2] == ord('8') and command[3]==ord('1')): # R
		rightturn(speed)
		status = "rightturn"
	else:
		stop()
		status = "stationary"
	status = status + " speed:" + str(speed)
	oled.draw_text(0, 40, status)
	oled.display()
	