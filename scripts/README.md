# Scripts de Gestión de KnoBot

Este directorio contiene scripts bash para facilitar la gestión y despliegue del proyecto KnoBot.

## Scripts Disponibles

### 🚀 Configuración Inicial

```bash
./scripts/setup.sh
```
Configura el entorno y construye las imágenes Docker. Ejecutar solo la primera vez o después de cambios en el Dockerfile.

### ▶️ Inicio

```bash
./scripts/start.sh
```
Levanta todos los servicios (Django, PostgreSQL, Redis) y ejecuta las migraciones.

### ⏹️ Detener

```bash
./scripts/stop.sh
```
Detiene todos los servicios.

### 🔄 Reiniciar

```bash
./scripts/restart.sh
```
Reinicia todos los servicios.

### 📋 Ver Logs

```bash
./scripts/logs.sh [servicio]
```
Muestra los logs en tiempo real. Por defecto muestra logs de `web`.

Ejemplos:
- `./scripts/logs.sh` - Logs de Django
- `./scripts/logs.sh db` - Logs de PostgreSQL
- `./scripts/logs.sh redis` - Logs de Redis

### 🔄 Migraciones

```bash
./scripts/migrate.sh
```
Crea y aplica migraciones de Django.

### 💻 Shell

```bash
./scripts/shell.sh [tipo]
```
Abre una shell interactiva.

Ejemplos:
- `./scripts/shell.sh django` - Django shell (por defecto)
- `./scripts/shell.sh bash` - Bash shell

### 👤 Crear Superusuario

```bash
./scripts/createsuperuser.sh
```
Crea un superusuario de Django para acceder al admin.

### 🧪 Tests

```bash
./scripts/test.sh
```
Ejecuta todos los tests del proyecto.

### 💾 Backup

```bash
./scripts/backup.sh
```
Crea un backup comprimido de la base de datos en el directorio `backups/`.

### 📥 Restaurar

```bash
./scripts/restore.sh backups/knowbot_backup_YYYYMMDD_HHMMSS.sql.gz
```
Restaura un backup de la base de datos.

## Flujo de Trabajo Típico

### Primera vez (servidor nuevo)

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd knowbot

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar variables

# 3. Configurar y construir
./scripts/setup.sh

# 4. Iniciar servicios
./scripts/start.sh

# 5. Crear superusuario
./scripts/createsuperuser.sh
```

### Desarrollo diario

```bash
# Iniciar servicios
./scripts/start.sh

# Ver logs
./scripts/logs.sh

# Después de cambios en modelos
./scripts/migrate.sh

# Detener al finalizar
./scripts/stop.sh
```

### Despliegue en producción

```bash
# 1. Actualizar código
git pull

# 2. Reconstruir si hay cambios en dependencias
./scripts/setup.sh

# 3. Reiniciar servicios
./scripts/restart.sh

# 4. Crear backup antes de migraciones
./scripts/backup.sh

# 5. Aplicar migraciones
./scripts/migrate.sh
```

## Servicios y Puertos

- **Django:** http://localhost:9000
- **PostgreSQL:** localhost:5435
- **Redis:** localhost:6380

## Notas Importantes

- Todos los scripts deben ejecutarse desde la raíz del proyecto
- Los scripts tienen permisos de ejecución (`chmod +x`)
- El auto-reload de Django está activado, los cambios en el código se reflejan automáticamente
- Los backups se guardan en el directorio `backups/` con timestamp
