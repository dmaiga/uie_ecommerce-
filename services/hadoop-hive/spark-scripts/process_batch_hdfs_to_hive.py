from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

import os

spark = SparkSession.builder \
    .appName("KPIProcessToHDFS") \
    .getOrCreate()

# Lecture des fichiers transaction et commentaires depuis HDFS
transactions_df = spark.read.option("header", "true").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/transactions/"
)
comments_df = spark.read.option("header", "true").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/comments/"
)

# Casting
transactions_df = transactions_df.withColumn("amount", col("amount").cast("double")) \
                                 .withColumn("partition_date", to_date("timestamp"))
comments_df = comments_df.withColumn("rating", col("rating").cast("int")) \
                         .withColumn("partition_date", to_date("timestamp"))

transactions_df.createOrReplaceTempView("transactions_temp")
comments_df.createOrReplaceTempView("comments_temp")

# KPI 1 : total_spent
total_spent = spark.sql("""
    SELECT product, ROUND(SUM(amount), 2) AS total_spent, TO_DATE(MAX(timestamp)) AS partition_date
    FROM transactions_temp
    GROUP BY product
""")

# KPI 2 : nb_transactions
tx_count = spark.sql("""
    SELECT product, COUNT(*) AS nb_transactions, TO_DATE(MAX(timestamp)) AS partition_date
    FROM transactions_temp
    GROUP BY product
""")

# KPI 3 : avg_rating
avg_rating = spark.sql("""
    SELECT product, ROUND(AVG(rating), 2) AS avg_rating, TO_DATE(MAX(timestamp)) AS partition_date
    FROM comments_temp
    GROUP BY product
""")

# Sauvegarde en CSV avec partition
total_spent.write.mode("append").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_total_spent/",
    header=True
)
tx_count.write.mode("append").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_nb_transactions/",
    header=True
)
avg_rating.write.mode("append").csv(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_avg_rating/",
    header=True
)

print("✅ DATA Processing Done.")
