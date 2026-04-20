# API de Gestión de Gastos 💰

API REST escalable para gestionar gastos personales con soporte para categorías jerárquicas, periodicidad (fijo/variable) y múltiples usuarios.

## 🚀 Características

- ✅ **Categorías predefinidas + personalizadas**: Conjunto base de categorías con posibilidad de agregar más
- ✅ **Subcategorías jerárquicas**: Ej: Transporte → Coche, Moto, Recambios
- ✅ **Tipos de transacción**: Ingresos, Gastos, Inversiones
- ✅ **Periodicidad**: Marcar transacciones como fijas o variables
- ✅ **Notas/Comentarios**: Campo de texto para detalles adicionales
- ✅ **Estadísticas**: Resumen de ingresos, gastos, inversiones
- ✅ **Multi-usuario**: Cada usuario tiene sus propias transacciones y categorías

## 📋 Estructura de Base de Datos

### Tablas principales

```
users
├── id (PK)
├── email
├── hashed_password
└── created_at

categories
├── id (PK)
├── name
├── description
├── transaction_type (income/expense/invest)
├── parent_id (FK - para subcategorías)
├── user_id (FK - NULL si es predefinida)
├── is_predefined
└── created_at

transactions
├── id (PK)
├── type (income/expense/invest)
├── amount
├── date
├── category_id (FK)
├── description
├── notes
├── frequency (fixed/variable)
├── user_id (FK)
├── created_at
└── updated_at
```

## 🔧 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env`:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/kaira_wallet
API_HOST=0.0.0.0
API_PORT=8000
```

### 5. Ejecutar con PostgreSQL local

**Opción A: Con Docker Compose**
```bash
cd ..
docker-compose up -d
```

**Opción B: PostgreSQL local**
Asegúrate de que PostgreSQL esté corriendo y crea la BD:
```bash
createdb kaira_wallet
```

### 6. Iniciar el servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación de API

### Swagger UI
```
http://localhost:8000/docs
```

### ReDoc
```
http://localhost:8000/redoc
```

## 🔌 Endpoints Principales

### Categorías

```
GET    /categories/predefined              # Obtener categorías predefinidas
GET    /categories/                        # Obtener categorías del usuario
GET    /categories/{category_id}           # Obtener una categoría específica
POST   /categories/                        # Crear categoría personalizada
DELETE /categories/{category_id}           # Eliminar categoría personalizada
```

### Transacciones

```
GET    /transactions/                      # Obtener transacciones del usuario
GET    /transactions/{transaction_id}      # Obtener una transacción específica
POST   /transactions/                      # Crear una transacción
PUT    /transactions/{transaction_id}      # Actualizar una transacción
DELETE /transactions/{transaction_id}      # Eliminar una transacción
```

### Estadísticas

```
GET    /stats/                             # Resumen general
GET    /stats/by-category/                 # Gastos por categoría
```

## 📝 Ejemplos de Uso

### Crear una categoría personalizada

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hobbies",
    "description": "Gastos en hobbies personales",
    "transaction_type": "expense"
  }' \
  -G -d "user_id=1"
```

### Crear una transacción

```bash
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "expense",
    "amount": 50.0,
    "description": "Gasolina para el coche",
    "category_id": 4,
    "notes": "Gasolina de 98 octanos",
    "frequency": "variable"
  }' \
  -G -d "user_id=1"
```

### Obtener estadísticas

```bash
curl "http://localhost:8000/stats/" -G -d "user_id=1"
```

## 🔄 Categorías Predefinidas

Se cargan automáticamente al iniciar la API:

### Gastos
- **Transporte**: Coche, Moto, Recambios, Gasolina
- **Alimentación**: Supermercado, Restaurante
- **Vivienda**: Alquiler, Servicios, Mantenimiento
- **Ocio**: Cine, Suscripciones

### Ingresos
- Salario
- Freelance
- Otros Ingresos

### Inversiones
- Bolsa
- Criptomonedas

## 🚀 Próximas Mejoras

- [ ] Autenticación JWT
- [ ] Búsqueda y filtrado avanzado
- [ ] Exportar a CSV/Excel
- [ ] Reportes mensuales
- [ ] Predicción de gastos con IA
- [ ] Alertas presupuestarias
- [ ] Integración con banco datos

## 📝 Notas de Desarrollo

- Las categorías predefinidas NO se pueden eliminar
- Cada transacción debe coincidir con el tipo de su categoría
- Los cambios a transacciones quedan auditados (updated_at)
- Las subcategorías heredan el transaction_type de su padre

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
