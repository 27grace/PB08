from mpu6050 import MPU6050
import pyb
from pyb import Pin, Timer, ADC, DAC, LED, UART
from oled_938 import OLED_938  # Use various class libraries in pyb

# import Peter's packages
from motor import MOTOR 
motor = MOTOR()

# Define LEDs
b_LED = LED(4)
pot = ADC(Pin('X11'))
a_out = DAC(1, bits =12) 

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
# set Kp
kp = pot.read()*5.0/4095 
oled.draw_text(0, 30, 'Kp = {:5.3f}'.format(kp))
oled.display()

# IMU connected to X9 and X10
imu = MPU6050(1, False)  # Use I2C port 1 on Pyboard


# ------ DRIVE ------
# Changing speed of motors
def slower(change):
	motor.dn_Aspeed(change)
	motor.dn_Bspeed(change)

def faster(change):
	motor.up_Aspeed(change)
	motor.up_Bspeed(change)


# drive functions
def forward(value):
	motor.A_forward(value) #actually backward -.-
	motor.B_forward(value)

def backward(value):
	motor.A_back(value) # actually forward -.-
	motor.B_back(value)

def rightturn(value):
	motor.A_back(value)
	motor.B_forward(value)

def leftturn(value):
	motor.A_forward(value)
	motor.B_back(value)

def stop():
	motor.A_stop()
	motor.B_stop()

def pitch_estimate(pitch, dt, alpha):
	theta = imu.pitch()
	pitch_dot = imu.get_gy()
	pitch = alpha*(pitch+pitch_dot*dt) +(1-alpha)*theta
	return (pitch, pitch_dot)

# --------------------------- MAIN LOOP ----------------------------------
pitch = 0
alpha = 0.95  # larger = longer time constant
tic = pyb.micros()
#tic1 = pyb.millis()

	
while True:
	b_LED.toggle()
	dt = pyb.micros()-tic 
	if dt>5000:
		[pitch, pitch_dot]=pitch_estimate(pitch, dt*0.000001, alpha)
		tic = pyb.micros()
	
		#kp = 2.5
		kd = 0.33

		print(pitch, "kp", kp)
		cspeed = kp*(pitch-0.21) + kd*pitch_dot #cspeed -> correction speed
		if cspeed > 0:
			forward(cspeed+5)
		elif cspeed <0:
			backward(-(cspeed-5))
			
		#a_out.write(int(pitch*40+2048))
		a_out.write(int(pitch_dot*10+2048))