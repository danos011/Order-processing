from confluent_kafka import Consumer, Producer
from dotenv import load_dotenv

import json
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')
KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET')

consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': KAFKA_AUTO_OFFSET_RESET
})
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

consumer.subscribe(['orders'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error(msg.error())
            continue

        order = json.loads(msg.value().decode('utf-8'))
        status = 'confirmed' if order.get('quantity', 0) > 0 else 'rejected'
        result = {'order_id': order.get('order_id'), 'status': status}

        logging.info(f'Processing order {order.get("order_id")}: {status}')

        producer.produce('notifications', value=json.dumps(result))
        producer.flush()
finally:
    consumer.close()
