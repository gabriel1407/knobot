#!/bin/bash

# KnoBot - Script de Restauración
# Este script restaura un backup de la base de datos

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el archivo de backup"
    echo "Uso: ./scripts/restore.sh backups/knowbot_backup_YYYYMMDD_HHMMSS.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: El archivo $BACKUP_FILE no existe"
    exit 1
fi

echo "=========================================="
echo "KnoBot - Restaurar Base de Datos"
echo "=========================================="
echo ""
echo "⚠️  ADVERTENCIA: Esto sobrescribirá la base de datos actual"
read -p "¿Estás seguro? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operación cancelada"
    exit 1
fi

# Descomprimir si es necesario
if [[ $BACKUP_FILE == *.gz ]]; then
    echo "🗜️  Descomprimiendo backup..."
    gunzip -c $BACKUP_FILE > /tmp/restore.sql
    RESTORE_FILE="/tmp/restore.sql"
else
    RESTORE_FILE=$BACKUP_FILE
fi

# Restaurar backup
echo "📥 Restaurando backup..."
docker-compose exec -T db psql -U postgres knowbot_db < $RESTORE_FILE

# Limpiar archivo temporal
if [ -f "/tmp/restore.sql" ]; then
    rm /tmp/restore.sql
fi

echo ""
echo "✅ Backup restaurado correctamente"
echo ""
