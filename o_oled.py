import time
from oled_938 import OLED_938	# Use OLED display driver

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64,
                   external_vcc=False, i2c_devid=61)  
				   
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'STAYING ALIVE')
def g_circ(times):
	for i in range(times):
		for r in range(32): #r represents radius
			oled.draw_circle(64, 32, r, 1)
			if (r%5 == 0):
				for n in range(r/5):
					oled.draw_circle(64, 32, r-4*n, 1)
			oled.display()
			time.sleep(0.01)
			oled.draw_circle(64, 32, r, 0)
			oled.display()
		for r in range(32): 
			if (r%5 == 0):
				for n in range(r/5):
					oled.draw_circle(64, 32, r-4*n, 0)
					oled.display()
def g_sq(times):
	for i in range(times):
		for r in range(32): #r represents radius
			oled.draw_square(64, 32, r, 1)
			try: 
				oled.draw_square(64, 32, r-1, 0)
			except:
				pass
			oled.display()
			time.sleep(0.01)
		for r in range(16): #r represents radius
			oled.draw_square(64, 32, 2*r, 0)
			oled.display()
			time.sleep(0.01)
g_sq(1)