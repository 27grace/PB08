'''    Start of comment section
-------------------------------------------------------
Name: Basic Beat Detection implementation using microphone class
Creator:  Peter YK Cheung
Date:   16 March 2017
Revision:  1.5
-------------------------------------------------------
'''    
import pyb
from pyb import Pin, Timer, ADC, DAC, LED
from array import array			# need this for memory allocation to buffers
from oled_938 import OLED_938	# Use OLED display driver
import time
from mic import MICROPHONE
from motor import MOTOR
from mpu6050 import MPU6050
import pyb
from pyb import Pin, Timer, ADC, DAC, LED, UART
from oled_938 import OLED_938  # Use various class libraries in pyb

# ------------------ DEFINE PARAMETERS ------------------------
#  The following two lines are needed by micropython 
#   ... must include if you use interrupt in your program
import micropython
micropython.alloc_emergency_exception_buf(100)

# Define LEDs
b_LED = LED(4)
pot = ADC(Pin('X11'))
a_out = DAC(1, bits =12) 

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)  
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'STAYING ALIVE')
oled.display()

# Create microphone object
SAMP_FREQ = 8000
N = 160
mic = MICROPHONE(Timer(7,freq=SAMP_FREQ),ADC('Y11'),N)

# Create motor object 
motor = MOTOR()

# Define constants for main program loop - shown in UPPERCASE
M = 50						# number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 2.0		# threshold for c to indicate a beat

# initialise variables for main program loop 
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))	# reserve storage for energy buffer
sum_energy = 0				# total energy in last 50 epochs
pyb.delay(100)
tic_beat = pyb.millis()			# mark time now in msec

# IMU connected to X9 and X10
imu = MPU6050(1, False)  # Use I2C port 1 on Pyboard

# ------------------------ FUNCTIONS ---------------------------
# ------ DRIVE ------
# Changing speed of motors functions
def slower(change):
	motor.dn_Aspeed(change)
	motor.dn_Bspeed(change)

def faster(change):
	motor.up_Aspeed(change)
	motor.up_Bspeed(change)

# drive functions
def forward(value):
	motor.A_forward(value) 
	motor.B_forward(value)

def backward(value):
	motor.A_back(value) 
	motor.B_back(value)

def rightturn(value):
	motor.A_back(100)
	motor.B_forward(100)

def leftturn(value):
	motor.A_forward(100)
	motor.B_back(100)

def stop():
	motor.A_stop()
	motor.B_stop()

def pitch_estimate(pitch, dt, alpha):
	theta = imu.pitch()
	pitch_dot = imu.get_gy()
	pitch = alpha*(pitch+pitch_dot*dt) +(1-alpha)*theta
	return (pitch, pitch_dot)

# -------- DANCE ----------
speed = 100 # dance speed

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
				slower(10)
			elif ord(char) == ord("f"):
				faster(10)
			elif ord(char) == ord("x"):
				stop()
			else:
				stop()
		else:
			try: #changing numbers to wait time
				wait = int(char)/10
				time.sleep(wait)
				print("delay")
			except:
				pass

def randomMove():
	randno = pyb.rng()%4
	if randno==0:
		dancethis("r1l1r1l1x") 
	elif randno==1:
		backward(speed)
		time.sleep(0.1)
		stop()
	elif randno==2:
		forward(speed)
		time.sleep(0.1)
		stop()
	elif randno==3:
		dancethis("r1l1r1l1x")
		stop()

# ------ BALANCE ------
def pitch_estimate(pitch, dt, alpha):
	theta = imu.pitch()
	pitch_dot = imu.get_gy()
	pitch = alpha*(pitch+pitch_dot*dt) +(1-alpha)*theta
	return (pitch, pitch_dot)

# --------------------------- MAIN LOOP ----------------------------------
# real-time program loop, variables are initialised above
while True:				# Main program loop
	if mic.buffer_full():		# semaphore signal from ISR - set if buffer is full
		b_LED.off()				# flash off
		# Get instantaneous energy
		E = mic.inst_energy()
		
		# compute moving sum of last 50 energy epochs
		sum_energy = sum_energy - e_buf[e_ptr] + E
		e_buf[e_ptr] = E		# over-write earlest energy with most recent
		e_ptr = (e_ptr + 1) % M	# increment e_ptr with wraparound - 0 to M-1
		
		# Compute ratio of instantaneous energy/average energy
		c = E*M/sum_energy
		
		# Look for a beat	
		time_elapsed = pyb.millis()-tic_beat
		if (time_elapsed > 400):	# if more than 400ms since last beat
			if (c>BEAT_THRESHOLD):		# look for a beat
				tic = pyb.millis()		# reset tic
				b_LED.on()				# beat found, flash blue LED ON
				randomMove()
			elif (time_elapsed > 600):
				tic_beat = pyb.millis()		# reset tic
				b_LED.on()
				randomMove()
		mic.set_buffer_empty()			# reset the buffer_full flag
	