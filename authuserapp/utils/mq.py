import pika
import json
import os

def send_inventory_update_notif(payload):
    print("Sending message to RabbitMQ:", payload) 
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
            credentials=pika.PlainCredentials(
                username=os.getenv("RABBITMQ_DEFAULT_USER", "user"),
                password=os.getenv("RABBITMQ_DEFAULT_PASS", "pass")
            )
        ))
        channel = connection.channel()

        channel.queue_declare(queue='inventory_updates', durable=True)

        message = json.dumps(payload)
        channel.basic_publish(
            exchange='',
            routing_key='inventory_updates',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
    except Exception as e:
        print("Unsuccessful RabbitMQ message:", e)
