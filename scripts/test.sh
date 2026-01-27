#!/bin/bash

# KnoBot - Script de Tests
# Este script ejecuta los tests de Django

set -e

echo "=========================================="
echo "KnoBot - Ejecutando Tests"
echo "=========================================="
echo ""

# Ejecutar tests
docker-compose exec web python manage.py test

echo ""
echo "✅ Tests completados"
echo ""
