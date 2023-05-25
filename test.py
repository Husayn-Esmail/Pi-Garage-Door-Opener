import garageapp
import time
import paho.mqtt.client as mqtt


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

while True: 

#    c = mqttsetup(ip, setTargetStateTopic)
    client = mqtt.Client()

    client.username_pw_set(username=auth_user, password=auth_password)

    # chatgpt generated`
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(ip, port, 60)
    client.subscribe(setTargetStateTopic)
    garageapp.thread_shred(client)
    time.sleep(1)
    
    
