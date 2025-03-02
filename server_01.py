from rabbitmq import RabbitMQ
import jsonpickle
import datetime
import random
import time
import zmq
import msgpack

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://127.0.0.1:5555")

received_object = socket.recv()
deserialized_object = msgpack.unpackb(received_object)
print(deserialized_object)

date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
server_ulid = " "
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
        rabbitmq = RabbitMQ()
        try:
            rabbitmq.publish(queue_name='server_01', message=message)
            print("Test message published successfully.")
        except Exception as e:
            print(f"Failed to publish test message: {e}")
        finally:
            rabbitmq.close()

if server_ulid != " ":
    while True:
        data = DataIot(server_ulid,date, round(random.uniform(20,40),1),round(random.uniform(0,100),1),round(random.uniform(110,220),1),round(random.uniform(1,10),1))
        message = jsonpickle.dumps(data.to_dict())
        publish_IoT_Data()
        time.sleep(1)