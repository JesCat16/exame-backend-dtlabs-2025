from rabbitmq import RabbitMQ
import requests
import sys
import json

url = "http://127.0.0.1:8000/data/"

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    jsonSend = json.loads(body.decode())
    response = requests.post(url, json=jsonSend)


def main():
    rabbitmq = RabbitMQ()
    try:
        print("Connection to RabbitMQ established successfully.")
        rabbitmq.consume(queue_name='servers', callback=callback)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)
    finally:
        rabbitmq.close()

main()