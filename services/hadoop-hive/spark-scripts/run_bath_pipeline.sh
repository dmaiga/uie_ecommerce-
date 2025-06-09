#!/bin/bash
echo "[`date`] ▶ Lancement du pipeline batch..."

python3 /spark-scripts/simulate_batch_data.py
/spark/bin/spark-submit /spark-scripts/ingest_batch_to_hdfs.py
/spark/bin/spark-submit /spark-scripts/process_batch_hdfs_to_hive.py

echo "[`date`] ✅ Pipeline terminé."
