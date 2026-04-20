"""
Script de ejemplo para probar la API de Gastos
Ejecutar con: python ejemplo_uso.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
USER_ID = 1  # Por ahora, user_id fijo (en producción será del JWT)

def print_response(response):
    """Imprime la respuesta formateada"""
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, default=str))
    except:
        print(response.text)
    print("-" * 80)

def test_health():
    """Verificar que la API está corriendo"""
    print("\n🏥 Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)

def test_get_predefined_categories():
    """Obtener categorías predefinidas"""
    print("\n📂 Obtener Categorías Predefinidas")
    response = requests.get(f"{BASE_URL}/categories/predefined")
    print_response(response)
    return response.json()

def test_get_all_categories():
    """Obtener todas las categorías"""
    print("\n📂 Obtener Todas las Categorías")
    response = requests.get(f"{BASE_URL}/categories/", params={"user_id": USER_ID})
    print_response(response)
    return response.json()

def test_create_custom_category():
    """Crear una categoría personalizada"""
    print("\n✨ Crear Categoría Personalizada")
    payload = {
        "name": "Hobbies",
        "description": "Gastos en hobbies y entretenimiento personal",
        "transaction_type": "expense"
    }
    response = requests.post(
        f"{BASE_URL}/categories/",
        json=payload,
        params={"user_id": USER_ID}
    )
    print_response(response)
    if response.status_code == 200:
        return response.json()

def test_create_transaction():
    """Crear una transacción"""
    print("\n💸 Crear Transacción")
    payload = {
        "type": "expense",
        "amount": 45.50,
        "description": "Llenar depósito de gasolina",
        "category_id": 5,  # Gasolina
        "notes": "Gasolina de 98 octanos en la estación Repsol",
        "frequency": "variable"
    }
    response = requests.post(
        f"{BASE_URL}/transactions/",
        json=payload,
        params={"user_id": USER_ID}
    )
    print_response(response)
    if response.status_code == 200:
        return response.json()

def test_get_transactions():
    """Obtener todas las transacciones"""
    print("\n📊 Obtener Transacciones")
    response = requests.get(
        f"{BASE_URL}/transactions/",
        params={"user_id": USER_ID}
    )
    print_response(response)
    return response.json()

def test_get_stats():
    """Obtener estadísticas"""
    print("\n📈 Obtener Estadísticas")
    response = requests.get(
        f"{BASE_URL}/stats/",
        params={"user_id": USER_ID}
    )
    print_response(response)

def test_get_stats_by_category():
    """Obtener estadísticas por categoría"""
    print("\n📈 Obtener Estadísticas por Categoría (Gastos)")
    response = requests.get(
        f"{BASE_URL}/stats/by-category/",
        params={"user_id": USER_ID, "transaction_type": "expense"}
    )
    print_response(response)

def test_create_multiple_transactions():
    """Crear múltiples transacciones de ejemplo"""
    print("\n🎯 Crear Transacciones de Ejemplo")
    
    transactions = [
        {
            "type": "expense",
            "amount": 45.00,
            "description": "Compra en Carrefour",
            "category_id": 7,  # Supermercado
            "notes": "Compra semanal de alimentos",
            "frequency": "variable"
        },
        {
            "type": "expense",
            "amount": 1000.00,
            "description": "Pago de alquiler - Abril",
            "category_id": 10,  # Alquiler
            "notes": "Alquiler del piso",
            "frequency": "fixed"
        },
        {
            "type": "income",
            "amount": 2500.00,
            "description": "Salario Abril",
            "category_id": 17,  # Salario
            "notes": "Nómina del trabajo",
            "frequency": "fixed"
        },
        {
            "type": "expense",
            "amount": 15.99,
            "description": "Suscripción Netflix",
            "category_id": 15,  # Suscripciones
            "notes": "Suscripción mensual",
            "frequency": "fixed"
        },
        {
            "type": "invest",
            "amount": 500.00,
            "description": "Compra de acciones Tesla",
            "category_id": 21,  # Bolsa
            "notes": "10 acciones a 50€ cada una",
            "frequency": "variable"
        }
    ]
    
    for tx in transactions:
        response = requests.post(
            f"{BASE_URL}/transactions/",
            json=tx,
            params={"user_id": USER_ID}
        )
        print(f"✓ {tx['description']}: {response.status_code}")

def main():
    """Ejecutar todos los tests"""
    print("=" * 80)
    print("🚀 Pruebas de la API de Gestión de Gastos")
    print("=" * 80)
    
    try:
        # Test básico
        test_health()
        
        # Categorías
        test_get_predefined_categories()
        test_get_all_categories()
        test_create_custom_category()
        
        # Transacciones
        print("\n" + "=" * 80)
        print("Creando transacciones de ejemplo...")
        print("=" * 80)
        test_create_multiple_transactions()
        
        # Ver transacciones
        print("\n" + "=" * 80)
        print("Mostrando datos finales...")
        print("=" * 80)
        test_get_transactions()
        test_get_stats()
        test_get_stats_by_category()
        
        print("\n✅ ¡Pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API")
        print("   Asegúrate de que el servidor está corriendo:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
