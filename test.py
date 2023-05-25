import garageapp
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


filename = garageapp.process_cmdline_arguments()
config = garageapp.read_configuration(filename)

method = config["method"]
stateHardware = config["stateHardware"]
ip = config["ip"]
port = config["port"]
relayPin, sensorPin, statePin = config["relayPin"], config["sensorPin"], config["statePin"]
auth_user = config["auth_user"]
auth_password = config["auth_password"]
setTargetStateTopic = config["setTargetStateTopic"]
getTargetState_topic = config["getTargetStateTopic"]
getCurrentState_topic = config["getCurrentStateTopic"]

def on_message(client, userdata, message):
    # call custom callback function
    garageapp.onTargetState(client, userdata, message, relayPin)

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe(setTargetStateTopic)

def temporary_sensor_readings():
    """
    Used only for my testing environment and will be substituted with the avoid
    sensor code as the necessary logic for the sensor is already tried and tested
    but the implementation for how to use the data once it's been received has not been.
    Basically I know that reading the avoid sensor works. but what I do with the data afterwards
    is not tested yet.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensorPin, GPIO.IN)

    # read GPIO
    state = GPIO.input(sensorPin)
    GPIO.cleanup()

    return state


# while True:
#    c = mqttsetup(ip, setTargetStateTopic)
client = mqtt.Client()

client.username_pw_set(username=auth_user, password=auth_password)

# chatgpt generated`
# client.on_connect = on_connect # I don't think this is necessary
client.on_message = on_message # this would be because of the required function call

client.connect(ip, port, 60)
client.subscribe(setTargetStateTopic)
garageapp.thread_shred(client) # I believe this is enough to keep the program going.
time.sleep(1)
    
    
