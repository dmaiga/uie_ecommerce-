# scripts/simulate_click_stream.py

import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
TOPIC = "user_clicks"

PRODUCTS = ['laptop', 'headphones', 'keyboard', 'monitor', 'mouse']
USERS = [f"user_{i}" for i in range(1, 21)]

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_click_event():
    return {
        "user_id": random.choice(USERS),
        "product": random.choice(PRODUCTS),
        "timestamp": datetime.utcnow().isoformat(),
        "action": random.choice(["view", "add_to_cart", "wishlist", "remove", "click"])
    }

def main():
    while True:
        event = generate_click_event()
        producer.send(TOPIC, value=event)
        print(f"Sent: {event}")
        time.sleep(random.uniform(0.5, 2.0)) 
if __name__ == "__main__":
    main()
