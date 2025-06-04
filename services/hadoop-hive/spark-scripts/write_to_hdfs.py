from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("WriteToHDFS") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
df = spark.read.csv("file:///opt/spark-data/sim_data.csv", header=True, inferSchema=True)
df.write.mode("overwrite").parquet("hdfs://namenode:8020/user/spark/sim_data_parquet")

spark.stop()
