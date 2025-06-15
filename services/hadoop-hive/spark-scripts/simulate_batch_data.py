# simulate_batch_data.py
# -*- coding: utf-8 -*-
import csv
import random
import uuid
from datetime import datetime, timezone
import os
import glob
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
    # 🔄 Nettoyer les anciens fichiers .csv dans le dossier
    for file in glob.glob(os.path.join(DATA_DIR, "*.csv")):
        os.remove(file)

    transactions = [generate_transaction() for _ in range(100)]
    comments = [generate_comment() for _ in range(100)]

    # ✅ Sauvegarde avec noms fixes
    with open(os.path.join(DATA_DIR, "transactions.csv"), "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

    with open(os.path.join(DATA_DIR, "comments.csv"), "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=comments[0].keys())
        writer.writeheader()
        writer.writerows(comments)

    print("✅ CSV batch written to", DATA_DIR)

if __name__ == "__main__":
    main()
