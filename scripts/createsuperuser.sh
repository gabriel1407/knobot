#!/bin/bash

# KnoBot - Script de Creación de Superusuario
# Este script crea un superusuario de Django

set -e

echo "=========================================="
echo "KnoBot - Crear Superusuario"
echo "=========================================="
echo ""

docker-compose exec web python manage.py createsuperuser

echo ""
echo "✅ Superusuario creado correctamente"
echo ""
