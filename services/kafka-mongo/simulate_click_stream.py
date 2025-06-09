from faker import Faker
import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

fake = Faker()
KAFKA_BROKER = "kafka:29092"
TOPIC = "user_clicks"

ACTIONS = ["view", "add_to_cart", "wishlist", "remove", "click"]

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_click_event():
    return {
        "user_id": fake.uuid4(),
        "username": fake.user_name(),
        "product": fake.word(ext_word_list=["laptop", "headphones", "keyboard", "monitor", "mouse"]),
        "timestamp": datetime.utcnow().isoformat(),
        "action": random.choice(ACTIONS),
        "session_id": fake.uuid4()
    }

def main():
    while True:
        event = generate_click_event()
        producer.send(TOPIC, value=event)
        print(f"Sent: {event}")
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    main()
