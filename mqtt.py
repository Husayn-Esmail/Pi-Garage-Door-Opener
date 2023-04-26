import paho.mqtt.client as mqtt

# need to add a user and password to the mosquitto configuration so that
# not just anyone can publish to the server.



def setTargetListener(topic, message, ip="127.0.0.1", port=1883):
    # set listening client id
    client = mqtt.Client("target_listener")
    keepalive = 60
    client.connect(ip, port, keepalive)
    received_message = ""
    def on_message(client, userdata, message):
        print(f"Received {message.payload.decode()} from {message.topic} topic")
        # store it outside the function so that I can access it's contents
        received_message = message
    client.subscribe(topic)
    client.on_message = on_message
    client.disconnect()
    if received_message.payload.decode("utf-8") == "O":
        return 1
    elif received_message.payload.decode("utf-8") == "C":
        return 1
    else:
        return 0


def getTargetPublisher(topic, message, ip="127.0.0.1", port=1883):
    # handles the connection to mqtt
    # def on_connect(client, userdata, flags, rc):
    #     if rc == 0:
    #         print("Connected to MQTT broker")
    #     else:
    #         print("Failed to connect, return code %d\n", rc)
    #     # set client id
    #     broker = "broker.emqx.io"
    #     client = mqtt.Client("target_publisher")
    #     client.on_connect = on_connect
    #     client.connect(broker, port=1883)
    #     return client
    
    # publishing to the given topic
    client = mqtt.Client() # setup client
    keepalive = 60
    # connect to publisher
    client.connect(ip, port, keepalive)
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"published {message} to {topic}")
    else:
        print("failed to publish to {topic} on {ip}:{port}")
    return result