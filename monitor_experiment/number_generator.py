from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time
import json


with open('../nodes_list.json') as f:
    data = json.load(f)
nodes = data["nodes"]

for node in nodes:
    if node["role"] == "start":
        host = node["host"]
        print(node["host"])
        mqttph = MqttPublishHandler(host, 'data-generator', 'test', 'test')
        mqttph.connect()
        break

number = 0
print("publisher script is started")

while True:
    ts = time.time()
    msg = str(ts) + ":" + str(number)
    mqttph.publish("T-1", msg, qos=1, retain=False)
    # print(number)
    # TODO change data generation rate
    # time.sleep(0.2)  # 5 data per second
    # time.sleep(0.3)  # 3 data per second
    time.sleep(0.4)
    # time.sleep(0.5)  # 2 data per second
    # time.sleep(1)  # 1 data per second
    number += 1
