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
	GPIO.output(21, 0)


# decides whether to open the garage door or not
def decide_open(topic, ip, port):
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
	setTargetState_topic = ""
	getTargetState_topic = ""
	getCurrentState_topic = ""
	ip = ""
	port = 0
	# unfortunately the infinite loop is necessary to poll the sensor.
	while True:
		try:
			# set GPIO pin mode
			GPIO.setmode(GPIO.BCM)

			# initialize pins
			GPIO.setup(20, GPIO.OUT)
			GPIO.setup(16, GPIO.IN)
			GPIO.setup(21, GPIO.OUT)

			# start the sensor
			GPIO.output(20, GPIO.HIGH)

			# listens for requested changes
			decide_open(setTargetState_topic, ip, port)

			# reflects the real world state
			status = irsensor.get_status(getCurrentState_topic, ip , port)
			# if status == mqtt.setTargetListener(listener_topic, ip, port):
			# 	mqtt.getTargetPublisher()
			time.sleep(1)
		except ConnectionRefusedError as err:
			print("***** ERROR OCCURED: ConnectionRefusedError *****")
			print(err)
			continue
		except KeyboardInterrupt:
			print("KeyboardInterrupt")
		else:
			continue
		finally:
			GPIO.cleanup()