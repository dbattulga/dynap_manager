from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time


mqttph = MqttPublishHandler('paravance-12.rennes.grid5000.fr', 'data-generator', 'test', 'test')
mqttph.connect()

number = 0

while True:
    mqttph.publish("T-0", number, qos=1, retain=True)
    print (number)
    time.sleep(1) # sleep for seconds
    number += 1

mqttph.disconnect()