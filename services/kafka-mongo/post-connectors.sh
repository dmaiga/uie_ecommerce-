#!/bin/sh


echo "Registering Mongo Sink Connector..."
curl -i -X POST -H "Content-Type: application/json" --data @/scripts/mongo-sink.json http://kafka-connect:8083/connectors

echo "Registering HDFS Sink Connector..."
curl -i -X POST -H "Content-Type: application/json" --data @/scripts/hdfs-sink.json http://kafka-connect:8083/connectors
