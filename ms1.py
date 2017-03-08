import pyb
from pyb import Pin, Timer

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP) # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP) 
B1 = Pin('X7', Pin.OUT_PP) # Control direction of motor A
B2 = Pin('X8', Pin.OUT_PP) 
PWMA = Pin('X1') # Control speed of motor A
PWMB = Pin('X2') # Control speed of motor B

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
	
def speed(value):
	motorA.pulse_width_percent(value)
	motorB.pulse_width_percent(value)

def forward(value):
	A_forward()
	B_forward()
	speed(value)

def backward(value):
	A_backward()
	B_backward()
	speed(value)
	
def stop():
	A1.low()
	A2.low()
	B1.low()
	B2.low()

forward(50)
