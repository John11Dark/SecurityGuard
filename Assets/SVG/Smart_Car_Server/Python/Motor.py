from Python.PCA9685 import PCA9685


class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)

    def duty_range(self, wheelOne, wheelTwo, wheelThree, wheelFour):
        if wheelOne > 4095:
            wheelOne = 4095
        elif wheelOne < -4095:
            wheelOne = -4095

        if wheelTwo > 4095:
            wheelTwo = 4095
        elif wheelTwo < -4095:
            wheelTwo = -4095

        if wheelThree > 4095:
            wheelThree = 4095
        elif wheelThree < -4095:
            wheelThree = -4095

        if wheelFour > 4095:
            wheelFour = 4095
        elif wheelFour < -4095:
            wheelFour = -4095
        return wheelOne, wheelTwo, wheelThree, wheelFour

    def leftUpperWheel(self, wheel):
        if wheel > 0:
            self.pwm.setMotorPwm(0, 0)
            self.pwm.setMotorPwm(1, wheel)
        elif wheel < 0:
            self.pwm.setMotorPwm(1, 0)
            self.pwm.setMotorPwm(0, abs(wheel))
        else:
            self.pwm.setMotorPwm(0, 4095)
            self.pwm.setMotorPwm(1, 4095)

    def leftLowerWheel(self, wheel):
        if wheel > 0:
            self.pwm.setMotorPwm(3, 0)
            self.pwm.setMotorPwm(2, wheel)
        elif wheel < 0:
            self.pwm.setMotorPwm(2, 0)
            self.pwm.setMotorPwm(3, abs(wheel))
        else:
            self.pwm.setMotorPwm(2, 4095)
            self.pwm.setMotorPwm(3, 4095)

    def rightUpperWheel(self, wheel):
        if wheel > 0:
            self.pwm.setMotorPwm(6, 0)
            self.pwm.setMotorPwm(7, wheel)
        elif wheel < 0:
            self.pwm.setMotorPwm(7, 0)
            self.pwm.setMotorPwm(6, abs(wheel))
        else:
            self.pwm.setMotorPwm(6, 4095)
            self.pwm.setMotorPwm(7, 4095)

    def rightLowerWheel(self, wheel):
        if wheel > 0:
            self.pwm.setMotorPwm(4, 0)
            self.pwm.setMotorPwm(5, wheel)
        elif wheel < 0:
            self.pwm.setMotorPwm(5, 0)
            self.pwm.setMotorPwm(4, abs(wheel))
        else:
            self.pwm.setMotorPwm(4, 4095)
            self.pwm.setMotorPwm(5, 4095)

    def setMotorModel(self, wheelOne, wheelTwo, wheelThree, wheelFour):
        wheelOne, wheelTwo, wheelThree, wheelFour = self.duty_range(
            wheelOne, wheelTwo, wheelThree, wheelFour
        )
        self.leftUpperWheel(wheelOne)
        self.leftLowerWheel(wheelTwo)
        self.rightUpperWheel(wheelThree)
        self.rightLowerWheel(wheelFour)
