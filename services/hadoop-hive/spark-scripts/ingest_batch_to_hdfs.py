# ingest_batch_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date

spark = SparkSession.builder.appName("IngestBatchToHDFS").getOrCreate()

transactions_path = "/opt/spark-data/batch/transactions_*.csv"
comments_path = "/opt/spark-data/batch/comments_*.csv"

# Lecture
transactions_df = spark.read.option("header", "true").option("inferSchema", "true").csv(transactions_path)
comments_df = spark.read.option("header", "true").option("inferSchema", "true").csv(comments_path)

# Ajout de colonne de date d’ingestion
transactions_df = transactions_df.withColumn("ingestion_date", current_date())
comments_df = comments_df.withColumn("ingestion_date", current_date())

# Ecriture dans HDFS 
transactions_df.write.mode("append").parquet(
    "hdfs://namenode:8020/user/hive/warehouse/data/transactions/"
)
comments_df.write.mode("append").parquet(
    "hdfs://namenode:8020/user/hive/warehouse/data/comments/"
)

print("✅ Ingestion terminée dans HDFS avec colonne ingestion_date.")
