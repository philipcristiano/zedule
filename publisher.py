import socket as python_socket
import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect ("tcp://localhost:5001")

import bson
import time
import datetime

while True:
    headers = bson.BSON.encode({
        'time': datetime.datetime.utcnow(),
        'key': 'testing',
    })
    data = 'BLAH'
    data = socket.send_multipart((headers, data))
    print '.',
    print socket.recv_multipart()
    time.sleep(5)
