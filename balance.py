'''
-----------------------------------------------------------
Name: Lab 4 Exercise 5
-----------------------------------------------------------
Draw Pendulum reflecting pitch angles (raw and filtered)
-----------------------------------------------------------
'''
from mpu6050 import MPU6050
import pyb
from pyb import Pin, Timer, ADC, DAC, LED, UART
from oled_938 import OLED_938  # Use various class libraries in pyb

# Define LEDs
b_LED = LED(4)
pot = ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=61)

oled.poweron()
oled.init_display()

# IMU connected to X9 and X10
imu = MPU6050(1, False)  # Use I2C port 1 on Pyboard

# ----- SETTING UP ------

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)  # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
B1 = Pin('X7', Pin.OUT_PP)  # Control direction of motor A
B2 = Pin('X8', Pin.OUT_PP)
PWMA = Pin('X1')  # Control speed of motor A
PWMB = Pin('X2')  # Control speed of motor B
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
speed = 100


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


def read_imu(dt):
    global g_pitch
    alpha = 0.7  # larger = longer time constant
    pitch = imu.pitch()
    roll = imu.roll()
    gy_dot = imu.get_gy()
    gx_dot = imu.get_gx()
    g_pitch = alpha * (g_pitch + gy_dot * dt * 0.001) + (1 - alpha) * pitch
    # show graphics
    oled.clear()
    oled.line(96, 26, pitch, 24, 1)
    oled.line(32, 26, g_pitch, 24, 1)
    print("g_pitch", g_pitch)
    oled.draw_text(0, 0, "Raw | PITCH |")
    oled.draw_text(83, 0, "filtered")
    oled.display()
    corrections = 0
    if g_pitch > 0.5:
        corrections = (g_pitch / 1) * 100
        forward(corrections)
        print("correcting f")
    if g_pitch < -0.5:
        corrections = (abs(g_pitch)/ 1) * 100
        backward(corrections)
        print("correcting b")

g_pitch = 0
tic = pyb.millis()
while True:
    #backward(100)
    b_LED.toggle()
    toc = pyb.millis()
    read_imu(toc - tic)
    tic = pyb.millis()
