#!/bin/bash

set -e  # Arrêter le script si une commande échoue
set -o pipefail

cd /spark-scripts || exit 1

echo "🔁 Début du pipeline à $(date)"

# 1. Génération des données simulées
echo "📦 Simulation des données..."
python3 simulate_batch_data.py || { echo "❌ Échec de la simulation"; exit 1; }

# 2. Ingestion vers HDFS
echo "🚀 Ingestion dans HDFS..."
spark-submit ingest_batch_to_hdfs.py || { echo "❌ Échec de l'ingestion"; exit 1; }

# 3. Traitement Spark : transformation + KPIs
echo "🧮 Traitement Spark..."
spark-submit process_batch_hdfs_to_hive.py || { echo "❌ Échec du traitement KPIs"; exit 1; }

# 4. Mise à jour des partitions Hive
echo "🛠️  Réparation des partitions Hive..."
hive -e "
USE uie_ecommerce;
MSCK REPAIR TABLE kpi_total_spent;
MSCK REPAIR TABLE kpi_nb_transactions;
MSCK REPAIR TABLE kpi_avg_rating;
" || { echo "❌ Échec du MSCK REPAIR"; exit 1; }

echo "✅ Pipeline terminé à $(date)"
