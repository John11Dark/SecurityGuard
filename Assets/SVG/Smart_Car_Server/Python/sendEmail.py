import imghdr
import smtplib
from email.message import EmailMessage

# from datetime import datetime
from time import sleep

# from .Video import videoStreaming


# get current date and time
# currentTime = datetime.now().strftime("%H:%M:%S")

# declare credentials for login
# Email = os.environ.get("ADMIN_EMAIL")

# Password = os.environ.get("ADMIN_PASSWORD")
# the server can't get the variables stored locally
# the above variable ruterns value only if it's running locally other wise it returns None
# so on the server side i used python .env
# i just left the above code to show my work


# setup the server connection
mailServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)


# Message
messageToSend = EmailMessage()


def sendMail(subject, receiver, body, email, password, attachment=False):
    """_summary_

    Args:
        subject (_str_): _description_. Email subject
        receiver (_str_): _description_ . Receiver Email address
        body (_str_): _description_. body content
        email (_str_): _description_ the sender email that the email going to be sent from
        password (_str_): _description_ the email password
        attachment (bool, optional): _description_. Defaults to False. if it's set to true it will capture a video attache it to the email
    """
    # open connection and wait
    # mailServer.connect()
    # sleep(0.2)
    # set the mail form content
    messageToSend["Subject"] = subject
    messageToSend["From"] = email
    messageToSend["TO"] = receiver
    messageToSend.set_content(body)
    # if the user wants to check status or the auto send mail sent will record a video and send it with the email
    if attachment:
        # VideoStreaming.takeVideo()
        sleep(15)  # wait until the video is taken
        try:
            with open("./Server_Assets/Videos/piVideo.mp4") as video:
                file = video.read()  # store the video in file variable
                fileType = imghdr.what(file)  # get the file type / extension
                messageToSend.add_attachment(
                    file, maintype="video", subtype=fileType
                )  # attach the video to the email
        except Exception as error:
            print(error)  # for testing purposes
            pass

    # check if login is successful if not print a message
    try:
        mailServer.login(email, password)
    except NameError as loginErr:
        print(
            f"an error occur while trying to login please check the credentials \n [{loginErr}]"
        )
    # send email and if an error occurs print a message
    try:
        mailServer.send_message(messageToSend)
        messageToSend.clear()
        messageToSend.clear_content()
    except ValueError as valueError:
        messageToSend.clear()
        messageToSend.clear_content()
        # for testing purposes
        print(f"mail not sent because of an error occurs \n\n ''[{ valueError }]\n\n''")
    #print("mail sent")  # for testing purposes
