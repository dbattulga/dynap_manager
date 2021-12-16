from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler
from mqtt import MqttPublishHandler
import csv
import time

line_count = 0


def f(msg):
    mqttph = MqttPublishHandler('10.93.0.122', 'data-forwarder', 'test', 'test')
    mqttph.connect()
    mqttph.publish("T-2", msg)
    mqttph.disconnect()


mp = MqttSubscriptionHandler("10.93.0.122", "status-checker", "test", "test")  # host, client id, username & password
mp.add_subscription("T-1")
mp.connect()
mp.with_on_message_f(f)

while True:
    number = 0
#mp.listen()
# f1.close()
