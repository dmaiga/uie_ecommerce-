-- Base de données
CREATE DATABASE IF NOT EXISTS uie_ecommerce;
USE uie_ecommerce;

-- Tables externes inchangées
CREATE EXTERNAL TABLE IF NOT EXISTS transactions (
  transaction_id STRING,
  user_id STRING,
  product STRING,
  amount DOUBLE,
  `timestamp` STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '\"',
  "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/transactions/';

CREATE EXTERNAL TABLE IF NOT EXISTS comments (
  comment_id STRING,
  user_id STRING,
  product STRING,
  comment STRING,
  rating INT,
  `timestamp` STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '\"',
  "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/comments/';

-- Tables KPI partitionnées
-- total_spent
CREATE EXTERNAL TABLE IF NOT EXISTS kpi_total_spent (
  product STRING,
  total_spent DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '\"',
  "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_total_spent/';

-- nb_transactions
CREATE EXTERNAL TABLE IF NOT EXISTS kpi_nb_transactions (
  product STRING,
  nb_transactions BIGINT
)


ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '\"',
  "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_nb_transactions/';

-- avg_rating
CREATE EXTERNAL TABLE IF NOT EXISTS kpi_avg_rating (
  product STRING,
  avg_rating DOUBLE
)

ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '\"',
  "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_avg_rating/';

