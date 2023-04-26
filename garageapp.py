#!/usr/bin/env python3
# garage door opener, takes a post request and opens the garage
# door if the key is correct

''' This is the second method for triggering the switch and
hosting the webserver. It achieves this by accepting a specific
code via a post request. '''

# import modules
import json
from flask import Flask, render_template, request
import time
# import RPi.GPIO as GPIO
import irsensor
import mqtt
from multiprocessing import Process


# NEW MOSQUITTO CODE
def trigger_relay():
	# sets the relay to flip for one second
	GPIO.output(21, 1)
	time.sleep(1)

def manage_state():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(20, GPIO.OUT)
	GPIO.setup(16, GPIO.IN)
	state = irsensor.get_status()
	topic = ""
	ip = ""
	port = 1883 # should be changed
	message = "O" if state else "C" # basically saying if state is 1 then open, else closed
	mqtt.getTargetPublisher(topic, message, ip , port)


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

	if the_input == secret_code:
		# executes the code to open the door
		# GPIO.output(21, 1)
		time.sleep(1)
		print("success") # for debug purposes/logs
		return True
	# if code isn't equal
	print("incorrect code") # for debug purposes/logs
	return False




# OLD WEB SERVER CODE
app = Flask(__name__)


# the backend code
@app.route('/', methods=['POST'])
def index():
	# handle post request
	# GPIO.setmode(GPIO.BCM)
	# GPIO.setup(21, GPIO.OUT)
	secret_code = "changeme"
	# the new way to authenticate for triggering the garage door
	secret_dict = {"code" : secret_code}
	if request.method == 'POST':
		# set request body type
		if request.content_type == 'application/json':
			# gets the json request from post request and stores it in a var
			content = request.get_data()
			# convert the data stored in content (of type bytes) to dict
			submission = json.loads(content.decode("utf-8"))
			# store return value of decide open
			open_garage = decide_open(submission, secret_dict)

	# otherwise handle get request
	# GPIO.cleanup()
	return render_template('index.html') 


# adds a rule that allows get requests, meant to pass status.
# not necessary for functionality
@app.route('/', methods=['GET'])
def set_status():
	# GPIO.setmode(GPIO.BCM)
	# GPIO.setup(20, GPIO.OUT)
	# GPIO.setup(16, GPIO.IN)
	# state = irsensor.get_status()
	state = 0
	print("status is working: %d" % state) # for debug/log purposes
	if state: # the garage is open
		status = 1
	else: # the garage is closed
		status = 0
	# renders the status template by passing in the value of status
	return render_template('status.html', status=status)

# runs the webserver
if __name__ == '__main__':
	from waitress import serve
	listener_topic = ""
	publisher_topic = ""
	
	while True:
		decide_open()
		irsensor.get_status(publisher_topic)
		time.sleep(1)
	serve(app, host = "0.0.0.0", port = 8080)



