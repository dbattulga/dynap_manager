from __future__ import absolute_import
#from mqtt import MqttSubscriptionHandler
import paho.mqtt.client as mqtt
import csv
import time

line_count = 0


def f(msg):
    print(msg)


#mp = MqttSubscriptionHandler("10.93.0.94", "status-checker-2", "test", "test")  # host, client id, username & password

# mp.add_subscription("T-1")
# mp.connect()
# mp.with_on_message_f(f)
# mp.listen()

client = mqtt.Client("sub-test-test", clean_session=True)
client.connect("192.168.1.8")
client.subscribe("T-2", qos=1)
client.disconnect()
client.loop_stop()
# f1.close()
