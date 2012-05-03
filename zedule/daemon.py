import datetime
import time
import threading

import bson
import pymongo
import pymongo.objectid
import zmq


monitor_threads = {}
context = zmq.Context()

def get_items_collection():
    mongo = pymongo.Connection('33.33.33.10')
    return mongo.zedule.items

def req_repl():
    "Handle incoming ZMQ requests"
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5001')
    collection = get_items_collection()

    while True:
        receive(socket, collection)

def receive(socket, collection):
    "Receive a single event from the socket"
    method, headers, data = socket.recv_multipart()
    headers = bson.BSON(headers)
    headers = headers.decode()

    sched_id = pymongo.objectid.ObjectId.from_datetime(headers['time'])
    doc = {
        'time': sched_id,
        'data': data,
        'key': headers['key'],
    }

    id_ = collection.insert(doc, safe=True)
    socket.send_multipart(['200', str(id_)])

def publisher():
    "Publish overdue items from the DB"
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:5002')
    collection = get_items_collection()
    import datetime
    while True:
        publish_one(socket, collection)

def publish_one(socket, collection):
    "Pull 1 item out of the DB and publish it"
    now = datetime.datetime.utcnow()
    now_id = pymongo.objectid.ObjectId.from_datetime(now)
    query = {'time': {'$lte': now_id}}
    item = collection.find_one(query)
    if not item:
        time.sleep(1)
        return

    socket.send_multipart([str(item['key']), bson.BSON.encode(item)])
    collection.remove({'_id': item['_id']})

def main():
    reply = threading.Thread(target=req_repl)
    reply.start()
    pub = threading.Thread(target=publisher)
    pub.start()
    reply.join()
    #pub.join()

if __name__ == '__main__':
    main()
