import csv
import time
import re


time1 = time.time()
time.sleep(2)
time2 = time.time()
print(round(time2 - time1, 3))

file1 = open('endResults.csv', 'a+')
writer = csv.writer(file1)

h3List = []
number = 0
strr = "A_job:B_Job:C_Job:"


while True:
    ts = time.time()
    msg = str(ts) + ":" + str(number) + ":" + strr
    time.sleep(0.01)
    ts2 = time.time()
    msg += str(ts2)
    print(msg)
    time.sleep(1)

    split_text = re.split(':', msg)
    print(split_text)
    writer.writerow(split_text)

    number += 1

