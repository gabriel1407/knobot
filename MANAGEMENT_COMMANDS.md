# Management Commands - KnoBot

Comandos de gestión para administrar la base de conocimiento, vector store y chat.

## 📚 Gestión de Base de Conocimiento

### `index_knowledge`

Indexa documentos de la base de conocimiento en el vector store para búsqueda semántica.

**Uso básico:**
```bash
# Indexar todos los documentos
docker-compose exec web python manage.py index_knowledge

# Indexar con limpieza previa del vector store
docker-compose exec web python manage.py index_knowledge --clear

# Indexar una base de conocimiento específica
docker-compose exec web python manage.py index_knowledge --knowledge-base <kb-id>

# Indexar un documento específico
docker-compose exec web python manage.py index_knowledge --document <doc-id>

# Personalizar tamaño de chunks
docker-compose exec web python manage.py index_knowledge --chunk-size 1000 --overlap 100
```

**Opciones:**
- `--knowledge-base <id>`: Indexar solo documentos de una base de conocimiento específica
- `--document <id>`: Indexar solo un documento específico
- `--clear`: Limpiar el vector store antes de indexar
- `--chunk-size <int>`: Tamaño de los chunks de texto (default: 500)
- `--overlap <int>`: Overlap entre chunks (default: 50)

**Ejemplo:**
```bash
# Indexar toda la base de conocimiento con chunks de 800 caracteres
docker-compose exec web python manage.py index_knowledge --chunk-size 800 --overlap 80
```

---

### `search_knowledge`

Realiza búsqueda semántica en la base de conocimiento.

**Uso básico:**
```bash
# Búsqueda simple
docker-compose exec web python manage.py search_knowledge "¿Cómo configurar el router?"

# Mostrar más resultados
docker-compose exec web python manage.py search_knowledge "internet lento" --n-results 10

# Filtrar por categoría
docker-compose exec web python manage.py search_knowledge "facturación" --category soporte
```

**Opciones:**
- `query`: Texto de búsqueda (requerido)
- `--n-results <int>`: Número de resultados a mostrar (default: 5)
- `--category <str>`: Filtrar por categoría

**Ejemplo:**
```bash
docker-compose exec web python manage.py search_knowledge "problemas de conexión" --n-results 3
```

**Salida:**
```
Buscando: "problemas de conexión"
==================================================

1. Score: 0.8542
   ID: doc-123-chunk-0
   Documento: Guía de Troubleshooting
   Categoría: soporte
   Chunk: 1/3
   Contenido: Si experimentas problemas de conexión, primero verifica...
--------------------------------------------------
```

---

### `clear_vector_store`

Limpia completamente el vector store (elimina todos los documentos indexados).

**Uso básico:**
```bash
# Con confirmación interactiva
docker-compose exec web python manage.py clear_vector_store

# Sin confirmación (usar con cuidado)
docker-compose exec web python manage.py clear_vector_store --confirm
```

**Opciones:**
- `--confirm`: Confirmar la eliminación sin preguntar

**⚠️ Advertencia:** Esta acción es irreversible. Deberás re-indexar todos los documentos después.

---

### `vector_store_stats`

Muestra estadísticas del vector store y la base de conocimiento.

**Uso básico:**
```bash
docker-compose exec web python manage.py vector_store_stats
```

**Salida:**
```
==================================================
ESTADÍSTICAS DEL SISTEMA
==================================================

📊 Vector Store:
   Documentos indexados: 156

📚 Base de Conocimiento:
   Total de documentos: 50
   Documentos activos: 48
   Documentos indexados: 48
   Porcentaje indexado: 100.0%

==================================================
```

---

## 💬 Gestión de Chat

### `test_chat`

Prueba el chat con RAG de forma interactiva en la terminal.

**Uso básico:**
```bash
# Chat con RAG activado
docker-compose exec web python manage.py test_chat

# Chat sin RAG (solo conversación)
docker-compose exec web python manage.py test_chat --no-rag

# Especificar usuario
docker-compose exec web python manage.py test_chat --user-id <user-id>

# Personalizar número de documentos de contexto
docker-compose exec web python manage.py test_chat --n-context 10
```

**Opciones:**
- `--user-id <id>`: ID del usuario (se crea uno de prueba si no se especifica)
- `--no-rag`: Desactivar RAG (solo conversación sin contexto)
- `--n-context <int>`: Número de documentos de contexto (default: 5)

**Ejemplo de sesión:**
```bash
$ docker-compose exec web python manage.py test_chat

============================================================
CHAT INTERACTIVO - KnoBot
============================================================
Usuario: test_user
Conversación ID: 550e8400-e29b-41d4-a716-446655440000
RAG: Activado
Documentos de contexto: 5

Escribe "salir" para terminar
============================================================

Tú: ¿Cómo reinicio mi router?
Procesando...

Asistente: Para reiniciar tu router, sigue estos pasos:
1. Desconecta el cable de alimentación del router
2. Espera 30 segundos
3. Vuelve a conectar el cable de alimentación
4. Espera 2-3 minutos hasta que todas las luces estén estables

[Contexto usado: 3 documentos]
[Tokens: 0]

Tú: salir
Finalizando conversación...
¡Hasta luego!
```

---

## 🔄 Flujo de Trabajo Típico

### 1. Configuración Inicial

```bash
# 1. Verificar estadísticas iniciales
docker-compose exec web python manage.py vector_store_stats

# 2. Indexar toda la base de conocimiento
docker-compose exec web python manage.py index_knowledge

# 3. Verificar que se indexó correctamente
docker-compose exec web python manage.py vector_store_stats
```

### 2. Agregar Nuevos Documentos

```bash
# Después de agregar documentos en el admin o API

# Indexar solo los nuevos documentos
docker-compose exec web python manage.py index_knowledge

# O indexar un documento específico
docker-compose exec web python manage.py index_knowledge --document <doc-id>
```

### 3. Actualizar Documentos Existentes

```bash
# Después de modificar un documento

# Re-indexar el documento específico
docker-compose exec web python manage.py index_knowledge --document <doc-id>
```

### 4. Limpiar y Re-indexar Todo

```bash
# Si hay problemas o cambios mayores

# Limpiar todo
docker-compose exec web python manage.py clear_vector_store --confirm

# Re-indexar todo
docker-compose exec web python manage.py index_knowledge
```

### 5. Probar el Sistema

```bash
# Buscar para verificar que funciona
docker-compose exec web python manage.py search_knowledge "router"

# Probar chat interactivo
docker-compose exec web python manage.py test_chat
```

---

## 📊 Monitoreo y Mantenimiento

### Verificar Estado del Sistema

```bash
# Ver estadísticas
docker-compose exec web python manage.py vector_store_stats

# Buscar documentos de prueba
docker-compose exec web python manage.py search_knowledge "test"
```

### Re-indexación Periódica

Se recomienda re-indexar periódicamente si hay muchas actualizaciones:

```bash
# Script de re-indexación
docker-compose exec web python manage.py index_knowledge --clear
```

---

## 🐛 Troubleshooting

### El vector store está vacío

```bash
# Verificar
docker-compose exec web python manage.py vector_store_stats

# Solución: Indexar documentos
docker-compose exec web python manage.py index_knowledge
```

### Búsquedas no retornan resultados relevantes

```bash
# Limpiar y re-indexar con chunks más pequeños
docker-compose exec web python manage.py clear_vector_store --confirm
docker-compose exec web python manage.py index_knowledge --chunk-size 300 --overlap 30
```

### Error al indexar documentos

```bash
# Ver logs detallados
docker-compose logs web

# Intentar indexar documento por documento
docker-compose exec web python manage.py index_knowledge --document <doc-id>
```

### Chat no usa contexto

```bash
# Verificar que hay documentos indexados
docker-compose exec web python manage.py vector_store_stats

# Probar búsqueda manual
docker-compose exec web python manage.py search_knowledge "tu consulta"

# Si no hay resultados, indexar
docker-compose exec web python manage.py index_knowledge
```

---

## 📝 Scripts de Automatización

### Script de Indexación Diaria

```bash
#!/bin/bash
# index_daily.sh

echo "Iniciando indexación diaria..."
docker-compose exec -T web python manage.py index_knowledge
echo "Indexación completada"
docker-compose exec -T web python manage.py vector_store_stats
```

### Script de Backup del Vector Store

```bash
#!/bin/bash
# backup_vector_store.sh

BACKUP_DIR="backups/vector_store"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp -r chroma_db $BACKUP_DIR/chroma_db_$TIMESTAMP
echo "Backup creado: $BACKUP_DIR/chroma_db_$TIMESTAMP"
```

---

## 🔗 Integración con Cron

Para automatizar la indexación:

```bash
# Editar crontab
crontab -e

# Agregar línea para indexar diariamente a las 2 AM
0 2 * * * cd /path/to/knowbot && ./scripts/index_daily.sh >> logs/index.log 2>&1
```

---

## 📚 Recursos Adicionales

- Ver `AI_SERVICES_README.md` para detalles de los servicios AI
- Ver `SUPPORTED_FORMATS.md` para formatos de archivos soportados
- Ver `scripts/README.md` para scripts de gestión Docker
