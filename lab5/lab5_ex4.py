# Initialise variables
DEADZONE = 5
speed = 0
A_speed = 0
A_count = 0

#------ Section to set up interrupts ------------
def isr_motorA(dummy):
    global A_count
    global A_speed
    A_speed = A_count
    A_count = 0

# Create external interrupts for motorA Hall effect sensor
import micropython
micropython.alloc.emergency_exception_buf(100)
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
        A_forward(speed)
        B_forward(speed)
    elif (speed <= DEADZONE):
        A_back(abs(speed))
        B_back(abs(speed))
    else:
        A_stop()
        B_stop()

    # Display new speed
    oled.draw_text(0, 20, 'Motor A: {:5.2f} rps'.format(A_speed/39))
    oled.display()
