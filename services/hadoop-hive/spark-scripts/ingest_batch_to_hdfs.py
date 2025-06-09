# scripts/ingest_batch_to_hdfs.py

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("IngestBatchToHDFS").getOrCreate()

# Lecture des CSV dans le conteneur
transactions_path = "/opt/spark-data/batch/transactions_*.csv"
comments_path = "/opt/spark-data/batch/comments_*.csv"

# Ingestion des transactions
transactions_df = spark.read.option("header", "true").option("inferSchema", "true").csv(transactions_path)
transactions_df.write.mode("append").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/transactions/",
    header=True
)

# Ingestion des commentaires
comments_df = spark.read.option("header", "true").option("inferSchema", "true").csv(comments_path)
comments_df.write.mode("append").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/comments/",
    header=True
)

print("✅ Ingestion terminée dans HDFS.")
