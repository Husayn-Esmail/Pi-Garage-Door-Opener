#!/usr/bin/env python3
# this program detects whether the garagedoor is open
# starts a timer, if it is open for a specific amount of time,
# a specified list of people will be notified. 

# import necessary modules

''' This method is able to determine the state of the garage 
namely: whether the garage is open or closed based on sensor
value. Therefore there needs to be a function that determines
it's state and returns a true or a flase value which can be
passed in via a get request. '''
import RPi.GPIO as GPIO
import time
import ssl
import smtplib

print("working") # for log/debug purposes
# Init GPIOs
# set GPIO pin mode
GPIO.setmode(GPIO.BCM)

# initialize pins
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

# start the sensor
GPIO.output(20, GPIO.HIGH)

# init smtp server and send email
def sendEmail():
	''' sends emails/text messages when called '''
	port = 465 # for ssl
	smtpServer = "smtp.gmail.com"
	senderEmail = "email@example.com"
	password = "password"
	message = """ATTENTION: The garage door has been open for 15 minutes, if this is not intentional, please close the door. """
	# create a secure ssl context
	context = ssl.create_default_context()
	
	# mail recievers
	# person name
	reciever1 = "phonenumber@carrier.email.com"
	with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
		server.login(senderEmail, password)
		# send emails
		server.sendmail(senderEmail, receiver1, message)

# starts a counter if the sensor detects it's open
def countIfOpen():
	# read data from the sensor returns 1 or 0 (1=not triggered, 0 = triggerd)
	data = GPIO.input(16)
	seconds = 0
	baseValue = 900
	# while triggered
	while data = 0:
		# start timer
		time.sleep(1)
		seconds += 1
		# to make sure data is updated and prevent an infinite loop
		data = GPIO.input(16)
		print('seconds', seconds)
		while seconds >= baseValue:
			sendEmail()
			print("completed")
			baseValue += 900

def get_status():
	''' returns the state of the garage opener
	note that the sensor data is reversed where true is that the
	sensor data is reversed where True is that the garage is not
	open and False is that it is open. '''
	state = GPIO.input(16)
	# garage is closed
	if state:
		return False
	# garage is open
	return True


if __name__ == '__main__':
	continueProgram = True
	while continueProgram:
		countIfOpen()
		time.sleep(1)

# clean up pin
GPIO.cleanup()

