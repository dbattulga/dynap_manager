from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time

mqttph = MqttPublishHandler('10.188.166.99', 'data-generator', 'test', 'test') #host, client id, username & password
#mqttph = MqttPublishHandler('172.16.96.43', 'data-generator', 'test', 'test') #host, client id, username & password
mqttph.connect()

number = 0

while True:
    mqttph.publish("T-1", number)
    print (number)
    time.sleep(0.01) # sleep for seconds
    number += 1

mqttph.disconnect()