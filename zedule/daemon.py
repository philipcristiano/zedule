import time

import threading

import dateutil.parser
import pymongo
import bson
import pymongo.objectid
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
        headers = bson.BSON(headers)
        print type(headers)
        headers = headers.to_dict()
        print headers

        #scheduled_for = dateutil.parser.parse(headers['time'])
        sched_id = pymongo.objectid.ObjectId.from_datetime(headers['time'])
        doc = {
            'time': sched_id,
            'data': data,
            'key': headers['key'],
        }

        print doc
        id_ = collection.insert(doc, safe=True)
        print id_, sched_id
        socket.send_multipart(['200', str(id_)])

def publisher():
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:5002')
    mongo = pymongo.Connection('33.33.33.10')
    db = mongo.zedule
    collection = db.items
    import datetime
    while True:
        now = datetime.datetime.utcnow()
        now_id = pymongo.objectid.ObjectId.from_datetime(now)
        query = {'time': {'$lte': now_id}}
        print 'looking for', now_id
        item = collection.find_one(query)
        print 'found', item
        if not item:
            time.sleep(5)
            continue

        socket.send_multipart([str(item['key']), bson.BSON.encode(item)])
        collection.remove({'_id': item['_id']})


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
    pub = threading.Thread(target=publisher)
    pub.start()
    reply.join()

if __name__ == '__main__':
    main()
