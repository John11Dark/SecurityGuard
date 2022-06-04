from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
# assign buzzer pin number
buzzerPin = 17
# set GPIO Mode
GPIO.setmode(GPIO.BCM)
# set pin to out
GPIO.setup(buzzerPin, GPIO.OUT)


def buzzer(status, anErrorOccur=False, serverRunning=False):
    """_summary_

    Args:
        status (_Boll_):
        anErrorOccur (_Boll_):
        _description_
        if status == true the buzzer will turn on
        else status == False the buzzer will turn off
        if anErrorOccur == True
        buzzer will play for 1.5 seconds then go low for 0.25 seconds
        if server running == True then te buzzer will play two times to
        tell that no error occurs
        if nothing happens the buzzer will be triggered when user press on buzzer button
    """
    if not serverRunning and not anErrorOccur:
        GPIO.output(buzzerPin, status)
    elif serverRunning and status:
        GPIO.output(buzzerPin, status)
        sleep(0.5)
        GPIO.output(buzzerPin, False)
        sleep(0.25)
        GPIO.output(buzzerPin, status)
        sleep(0.5)
        GPIO.output(buzzerPin, False)
    elif anErrorOccur and status:
        GPIO.output(buzzerPin, status)
        sleep(1.5)
        GPIO.output(buzzerPin, False)
        sleep(0.25)
        GPIO.output(buzzerPin, status)
        sleep(1.5)
        GPIO.output(buzzerPin, False)
    else:
        GPIO.output(buzzerPin, False)
