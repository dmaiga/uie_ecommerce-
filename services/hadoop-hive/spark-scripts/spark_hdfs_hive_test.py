from pyspark.sql import SparkSession

# 1. Démarrer Spark avec support Hive
spark = SparkSession.builder \
    .appName("Test Spark-HDFS-Hive") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# 2. Lire le fichier CSV depuis HDFS
df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://namenode:8020/user/spark/input/sim_data.csv")

# 3. Afficher les 5 premières lignes
print("==== Aperçu des données ====")
df.show(5)

# 4. Effectuer un traitement simple : calculer moyenne si colonne numérique "value"
if 'value' in df.columns:
    df.groupBy().avg("value").show()

# 5. Sauvegarder en tant que table Hive externe
df.write.mode("overwrite").saveAsTable("default.sim_data")

print("✅ Table Hive 'default.sim_data' créée avec succès !")

# 6. Vérifier que la table est bien créée
spark.sql("SHOW TABLES").show()
spark.sql("SELECT * FROM sim_data LIMIT 5").show()

spark.stop()
