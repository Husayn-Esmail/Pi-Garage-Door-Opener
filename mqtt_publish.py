import time
import paho.mqtt.client as mqtt
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python how the publisher was written, i'm not a huge fan

# listen to garage/state
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        # set connecting client id
        broker = 'broker.emqx.io'
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(broker, port=1883)
        return client

def publish(topic, msg):
    msg_count = 0
    client = mqtt.Client()
    client.connect("0.0.0.0", 1883, 60)
    time.sleep(1)
    # msg = f"messages: {msg_count}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed ot send message to {topic}")
    msg_count += 1
    return result



def publish_message(message, channel):
    # initialization of the mqtt publisher
    client = mqtt.Client()
    client.connect("0.0.0.0", 1883, 60)
    client.publish(channel, message)
    client.disconnect()

if __name__ == '__main__':
    # data and channel
    x = 1
    while True: 
        if x == 1:
            message = "O"
            topic = "homebridge/gettarget"
            publish(topic, message)
            x = 0
        time.sleep(5)
        if x == 0:
            message = "C"
            topic = "homebridge/gettarget"
            publish(topic, message)
            x = 1
        input("press enter to receive")

