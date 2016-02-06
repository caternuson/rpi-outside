#!/usr/bin/env python

#
# simple socket based temperature sender
#

import socket
import Adafruit_BMP.BMP085 as BMP085
from datetime import datetime

HOST = ''
PORT = 65050
SIZE = 1024
BACKLOG = 5
ERROR_VAL = '-999'

def get_current_temp():
    sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
    return("%7.2f" % (32.0+1.8*sensor.read_temperature()))

def get_now():
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((HOST,PORT))
s.listen(BACKLOG)
print "%s Started." % (get_now())
while True:
    client, addr = s.accept()
    print "%s Connection from %s." % (get_now(),addr[0])
    data = client.recv(SIZE)
    if data:
        if "GCT" in data:
            client.send(get_current_temp())
        else:
            client.send(ERROR_VAL)
    client.close()
