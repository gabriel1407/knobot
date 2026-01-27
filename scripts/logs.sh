#!/bin/bash

# KnoBot - Script de Logs
# Este script muestra los logs de los servicios

# Por defecto muestra logs de web, pero acepta parámetro
SERVICE=${1:-web}

echo "=========================================="
echo "KnoBot - Logs del servicio: $SERVICE"
echo "=========================================="
echo ""
echo "Presiona Ctrl+C para salir"
echo ""

docker-compose logs -f --tail=100 $SERVICE
