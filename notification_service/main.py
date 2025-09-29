from confluent_kafka import Consumer
from dotenv import load_dotenv

import os
import logging.config

load_dotenv()

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('notification_service')

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')
KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET')

consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': KAFKA_AUTO_OFFSET_RESET
})

consumer.subscribe(['notifications'])

logger.info('Сервис запущен и готов к обработке сообщений')

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(msg.error())
            print(msg.error())
            continue

        logger.info(f'Notification received: {msg.value().decode("utf-8")}')
finally:
    consumer.close()
