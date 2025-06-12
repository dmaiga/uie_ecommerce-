import requests
import json

ranger_url = "http://ranger-admin:6080/service/public/v2/api/service"

headers = {
    "Content-Type": "application/json",
}

auth = ('admin', 'admin123')  # à adapter si tu changes les identifiants

# === HIVE ===
ranger_hive_service = {
    "isEnabled": True,
    "configs": {
        "username": "hive",
        "password": "hive",
        "jdbc.driverClassName": "org.apache.hive.jdbc.HiveDriver",
        "jdbc.url": "jdbc:hive2://hive-server:10000"
    },
    "description": "Hive service",
    "name": "ranger-hive",
    "type": "hive"
}

# === TRINO ===
ranger_trino_service = {
    "isEnabled": True,
    "configs": {
        "username": "trino",
        "password": "trino",
        "jdbc.driverClassName": "io.trino.jdbc.TrinoDriver",
        "jdbc.url": "jdbc:trino://trino:8080"
    },
    "description": "Trino service",
    "name": "ranger-trino",
    "type": "trino"
}

# Ajouter les services à Ranger
for service in [ranger_hive_service, ranger_trino_service]:
    response = requests.post(ranger_url, headers=headers, auth=auth, data=json.dumps(service))
    print(f"Creating service {service['name']}: {response.status_code} - {response.text}")
