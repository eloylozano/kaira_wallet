# Kaira Wallet

Kaira Wallet es una aplicacion de finanzas personales para registrar ingresos, gastos e inversiones, consultar estadisticas y mantener una vision clara del presupuesto mensual y del patrimonio.

El proyecto esta dividido en un backend FastAPI con PostgreSQL y un frontend SvelteKit/Svelte 5 con una interfaz responsive orientada a uso diario.

## Funcionalidades

- Registro, edicion, busqueda, filtrado y paginacion de movimientos.
- Tipos de movimiento: ingresos, gastos e inversiones.
- Categorias jerarquicas con iconos, subcategorias y gestion desde ajustes.
- Presupuesto mensual, resumen de balance y ultimos movimientos en el dashboard.
- Estadisticas por mes, distribucion, libertad financiera y composicion de cartera.
- Reglas de inversion para agrupar activos y mostrar alias/colores en graficas.
- Bloqueo por PIN y cabecera `X-Kaira-PIN` para proteger la API.
- Graficas con ECharts y controles tactiles con Svelte 5.

## Stack

### Frontend

- SvelteKit + Svelte 5
- TypeScript
- Tailwind CSS
- ECharts
- Flatpickr
- Lucide Svelte

### Backend

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn

## Estructura

```text
backend/                 API FastAPI, modelos, routers y servicios de estadisticas
frontend/kaira_wallet/   Aplicacion SvelteKit
ai_module/               Espacio reservado para modulo de IA
docker-compose.yaml      Entorno completo con PostgreSQL, API y frontend
```

## Arranque con Docker

Desde la raiz del repositorio:

```bash
docker compose up --build
```

Servicios por defecto:

- Frontend: `http://localhost:5174`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## Desarrollo local

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API crea las tablas al arrancar e inicializa un usuario local y categorias base.

### Frontend

```bash
cd frontend/kaira_wallet
npm install
npm run dev
```

Comandos utiles:

```bash
npm run check
npm run build
npm run format
```

## Configuracion

El backend espera una base PostgreSQL. Con Docker Compose se usa:

```text
DATABASE_URL=postgresql://user:pass@db:5432/kaira_wallet
```

La API esta protegida por PIN mediante la cabecera:

```text
X-Kaira-PIN: 8061
```

El frontend lee su configuracion desde `frontend/kaira_wallet/.env`.

## Estado del proyecto

Kaira Wallet esta en desarrollo activo. La base funcional ya cubre movimientos, categorias, ajustes, presupuesto y visualizaciones, pero quedan advertencias de accesibilidad/CSS por pulir y mejoras pendientes alrededor de autenticacion y despliegue final.

## Autor

Eloy Lozano
