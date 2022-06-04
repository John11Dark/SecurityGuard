from socket import timeout
from time import sleep, time
import RPi.GPIO as GPIO
from Python.Motor import *
from Python.ReadVoltages import *
from Python.servo import *
from Python.Buzzer import *


class Ultrasonic:
    def __init__(self):
        # set GPIO warning to false
        GPIO.setwarnings(False)
        # the sender sensor
        self.senderPin = 27
        # the receiver server Pin
        self.receiverPin = 22
        #
        self.Servo = Servo()
        #
        self.Motor = Motor()

        # activate the Broadcom-chip specific pin
        GPIO.setmode(GPIO.BCM)
        # set the trigger pin to send signal
        GPIO.setup(self.senderPin, GPIO.OUT)
        # set receiver signal to receive the trigger pin signal
        GPIO.setup(self.receiverPin, GPIO.IN)

    def sendSignal(self):
        # send signal
        GPIO.output(self.senderPin, True)

        # then wait for 0.5 ms to make sure that the signal has been sent out
        sleep(0.00015)
        # then set pin to False so it does not send another signal
        GPIO.output(self.senderPin, False)

    def receiveSignal(self, value, timeOut):
        count = timeOut
        while (GPIO.input(self.receiverPin) != value) and (count > 0):
            timeOut = count -1

    def getDistance(self):
        distanceCM = [0, 0, 0, 0, 0]
        for i in range(3):
            self.sendSignal()
            self.receiveSignal(True, 10000)
            startTime = time.time()
            self.receiveSignal(False, 10000)
            finishTime = time.time()
            pulseLen = finishTime - startTime
            distanceCM[i] = pulseLen / 0.000058

        distanceCM = sorted(distanceCM)
        return int(distanceCM[2])

    def runMotor(self, L, M, R):
        if (L < 30 and M < 30 and R < 30) or M < 30:
            self.Motor.setMotorModel(-1450, -1450, -1450, -1450)
            sleep(0.1)
            if L < R:
                self.Motor.setMotorModel(1450, 1450, -1450, -1450)
            else:
                self.Motor.setMotorModel(-1450, -1450, 1450, 1450)
        elif L < 30 and M < 30:
            self.Motor.setMotorModel(1500, 1500, -1500, -1500)
        elif R < 30 and M < 30:
            self.Motor.setMotorModel(-1500, -1500, 1500, 1500)
        elif L < 20:
            self.Motor.setMotorModel(2000, 2000, -500, -500)
            if L < 10:
                self.Motor.setMotorModel(1500, 1500, -1000, -1000)
        elif R < 20:
            self.Motor.setMotorModel(-500, -500, 2000, 2000)
            if R < 10:
                self.Motor.setMotorModel(-1500, -1500, 1500, 1500)
        else:
            self.Motor.setMotorModel(600, 600, 600, 600)

    def run(self):
        for i in range(30, 151, 60):
            self.Servo.setServoPwm("0", i)
            sleep(0.2)
            if i == 30:
                L = self.getDistance()
            elif i == 90:
                M = self.getDistance()
            else:
                R = self.getDistance()
        while True:
            for i in range(90, 30, -60):
                self.Servo.setServoPwm("0", i)
                sleep(0.2)
                if i == 30:
                    L = self.getDistance()
                elif i == 90:
                    M = self.getDistance()
                else:
                    R = self.getDistance()
                self.run_motor(L, M, R)
            for i in range(30, 151, 60):
                self.Servo.setServoPwm("0", i)
                sleep(0.5)
                if i == 30:
                    L = self.getDistance()
                    if L < 10:
                        buzzer(True)
                        sleep(1)
                        buzzer(False)
                elif i == 90:
                    M = self.getDistance()
                    if M < 10:
                        buzzer(True)
                        sleep(1)
                        buzzer(False)

                else:
                    R = self.getDistance()
                    if R < 10:
                        buzzer(True)
                        sleep(1)
                        buzzer(False)
                self.runMotor(L, M, R)
