-- Base de données
CREATE DATABASE IF NOT EXISTS uie_ecommerce;
USE uie_ecommerce;

-- Tables externes inchangées
CREATE EXTERNAL TABLE IF NOT EXISTS transactions (
  transaction_id STRING,
  user_id STRING,
  product STRING,
  amount STRING,
  `timestamp` STRING
)

STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/transactions/';

CREATE EXTERNAL TABLE IF NOT EXISTS comments (
  comment_id STRING,
  user_id STRING,
  product STRING,
  comment STRING,
  rating string,
  `timestamp` STRING
)

STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/comments/';

-- Tables KPI partitionnées
-- Supprimer les anciennes tables
DROP TABLE IF EXISTS uie_ecommerce.kpi_nb_transactions;
DROP TABLE IF EXISTS uie_ecommerce.kpi_total_spent;
DROP TABLE IF EXISTS uie_ecommerce.kpi_avg_rating;

-- Créer la nouvelle table : nombre de transactions
CREATE EXTERNAL TABLE uie_ecommerce.kpi_nb_transactions (
    product STRING,
    nb_transactions BIGINT,
    kpi_date DATE
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_nb_transactions/';

-- Créer la nouvelle table : total dépensé
CREATE EXTERNAL TABLE uie_ecommerce.kpi_total_spent (
    product STRING,
    total_spent DOUBLE,
    kpi_date DATE
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_total_spent/';

-- Créer la nouvelle table : note moyenne
CREATE EXTERNAL TABLE uie_ecommerce.kpi_avg_rating (
    product STRING,
    avg_rating DOUBLE,
    kpi_date DATE
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/data/kpis/kpi_avg_rating/';
