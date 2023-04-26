import paho.mqtt.client as mqtt
import time
# need to add a user and password to the mosquitto configuration so that
# not just anyone can publish to the server.

received = -1
def setTargetListener(topic, ip="127.0.0.1", port=1883):
    global received
    """
    Listens to an mqtt topic (string) for prespecified messages on
    a given ip (strint) and port (integer). Returns 0 or 1 Depending
    on the message received.
    """
    # set listening client id
    client = mqtt.Client("target_listener")
    keepalive = 60
    client.connect(ip, port, keepalive)
    # used to handle message receiving
    def on_message(client, userdata, message):
        global received # need to declare as a global or can't return
        received = message.payload.decode('utf-8')
        print(f"Received {message.payload.decode()} from {message.topic} topic")
    client.subscribe(topic)
    client.on_message = on_message
    # listen for 4 seconds at a time
    client.loop_start()
    time.sleep(4)
    # need to do this inside the loop
    if received == "O" or received == "C":
        received = -1
        client.loop_stop()
        client.disconnect()
        return 1
    else:
        client.loop_stop()
        client.disconnect()
        return 0


    


def getTargetPublisher(topic, message, ip="127.0.0.1", port=1883):
    """
    Publishes a message (string) to an mqtt topic (string) at a given ip (string)
    and given port (integer)
    """
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

if __name__ == "__main__":
    while True:
        target = setTargetListener("homebridge/settarget")
        print("target", target)
        if target:
            print("*******************************")