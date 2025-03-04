import zmq
import msgpack
import requests
import json
import time
#This worker is used to activate servers ability to push data
#url to connect to API
url = "http://127.0.0.1:8000/health"

#Publish messages 
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://127.0.0.1:5557")

while True:
    #Get activate servers list
    servers = requests.get(url).text
    if servers == None:
        continue
    else:
        listjsons = servers.split()
        for serv in listjsons:
            #See each server on the list and send it's ulid to active servers
            jsonS = json.loads(serv)
            for item in jsonS:
                activation = {"server_ulid": item.get("server_ulid"), "server_name": item.get("server_name")}
                #package the message 
                serialize_object = msgpack.packb(activation)
                #Send message to activate server message publish
                socket.send(serialize_object)
                time.sleep(10)
    #Worker will pass through this process every 5 minutes
    time.sleep(300)
    

