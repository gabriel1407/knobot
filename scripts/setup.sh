#!/bin/bash

# KnoBot - Script de Configuración Inicial
# Este script configura el entorno y construye las imágenes Docker

set -e

echo "=========================================="
echo "KnoBot - Configuración Inicial"
echo "=========================================="

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "❌ Error: No se encontró el archivo .env"
    echo "Por favor, copia .env.example a .env y configura las variables"
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    exit 1
fi

echo "✅ Docker instalado"

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker Compose instalado"

# Construir imágenes
echo ""
echo "📦 Construyendo imágenes Docker..."
DOCKER_BUILDKIT=0 docker-compose build

echo ""
echo "✅ Imágenes construidas exitosamente"
echo ""
echo "=========================================="
echo "Configuración completada"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "  1. Ejecuta: ./scripts/start.sh"
echo "  2. Accede a: http://localhost:9000"
echo ""
