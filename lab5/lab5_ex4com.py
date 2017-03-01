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

# Define pins for motor speed sensors
A_sense = Pin('Y4', Pin.PULL_NONE) # Pin.PULL_NONE = leave this as input pin
B_sense = Pin('Y6', Pin.PULL_NONE)

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

# Initialise variables
DEADZONE = 5
speed = 0
A_speed = 0
A_count = 0

#------ Section to set up interrupts ------------
def isr_motorA(dummy):
    global A_count
    A_count += 1

def isr_speed_timer(dummy):
	global A_count
	global A_speed
	A_speed = A_count
	A_count = 0

# Create external interrupts for motorA Hall effect sensor
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE, isr_motorA)

# Create timer interrupts at 100 msec intervals
speed_timer = pyb.Timer(4, freq = 10)
speed_timer.callback(isr_speed_timer)

# ------- END of interrupt Section -----------------

while True:
    # drive motor - controlled by potentiometer
    speed = int((pot.read() - 2048)*200/4096)
    if (speed >= DEADZONE):
        forward(speed)
    elif (speed <= DEADZONE):
        backward(speed)
    else:
        stop()

    # Display new speed
    oled.draw_text(0, 20, 'Motor A: {:5.2f} rps'.format(A_speed/39))
    oled.display()
