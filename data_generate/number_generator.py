from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time


mqttph = MqttPublishHandler('petitprince-15.luxembourg.grid5000.fr', 'data-generator', 'test', 'test')
mqttph.connect()

number = 0

while True:
    mqttph.publish("T-1", number)
    print (number)
    time.sleep(1) # sleep for seconds
    number += 1

mqttph.disconnect()