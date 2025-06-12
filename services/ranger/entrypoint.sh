#!/bin/bash
set -e

SETUP_FLAG="${RANGER_HOME}/.setupDone"

if [ ! -f "$SETUP_FLAG" ]; then
  echo "[RANGER] First-time setup..."
  cd ${RANGER_HOME}/admin
  ./setup.sh || { echo "❌ Ranger setup failed"; exit 1; }
  touch "$SETUP_FLAG"
fi

echo "[RANGER] Starting Ranger Admin..."
cd ${RANGER_HOME}/admin
./ews/ranger-admin-services.sh start

# Attente de disponibilité
echo "[RANGER] Waiting 30s for Ranger Admin to boot..."
sleep 30

# Création des services via Python
python3 ${RANGER_SCRIPTS}/create-ranger-services.py || echo "⚠️ Ranger services script error"

# Garder le conteneur actif
RANGER_PID=$(ps -ef | grep -v grep | grep -i 'org.apache.ranger.server.tomcat.EmbeddedServer' | awk '{print $2}')
if [ -z "$RANGER_PID" ]; then
  echo "❌ Ranger Admin not running"
  exit 1
fi

tail --pid=$RANGER_PID -f /dev/null
