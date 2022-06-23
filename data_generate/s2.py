import paho.mqtt.client as mqtt


broker = "192.168.1.8"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Message received [{msg.topic}]: {msg.payload}")


client = mqtt.Client("sub-test-test", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883)
client.subscribe("T-2", qos=1)
#client.reconnect()
client.loop_forever()
