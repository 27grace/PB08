import pyb
from pyb import Pin, Timer, ADC
from oled_938 import OLED_938 #Use OLED display driver

#Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')
B1 = Pin('X7', Pin.OUT_PP)
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')

#Configure timer 2 to produce 1 kHz clock for PWM control
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

#Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))

#I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda':'Y10', 'scl':'Y9', 'res':'Y8'}, height = 64, external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
oled.draw_text(0,0,'Lab 5 - Exercise 3a')
oled.display()

#Define pins for motor speed sensors
A_sense = Pin('Y4', Pin.PULL_NONE) #Pin.PULL_NONE = leave this as input pin
B_sense = Pin('Y6', Pin.PULL_NONE)

def A_forward(value):
    A1.low()
    A2.high()
    motorA.pulse_width_percent(value)

def A_back(value):
    A2.low()
    A1.high()
    motorA.pulse_width_percent(value)

def A_stop():
    A1.high()
    A2.high()

def B_forward(value):
    B2.low()
    B1.high()
    motorB.pulse_width_percent(value)

def B_back(value):
    B2.high()
    B1.low()
    motorB.pulse_width_percent(value)

def B_stop():
    B1.high()
    B2.high()


DEADZONE = 5
speed = 0
A_state = 0
A_speed = 0
A_count = 0

B_state = 0
B_speed = 0
B_count = 0

def isr_motorA(dummy):
    global A_count
    A_count += 1
def isr_motorB(dummy):
    global B_count
    B_count += 1
def isr_speed_timer(dummy):
    global A_count
    global A_speed
    A_speed = A_count
    A_count = 0
    global B_count
    global B_speed
    B_speed = B_count
    B_count = 0

import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt
motorA_int = ExtInt ('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorA)
motorB_int = ExtInt ('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorB)

# create timer that interrupts at 100 msec intervals
speed_timer = pyb.Timer(4, freq =10)
speed_timer.callback(isr_speed_timer)

# drive motor - controlled by potentiometer

while True:
    speed = int((pot.read() - 2048) * 200 / 4096)
    if (speed >= DEADZONE):
        A_forward(speed)
        B_forward(speed)
    elif (speed <=- DEADZONE):
        A_back(abs(speed))
        B_back(abs(speed))
    else:
        A_stop()
        B_stop()


    # Display new speed
    oled.draw_text(0, 20, 'Motor A: {:5.2f} rps'.format(A_speed / 39))
    oled.draw_text(0, 30, 'Motor B: {:5.2f} rps'.format(B_speed / 39))
    oled.display()