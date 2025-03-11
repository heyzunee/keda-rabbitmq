from datetime import datetime

from src.config import *
from src.rabbitmq.connection import RabbitMQProducer

if __name__ == "__main__":
    message = {
        "request_id": "123",
        "request": "This is a test request",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    publisher = RabbitMQProducer()
    publisher.publish_message(routing_key=RABBIT_MQ_INPUT_QUEUE, body=message)
