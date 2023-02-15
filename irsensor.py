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

print("irsensor being called") # for log/debug purposes
# Init GPIOs
# set GPIO pin mode
GPIO.setmode(GPIO.BCM)

# initialize pins
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.IN)

# start the sensor
GPIO.output(20, GPIO.HIGH)

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
		print(get_status())
		time.sleep(1)

# clean up pin
GPIO.cleanup()

