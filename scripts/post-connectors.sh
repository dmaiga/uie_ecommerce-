#!/bin/bash

echo "Waiting for Kafka Connect to be ready..."
sleep 10

echo "Posting MongoDB sink connector"
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @kafka/connect/configs/connect-mongo-sink.json
