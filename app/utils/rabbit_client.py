import json
import logging
import pika
from app.infrastructure.config import settings

logger = logging.getLogger(__name__)

RABBIT_URL = settings.RABBITMQ_URL

def get_channel():
    connection = pika.BlockingConnection(
        pika.URLParameters(RABBIT_URL)
    )
    channel = connection.channel()
    return connection, channel


def publish(queue: str, message: dict):
    try:
        conn, channel = get_channel()

        channel.queue_declare(
            queue=queue,
            durable=True
        )

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message).encode("utf-8")
        )

        conn.close()

    except Exception as e:
        logger.error(f"Rabbit publish failed: {e}")