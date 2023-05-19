#!/usr/bin/env python3
"""
Uses mqtt to open and close the garage as well as get it's current state.
"""

# import modules
import time
import RPi.GPIO as GPIO
import irsensor
import mqtt
import socket
import sys


# NEW MOSQUITTO CODE
def trigger_relay():
	'''
	Flips relay on for 1 second and then off again to trigger garagedoor motor.
	'''
	GPIO.output(21, 1)
	time.sleep(1)
	GPIO.output(21, 0)

def read_sensor(reverse=False):
	'''
	Reads value of a door sensor and returns the interpretted value
	in respect to the garagedoor state. Has an option to reverse based
	on the sensor's reading process.
	'''
	pass

def main():
	DOORSTATE = "C" # default state of closed

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


def read_configuration(filename):
	"""
	Processes configuration file using a passed in filename (string)
	and returns a dictionary with each attribute as the key and the
	setting as the value.
	"""
	config = {
		"method" : "",
		"stateHardware" : False,
		"auth_user": "",
		"auth_password" : "",
		"setTargetStateTopic": "", 
		"getTargetStateTopic": "",
		"getCurrentStateTopic": "", 
		"ip": "", 
		"port": 0}
	with open (filename, 'r') as f:
		for key in config.keys():
			config[key] = f.readline().rstrip('\n')
			# convert port to int
			if key == 'port':
				config[key] = int(config[key])
			# convert stateHardware to boolean
			if key == "stateHardware":
				if config[key] == "False":
					config[key] = False
				else:
					config[key] = True
			# ensure that whatever method entered is consistent
			if key == "method":
				# for consistency
				config[key] = config[key].lower()	
	return config


# runs the mqtt server
if __name__ == '__main__':
	if len(sys.argv) < 2: 
		print("missing argument: filename")
		exit()
	filename = sys.argv[1]
	config = read_configuration(filename)
	setTargetState_topic, getTargetState_topic, \
		getCurrentState_topic, ip, port = config["setTargetState_topic"], config["getTargetState_topic"], \
		config["getCurrentState_topic"], config["ip"], config["port"]

	# # unfortunately the infinite loop is necessary to poll the sensor.
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
			time.sleep(1)
		except ConnectionRefusedError as err:
			print("""***** 
			
			
			ERROR OCCURED: ConnectionRefusedError 
			
			
			*****""")
			print(err)
			continue
		except socket.timeout as err:
			print("""*****
			 
			
			ERROR OCCURED: likely a socket.timeout error 
			
			
			*****""")
			print(err)
			continue
		except OSError as err:
			print("""
			
			
			OS ERROR OCCURRED

			

			""")
			print(err)
			continue
		except KeyboardInterrupt:
			print("""
			****
			
			KeyboardInterrupt
			
			****
			""")
			exit()
		else:
			continue
		finally:
			GPIO.cleanup()