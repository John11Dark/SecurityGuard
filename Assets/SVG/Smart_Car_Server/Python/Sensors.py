from time import sleep, time
import RPi.GPIO as GPIO
from Python.Motor import *
from Python.ReadVoltages import *
from Python.servo import *
from Python.Buzzer import *


class LineTracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        self.Motor = Motor()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def run(self):
        while True:
            self.LMR = 0x00
            if GPIO.input(self.IR01) == True:
                self.LMR = self.LMR | 4
            if GPIO.input(self.IR02) == True:
                self.LMR = self.LMR | 2
            if GPIO.input(self.IR03) == True:
                self.LMR = self.LMR | 1
            if self.LMR == 2:
                self.Motor.setMotorModel(-800, -800, -800, -800)
            elif self.LMR == 4:
                self.Motor.setMotorModel(1500, 1500, -2500, -2500)
            elif self.LMR == 6:
                self.Motor.setMotorModel(2000, 2000, -4000, -4000)
            elif self.LMR == 1:
                self.Motor.setMotorModel(-2500, -2500, 1500, 1500)
            elif self.LMR == 3:
                self.Motor.setMotorModel(-4000, -4000, 2000, 2000)
            elif self.LMR == 7:
                self.Motor.setMotorModel(0, 0, 0, 0)


class Light:
    def run(self):
        self.adc = Adc()
        self.PWM = Motor()
        self.PWM.setMotorModel(0, 0, 0, 0)
        while True:
            L = self.adc.recvADC(0)
            R = self.adc.recvADC(1)
            if L < 2.99 and R < 2.99:
                self.PWM.setMotorModel(-600, -600, -600, -600)

            elif abs(L - R) < 0.15:
                self.PWM.setMotorModel(0, 0, 0, 0)

            elif L > 3 or R > 3:
                if L > R:
                    self.PWM.setMotorModel(1200, 1200, -1400, -1400)

                elif R > L:
                    self.PWM.setMotorModel(-1400, -1400, 1200, 1200)


class Ultrasonic:
    def __init__(self):
        self.PWM = Motor()
        self.pwm_S = Servo()
        # set GPIO warning to false
        GPIO.setwarnings(False)
        # the sender sensor
        self.senderPin = 27
        # the receiver server Pin
        self.receiverPin = 22
        # activate the Broadcom-chip specific pin
        GPIO.setmode(GPIO.BCM)
        # set the trigger pin to send signal
        GPIO.setup(self.senderPin, GPIO.OUT)
        # set receiver signal to receive the trigger pin signal
        GPIO.setup(self.receiverPin, GPIO.IN)

    def sendSignal(self):
        # send signal
        GPIO.output(self.senderPin, True)

        # then wait for 0.15 ms to make sure that the signal has been sent out
        time.sleep(0.00015)

        # then set pin to False so it does not send another signal
        GPIO.output(self.senderPin, False)

    def receiveSignal(self, value, timeOut):
        while (GPIO.input(self.receiverPin) != value) and (timeOut > 0):
            timeOut = -1

    def getDistance(self):
        distance_cm = [0, 0, 0, 0, 0]
        for i in range(3):
            self.sendSignal()
            self.receiveSignal(True, 10000)
            startTime = time.time()
            self.receiveSignal(False, 10000)
            finishTime = time.time()
            pulseLen = finishTime - startTime
            distance_cm[i] = pulseLen / 0.000058
        distance_cm = sorted(distance_cm)
        return int(distance_cm[2])
