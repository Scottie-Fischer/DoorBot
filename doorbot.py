#Mail Libraries
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#GPIO Libraries
import PRi.GPIO as GPIO
import time


#Mail Send/Recv Setup
sender = "doorbotpi22@gmail.com"
password = raw_input("Please enter sending email password\n")

receiver = raw_input("\nPlease enter receiving email\n")

message_cont = """From: DoorBot <doorbotpi22@gmail.com>

THIS IS A WARNING YOUR DOOR HAS BEEN LEFT OPEN!
I REPEAT, THE DOG HAS ACCESS TO THE GOODS!"""

#MIME Setup
message = MIMEMultipart()
message ['From'] = sender
message['To'] = receiver
message['Subject'] = "WARNING: DOOR LEFT OPEN"
message.attach(MIMEText(message_cont,'plain;'))


#create SMTP session for sending mail
session = smtplib.SMTP('smtp.gmail.com',587)
session.starttls()
session.login(sender,password)
text = message.as_string()

#GPIO Setup
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 23

#set GPIO direction
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

dist_count = 0

def distance():
    
    #Makes Sure the Signal is Cleared
    GPIO.output(GPIO)TRIGGER,False)
    time.sleep(0.001)

    #Trigger to High
    GPIO.output(GPIO_TRIGGER,True)

    #Trigger to Low after 0.01ms
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)

    #Calculate Time==================
    StartTime  = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    #Time Calculation Done===========

    #Using the Speed of Sound to find D
    distance = (TimeElapsed * 34300)/2
    
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Distance Measured = %.1f cm") % dist
            if dist > 158:
                dist_count++
                if dist_count > 4:
                    session.sendmail(sender,receiver,text)
                    dist_count = 0
            #Wait a few seconds
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measured stopped by User")
    finally:
        GPIO.cleanup()
        session.quit()


