import pika
import os

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.connection = None
        self.channel = None
        self.connect()

    def get_all_queues(self):
        url = "http://localhost:15672/api/queues"
        auth = (self.user, self.password)
        headers = {"Content-Type": "application/json"}
    
    def create_queue(self, queue_name):
        if not self.channel:
            raise Exception("Connection is not established.")
        
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            print(f"Queue '{queue_name}' created.")
        except Exception as e:
            print(f"Error declaring the queue: {e}")

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        if not self.channel:
            raise Exception("Connection is not established.")
        
        try:
            # Declare the queue
            self.create_queue(queue_name)
            
            # Publish the message
            self.channel.basic_publish(
                exchange='',  # Default exchange (direct)
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            print(f"Sent message to queue {queue_name}: {message}")
        except Exception as e:
            print(f"Error declaring or publishing to the queue: {e}")