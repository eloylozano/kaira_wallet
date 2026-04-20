finanzas-app/
├── backend/                # FastAPI Project
│   ├── app/
│   │   ├── api/            # Endpoints (gastos, auth, categorias)
│   │   ├── core/           # Configuración (JWT, Variables de entorno)
│   │   ├── models/         # Modelos de SQLAlchemy (Tablas SQL)
│   │   ├── schemas/        # Esquemas de Pydantic (Validación)
│   │   └── services/       # Lógica: IA en V2 y cálculos
│   ├── tests/              # Pruebas unitarias
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Svelte 5 + Tailwind
│   ├── src/
│   │   ├── components/     # UI de gastos y gráficos
│   │   ├── lib/            # Store y lógica de API
│   │   └── routes/         # Navegación PWA
│   ├── static/             # manifest.json y assets de PWA
│   └── Dockerfile
├── ai_module/              # Scripts de ML (V2: entrenamiento y patrones)
├── docker-compose.yml      # Orquestación de DB, Backend y Frontend
└── .env                    # Credenciales de DB y Keys de seguridad