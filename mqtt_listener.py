import time
import paho.mqtt.client as mqtt

def subscribe(topic):
    client = mqtt.Client()
    client.connect("0.0.0.0", 1883, 60)
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message


def get_message(channel):
    client = mqtt.Client('1231232')
    client.connect("0.0.0.0", 1883, 60)
    def on_message(client, userdata, message):
        print(f"Received `{message.payload.decode()}` from `{message.topic}` topic")
    client.subscribe(channel)
    client.on_message = on_message
    client.disconnect()


def sub(topic):
    client = mqtt.Client("listener")
    client.connect("0.0.0.0", 1883, 60)
    client.subscribe(topic, qos=0)
    def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
    client.on_message = on_message
    client.loop_start()
    time.sleep(4)
    client.loop_stop()




if __name__ == "__main__":
    channel = "mqtt_test_channel"
    while True:
        sub(channel)
        # subscribe(channel)
