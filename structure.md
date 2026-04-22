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

# 🧠 ESTRUCTURA OPTIMIZADA FINAL

---

## 💸 INCOME (3 padres → 6 hijos)

### 🟢 Trabajo
- Salario

### 🎁 Extra
- Billetazo
- Bizum *(solo ingresos reales, no método de pago)*

### 📈 Finanzas
- Intereses (TAE, cuentas remuneradas)
- Dividendos

---

## 💸 EXPENSE (CORE DEL SISTEMA)

---

## 🍔 VIDA BÁSICA (NECESIDAD)

👉 TODO lo necesario para vivir

- Supermercado
- Pan / básico diario
- Comida puntual fuera *(si no es ocio)*

---

## 🎉 OCIO & ESTILO DE VIDA

👉 TODO lo no necesario

- Restaurantes / cenas sociales
- Salidas / fiestas
- Tardeo
- Suscripciones *(Netflix, Spotify, etc)*

---

## 🚗 MOVILIDAD (UNIFICADO)

👉 AQUÍ TODO transporte (sin fragmentar)

- Gasolina
- Seguro
- Mantenimiento
- Recambios

📌 sub-uso interno (NO categorías separadas):

- Moto
- Coche
- Bici

👉 esto debería ser atributo, no categoría

---

## 🖥 TECNOLOGÍA & CONSUMO DIGITAL

- Ordenadores
- Amazon tech
- PCComponentes
- Gadgets
- AliExpress tech / caprichos

---

## 👕 PERSONAL

- Ropa
- Calzado
- Accesorios

---

## 🏥 SALUD & BIENESTAR

- Medicamentos
- Médico / tratamientos
- Peluquería
- Cuidados personales

---

## 📈 INVEST (PATRIMONIO)

---

### 🟡 ETF
- Globales
- Sectoriales

### 🟡 INDEXADOS
- Fondos indexados

### 🟡 ACCIONES
- Tesla
- Nvidia
- etc

### 🟡 CRYPTO
- Bitcoin
- Ethereum
- Altcoins

### 🟡 CASH Y RENTABILIDAD
- Intereses TAE
- Intereses compuestos