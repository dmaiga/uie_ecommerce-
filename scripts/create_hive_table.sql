CREATE EXTERNAL TABLE IF NOT EXISTS sim_data (
  id INT,
  name STRING,
  age INT
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/spark/sim_data_parquet';
