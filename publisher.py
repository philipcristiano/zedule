import datetime
import random
import socket as python_socket
import sys
import time

import bson
import zmq


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect ("tcp://localhost:5001")

count = 0
while True:
    now = datetime.datetime.utcnow()
    offset = datetime.timedelta(seconds=random.random() * 20)
    schedule_for = now + offset
    headers = bson.BSON.encode({
        'time': schedule_for,
        'key': 'testing',
    })
    data = str(count)
    method = 'insert'
    data = socket.send_multipart((method, headers, data))
    print '.', socket.recv_multipart()
    count +=1
    time.sleep(1)
