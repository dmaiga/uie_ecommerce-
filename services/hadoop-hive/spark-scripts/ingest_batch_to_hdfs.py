# ingest_batch_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date
import os

spark = SparkSession.builder.appName("IngestBatchToHDFS").getOrCreate()

transactions_path = "/opt/spark-data/batch/transactions.csv"
comments_path = "/opt/spark-data/batch/comments.csv"

if not os.path.exists(transactions_path):
    print("❌ Fichier transactions.csv introuvable.")
    exit(1)
if not os.path.exists(comments_path):
    print("❌ Fichier comments.csv introuvable.")
    exit(1)

transactions_df = spark.read.option("header", "true").option("inferSchema", "true").csv(transactions_path)
comments_df = spark.read.option("header", "true").option("inferSchema", "true").csv(comments_path)

transactions_df = transactions_df.withColumn("ingestion_date", current_date())
comments_df = comments_df.withColumn("ingestion_date", current_date())

transactions_df.write.mode("append").parquet("hdfs://namenode:8020/user/hive/warehouse/data/transactions/")
comments_df.write.mode("append").parquet("hdfs://namenode:8020/user/hive/warehouse/data/comments/")

# Suppression des fichiers
for f in [transactions_path, comments_path]:
    try:
        os.remove(f)
        print(f"🗑️ Fichier supprimé : {f}")
    except Exception as e:
        print(f"⚠️ Erreur suppression {f} : {e}")

print("✅ Ingestion terminée dans HDFS avec colonne ingestion_date.")
