# dependencies module
from crypt import methods
import inspect, ctypes, os, socket
from logging import shutdown
import cv2 as CV
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, make_response, jsonify
from random import randint as rand
from flask_socketio import SocketIO, emit
from time import sleep
from datetime import datetime
from newstream import Camera as cam


# modules I have created
from Python.Sensors import *
from Python.sendEmail import sendMail
from Python.ReadVoltages import Adc
from Python.Buzzer import buzzer
from Python.Ultrasonic import Ultrasonic as lt

# Freenove modules but i modified them more explanation are givin on week Five
# https://securityguardjohnmuller.netlify.app/#weekNumFive
# the original  code is on
# https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi
from Python.Motor import Motor
from Python.servo import Servo
from Python.led import Led
from Python.Video import VideoStreaming

# create new instance of modules
wheelMotor = Motor()
servoMotor = Servo()
lineTracking = LineTracking()
lightTracking = Light()
batteryInfo = Adc()
newLed = Led()
lightTracking = Light()
ultrasonicSensor = Ultrasonic()
newLineTracking = LineTracking()
videoCapture = CV.VideoCapture(0)
newUltraSonic = lt

# get environment variables
load_dotenv()
serverEmail = os.getenv("ADMIN_EMAIL")
serverPassword = os.getenv("ADMIN_PASSWORD")

# initial and declare variables
maxServoValue = 180
minServoValue = 0
userName = None
serverThreads = []
LEDsThreads = []
sensorsThreads = []
socketConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketConnection.connect(("1.1.1.1", 0))
IPAddress = socketConnection.getsockname()[0]
receiverEmailAddress = "Godsaveme2001@gmail.com"


# this this variable changes when the page loads first time and send an email before its status changes
# the reason if it so it send an email when the server starts but not on every re/load
serverHasStarted = os.getenv("serverHasStarted")
pageAlreadyAccessedStarted = os.getenv("pageAlreadyAccessedStarted")
objectsDistance = 0
rightSensorReadings = 0
leftSensorReadings = 0
# get current time for email status
currentTime = datetime.now().strftime("%H:%M:%S")
currentDate = datetime.now().date()


def Color(red, green, blue, white=0):
    """_summary_

    this function Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    Args:
        red (_int_): _description_ RGB color value between 0 and 255
        green (_int_): _description_ RGB color value between 0 and 255
        blue (_int_): _description_. RGB color value between 0 and 255
        white (int, optional): _description_. Defaults to 0.

    Returns:
        _int_: _description_. it returns 24 bit color value
    """
    return (white << 24) | (red << 16) | (green << 8) | blue


def asyncRaise(thread, executeType):
    """_summary_
    this function destroy the thread given thread id if the executeType == system exit
    Args:
        thread (_integer_): _description_
        the thread initialized id thread.ident
        executeType (_object_): _description_
        SystemExit specifies what to do with the the thread

    Raises:
        ValueError: _description_
        SystemError: _description_
    """

    threadIndent = ctypes.c_long(thread)
    if not inspect.isclass(executeType):
        executeType = type(executeType)
    result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        threadIndent, ctypes.py_object(executeType)
    )
    if result == 0:
        raise ValueError("invalid thread id")
    elif result != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(threadIndent, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def killThread(Threads):
    """_summary_
    this function kills the given thread(s)
    and removes it from the given list
    Args:
        Threads (_list_): _description_
        get an array of threads
    """
    if len(Threads) != 0:
        for thread in Threads:
            try:
                asyncRaise(thread.ident, SystemExit)
                Threads.remove(thread)
                print(f"{thread} has been stopped")  # for testing purposes
            except ValueError as error:
                print(f"an error occur : \n{error}")


def getTemperature():
    """_summary_
    this function gets CPU readings from the terminal and formats it to
    get only the float number and returns it

    Returns:
        _float_: _description_
        returns CPU Temperature as a float type
    """
    # Read data from Raspberry Pi (specifically read CPU temperature)
    temperature = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return format(temperature[5:-3])




def getBatteryPercentage():
    """_summary_
    this function get voltages readings and converts it to percentage and returns it as integer value
    Returns:
        _int_: _description_
        returns Battery Percentage as an integer
    """
    batteryValue = batteryInfo.recvADC(2)
    batteryValue = batteryValue / 1.4 * 30
    print(batteryValue)
    return int(batteryValue)


def colorAnimation(MODE="string"):
    """_summary_
    this is a while True function gets executed in the background by calling it via
    thread it plays a random LEDs animation

    ____used like____
    calling it inside thread as [ <MODE>Animation = Thread(target=colorAnimation, args("MODE=<MODE>",)) ]
    then start it when needed as <MODE>Animation.start()

    Args:
        MODE (_str_): _description_
        ___Available MODEs___
        MODE == "RGB" it plays RGB animations
        MODE == "Random" it plays RGB animations
        MODE == "Cycle" it plays RGB animations
        MODE == "Animation" it plays RGB animations
        MODE == "Rainbow" it plays RGB animations
    """
    if MODE == "RGB":
        while True:
            newLed.customRGB(newLed.strip)
    elif MODE == "Random":
        while True:
            newLed.rainbowCycle(newLed.strip)
    elif MODE == "Cycle":
        while True:
            newLed.customRandomAnimation(newLed.strip)
    elif MODE == "Rainbow":
        while True:
            newLed.rainbow(newLed.strip)
    elif MODE == "Animation":
        while True:
            newLed.theaterChaseRainbow(newLed.strip)
    else:
        # the below function just for good practice code
        print("not supported mode")
        return None


def ultrasonicBackground():
    """_summary_
    this is a while True function gets execute in the background by calling it via
    thread
    it gets objects distance reading and stores it in a global variables

    ____like____
    calling it inside thread as [ ultrasonicThread = Thread(target=ultrasonicBackground) ]
    then start it when needed as ultrasonicThread.start()
    """
    global objectsDistance
    while True:
        objectsDistance = ultrasonicSensor.getDistance()
        sleep(0.5)

# declare a thread and append it to threads list 
ultrasonicThread = Thread(target=ultrasonicBackground)
serverThreads.append(ultrasonicThread)
sensorsThreads.append(ultrasonicThread)



def lightSensorReadingsBackground():
    """_summary_
    this is a while True function gets execute in the background by calling it via
    thread
    it gets left and right sensor reading and stores it in a global variables

    ____like____
    calling it inside thread as [ lightSensorsThread = Thread(target=lightSensorReadingsBackground) ]
    then start it when needed as lightSensorsThread.start()
    """
    global leftSensorReadings
    global rightSensorReadings
    while True:
        leftSensorReadings = batteryInfo.recvPCF8591(0)
        rightSensorReadings = batteryInfo.recvPCF8591(2)
        sleep(0.5)
        # print(leftSensorReadings, rightSensorReadings) # for testing purposes

# declare a thread and append it to threads list 
lightSensorsThread = Thread(target=lightSensorReadingsBackground)
serverThreads.append(lightSensorsThread)
sensorsThreads.append(lightSensorsThread)


# destroy all components and send an email
def destroy(Error, shutDown=False):
    """_summary_

    Args:
        Error (_String/None_): _description_
        this function makes sure that the server closed correctly and all
        components and threads are set to their default values and send an email that server
        has closed manually if Error parameter has value will change such as error exception
        the subject and body of the email will change
        other wise if Error is set to None the default email will be sent
    """
    # send an email that says server is down
    isAnErrorOccur = Error != None
    if isAnErrorOccur:
        messageSubject = "an error occur"
        messageBody = f"unexpected error occur cause the server to shutdown at {currentTime}\nThe error was\n{Error}"
    else:
        messageSubject = "Server went down"
        messageBody = (
            f"server shutdown manually at {currentTime} all looks good!{Error}"
        )

    # send email with server status
    sendMail(
        subject=messageSubject,
        receiver=receiverEmailAddress,
        body=messageBody,
        email=serverEmail,
        password=serverPassword,
    )

    # wait two 1 after email has
    sleep(1)
    # Stop all wheels
    wheelMotor.setMotorModel(0, 0, 0, 0)

    # set servo motor one(1) Left right to center
    servoOneUpDownCurrentValue = 90
    servoMotor.setServoPwm("1", servoOneUpDownCurrentValue)

    # set servo motor Zero(0) Left right to center
    servoZeroRightLeftCurrentValue = 90
    servoMotor.setServoPwm("0", servoZeroRightLeftCurrentValue)

    # turn buzzer off
    buzzer(False, False, False)
    # make sure that the enviorment varibles are set to defults value
    os.environ["pageAlreadyAccessedStarted"] = "False"
    os.environ["serverHasStarted"] = "False"
    # destroy / turn off the LEDs
    newLed.colorWipe(newLed.strip, Color(0, 0, 0), 10)
    # make sure that all threads are exited / stopped
    killThread(serverThreads)
    # wait 1 second to make sure that all threads has been stopped
    sleep(1)
    # if shutdown requested via the user close the server
    if shutDown:
        os.system("sudo shutdown now")
    # then exit / close the programme
    exit()


try:
    # setting flask server as a single module by setting __name__
    # setting template and statics folder so flask sever knows where to look for resources
    app = Flask(__name__, template_folder="Templates", static_folder="Static")
    # socketio = SocketIO(app, async_mode=None)

    # when server starts send an email with it's current ip address
    if serverHasStarted == "False":
        # for testing purposes
        print("Server Running... ")

        # to let the user knows that server has started
        for _ in range(4):
            # turn buzzer on
            buzzer(status=True)
            newLed.colorWipe(255.166, 99)
            buzzer(status=False)
            sleep(0.25)
            newLed.colorWipe(0.0, 0)

        sendMail(
            subject="Server has started",
            receiver=receiverEmailAddress,
            body=f"""Hey, this is the smart car auto mail system\nThe Server has started running on http://{IPAddress}:5500/\nat {currentTime} - {currentDate} everything looks fine! """,
            password=serverPassword,
            email=serverEmail,
        )

        os.environ["serverHasStarted"] = "True"

    # when host is loaded return to app page index
    # and receive data from it
    @app.route("/", methods=["POST", "GET"])
    def index():
        global userName
        # credentials = request.get_data()
        # password == credentials["password"]
        # email == credentials["email"]
        # if password ==  os.environ[str(password)] and email == os.environ[str(email)]
        # userName = os.environ[str(email) + "userName"]
        # if page is not accessed after server has started running send an email
        if pageAlreadyAccessedStarted == "False":
            sendMail(
                subject="Server has accessed",
                receiver=receiverEmailAddress,
                body=f"Hey, this is the smart car auto mail system\nThe Server has accessed at {currentTime} by {userName} \n everything looks fine! ",
                password=serverPassword,
                email=serverEmail,
            )
            # change the env value
            os.environ["pageAlreadyAccessedStarted"] = "True"
        return render_template("app.html")

    # send CPU and power data to the client
    # get other objects distance

    @app.route("/data/<type>")
    def sendData(type):
        userName = " John Muller"
        data = {
            "username": userName,
            "Temperature": getTemperature(),  # CPU Temperature
            "power": getBatteryPercentage(),  # Battery info
            "dataDistance": objectsDistance,
            "roomTemperature": rand(0, 150),
        }

        if type == "All":
            response = make_response(jsonify(data))
            return response
        elif type == "Light":
            lightSensorData = data["rightSensorReadings": rightSensorReadings,
            "leftSensorReadings": leftSensorReadings]
            # start reading light distance 
            lightSensorsThread.start()
            lightSensorsThread.join()
            response = make_response(jsonify(lightSensorData))
            return response
        elif type == "distance":
            # start reading objects distance 
            ultrasonicThread.start()
            ultrasonicThread.join()
        else:
            # stopping only these two 
            killThread(sensorsThreads)
            return  render_template("app.html")
    def captureAnImage():
        """_summary_
        this is an infinite function that capture an image and stores it in the PWD directory
        then returns the captured image
        Yields:
            _byte_: _description_ return image data JPEG data in JFIF or Exif formats
        """
        while True:
            frame = cam.get_frame()
            CV.imwrite("pic.jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )

    @app.route("/videoStream")
    def videoStream():
        return Response(
            captureAnImage(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    # wheel directions and buzzer route
    # this route is created to move the car according to the requested value
    @app.route("/wheel/<direction>")

    # create a function that checks the direction and call wheelMotor function
    # to set the wheels and move the car according the given direction
    def wheelDirections(direction):
        # wheel button is clicked in the frontend (user's interface)
        # Do the following

        # if objectsDistance >= 20:

        # if direction is set to forward
        if direction == "forward":
            # moving the car forward
            # set all wheels value negative so the car moves forward
            wheelMotor.setMotorModel(-2000, -2000, -2000, -2000)
            # the below function is { return render_template("app.html")} doing nothing in this case
            # because in the front end i am not sending request to get new page so the page
            # do not refresh
            # i just did it so it does not give an error
            # also if the user hit to the directory for example host/wheel/forward the flask server will
            # redirecting the user to app page but the wheel will keep running and that what wheel happen if i sent
            # GET request like "host/wheel/forward"
            # i can return none but the flask server will give a warning
            # and if i return text like "car is moving forward" it will go to a new page showing the text and it's not
            # effecting way
            # more explanation are given on week four "https://securityguardjohnmuller.netlify.app/#weekNumFour"
            return render_template("app.html")

        # if direction is set to backward
        elif direction == "backward":
            # moving the car forward
            # set all wheels value positive so the car moves backward
            wheelMotor.setMotorModel(2000, 2000, 2000, 2000)
            return render_template("app.html")

        # if direction is set to left
        elif direction == "left":
            # turning the car to the left
            # set the left wheels value positive and lower than the right wheels so the car turn to the left
            wheelMotor.setMotorModel(-1500, -1500, 1500, 1500)
            return render_template("app.html")

        # if direction is set to right
        elif direction == "right":
            # turning the car to the left
            # set the right wheels value negative and lower than the left wheels so the car turn to the right
            wheelMotor.setMotorModel(1500, 1500, -1500, -1500)
            return render_template("app.html")

        # if direction is set to buzzer
        elif direction == "buzzer":
            # turn buzzer on
            buzzer(True)
            return render_template("app.html")

        # if direction is set to stop or anything else
        else:
            # make sure that wheels are set to zero
            wheelMotor.setMotorModel(0, 0, 0, 0)
            # and buzzer is turned on
            buzzer(False)
            # if the user hard coded a the url for example host/wheel/example
            # but in my case i am sending stop when button reveals or not clicked
            # more explanation are given on week four "https://securityguardjohnmuller.netlify.app/#weekNumFour"
            return "invalid request"
        # else:
        # wheelMotor.setMotorModel(0, 0, 0, 0)
        # buzzer(False)
        # return render_template("app.html")

    # servo directions route
    @app.route("/servo/<directionURL>", methods=["POST"])
    def servoDirections(directionURL):
        # get value from the clint side and store it in a variable
        currentDirectionValue = request.get_json()
        # print(currentDirectionValue) # for testing purposes
        if (
            # check if the current value is between the minimum and maximum value
            # if value is not in between min and max the function will return invalid request
            # the below code is to double check so if someone has make changes on the clint side it won't effect in her
            currentDirectionValue >= minServoValue
            and currentDirectionValue <= maxServoValue
        ):

            # the upper (left right)servo motor has address is 0
            # the bottom (up and down ) servo motor has address 1
            # if direction url is "example" will move to it's given direction

            if directionURL == "up":
                servoMotor.setServoPwm("1", currentDirectionValue)
                return render_template("app.html")

            elif directionURL == "right":
                servoMotor.setServoPwm("0", currentDirectionValue)
                return render_template("app.html")

            elif directionURL == "down":
                servoMotor.setServoPwm("1", currentDirectionValue)
                return render_template("app.html")

            elif directionURL == "left":
                servoMotor.setServoPwm("0", currentDirectionValue)
                return render_template("app.html")
            else:
                servoMotor.setServoPwm("1", 90)
                servoMotor.setServoPwm("0", 90)
            return render_template("app.html")
        else:
            return "invalid request please try again "

    # send Email Route
    @app.route("/Email/<Type>", methods=["POST", "GET"])
    def sendEmail(Type):

        # when user press on send email if method equal to "POST"
        # the data will be sent to the given gmail with it's body
        # but the subject is initialed in here
        if Type == "POST":
            data = request.get_json()
            sendMail(
                subject="Smart car mail system",
                receiver=data["receiver"],
                body=data["body"],
                password=serverPassword,
                email=serverEmail,
            )
        # if method == "GET" then the system summary message will be sent
        elif Type == "GET":
            sendMail(
                subject="Smart car summary",
                receiver=receiverEmailAddress,
                body=f"""Hey, this is the smart car auto mail system\n
                everything looks fine!{currentTime}\n
                one accessed user: {userName}\n
                everything looks fine!""",
                password=serverPassword,
                email=serverEmail,
                attachment=True,
            )

    # LEDs route
    @app.route("/LEDs/<stripType>/<LEDStatus>", methods=["POST", "GET"])
    def LEDs(stripType, LEDStatus):

        if stripType != "single":

            # make sure that the animation Mode is switched off
            killThread(LEDsThreads)

            # make sure that the all LEDs are switched off
            sleep(0.5)
            newLed.colorWipe(newLed.strip, Color(0, 0, 0), 10)

            if stripType == "RGB" and LEDStatus == "on":
                RGBModeThread = Thread(target=colorAnimation, args=("RGB",))
                serverThreads.append(RGBModeThread)
                LEDsThreads.append(RGBModeThread)
                print(
                    "RGB animation mode thread has started!.."
                )  # for testing purposes
                RGBModeThread.start()

            elif stripType == "chaserAnimation" and LEDStatus == "on":
                theaterChaseRainbow = Thread(target=colorAnimation, args=("Animation",))
                serverThreads.append(theaterChaseRainbow)
                LEDsThreads.append(theaterChaseRainbow)
                print(
                    "Chaser animation mode thread has started!.."
                )  # for testing purposes
                theaterChaseRainbow.start()

            elif stripType == "rainbow" and LEDStatus == "on":
                rainbow = Thread(target=colorAnimation, args=("Rainbow",))
                serverThreads.append(rainbow)
                LEDsThreads.append(rainbow)
                print(
                    "Rainbow animation mode thread has started!.."
                )  # for testing purposes
                rainbow.start()

            elif stripType == "cycle" and LEDStatus == "on":
                rainbowCycle = Thread(target=colorAnimation, args=("Cycle",))
                serverThreads.append(rainbowCycle)
                LEDsThreads.append(rainbowCycle)
                print(
                    "Cycle animation mode thread has started!.."
                )  # for testing purposes
                rainbowCycle.start()

            elif stripType == "randomColors" and LEDStatus == "on":
                randomAnimation = Thread(target=colorAnimation, args=("Random",))
                serverThreads.append(randomAnimation)
                LEDsThreads.append(randomAnimation)
                print(
                    "Cycle animation mode thread has started!.."
                )  # for testing purposes
                randomAnimation.start()

            return render_template("app.html")

        elif stripType == "single" and LEDStatus == "on":
            data = request.get_json()
            print(data)  # for testing purposes
            index = int(data["index"])
            RGB = data["RGB"]
            print(f"type of {index} is {type(index)}")  # for testing purposes
            newLed.ledIndex(index, RGB["R"], RGB["G"], RGB["B"])
            return render_template("app.html")

        elif stripType == "single" and LEDStatus == "off":
            data = request.get_json()
            index = int(data["index"])
            newLed.ledIndex(index, 0, 0, 0)
            return render_template("app.html")

        else:
            # destroy / turn off the LEDs
            killThread(LEDsThreads)  # to kill the thread
            # to make sure that all LEDs are low / turned off
            return "invalid request"

    # Sensor mode route
    @app.route("/sensor/<sensorType>/<modeStatus>")
    def sensors(sensorType, modeStatus):

        if modeStatus == "start":
            # make sure that the previous modes / threads has been stopped
            killThread(sensorsThreads)
            # also make sure that wheels are set to 0 if the thread exited and the pins are set to high
            wheelMotor.setMotorModel(0, 0, 0, 0)

            if sensorType == "ultraSonic":
                ultrasonicModeThread = Thread(target=newUltraSonic.run)
                sensorsThreads.append(ultrasonicModeThread)
                serverThreads.append(ultrasonicModeThread)
                print("ultrasonic mode thread has started!...")  # for testing purposes
                ultrasonicModeThread.start()
                return render_template("app.html")

            elif sensorType == "lineTracking":
                lineTrackingModeThread = Thread(target=newLineTracking.run)
                sensorsThreads.append(lineTrackingModeThread)
                serverThreads.append(lineTrackingModeThread)
                print(
                    "line tracking mode thread has started!..."
                )  # for testing purposes
                lineTrackingModeThread.start()
                return render_template("app.html")

            elif sensorType == "lightTracking":
                lightTrackingModeThread = Thread(target=lightTracking.run)
                sensorsThreads.append(lightTrackingModeThread)
                serverThreads.append(lightTrackingModeThread)
                lightTrackingModeThread.start()
                return render_template("app.html")

            elif sensorType == "faceTracking1":
                # TODO this code not ready because i am waiting for the camera
                faceTrackingModeThread = Thread(target=VideoStreaming.face_detect.run)
                sensorsThreads.append(faceTrackingModeThread)
                serverThreads.append(faceTrackingModeThread)
                faceTrackingModeThread.start()
                return render_template("app.html")
        else:
            killThread(sensorsThreads)
            return render_template("app.html")

    # if user press on close button and confirm that they sure
    # close server
    @app.route("/server/disconnect")
    def shutServerDown():
        destroy(Error=None, shutDown=True)
        # this return is not getting returned but flask server keeps giving me an error
        return "System went down "

    if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=5500, threaded=True)
except Exception as errorException:
    print("an error occurred\n", errorException)  # for testing purposes
    buzzer(
        status=True, anErrorOccur=True
    )  # to let the user know that there is an error
    destroy(errorException)  # make sure that all components are set to low/destroyed
except KeyboardInterrupt:
    print("Keyboard Interrupt")  # for testing purposes
    destroy(None)
finally:
    print("finally")  # for testing purposes
    destroy(None)
