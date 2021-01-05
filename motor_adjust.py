import motor
import sys
from time import sleep

MOTOR_PINS = [9, 18, 15, 14]
m = motor.StepperMotor(MOTOR_PINS)

STEPS = 300

m.remainingSteps = STEPS
for i in range(STEPS):
    print(i)
    m.direction = 1
    m.step()
    sleep(.05)
