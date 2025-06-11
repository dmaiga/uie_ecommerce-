# kpi_process_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, current_date

spark = SparkSession.builder.appName("KPIProcessToHDFS").getOrCreate()

transactions_df = spark.read.parquet("hdfs://namenode:8020/user/hive/warehouse/data/transactions/")
comments_df = spark.read.parquet("hdfs://namenode:8020/user/hive/warehouse/data/comments/")

# Casts
transactions_df = transactions_df \
    .withColumn("amount", col("amount").cast("double")) \
    .withColumn("transaction_date", to_date("timestamp"))

comments_df = comments_df \
    .withColumn("rating", col("rating").cast("int")) \
    .withColumn("comment_date", to_date("timestamp"))

# Vues temporaires
transactions_df.createOrReplaceTempView("transactions_temp")
comments_df.createOrReplaceTempView("comments_temp")

# KPI 1
total_spent = spark.sql("""
    SELECT product, ROUND(SUM(amount), 2) AS total_spent, TO_DATE(MAX(timestamp)) AS kpi_date
    FROM transactions_temp
    GROUP BY product
""")

# KPI 2
tx_count = spark.sql("""
    SELECT product, COUNT(*) AS nb_transactions, TO_DATE(MAX(timestamp)) AS kpi_date
    FROM transactions_temp
    GROUP BY product
""")

# KPI 3
avg_rating = spark.sql("""
    SELECT product, ROUND(AVG(CAST(rating AS DOUBLE)), 2) AS avg_rating, TO_DATE(MAX(timestamp)) AS kpi_date
    FROM comments_temp
    WHERE rating IS NOT NULL
    GROUP BY product
""")

# Sauvegarde 
total_spent.write.mode("append").parquet(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_total_spent/"
)

tx_count.write.mode("append").parquet(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_nb_transactions/"
)

avg_rating.write.mode("append").parquet(
    "hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_avg_rating/"
)

print("✅ KPIs générés avec kpi_date et enregistrés dans HDFS.")
