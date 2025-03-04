import zmq
import msgpack
import requests
import json
import time

url = "http://127.0.0.1:8000/health"

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://127.0.0.1:5557")

while True:
    servers = requests.get(url).text
    listjsons = servers.split()
    listServers = []
    for serv in listjsons:
        jsonS = json.loads(serv)
        for item in jsonS:
            print(item)
            activation = {"server_ulid": item.get("server_ulid"), "server_name": item.get("server_name")}
            serialize_object = msgpack.packb(activation)
            socket.send(serialize_object)
    time.sleep(300)
    

