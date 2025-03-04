from rabbitmq import RabbitMQ
import requests
import sys
import json
import time
import threading

url = "http://127.0.0.1:8000/data/"

def createQueue01():
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.publish(queue_name='server_01', message=None)
        print("Test message published successfully.")
    except Exception as e:
            print(f"Failed to publish test message: {e}")
    finally:
        rabbitmq.close()

def createQueue02():
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.publish(queue_name='server_02', message=None)
        print("Test message published successfully.")
    except Exception as e:
            print(f"Failed to publish test message: {e}")
    finally:
        rabbitmq.close()

def createQueue03():
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.publish(queue_name='server_03', message=None)
        print("Test message published successfully.")
    except Exception as e:
            print(f"Failed to publish test message: {e}")
    finally:
        rabbitmq.close()


def callback(ch, method, properties, body):
    jsonSend = json.loads(body.decode())
    response = requests.post(url, json=jsonSend)

def consume_server_01():
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.consume(queue_name='server_01', callback=callback)
        time.sleep(1)

    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)

def consume_server_02():
    rabbitmq = RabbitMQ()
    try:
        print("Connection to RabbitMQ established successfully.")
        rabbitmq.consume(queue_name='server_02', callback=callback)
        time.sleep(1)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)

def consume_server_03():
    rabbitmq = RabbitMQ()
    try:
        print("Connection to RabbitMQ established successfully.")
        rabbitmq.consume(queue_name='server_03', callback=callback)
        time.sleep(1)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)

createQueue01()
createQueue02()
createQueue03()

cosumer01 = threading.Thread(target=consume_server_01)
cosumer02 = threading.Thread(target=consume_server_02)
cosumer03 = threading.Thread(target=consume_server_03)

cosumer01.start()
cosumer02.start()
cosumer03.start()