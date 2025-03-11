import json
import logging
import time
from typing import Dict

import pika
from pika.exceptions import AMQPConnectionError

from ..config import *

logger = logging.getLogger(PROJECT_NAME)


class RabbitMQClient:
    def __init__(self):
        self._init_connection_parameters()
        self._connect()

    def _connect(self):
        attempts = 0
        while True:
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    break
            except (AMQPConnectionError, Exception) as e:
                time.sleep(5)
                attempts += 1
                if attempts == 20:
                    raise AMQPConnectionError(e)

    def _init_connection_parameters(self):
        self.credentials = pika.PlainCredentials(username=RABBIT_MQ_USERNAME, password=RABBIT_MQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            host=RABBIT_MQ_HOST,
            port=int(RABBIT_MQ_PORT),
            virtual_host="/",
            credentials=self.credentials,
        )

    def check_connection(self):
        if not self.connection or self.connection.is_closed:
            self._connect()

    def close(self):
        self.channel.close()
        self.connection.close()


class RabbitMQConsumer(RabbitMQClient):
    def __init__(self):
        super().__init__()
        self.channel_tag = None

    def consume_message(self, queue_name, callback):
        try:
            self.check_connection()
            self.channel.queue_declare(queue=queue_name, passive=True)
            self.channel_tag = self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            logger.debug("[*] Waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Error consuming message: {e}")
            raise e


class RabbitMQProducer(RabbitMQClient):
    def __init__(self):
        super().__init__()

    def publish_message(
        self,
        routing_key: str,
        body: Dict,
        exchange_name: str = "",
    ):
        try:
            self.check_connection()
            self.channel.queue_declare(queue=routing_key, passive=True)
            body = json.dumps(body)
            self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
            logger.debug(f"Sent message. Exchange: {exchange_name}, Routing Key: {routing_key}, Body: {body[:128]}")
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            raise e
