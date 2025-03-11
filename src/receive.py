from src.config import RABBIT_MQ_INPUT_QUEUE
from src.rabbitmq.connection import RabbitMQConsumer


def callback(ch, method, properties, body):
    print(f"[x] Received {body.decode()}")


if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.consume_message(queue_name=RABBIT_MQ_INPUT_QUEUE, callback=callback)
