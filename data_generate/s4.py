import time
import paho.mqtt.client as paho


broker = "192.168.1.8"
port = 1883

def on_publish(client,userdata,result):
    pass

client1 = paho.Client("pub-test")
client1.on_publish = on_publish
client1.connect(broker, port)

number = 0
while True:
    client1.publish("T-2", number, qos=1, retain=False)
    print (number)
    time.sleep(1) # sleep for seconds
    number += 1
