# simulate_batch_data.py
# -*- coding: utf-8 -*-
import csv
import random
import uuid
from datetime import datetime, timezone
import os
from faker import Faker

fake = Faker()
DATA_DIR = "/opt/spark-data/batch"
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCTS = ['laptop', 'headphones', 'keyboard', 'monitor', 'mouse', 'webcam', 'microphone', 'charger', 'tablet']
USERS = ["user_{}".format(i) for i in range(1, 51)]  

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "product": random.choice(PRODUCTS),
        "amount": round(random.uniform(20.0, 1000.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def generate_comment():
    return {
        "comment_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "product": random.choice(PRODUCTS),
        "comment": fake.sentence(nb_words=8),
        "rating": random.randint(1, 5),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    transactions = [generate_transaction() for _ in range(100)]
    comments = [generate_comment() for _ in range(100)]

    with open(os.path.join(DATA_DIR, f"transactions_{now}.csv"), "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

    with open(os.path.join(DATA_DIR, f"comments_{now}.csv"), "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=comments[0].keys())
        writer.writeheader()
        writer.writerows(comments)

    print(f"✅ CSV batch written to {DATA_DIR} (timestamp: {now})")

if __name__ == "__main__":
    main()
