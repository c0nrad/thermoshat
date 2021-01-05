import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

components = [7, 25, 10, 17, 4, 8, 22, 21]
controls = [24, 23]

for component in components:
    GPIO.setup(component, GPIO.OUT)
    GPIO.output(component, 0)

for control in controls:
    GPIO.setup(control, GPIO.OUT)
    GPIO.output(control, 1)

digitComponentMap = {' ': (0, 0, 0, 0, 0, 0, 0),
                     '0': (1, 1, 1, 1, 1, 1, 0),
                     '1': (0, 1, 1, 0, 0, 0, 0),
                     '2': (1, 1, 0, 1, 1, 0, 1),
                     '3': (1, 1, 1, 1, 0, 0, 1),
                     '4': (0, 1, 1, 0, 0, 1, 1),
                     '5': (1, 0, 1, 1, 0, 1, 1),
                     '6': (1, 0, 1, 1, 1, 1, 1),
                     '7': (1, 1, 1, 0, 0, 0, 0),
                     '8': (1, 1, 1, 1, 1, 1, 1),
                     '9': (1, 1, 1, 1, 0, 1, 1)}


def display(s):
    for control in range(2):
        for loop in range(0, 7):
            GPIO.output(components[loop],
                        digitComponentMap[s[control]][loop])
        GPIO.output(controls[control], 0)
        time.sleep(0.001)
        GPIO.output(controls[control], 1)
