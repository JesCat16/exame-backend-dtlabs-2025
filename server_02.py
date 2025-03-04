from rabbitmq import RabbitMQ
import jsonpickle
import datetime
import random
import time
import zmq
import msgpack

#Pull messages from connection
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://127.0.0.1:5557")

server_name = " "
server_ulid = " "

#Get messages and see if server_name is the same as this server
while server_name != "server_02":
    received_object = socket.recv()
    deserialized_object = msgpack.unpackb(received_object)
    server_name = deserialized_object.get("server_name")

#If the name is the same it will save his ulid to send the data to consumer
if server_name == "server_02":
    server_ulid = deserialized_object.get("server_ulid")

# Establishes data structure
class DataIot():
    server_ulid: str
    timestamp: str
    temperature: float
    humidity:float
    voltage: float
    current: float
    def __init__(self,server_ulid,timestamp,temp,humid,volt,current):
        self.server_ulid = server_ulid
        self.timestamp = timestamp
        self.temperature = temp
        self.humidity = humid
        self.voltage = volt
        self.current = current
    def to_dict(self):
        return {"server_ulid": self.server_ulid,
                "timestamp": self.timestamp,
                "temperature": self.temperature,
                "humidity": self.humidity,
                "voltage": self.voltage,
                "current": self.current}

def publish_IoT_Data():
        #Creates a connection
        rabbitmq = RabbitMQ()
        try:
            #Publish messages to queue
            rabbitmq.publish(queue_name='server_02', message=message)
            print("Test message published successfully.")
        except Exception as e:
            print(f"Failed to publish test message: {e}")
        finally:
            rabbitmq.close()
#If he now have the ulid saved, he will start sending the data he have through RabbitMQ
if server_ulid != " ":
    while True:
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        #Create data
        data = DataIot(server_ulid,date, round(random.uniform(20,40),1),round(random.uniform(0,100),1),round(random.uniform(110,220),1),round(random.uniform(1,10),1))
        #Package the data message
        message = jsonpickle.dumps(data.to_dict())
        #Publish data
        publish_IoT_Data()
        time.sleep(5)