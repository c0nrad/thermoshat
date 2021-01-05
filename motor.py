import sys
import time
import RPi.GPIO as GPIO


PinMap = [[1, 0, 0, 1],
          [1, 0, 0, 0],
          [1, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 1, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 1],
          [0, 0, 0, 1]]
PinMapLength = len(PinMap)

# I think this is wrong
STEPS_PER_DEGREE = 4000/360


class StepperMotor:

    def __init__(self, pins):
        self.pins = pins
        self.direction = 2

        self.index = 0
        self.remainingSteps = 0

        self.clear()

    def step(self):

        for pin in range(0, 4):
            xpin = self.pins[pin]
            if PinMap[self.index][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        self.index += self.direction
        self.index %= PinMapLength

        self.remainingSteps -= 1

        if self.remainingSteps == 0:
            self.clear()

    def clear(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
