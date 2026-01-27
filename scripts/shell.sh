#!/bin/bash

# KnoBot - Script de Shell
# Este script abre una shell de Django o bash en el contenedor

TYPE=${1:-django}

echo "=========================================="
echo "KnoBot - Shell"
echo "=========================================="

if [ "$TYPE" = "django" ]; then
    echo "Abriendo Django shell..."
    docker-compose exec web python manage.py shell
elif [ "$TYPE" = "bash" ]; then
    echo "Abriendo bash shell..."
    docker-compose exec web bash
else
    echo "❌ Tipo de shell inválido. Usa: django o bash"
    exit 1
fi
