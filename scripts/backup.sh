#!/bin/bash

# KnoBot - Script de Backup
# Este script crea un backup de la base de datos

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/knowbot_backup_$TIMESTAMP.sql"

echo "=========================================="
echo "KnoBot - Backup de Base de Datos"
echo "=========================================="

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

# Crear backup
echo "📦 Creando backup..."
docker-compose exec -T db pg_dump -U postgres knowbot_db > $BACKUP_FILE

# Comprimir backup
echo "🗜️  Comprimiendo backup..."
gzip $BACKUP_FILE

echo ""
echo "✅ Backup creado: ${BACKUP_FILE}.gz"
echo ""
