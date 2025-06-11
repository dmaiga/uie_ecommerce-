import os
import time
from datetime import datetime

while True:
    print(f"🔄 Démarrage du pipeline à {datetime.now().isoformat()}")
    os.system("python3 /spark-scripts/simulate_batch_data.py")
    os.system("python3 /spark-scripts/ingest_batch_to_hdfs.py")
    os.system("/opt/spark/bin/spark-submit /spark-scripts/process_batch_hdfs_to_hive.py")
    os.system('hive -e "USE uie_ecommerce; MSCK REPAIR TABLE kpi_total_spent; MSCK REPAIR TABLE kpi_nb_transactions; MSCK REPAIR TABLE kpi_avg_rating;"')
    print("✅ Pipeline exécuté. Pause de 5 minutes.\n")
    time.sleep(300)  # 5 minutes
