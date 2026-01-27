#!/bin/bash

# KnoBot - Script de Detención
# Este script detiene todos los servicios

set -e

echo "=========================================="
echo "KnoBot - Deteniendo Servicios"
echo "=========================================="

docker-compose down

echo ""
echo "✅ Servicios detenidos correctamente"
echo ""
