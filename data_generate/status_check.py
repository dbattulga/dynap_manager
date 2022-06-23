from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler
import csv
import time

line_count = 0


def f(msg):
    print(msg)


mp = MqttSubscriptionHandler("192.168.1.8", "test-status-checker", "test", "test")  # host, client id, username & password

mp.add_subscription("T-1")
mp.connect()
mp.with_on_message_f(f)
mp.listen()
# f1.close()
