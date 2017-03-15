#!/usr/bin/python

class motorDrives:
    def __init__(self, state, speed):
        self.A1 = Pin('X3', Pin.OUT_PP)  # Control direction of motor A
        self.A2 = Pin('X4', Pin.OUT_PP)
        self.B1 = Pin('X7', Pin.OUT_PP)  # Control direction of motor A
        self.B2 = Pin('X8', Pin.OUT_PP)
        self.PWMA = Pin('X1')  # Control speed of motor A
        self.PWMB = Pin('X2')  # Control speed of motor B

    def A_forward(self):
        self.A1.low()
        self.A2.high()

    def A_backward(self):
        self.A1.high()
        self.A2.low()

    def B_backward(self):
        self.B1.low()
        self.B2.high()

    def B_forward(self):
        self.B1.high()
        self.B2.low()

    # drive functions
    def forward(self, value):
        self.A_forward()
        self.B_forward()
        self.speedChange(value)

    def backward(self, value):
        self.A_backward()
        self.B_backward()
        self.speedChange(value)

    def rightturn(self, value):
        self.A_forward()
        self.B_backward()
        self.speedChange(value)

    def leftturn(self, value):
        self.A_backward()
        self.B_forward()
        self.speedChange(value)

    def stop(self):
        self.A1.low()
        self.A2.low()
        self.B1.low()
        self.B2.low()

class PB08:
    def __init__(self, state, speed):
        self.state = state
        self.speed = speed

    def backward(self, value):
        motorDrives.backward(value)
        self.state = "backward"
        self.speed = value

    def rightturn(self, value):
        motorDrives.rightturn(value)
        self.state = "right turn"
        self.speed = value

    def leftturn(self, value):
        motorDrives.leftturn(value)
        self.state = "left turn"
        self.speed = value

    def stop(self):
        motorDrives.stop()
        self.state = "stop"
        self.speed = 0
