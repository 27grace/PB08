import pyb
from pyb import Pin, Timer, UART
from oled_938 import OLED_938  # Use various class libraries in pyb

# import Peter's packages
from motor import MOTOR 
motor = MOTOR()

# Define UART
uart = UART(6)
uart.init(9600, bits = 8, parity = None, stop = 2)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout = {'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height = 64, external_vcc = False, i2c_devid = 61)
oled.poweron()
oled.init_display()

# ------ DRIVE ------
# Changing speed of motors
def slower(change):
	global speed 
	speed = speed - change
	if speed > 0:
		forward(speed)
	elif speed < 0: # speed <=0
		backward(-speed)

def faster(change):
	global speed 
	if speed > 0:
		forward(speed+change)
	elif speed == 0:
		backward(speed-change)
	elif speed < 0: # speed <=0
		backward(-(speed-change))
	speed = abs(speed + change)

# drive functions
def forward(value):
	value = abs(value)
	motor.A_forward(value) 
	motor.B_forward(value)
	printstatus("forward " + str(value))

def backward(value):
	value = abs(value)
	motor.A_back(value) 
	motor.B_back(value)
	printstatus("backward " + str(value))

def rightturn(value):
	motor.A_back(value)
	motor.B_forward(value)
	printstatus("right " + str(value))

def leftturn(value):
	motor.A_forward(value)
	motor.B_back(value)
	printstatus("left " + str(value))

def stop():
	motor.A_stop()
	motor.B_stop()
	printstatus("stop ") 
	
def printstatus(status):
	oled.clear()
	oled.draw_text(0, 0, status)
	oled.display()

# USe keypad U, D, L, R keys to control direction
speed = 25
oled.draw_text(0, 40, "working")
oled.display()
while True:
	while (uart.any()!=10):
		pass
	command = uart.read(10)
	if (command[2]==ord('5') and command[3]==ord('1')): # U
		forward(speed)
	elif (command[2] == ord('6') and command[3]==ord('1')): # D
		backward(speed)
	elif (command[2] == ord('7') and command[3]==ord('1')): # L
		leftturn(speed)
	elif (command[2] == ord('8') and command[3]==ord('1')): # R
		rightturn(speed)
	elif (command[2] == ord('2') and command[3]==ord('1')): # 2 increase speed
		faster(5)
	elif (command[2] == ord('4') and command[3]==ord('1')): # 4 reduce speed
		slower(5)
	elif (command[2] == ord('1') and command[3]==ord('1')): # 1 stop
		stop()
	else:
		stop()
		printstatus("stationary ")
	