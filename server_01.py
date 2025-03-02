from rabbitmq import RabbitMQ
import jsonpickle
import datetime
import random
import time

date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

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

def publish_test_message():
        rabbitmq = RabbitMQ()
        try:
            rabbitmq.publish(queue_name='server_01', message=message)
            print("Test message published successfully.")
        except Exception as e:
            print(f"Failed to publish test message: {e}")
        finally:
            rabbitmq.close()
    
while True:
    data = DataIot("aaaaaaaa",date, round(random.uniform(20,40),1),round(random.uniform(0,100),1),round(random.uniform(110,220),1),round(random.uniform(1,10),1))
    message = jsonpickle.dumps(data.to_dict())

    publish_test_message()
    time.sleep(1)