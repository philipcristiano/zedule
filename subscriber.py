import socket as python_socket
import sys

import bson
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.identity = 'subscriber'

print "Reading"
socket.connect ("tcp://localhost:5002")

socket.setsockopt(zmq.SUBSCRIBE, 'testing')

while True:
    key, data = socket.recv_multipart()

    data = bson.BSON(data).to_dict()
    print data
