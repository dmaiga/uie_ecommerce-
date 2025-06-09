
# -*- coding: utf-8 -*-
import csv
import random
import uuid
from datetime import datetime
import os




DATA_DIR = "/opt/spark-data/batch"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

PRODUCTS = ['laptop', 'headphones', 'keyboard', 'monitor', 'mouse']
COMMENTS = ['Great product!', 'Not satisfied', 'Will buy again', 'Too expensive', 'Excellent!']
USERS = ["user_{}".format(i) for i in range(1, 21)]

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "product": random.choice(PRODUCTS),
        "amount": round(random.uniform(20.0, 500.0), 2),
        "timestamp": datetime.utcnow().isoformat()
    }

def generate_comment():
    return {
        "comment_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "product": random.choice(PRODUCTS),
        "comment": random.choice(COMMENTS),
        "rating": random.randint(1, 5),
        "timestamp": datetime.utcnow().isoformat()
    }

def main():
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    transactions = [generate_transaction() for _ in range(15)]
    comments = [generate_comment() for _ in range(15)]

    # Transactions
    with open(os.path.join(DATA_DIR, "transactions_{}.csv".format(now)), "wb") as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

    # Comments
    with open(os.path.join(DATA_DIR, "comments_{}.csv".format(now)), "wb") as f:
        writer = csv.DictWriter(f, fieldnames=comments[0].keys())
        writer.writeheader()
        writer.writerows(comments)

    print("✅ CSV batch written to {} (timestamp: {})".format(DATA_DIR, now))

if __name__ == "__main__":
    main()
