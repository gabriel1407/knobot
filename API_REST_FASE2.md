# API REST - Fase 2: Autenticación JWT

## ✅ Implementación Completada

### **Configuración JWT**

- ✅ JWT configurado en `settings.py`
- ✅ `rest_framework_simplejwt` instalado y configurado
- ✅ Token blacklist habilitado
- ✅ Access token: 1 hora de duración
- ✅ Refresh token: 7 días de duración
- ✅ Rotación automática de refresh tokens

### **Serializers Creados** (`apps/users/auth_serializers.py`)

1. **`CustomTokenObtainPairSerializer`** - Token JWT personalizado con claims
2. **`LoginSerializer`** - Login con username o email
3. **`RegisterSerializer`** - Registro de nuevos usuarios
4. **`ChangePasswordSerializer`** - Cambio de contraseña
5. **`PasswordResetRequestSerializer`** - Solicitud de reset (preparado)
6. **`PasswordResetConfirmSerializer`** - Confirmación de reset (preparado)

### **Views Creadas** (`apps/users/auth_views.py`)

1. **`LoginView`** - Login y obtención de tokens
2. **`RegisterView`** - Registro de usuarios
3. **`LogoutView`** - Logout con blacklist de token
4. **`RefreshTokenView`** - Refrescar access token
5. **`MeView`** - Información del usuario autenticado
6. **`ChangePasswordView`** - Cambiar contraseña
7. **`VerifyTokenView`** - Verificar validez de token

---

## 📋 Endpoints de Autenticación

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/` | Login con username/email | No |
| POST | `/api/auth/register/` | Registro de usuario | No |
| POST | `/api/auth/logout/` | Logout (blacklist token) | Sí |
| POST | `/api/auth/refresh/` | Refrescar access token | No |
| POST | `/api/auth/verify/` | Verificar token | No |
| POST | `/api/auth/token/` | Obtener token (alternativo) | No |
| GET | `/api/auth/me/` | Ver mi perfil | Sí |
| POST | `/api/auth/change-password/` | Cambiar contraseña | Sí |

---

## 🧪 Ejemplos de Uso

### **1. Registro de Usuario**

```bash
curl -X POST http://localhost:9000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juanperez",
    "email": "juan@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+57 300 1234567",
    "company": "Mi Empresa"
  }'
```

**Respuesta:**
```json
{
  "message": "Usuario registrado exitosamente",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "juanperez",
    "email": "juan@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "customer"
  }
}
```

---

### **2. Login**

```bash
# Login con username
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juanperez",
    "password": "SecurePass123!"
  }'

# Login con email
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan@example.com",
    "password": "SecurePass123!"
  }'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "juanperez",
    "email": "juan@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "customer",
    "company": "Mi Empresa"
  }
}
```

---

### **3. Usar Token en Requests**

```bash
# Agregar token en header Authorization
curl http://localhost:9000/api/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

### **4. Refrescar Access Token**

```bash
curl -X POST http://localhost:9000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### **5. Ver Mi Perfil**

```bash
curl http://localhost:9000/api/auth/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "juanperez",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+57 300 1234567",
  "role": "customer",
  "company": "Mi Empresa",
  "created_at": "2026-01-27T20:00:00Z",
  "last_login": "2026-01-27T21:30:00Z"
}
```

---

### **6. Cambiar Contraseña**

```bash
curl -X POST http://localhost:9000/api/auth/change-password/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
  }'
```

**Respuesta:**
```json
{
  "message": "Contraseña actualizada exitosamente"
}
```

---

### **7. Verificar Token**

```bash
curl -X POST http://localhost:9000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

**Respuesta (válido):**
```json
{
  "valid": true,
  "message": "Token válido"
}
```

**Respuesta (inválido):**
```json
{
  "valid": false,
  "message": "Token inválido o expirado"
}
```

---

### **8. Logout**

```bash
curl -X POST http://localhost:9000/api/auth/logout/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

**Respuesta:**
```json
{
  "message": "Logout exitoso"
}
```

---

## 🔐 Configuración JWT

### **Duración de Tokens**

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),      # 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # 7 días
    'ROTATE_REFRESH_TOKENS': True,                    # Rotar en cada refresh
    'BLACKLIST_AFTER_ROTATION': True,                 # Blacklist del anterior
    'UPDATE_LAST_LOGIN': True,                        # Actualizar last_login
}
```

### **Claims Personalizados**

Los tokens JWT incluyen claims adicionales:
- `username` - Nombre de usuario
- `email` - Email del usuario
- `role` - Rol del usuario (customer, agent, admin)
- `user_id` - ID del usuario (UUID)

---

## 🔄 Flujo de Autenticación

### **1. Registro/Login**
```
Usuario → POST /auth/register/ o /auth/login/
       ← { access, refresh, user }
```

### **2. Requests Autenticados**
```
Usuario → GET /api/users/me/
          Header: Authorization: Bearer {access_token}
       ← { user_data }
```

### **3. Token Expirado**
```
Usuario → GET /api/users/me/
          Header: Authorization: Bearer {expired_token}
       ← 401 Unauthorized

Usuario → POST /auth/refresh/
          Body: { refresh }
       ← { access, refresh }

Usuario → GET /api/users/me/
          Header: Authorization: Bearer {new_access_token}
       ← { user_data }
```

### **4. Logout**
```
Usuario → POST /auth/logout/
          Body: { refresh }
       ← { message: "Logout exitoso" }
```

---

## 🛡️ Seguridad

### **Token Blacklist**
- Los refresh tokens se agregan a una blacklist al hacer logout
- Los tokens rotados también se blacklistan
- Previene reutilización de tokens comprometidos

### **Validaciones**
- ✅ Contraseñas validadas con `django.contrib.auth.password_validation`
- ✅ Usuarios inactivos no pueden hacer login
- ✅ Confirmación de contraseña requerida
- ✅ Verificación de contraseña actual al cambiar

### **Permisos**
- Login/Register: Público (AllowAny)
- Logout/Me/Change Password: Autenticado (IsAuthenticated)
- Refresh/Verify: Público (AllowAny)

---

## 📱 Integración Frontend

### **Ejemplo JavaScript/React**

```javascript
// Login
const login = async (username, password) => {
  const response = await fetch('http://localhost:9000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  // Guardar tokens
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
};

// Request autenticado
const fetchProtected = async (url) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.status === 401) {
    // Token expirado, refrescar
    await refreshToken();
    return fetchProtected(url); // Reintentar
  }
  
  return response.json();
};

// Refrescar token
const refreshToken = async () => {
  const refresh = localStorage.getItem('refresh_token');
  
  const response = await fetch('http://localhost:9000/api/auth/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh })
  });
  
  const data = await response.json();
  
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
};

// Logout
const logout = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const token = localStorage.getItem('access_token');
  
  await fetch('http://localhost:9000/api/auth/logout/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh })
  });
  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};
```

---

## 🧪 Testing

### **Crear Usuario de Prueba**

```bash
docker-compose exec web python manage.py shell
```

```python
from apps.users.models import User

# Crear usuario
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='TestPass123!',
    first_name='Test',
    last_name='User',
    role='customer'
)
```

### **Probar Login**

```bash
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

---

## 🎯 Próximos Pasos

### **Fase 3: Chat Endpoints**
- [ ] Serializers para Conversation y Message
- [ ] ConversationViewSet con filtros por usuario
- [ ] MessageViewSet
- [ ] Endpoint POST /chat/ para enviar mensaje con RAG
- [ ] WebSocket para chat en tiempo real (opcional)

---

## 📝 Notas Técnicas

**Autenticación Dual:**
- JWT (Bearer token) - Recomendado para APIs y mobile
- Session - Para Django admin y desarrollo

**Rotación de Tokens:**
- Cada vez que se refresca un access token, se genera un nuevo refresh token
- El refresh token anterior se blacklistea automáticamente
- Mejora la seguridad al limitar la ventana de uso de tokens

**Login Flexible:**
- Los usuarios pueden hacer login con username o email
- El sistema detecta automáticamente cuál están usando

---

**Última actualización:** 27 de enero de 2026  
**Estado:** Fase 2 Completada ✅
