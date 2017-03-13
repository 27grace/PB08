import pyb
from pyb import Pin, Timer, ADC, DAC, LED
from array import array
from oled_938 import OLED_938	# Use OLED display driver

#  The next two lines are needed by micropython to catch errors
import micropython
micropython.alloc_emergency_exception_buf(100)

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Beat Detection')
oled.display()

# define LED
led = pyb.LED(1) # red one on pyBench

# define ports for microphone in and trigger out
mic = ADC(Pin('Y11'))
trigger = Pin('X5',Pin.OUT_PP)

# define parameters
N = 160				# size of sample buffer in 20ms where fs = 8000 Hz
s_buf = array('H', 0 for i in range(N))  # reserve buffer memory
N_ave = 50			# size of average energy
E_buf = array('L', 0 for i in range(N_ave))  # reserve buffer energy memory
global ptr #pointer
global buffer_full
ptr = 0				# buffer index
insta_E = 0 		#intantaneous energy
E_ptr = 0 			# energy buffer index
buffer_full = False	# semaphore - ISR communicate with main program
ave_E = 0	# average energy
threshold = 2.5 # threshold ratio (=instantaneous energy/average energy)
tic = 0 # initialising tic

# Interrupt service routine to fill sample buffer s_buf
def isr_sampling(dummy): 	# timer interrupt at 8kHz
	global ptr				# need to make ptr visible in here
	global buffer_full	# need to make buffer_filled visible in here
	global insta_E
	sig = mic.read()
	s_buf[ptr] = sig	# take a sample every timer interrupt
	insta_E = insta_E + sig*sig
	ptr += 1
	if (ptr == N):
		ptr = 0
		buffer_full = True

# Create timer interrupt - one every 1/8000 sec or 125 usec
timer = pyb.Timer(7, freq=8000)
timer.callback(isr_sampling)

while True:
	if buffer_full:		# semaphore signal from ISR to say buffer full
		# plot_sig(s_buf,'Hello World!')
		E_buf[E_ptr]=insta_E
		insta_E = 0
		E_ptr += 1
		toc = pyb.millis()
		time_elapsed = toc-tic
		print("time", time_elapsed)
		# calculating ave energy after E_buf is full
		if (E_ptr == N_ave):
			E_ptr = 0
			for e in E_buf:
				ave_E = (ave_E + e) / N_ave

		# taking into consideration time_elapsed
		if time_elapsed > 800:
			led.on()
			print("beat")
			tic = pyb.millis()
		elif time_elapsed >500:
			# detecting energy over threshold using blinker
			if ((insta_E/ave_E)> threshold):
				led.on()
				print("beat")
				tic = pyb.millis()
			else:
				led.off()

		buffer_full = False


