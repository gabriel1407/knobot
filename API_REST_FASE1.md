# API REST - Fase 1 Completada

## ✅ Componentes Implementados

### **1. Core Components (`core/`)**

#### `core/viewsets.py` - BaseModelViewSet
- ✅ Soporte para 2 serializers (list y write)
- ✅ Soft delete automático
- ✅ Filtrado por `is_active` por defecto
- ✅ Acciones bulk: `bulk_delete`, `bulk_restore`
- ✅ Acción individual: `restore`

#### `core/serializers.py` - Serializers Base
- ✅ `BaseSerializer` - Campos comunes del BaseModel
- ✅ `BaseListSerializer` - Para operaciones GET
- ✅ `BaseWriteSerializer` - Para operaciones POST/PUT/PATCH

#### `core/pagination.py` - Paginación
- ✅ `StandardResultsSetPagination` - 20 items por página
- ✅ `LargeResultsSetPagination` - 50 items por página
- ✅ Respuesta con metadatos (count, next, previous, total_pages)

#### `core/permissions.py` - Permisos Personalizados
- ✅ `IsOwnerOrReadOnly` - Solo el propietario puede editar
- ✅ `IsAdminOrReadOnly` - Solo admins pueden editar
- ✅ `IsAgentOrAdmin` - Solo agentes o admins

#### `core/mixins.py` - Mixins Reutilizables
- ✅ `SoftDeleteMixin` - Soft delete y restore
- ✅ `BulkActionsMixin` - Acciones en bulk

---

### **2. Users App (`apps/users/`)**

#### `serializers.py`
- ✅ `UserListSerializer` - Para GET (detallado)
- ✅ `UserWriteSerializer` - Para POST/PUT/PATCH (con validación de contraseña)
- ✅ `UserProfileSerializer` - Para perfil del usuario autenticado

#### `views.py` - UserViewSet
- ✅ CRUD completo de usuarios
- ✅ Endpoint `/users/me/` - Ver/editar perfil
- ✅ Endpoint `/users/change_password/` - Cambiar contraseña
- ✅ Endpoint `/users/{id}/activate/` - Activar usuario
- ✅ Endpoint `/users/{id}/deactivate/` - Desactivar usuario
- ✅ Endpoint `/users/{id}/restore/` - Restaurar usuario eliminado
- ✅ Filtros: role, is_active, company
- ✅ Búsqueda: username, email, first_name, last_name
- ✅ Ordenamiento: created_at, username, email

#### `urls.py`
- ✅ Router configurado para UserViewSet

---

### **3. URLs Principales (`knowbot/urls.py`)**

- ✅ `/admin/` - Django Admin
- ✅ `/api/users/` - Endpoints de usuarios
- ✅ `/api/schema/` - Schema OpenAPI
- ✅ `/api/docs/` - Documentación Swagger UI

---

## 📋 Endpoints Disponibles

### **Users**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/users/` | Listar usuarios | Autenticado |
| POST | `/api/users/` | Crear usuario (registro) | Público |
| GET | `/api/users/{id}/` | Ver detalle de usuario | Autenticado |
| PUT | `/api/users/{id}/` | Actualizar usuario completo | Admin |
| PATCH | `/api/users/{id}/` | Actualizar usuario parcial | Admin |
| DELETE | `/api/users/{id}/` | Eliminar usuario (soft) | Admin |
| POST | `/api/users/{id}/restore/` | Restaurar usuario | Admin |
| POST | `/api/users/{id}/activate/` | Activar usuario | Admin |
| POST | `/api/users/{id}/deactivate/` | Desactivar usuario | Admin |
| GET | `/api/users/me/` | Ver mi perfil | Autenticado |
| PUT | `/api/users/me/` | Actualizar mi perfil | Autenticado |
| PATCH | `/api/users/me/` | Actualizar mi perfil parcial | Autenticado |
| POST | `/api/users/change_password/` | Cambiar mi contraseña | Autenticado |
| POST | `/api/users/bulk_delete/` | Eliminar múltiples usuarios | Admin |
| POST | `/api/users/bulk_restore/` | Restaurar múltiples usuarios | Admin |

---

## 🧪 Ejemplos de Uso

### **1. Crear Usuario (Registro)**

```bash
curl -X POST http://localhost:9000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "customer"
  }'
```

### **2. Listar Usuarios**

```bash
# Todos los usuarios activos
curl http://localhost:9000/api/users/ \
  -H "Authorization: Token <your-token>"

# Con filtros
curl "http://localhost:9000/api/users/?role=customer&company=ISP1" \
  -H "Authorization: Token <your-token>"

# Con búsqueda
curl "http://localhost:9000/api/users/?search=juan" \
  -H "Authorization: Token <your-token>"

# Incluir inactivos
curl "http://localhost:9000/api/users/?show_inactive=true" \
  -H "Authorization: Token <your-token>"
```

### **3. Ver Mi Perfil**

```bash
curl http://localhost:9000/api/users/me/ \
  -H "Authorization: Token <your-token>"
```

### **4. Actualizar Mi Perfil**

```bash
curl -X PATCH http://localhost:9000/api/users/me/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Carlos",
    "phone": "+57 300 1234567"
  }'
```

### **5. Cambiar Contraseña**

```bash
curl -X POST http://localhost:9000/api/users/change_password/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
  }'
```

### **6. Eliminar Usuario (Soft Delete)**

```bash
curl -X DELETE http://localhost:9000/api/users/{user-id}/ \
  -H "Authorization: Token <admin-token>"
```

### **7. Restaurar Usuario**

```bash
curl -X POST http://localhost:9000/api/users/{user-id}/restore/ \
  -H "Authorization: Token <admin-token>"
```

### **8. Bulk Delete**

```bash
curl -X POST http://localhost:9000/api/users/bulk_delete/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["uuid1", "uuid2", "uuid3"]
  }'
```

---

## 🔐 Autenticación

Actualmente configurado con Token Authentication. Para obtener un token:

```bash
# Crear superusuario primero
docker-compose exec web python manage.py createsuperuser

# Obtener token (requiere endpoint de login - próxima fase)
```

---

## 📊 Respuesta de Paginación

```json
{
  "count": 100,
  "next": "http://localhost:9000/api/users/?page=2",
  "previous": null,
  "total_pages": 5,
  "current_page": 1,
  "page_size": 20,
  "results": [
    {
      "id": "uuid",
      "username": "juan",
      "email": "juan@example.com",
      "first_name": "Juan",
      "last_name": "Pérez",
      "role": "customer",
      "is_active": true,
      "created_at": "2026-01-27T20:00:00Z",
      ...
    }
  ]
}
```

---

## ✅ Verificación

```bash
# Verificar sistema
docker-compose exec web python manage.py check

# Ver documentación Swagger
# Abrir en navegador: http://localhost:9000/api/docs/
```

---

## 🎯 Próximos Pasos

### **Fase 2: Autenticación**
- [ ] Implementar login/logout endpoints
- [ ] Implementar refresh token
- [ ] Agregar JWT authentication

### **Fase 3: Chat Endpoints**
- [ ] Serializers para Conversation y Message
- [ ] ConversationViewSet
- [ ] MessageViewSet
- [ ] Endpoint para enviar mensaje al chat con RAG

### **Fase 4: Knowledge Endpoints**
- [ ] Serializers para KnowledgeBase y Document
- [ ] KnowledgeBaseViewSet
- [ ] DocumentViewSet
- [ ] Endpoint para subir archivos
- [ ] Endpoint para búsqueda semántica

### **Fase 5: Tickets y Analytics**
- [ ] TicketViewSet
- [ ] AnalyticsViewSet
- [ ] IntegrationViewSet

---

## 📝 Notas Técnicas

**Patrón de 2 Serializers:**
- `list_serializer_class`: Usado en GET (list, retrieve) - Incluye campos detallados y relaciones
- `write_serializer_class`: Usado en POST/PUT/PATCH - Solo campos necesarios para crear/actualizar

**Soft Delete:**
- Los objetos eliminados no se borran físicamente
- Se marcan con `is_active=False`
- Pueden ser restaurados con el endpoint `/restore/`
- Por defecto, las queries filtran objetos inactivos

**Filtros Disponibles:**
- Filtrado: `?role=customer&is_active=true`
- Búsqueda: `?search=juan`
- Ordenamiento: `?ordering=-created_at`
- Paginación: `?page=2&page_size=50`
- Mostrar inactivos: `?show_inactive=true`

---

**Última actualización:** 27 de enero de 2026
**Estado:** Fase 1 Completada ✅
