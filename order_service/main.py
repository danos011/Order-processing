from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer
from dotenv import load_dotenv

import json
import logging
import os

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')

app = FastAPI()

producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

@app.post("/orders")
def create_order(order: dict):
    try:
        data = json.dumps(order)
        producer.produce('orders', value=data, callback=delivery_report)
        producer.flush()
        return {"message": "Order received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
