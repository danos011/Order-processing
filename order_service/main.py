from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer
from dotenv import load_dotenv

import json
import logging.config
import os

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

app = FastAPI()

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('order_service')

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})


def delivery_report(err, msg):
    if err:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')


logger.info('Сервис запущен и готов к обработке сообщений')


@app.post("/orders")
def create_order(order: dict):
    try:
        data = json.dumps(order)
        producer.produce('orders', value=data, callback=delivery_report)
        producer.flush()
        return {"message": "Order received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
