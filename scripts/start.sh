#!/bin/bash

# KnoBot - Script de Inicio
# Este script levanta todos los servicios

set -e

echo "=========================================="
echo "KnoBot - Iniciando Servicios"
echo "=========================================="

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Levantar servicios
echo ""
echo "🚀 Levantando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado
echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

# Ejecutar migraciones
echo ""
echo "🔄 Ejecutando migraciones..."
docker-compose exec -T web python manage.py migrate

echo ""
echo "=========================================="
echo "✅ Servicios iniciados correctamente"
echo "=========================================="
echo ""
echo "Servicios disponibles:"
echo "  🌐 Django:      http://localhost:9000"
echo "  🗄️  PostgreSQL:  localhost:5435"
echo "  🔴 Redis:       localhost:6380"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:       ./scripts/logs.sh"
echo "  Detener:        ./scripts/stop.sh"
echo "  Reiniciar:      ./scripts/restart.sh"
echo ""
