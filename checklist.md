

# 🚀 Checklist: App de Gastos Inteligente (V1 & Preparación V2)

### 🏗️ 1. Entorno de Desarrollo (En Windows)
* [x] **Docker Desktop:** Instalado para gestionar los contenedores de la base de datos y el backend de forma aislada.
* [x] **Node.js & NPM:** Para el frontend con Svelte 5.
* [x] **Python 3.11+:** Entorno virtual configurado para FastAPI.
* [x] **PostgreSQL:** Contenedor de Docker corriendo (es mejor que SQLite para escalar a IA por la gestión de tipos de datos y concurrencia).

### 🛠️ 2. Backend (FastAPI - Escalable)
* [ ] **Estructura de API REST:** Endpoints definidos para `/ingresos`, `/gastos` y `/categorias`.
* [ ] **Autenticación JWT:** Implementada para asegurar que solo tú accedas a tus datos financieros.
* [ ] **Capa de Persistencia:** Uso de SQLAlchemy o Tortoise ORM para facilitar la migración de datos en el futuro.
* [ ] **Logging:** Configurado para registrar errores, fundamental para cuando la app actúe como servidor 24/7.

### 📱 3. Frontend (Svelte 5 - PWA)
* [ ] **Diseño Responsive:** Uso de Tailwind CSS para que se vea perfecto en el iPhone 13 y en el monitor de tu PC .
* [ ] **Manifest.json:** Configurado con `display: standalone` y `background_color` para que parezca nativa en iOS.
* [ ] **Service Workers:** Configuración básica para permitir el uso offline (importante para anotar gastos sin cobertura).
* [ ] **Iconografía:** Assets de iconos en diferentes tamaños (192x192, 512x512) para que el logo aparezca en el escritorio del iPhone.

### 📊 4. Análisis y Servidor
* [ ] **Conexión Power BI:** Configurar el conector de PostgreSQL para visualizar tus métricas actuales en Windows .
* [ ] **Configuración VPN:** (WireGuard o Tailscale) para que tu iPhone 13 pueda hablar con tu PC/Servidor de forma segura desde fuera de casa.

### 🧠 5. Preparación para la V2 (IA & Patrones)
* [ ] **Histórico Limpio:** Asegurar que cada registro de gasto tenga una etiqueta de "Categoría" y "Fecha" normalizada.
* [ ] **Módulo de Ingesta:** Crear un script de exportación de datos en formato `.csv` o `.json` para entrenar modelos de Scikit-learn en el futuro.
* [ ] **Almacenamiento de Embeddings:** (Opcional) Si planeas usar IA para clasificar tickets, deja espacio en la base de datos para vectores (pgvector en Postgres).

---
