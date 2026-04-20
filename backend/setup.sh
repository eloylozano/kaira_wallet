#!/bin/bash
# Script para configurar e inicializar el proyecto rápidamente

echo "🚀 Inicializando Karia Wallet Mind Backend..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "✨ Activando entorno virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "✓ Archivo .env creado. Por favor, actualiza la configuración si es necesario."
fi

echo ""
echo "✅ ¡Inicialización completada!"
echo ""
echo "Próximos pasos:"
echo "1. Asegúrate de que PostgreSQL está corriendo"
echo "2. Actualiza las variables en .env si es necesario"
echo "3. Ejecuta el servidor:"
echo "   uvicorn main:app --reload"
echo ""
echo "O si estás usando Docker Compose, ejecuta:"
echo "   docker-compose up -d"
echo ""
echo "Luego accede a:"
echo "   📖 Documentación: http://localhost:8000/docs"
echo "   🧪 Ejemplos: python ejemplo_uso.py"
