import time

import threading

import dateutil.parser
import msgpack
import pymongo
import zmq


monitor_threads = {}
context = zmq.Context()

def req_repl():
    print 'starting req-reply'
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5001')
    mongo = pymongo.Connection('33.33.33.10')
    db = mongo.zedule
    collection = db.items

    while True:
        headers, data = socket.recv_multipart()
        headers = msgpack.unpackb(headers)
        print headers
        scheduled_for = dateutil.parser.parse(headers['time'])
        doc = {
            'time': scheduled_for,
            'data': data,
        }

        id_ = collection.insert(doc)
        print id_
        socket.send_multipart(['200', str(id_)])



def load_monitors():
    "Load monitors from config"
    monitors = []
    for monitor_item in config['monitors']:
        monitor_name = 'monitor.monitors.{0}'.format(monitor_item)
        print monitor_name
        monitors.append(importlib.import_module(monitor_name))
    return monitors

def main():

    reply = threading.Thread(target=req_repl)
    reply.start()
    reply.join()

if __name__ == '__main__':
    main()
