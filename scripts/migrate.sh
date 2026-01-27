#!/bin/bash

# KnoBot - Script de Migraciones
# Este script ejecuta las migraciones de Django

set -e

echo "=========================================="
echo "KnoBot - Ejecutando Migraciones"
echo "=========================================="

# Crear migraciones
echo "📝 Creando migraciones..."
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
echo ""
echo "🔄 Aplicando migraciones..."
docker-compose exec web python manage.py migrate

echo ""
echo "✅ Migraciones completadas"
echo ""
