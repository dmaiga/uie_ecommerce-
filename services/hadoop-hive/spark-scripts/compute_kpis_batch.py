import os

def repair_hive_tables():
    print("🔄 Réparation des partitions Hive...")
    repair_commands = """
    hive -e "
    USE uie_ecommerce;
    MSCK REPAIR TABLE kpi_total_spent;
    MSCK REPAIR TABLE kpi_nb_transactions;
    MSCK REPAIR TABLE kpi_avg_rating;
    "
    """
    os.system(repair_commands)
    print("✅ Réparation des partitions Hive terminée.")

# Appeler la fonction après l’écriture HDFS
repair_hive_tables()
