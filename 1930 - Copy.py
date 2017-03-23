import pyb
from pyb import Pin, Timer, ADC, DAC, LED, UART
from array import array  # need this for memory allocation to buffers
from oled_938 import OLED_938  # Use OLED display driver
import time
#  The following two lines are needed by micropython
#   ... must include if you use interrupt in your program
import micropython

micropython.alloc_emergency_exception_buf(100)

# ----- SETTING UP ------

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active


# define ports for microphone, LEDs and trigger out (X5)
mic = ADC(Pin('Y11'))
MIC_OFFSET = 1523  # ADC reading of microphone for silence
dac = pyb.DAC(1, bits=12)  # Output voltage on X5 (BNC) for debugging
b_LED = LED(4)# flash for beats on blue LED
N = 160  # size of sample buffer s_buf[]
s_buf = array('H', 0 for i in range(N))  # reserve buffer memory
ptr = 0  # sample buffer index pointer
buffer_full = False  # semaphore - ISR communicate with main program

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)  # Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
B1 = Pin('X8', Pin.OUT_PP)  # Control direction of motor A
B2 = Pin('X7', Pin.OUT_PP)
PWMA = Pin('X1')  # Control speed of motor A
PWMB = Pin('X2')  # Control speed of motor B


uart = UART(6)
uart.init(9600, bits=8, parity=None, stop=2)


# Define UART
uart = UART(6)
uart.init(9600, bits=8, parity=None, stop=2)

# Configure timer 2 to produce 1KHz clock for PWM control
tim = Timer(2, freq=1000)
motorA = tim.channel(1, Timer.PWM, pin=PWMA)
motorB = tim.channel(2, Timer.PWM, pin=PWMB)


# Setting motor direction


def A_motorspeed(value):
    if value > 0:
        A2.low()
        A1.high()
        motorA.pulse_width_percent(value)
    elif value < 0:
        A2.high()
        A1.low()
        motorA.pulse_width_percent(abs(value))
    else:
        A2.low()
        A1.low()

def B_motorspeed(value):
    if value > 0:
        B2.low()
        B1.high()
        motorB.pulse_width_percent(value)
    elif value < 0:
        B2.high()
        B1.low()
        motorB.pulse_width_percent(abs(value))
    else:
        B2.low()
        B1.low()

def motorsettings(a,b):
    A_motorspeed(a)
    B_motorspeed(b)

def anti_clockwise(a):
    if a == 1 :
        motorsettings(-25,25)
    elif a == 2:
        motorsettings(-50,50)
    elif a == 3:
        motorsettings(-75,75)
    else:
        motorsettings(-100,100)

def clockwise(a):
    if a == 1 :
        motorsettings(25,-25)
    elif a == 2:
        motorsettings(50,-50)
    elif a == 3:
        motorsettings(75,-75)
    else:
        motorsettings(100,-100)

def left_pivot(a,b): #if b is 1 anticlockwise(forward), otherwise clockwise(backward)
    if a == 1 :
        x = -25
        if b == 1:
            motorsettings(0,abs(x))
        else:
            motorsettings(0,x)
    elif a == 2:
        x = -50
        if b == 1:
            motorsettings(0, abs(x))
        else:
            motorsettings(0, x)
    elif a == 3:
        x = -75
        if b == 1:
            motorsettings(0, abs(x))
        else:
            motorsettings(0, x)
    else:
        x = -100
        if b == 1:
            motorsettings(0, abs(x))
        else:
            motorsettings(0, x)

def right_pivot(a,b):
    # if b is 1 anticlockwise(forward), otherwise clockwise(backward)
    if a == 1:
        x = -25
        if b == 1:
            motorsettings(abs(x),0)
        else:
            motorsettings(x,0)
    elif a == 2:
        x = -50
        if b == 1:
            motorsettings(abs(x),0)
        else:
            motorsettings(x,0)
    elif a == 3:
        x = -75
        if b == 1:
            motorsettings(abs(x),0)
        else:
            motorsettings(x,0)
    else:
        x = -100
        if b == 1:
            motorsettings(abs(x),0)
        else:
            motorsettings(x,0)

def pivot(direction,a,b):
    if direction == True:
        left_pivot(a,b)
    else:
        right_pivot(a,b)
    global toggle
    toggle = not toggle
        
def stop():
    motorsettings(0,0)

def twist(period,beats): #beats is the number of beats it dances for
    delay = period
    x = 0
    while x < beats/2:
        clockwise(4)
        pyb.delay(delay)
        anti_clockwise(4)
        pyb.delay(delay)
        x += 1
    #clockwise(4)
    #pyb.delay(500)
    stop()
    global toggle
    toggle = not toggle

def reverse_twist(period,beats):
    delay = period
    x = 0
    while x < beats/2:
        anti_clockwise(4)
        pyb.delay(delay)
        clockwise(4)
        pyb.delay(delay)

    stop()
    global toggle
    toggle = not toggle


def shimmy(period,beats): #beats is the number of beats it dances for
    delay = period/4.0
    delay = int(delay)
    x = 0
    while x < beats/2:
        clockwise(4)
        pyb.delay(delay)
        anti_clockwise(4)
        pyb.delay(delay)
        x += 1
    stop()
    global toggle
    toggle = not toggle

def forward_strut(period,beats):
    delay = period*2
    x = 0
    a = 1
    while x < beats/2:
        right_pivot(2,a)
        pyb.delay(delay)
        left_pivot(2,a)
        pyb.delay(delay)
        x += 1
    stop()
    global toggle
    toggle = not toggle

def backward_strut(period,beats):
    delay = period*2
    x = 0
    a = 0
    while x < beats/2:
        left_pivot(2,a)
        pyb.delay(delay)
        right_pivot(2,a)
        pyb.delay(delay)
        x += 1
    stop()
    global toggle
    toggle = not toggle

def flash():  # routine to flash blue LED when beat detected
    b_LED.on()
    pyb.delay(30)
    b_LED.off()

deadzone = 5
speed = 100



## create a list of moves 'st sh tw f b l r s' and read that list
dance_list = ['stf','stf','stf','stf','b','f','sh','f','b', 'stb' ,'stb' ,'stb' ,'stb','sh','stf','stf','stf','stf','b','f','sh','f','b', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'stf','stf','stf','stf','stf','stf','tw','stb' ,'stb' ,'stb' ,'stb','stb','stb','tw','stf','stf','stf','stf','stf','stf','tw','stb' ,'stb' ,'stb' ,'stb','stb','stb','tw',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','tw','tw','tw', 'b','f' , 'b','f' , 'b','stf','stf','sh','stf','stf','spin', 'stb' ,'stb' ,'stb' ,'stb','spin',
'stf','stf','stf','stf','b','f','sh','f','b', 'stb' ,'stb' ,'stb' ,'stb','sh','stf','stf','stf','stf','b','f','sh','f','b', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','tw','tw','tw', 'b','f' , 'b','f' , 'b','stf','stf','sh','stf','stf','spin', 'stb' ,'stb' ,'stb' ,'stb','spin',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh',
'stf','stf','stf','stf','b','f','sh','f','b', 'stb' ,'stb' ,'stb' ,'stb','sh',
'tw','f' , 'b','tw', 'f' , 'b','f','tw', 'stf','stf','stf','stf','sh', 'stb' ,'stb' ,'stb' ,'stb','sh']
def move_select():
    global count
    if count == len(dance_list):
        count = 0
    m = dance_list[count]
    if m == 'stf':
        print ('strut')
        global toggle_2
        pivot(toggle_2 , 2, 1)
        toggle_2 = not toggle_2
    if m == 'stb':
        print ('strut')
        global toggle_2
        pivot(toggle_2, 2, 0)
        toggle_2 = not toggle_2
    if m == 'sh':
        print ('shimmy')
        shimmy(580, 4)
    if m == 'tw':
        print('twist')
        twist(580, 4)
    if m == 'f':
        motorsettings(50, 50)
        global toggle
        toggle = not toggle
    if m == 'b':
        motorsettings(-50,-50)
        global toggle
        toggle = not toggle
    if m == 's':
        stop()
        global toggle
        toggle = not toggle
    if m =='spin':
        motorsettings(-75,75)
        pyb.delay(1160)
        motorsettings(75,-75)
        pyb.delay(1160)



# energy
def energy(buf):  # Compute energy of signal in buffer
    sum = 0
    for i in range(len(buf)):
        s = buf[i] - MIC_OFFSET  # adjust sample to remove dc offset
        sum = sum + s * s  # accumulate sum of energy
    return sum


# ---- The following section handles interrupts for sampling data -----
# Interrupt service routine to fill sample buffer s_buf
def isr_sampling(dummy):  # timer interrupt at 8kHz
    global ptr  # need to make ptr visible inside ISR
    global buffer_full  # need to make buffer_full inside ISR

    s_buf[ptr] = mic.read()  # take a sample every timer interrupt
    ptr += 1  # increment buffer pointer (index)
    if (ptr == N):  # wraparound ptr - goes 0 to N-1
        ptr = 0
        buffer_full = True  # set the flag (semaphore) for buffer full


# Create timer interrupt - one every 1/8000 sec or 125 usec
sample_timer = pyb.Timer(7, freq=8000)  # set timer 7 for 8kHz
sample_timer.callback(isr_sampling)  # specify interrupt service routine

# -------- End of interrupt section ----------------

# Define constants for main program loop - shown in UPPERCASE
M = 50  # number of instantaneous energy epochs to sum
BEAT_THRESHOLD = 1 # threshold for c to indicate a beat
SILENCE_THRESHOLD = 1.3  # threshold for c to indicate silence

# initialise variables for main program loop
e_ptr = 0  # pointer to energy buffer
e_buf = array('L', 0 for i in range(M))  # reserve storage for energy buffer
sum_energy = 0  # total energy in last 50 epochs
pyb.delay(100)
tic = pyb.millis()  # mark time now in msec
toggle = True
toggle_2 = True
count = 0
count_3 = 0




def threshold_setting():

    global BEAT_THRESHOLD , sum_energy , e_ptr , buffer_full

    while True:
        tic = pyb.millis()
        while (uart.any() != 10):
            if buffer_full:  # semaphore signal from ISR - set if buffer is full

                # Calculate instantaneous energy
                E = energy(s_buf)

                # compute moving sum of last 50 energy epochs
                sum_energy = sum_energy - e_buf[e_ptr] + E
                e_buf[e_ptr] = E  # over-write earlest energy with most recent
                e_ptr = (e_ptr + 1) % M  # increment e_ptr with wraparound - 0 to M-1

                # Compute ratio of instantaneous energy/average energy
                c = E * M / sum_energy
                dac.write(min(int(c * 4095 / 3), 4095))  # useful to see on scope, can remove

                time_elapsed = pyb.millis() - tic
                if (time_elapsed > 500 and c > BEAT_THRESHOLD):  # if more than 500ms since last beat
                    flash()

            pass
        command = uart.read(10)
        if command[2]==ord('5') and BEAT_THRESHOLD < 10:
            BEAT_THRESHOLD+= 0.5
            flash()
        elif command[2]==ord('6') and BEAT_THRESHOLD > 0 :
            BEAT_THRESHOLD -= 0.5
            flash()
        elif command[2] ==ord('7')and BEAT_THRESHOLD:
            BEAT_THRESHOLD -= 0.25
            flash()
        elif command[2] == ord('8') and BEAT_THRESHOLD < 10:
            BEAT_THRESHOLD += 0.25
            flash()
        elif command[2] == ord('1'):
            stop()
            main()
        elif command[2]==ord('2'):
            start_dancing()
        elif command[2]==ord('3'):
            stop()
            main()


def start_dancing():
    tic = pyb.millis()
    global BEAT_THRESHOLD, sum_energy, e_ptr , buffer_full , toggle , count, count_3

    while True:  # Main program loop
        while (uart.any() != 10):
            if buffer_full:  # semaphore signal from ISR - set if buffer is full

                # Calculate instantaneous energy
                E = energy(s_buf)

                # compute moving sum of last 50 energy epochs
                sum_energy = sum_energy - e_buf[e_ptr] + E
                e_buf[e_ptr] = E  # over-write earlest energy with most recent
                e_ptr = (e_ptr + 1) % M  # increment e_ptr with wraparound - 0 to M-1

                # Compute ratio of instantaneous energy/average energy
                c = E * M / sum_energy
                dac.write(min(int(c * 4095 / 3), 4095))  # useful to see on scope, can remove
                time_elapsed = pyb.millis() - tic
                if (time_elapsed > 500 and c > BEAT_THRESHOLD):  # if more than 500ms since last beat
                    flash()
                    print (c)
                    if toggle == True:
                        move_select()
                        toggle = not toggle
                        count += 1

                      # reset tic

                dac.write(0)
                buffer_full = False
            pass
        command = uart.read(10)

        if command[2] == ord('1'):
            stop()
            main()
        elif command[2]==ord('2'):
            start_dancing()
            break
        elif command[2]==ord('3'):
            stop()
            main()
def main():
    while True:
        while (uart.any() != 10):
            pass

        command = uart.read(10)

        if command[2] == ord('1'):
            threshold_setting()
        elif command[2] == ord('2'):
            start_dancing()
        elif command[2] == ord('3'):
            motorsettings(-50,50)
            pyb.delay(1000)
            motorsettings(50,-50)
            pyb.delay(1000)
            stop()
        elif command[2] == ord('4'):
            motorsettings(50,50)
            pyb.delay(500)
            motorsettings(-50,-50)
            pyb.delay(500)
            stop()
        

