from datetime import datetime
from mpu6050 import mpu6050
from time import sleep
import math
import display
import metrics
import motor

TEMP_BUFFER_SIZE = 10
ANGLE_BUFFER_SIZE = 10
MOTOR_PINS = [9, 18, 15, 14]

ANGLE_RANGE = 50

DAY_TARGET_TEMPERATURE = 74
NIGHT_TARGET_TEMPERATURE = 50

MIN_ANGLE_DEGREE = 180+ANGLE_RANGE
MAX_ANGLE_DEGREE = 180-ANGLE_RANGE

ANGLE_CHANGE = 15

TEMP_OFFSET = 5


class Thermostat:

    def __init__(self):
        self.mpu6050_sensor = mpu6050(0x68)

        self.tmp_buffer = [self.get_temp_raw()
                           for _ in range(TEMP_BUFFER_SIZE)]
        self.angle_buffer = [self.get_angle_raw()
                             for _ in range(ANGLE_BUFFER_SIZE)]

        self.motor = motor.StepperMotor(MOTOR_PINS)

    def get_target_temperature(self):
        now = datetime.utcnow()
        print(now)
        if now.hour > 3 and now.hour < 11:  # UTC time, 10pm->6am est
            return NIGHT_TARGET_TEMPERATURE
        return DAY_TARGET_TEMPERATURE

    def get_accel(self):
        return self.mpu6050_sensor.get_accel_data()

    def get_temp(self):
        self.tmp_buffer = self.tmp_buffer[1:]
        self.tmp_buffer.append(self.get_temp_raw())
        return sum(self.tmp_buffer)/len(self.tmp_buffer)

    def get_temp_raw(self):
        return CtoF(self.mpu6050_sensor.get_temp()) - 5

    def get_angle(self):
        angle = self.get_angle_raw()

        self.angle_buffer = self.angle_buffer[1:]
        self.angle_buffer.append(angle)

        return sum(self.angle_buffer) / len(self.angle_buffer)

    def get_angle_raw(self):
        current_accelerometer_data = self.get_accel()
        return ((math.atan2(
            -current_accelerometer_data["y"], -current_accelerometer_data["z"]) + math.pi) * 180 / math.pi)

    def loop(self):
        i = -1
        temp = round(self.get_temp())

        while True:
            sleep(.001)
            i += 1

            if i % 100 == 0:
                # Update buffers
                self.get_angle()
                temp = self.get_temp()

            display.display(str(temp).ljust(4))

            if i % 10 == 0:
                if self.motor.remainingSteps > 0:
                    self.motor.step()

            #     temp = round(self.get_temp())
            #     print("Temp", temp)
            #     print("Angle", self.get_angle())

            if i % 10000 == 0:
                metrics.save_metric("temperature", self.get_temp())
                metrics.save_metric("angle", self.get_angle())

            if i % 200000 == 0:
                print("[+] i=%d, Temp=%d, Angle=%d, Stepper=%d" %
                      (i, temp, self.get_angle(), self.motor.remainingSteps))
                print(self.tmp_buffer, self.angle_buffer)

                target_temperature = self.get_target_temperature()
                print("[+] Target Temperature", target_temperature)

                if temp < target_temperature:
                    print("[-] Temp below target")
                    if self.get_angle() < MAX_ANGLE_DEGREE:
                        print("[***] Already max angle")
                        continue

                    self.motor.direction = -1
                    self.motor.remainingSteps = round(
                        ANGLE_CHANGE * motor.STEPS_PER_DEGREE)
                    print("[-] Adding motorSteps=%d" %
                          self.motor.remainingSteps)

                if temp > target_temperature:
                    print("[-] Temp above target")
                    if self.get_angle() > MIN_ANGLE_DEGREE:
                        print("[***] Already min angle")
                        continue

                    self.motor.direction = 1
                    self.motor.remainingSteps = round(
                        ANGLE_CHANGE * motor.STEPS_PER_DEGREE)
                    print("[-] Adding motorSteps=%d" %
                          self.motor.remainingSteps)


def CtoF(c):
    return (c * 9/5) + 32


def calculate_accel_difference(initial, current):
    return {"x": initial["x"] - current["x"], "y": initial["y"] - current["y"], "z": initial["z"] - current["z"]}


if __name__ == "__main__":

    w = Thermostat()
    w.loop()
