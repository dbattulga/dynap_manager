from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler
import csv
import time


# file_A = 'siteA_10ms.csv'
# file_B = 'siteB_10ms.csv'
# #f1 = open(dest_file, 'a+')
# header = ["Site", "Timestamp", "Count"]

line_count = 0
def f(msg):
    #f1.write(msg.decode())
    #time.sleep(1)
    # md = msg.decode().split(',')
    # if md[0] == 'A':
    #     with open(file_A, "a+") as writefile:
    #         csv_writer = csv.writer(writefile)
    #         csv_writer.writerow(md)
    # if md[0] == 'B':
    #     with open(file_B, "a+") as writefile:
    #         csv_writer = csv.writer(writefile)
    #         csv_writer.writerow(md)
    print(msg)


mp = MqttSubscriptionHandler("10.188.166.99", "status-checker", "test", "test") #host, client id, username & password
#mp = MqttSubscriptionHandler("127.0.0.1", "3", "mqtt-sub", "mqtt-sub") #host, client id, username & password
mp.add_subscription("T-1")
mp.connect()
mp.with_on_message_f(f)
mp.listen()
#f1.close()