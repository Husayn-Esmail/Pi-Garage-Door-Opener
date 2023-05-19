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

def read_sensor(sensor_pin, state_pin, reverse=False):
	'''
	Reads value of a door sensor and returns the interpretted value
	in respect to the garagedoor state. Has an option to reverse based
	on the sensor's reading process.
	'''
	# start the sensor
	GPIO.output(sensor_pin, GPIO.HIGH)
	state = GPIO.input(state_pin)
	# garage is closed
	if reverse:
		state = not state
	
	if not state:
		return "C"
	return "O"

def main():
	# configuration
	filename = process_cmdline_arguments()
	config = read_configuration(filename)
	method = config["method"]
	stateHardware = config["stateHardware"]
	auth_user = config["auth_user"]
	auth_password = config["auth_password"]
	setTargetStateTopic = config["setTargetStateTopic"]
	getTargetState_topic = config["getTargetStateTopic"]
	getCurrentState_topic = config["getCurrentStateTopic"]
	ip = config["ip"]
	port = config["port"]
	relayPin, sensorPin, statePin = config["relayPin"], config["sensorPin"], config["statePin"]


	DOORSTATE = "C" # default state of closed

	# Init GPIO
	GPIO.setmode(GPIO.BCM)
	# setup
	GPIO.setup(relayPin, GPIO.OUT)
	GPIO.setup(sensorPin, GPIO.OUT)
	GPIO.setup(statePin, GPIO.IN)
	# start sensor
	GPIO.output(sensorPin, GPIO.HIGH)

	# GLOBAL STATE VAR
	DOORSTATE = read_sensor(sensorPin, statePin)


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
		"port": 0,
		"relayPin": 0,
		"sensorPin": 0,
		"statePin": 0
		}
	with open (filename, 'r') as f:
		for key in config.keys():
			config[key] = f.readline().rstrip('\n')
			# convert port and pins to int
			if key == 'port' or key == "relayPin" or key == "sensorPin" or key == "statePin":
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

def process_cmdline_arguments():
	'''
	Manages the reading of commmand line arguments and validation.
	Returns a filename for configuration.
	'''
	if len(sys.argv) < 2: 
		print("missing argument: filename")
		exit()
	filename = sys.argv[1]
	return filename

# runs the mqtt server
if __name__ == '__main__':
	filename = process_cmdline_arguments()
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