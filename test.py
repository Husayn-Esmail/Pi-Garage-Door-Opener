# wayy more imports than I would like but it is necessary for some of the setup.
import garageapp
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO



# setting a bunch of global variables because that's really good practice...
# it's just needed so that my testing functions can have access to the same variables
# without me having to reassign them every single time.
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
    return message
    # garageapp.onTargetState(client, userdata, message, relayPin)

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe(setTargetStateTopic)

def temporary_sensor_readings(reverse=False):
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
    if reverse:
        state = not state
    if not state:
        # return closed
        return "C"
    # else return open
    return "O"


def test_temporary_sensor():
    '''
    I used a photo resistor instead of an avoid so I could simulate what it would be like if the
    avoid sensor was actually getting feedback, unfortunately, I do not have two avoid sensors and
    my only sensor is currently deployed so I couldn't use that and had to improvise. Technically they
    output the same result and this is a closer method than just generating random values because I can
    simulate times when the relay triggers but the garage motor doesn't necessarily open/close which
    does happen on occasion.
    '''
    while True:
        print("LDR: ", temporary_sensor_readings())
        time.sleep(3)

def test_thread_shred():
    '''
    Again not an automated test as this tests the ability for the program to listen to
    a given mqtt topic with authentication and everything and see if calling from
    homebridge installation actually causes the relay to trigger. It's not as isolated as
    it could be because it relies on the relay function but it does work.
    '''
    client = mqtt.Client()
    client.username_pw_set(username=auth_user, password=auth_password)

    # chatgpt generated
    client.on_message = on_message # this would be because of the required function call

    client.connect("localhost", 1885, 60)
    client.subscribe(setTargetStateTopic)
    # loops the program forever
    garageapp.thread_shred(client)
    time.sleep(1)
    

def test_mqtt_client():
    '''
    The point of this is to test if the mqttsetup function works
    '''
    c = garageapp.mqttsetup(ip, port, setTargetStateTopic, relayPin, [auth_user, auth_password])
    garageapp.thread_shred(c)

def test_relay():
    '''
    This is something that must be tested manually so it is not automated in any way.
    All it does is loop forever, call my relay trigger function and then wait for the user
    to press enter to see if it works again.
    '''
    while True:
        garageapp.trigger_relay(relayPin)
        input("Press enter to do it again")

if __name__ == '__main__':
    test_mqtt_client()