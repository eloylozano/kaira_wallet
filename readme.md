# 🪙 Kaira Wallet

**Kaira Wallet** es una plataforma de gestión financiera personal de alto rendimiento, diseñada con un enfoque en la privacidad, la velocidad y la inteligencia artificial. Permite el seguimiento de patrimonio neto, inversiones y flujo de caja con una interfaz moderna basada en *glassmorphism*.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Svelte](https://img.shields.io/badge/Svelte-5.0-ff3e00?logo=svelte)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)

## 🚀 Características Principales

* **Dashboard de Patrimonio (Equity):** Visualización en tiempo real del ratio de liquidez (Cash vs. Inversión) mediante gráficos dinámicos con ECharts.
* **Kaira Wallet Mind (AI):** Motor de procesamiento inteligente que utiliza LLMs locales (vía Ollama) para la categorización automática de transacciones y análisis de gastos.
* **Arquitectura Moderna:** Frontend reactivo con Svelte 5 (Runes) para una gestión de estado ultra eficiente.
* **Enfoque en Privacidad:** Sistema de bloqueo por PIN y persistencia local/híbrida.
* **Diseño Premium:** Interfaz oscura con efectos de desenfoque, optimizada para escritorio y móvil.

## 🛠️ Tech Stack

### Frontend
* **Framework:** [Svelte 5](https://svelte.dev/) (usando `$state`, `$derived`, `$effect`).
* **Estilos:** Tailwind CSS.
* **Gráficos:** Apache ECharts.
* **Componentes:** Flatpickr (calendarios optimizados), Lucide Icons.

### Backend
* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI.
* **IA:** Ollama (procesamiento de lenguaje natural para finanzas).
* **Base de datos:** SQLite / PostgreSQL (según despliegue).

## 📦 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/kaira-wallet.git](https://github.com/tu-usuario/kaira-wallet.git)
cd kaira-wallet

```

### 2. Configurar el Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

```

### 3. Configurar el Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev

```

## 🌐 Despliegue

Este proyecto está preparado para desplegarse de forma híbrida:

* **Frontend:** Optimizado para [Vercel](https://vercel.com) con `ssr = false` para garantizar compatibilidad con librerías del navegador.
* **Backend:** Compatible con Render, Railway o contenedores Docker.

## 📝 Roadmap

* [x] Integración de Svelte 5 Runes.
* [x] Dashboard de Equity con ECharts.
* [ ] Conexión bancaria mediante API segura.
* [ ] Exportación de informes en PDF/Excel.
* [ ] Soporte para multi-divisa y criptoactivos.

## 👤 Autor

**Eloy Lozano** *Full Stack Developer & AI Specialist student*

* Website: [eloylozano.es](https://eloylozano.es)
* LinkedIn: [Tu perfil]

---

