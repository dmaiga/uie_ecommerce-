#!/bin/bash
cd scripts
echo "Waiting for Kafka Connect to be ready..."
until curl -s http://localhost:8083/ > /dev/null; do
  echo "Still waiting for Kafka Connect..."
  sleep 5
done

echo "Kafka Connect is up! Registering Mongo Sink Connector..."
curl -X POST -H "Content-Type: application/json" --data @mongo-sink.json http://localhost:8083/connectors

echo "Registering HDFS Sink Connector..."
curl -X POST -H "Content-Type: application/json" --data @hdfs-sink.json http://localhost:8083/connectors
