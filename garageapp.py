#!/usr/bin/env python3
"""
Uses mqtt to open and close the garage as well as get it's current state.
"""

# import modules
import time
import RPi.GPIO as GPIO
import irsensor
import mqtt


# NEW MOSQUITTO CODE
def trigger_relay():
	# sets the relay to flip for one second
	GPIO.output(21, 1)
	time.sleep(1)

# decides whether to open the garage door or not
def decide_open(the_input, secret_code, topic, ip, port):
	'''
	This function handles flipping the momentary switch.
	validates input against secret code, returns true or
	false depending on whether the input matches and the
	door can be opened.
	'''
	target = mqtt.setTargetListener(topic, ip, port)
	if target:
		trigger_relay()

# runs the mqtt server
if __name__ == '__main__':
	listener_topic = ""
	publisher_topic = ""
	ip = ""
	port = 0
	while True:
		decide_open()
		irsensor.get_status(publisher_topic)
		time.sleep(1)
	GPIO.cleanup()