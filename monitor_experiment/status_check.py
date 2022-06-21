from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler
import csv
import time

line_count = 0


def f(msg):
    print(msg)


mp = MqttSubscriptionHandler("paravance-27.rennes.grid5000.fr", "status-checker", "test", "test")  # host, client id, username & password

mp.add_subscription("T-2")
mp.connect()
mp.with_on_message_f(f)
mp.listen()
# f1.close()
