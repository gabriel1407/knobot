#!/bin/bash

# KnoBot - Script de Reinicio
# Este script reinicia todos los servicios

set -e

echo "=========================================="
echo "KnoBot - Reiniciando Servicios"
echo "=========================================="

# Detener servicios
echo "🛑 Deteniendo servicios..."
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

echo ""
echo "✅ Servicios reiniciados correctamente"
echo ""
