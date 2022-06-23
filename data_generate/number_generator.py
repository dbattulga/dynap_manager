from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time


mqttph = MqttPublishHandler('192.168.1.8', 'data-generator', 'test', 'test')
mqttph.connect()

number = 0

while True:
    mqttph.publish("T-0", number, qos=1, retain=False)
    print(number)
    time.sleep(1) # sleep for seconds
    number += 1

mqttph.disconnect()


