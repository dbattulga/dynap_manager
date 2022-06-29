from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler
import time
import csv
import re
import json


with open('../nodes_list.json') as f:
    data = json.load(f)
nodes = data["nodes"]

file1 = open('../results/latency_result.csv', 'a+')
writer = csv.writer(file1)
writer.writerow(["start_timestamp", "data", "end_timestamp"])

for node in nodes:
    if node["role"] == "end":
        host = node["host"]
        print(node["host"])
        mp = MqttSubscriptionHandler(host, "status-checker", "test", "test")  # host, client id, username & password
        break

line_count = 0

def on_message(msg):
    time1 = time.time()
    msg1 = msg.decode("utf-8")
    msg1 += ":" + str(time1)
    split_text = re.split(':', msg1)
    writer.writerow(split_text)
    #print(msg1)

# TODO change topic number accordingly
print("status checker script is started")
mp.add_subscription("T-13")
mp.connect()
mp.with_on_message_f(on_message)
mp.listen()
