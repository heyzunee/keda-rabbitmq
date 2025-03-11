"""Config file"""

import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "keda-rabbitmq"
VERSION = "1.0"

RABBIT_MQ_HOST = os.environ["RABBIT_MQ_HOST"]
RABBIT_MQ_PORT = os.environ["RABBIT_MQ_PORT"]
RABBIT_MQ_USERNAME = os.environ["RABBIT_MQ_USERNAME"]
RABBIT_MQ_PASSWORD = os.environ["RABBIT_MQ_PASSWORD"]
RABBIT_MQ_INPUT_QUEUE = os.environ["RABBIT_MQ_INPUT_QUEUE"]
