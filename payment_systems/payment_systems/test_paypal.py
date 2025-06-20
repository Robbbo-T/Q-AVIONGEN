"""
🧪 Q-AVIOGEN PayPal Test Suite
Testing completo de la integración PayPal
"""

import asyncio
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

def test_server_health():
    """🏥 Test health check"""
    print("🏥 Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Servidor PayPal healthy")
            return True
        else:
            print(f"❌ Servidor unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_plans_endpoint():
    """📋 Test planes disponibles"""
    print("\n📋 Testing planes disponibles...")
    try:
        response = requests.get(f"{BASE_URL}/plans", timeout=10)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ {len(plans['plans'])} planes disponibles")
            for plan_name, plan_data in plans['plans'].items():
                print(f"   - {plan_data['name']}: €{plan_data['monthly_price']}/mes")
            return True
        else:
            print(f"❌ Error obteniendo planes: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_revenue_projection():
    """💰 Test proyección de revenue"""
    print("\n💰 Testing proyección de revenue...")
    try:
        response = requests.get(f"{BASE_URL}/revenue/projection", timeout=10)
        if response.status_code == 200:
            projection = response.json()
            print(f"✅ Target mensual: {projection['paypal_monthly_revenue']}")
            print(f"✅ Proyección anual: {projection['annual_projection']}")
            return True
        else:
            print(f"❌ Error obteniendo proyección: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_subscription():
    """🎯 Test crear suscripción (solo sandbox)"""
    print("\n🎯 Testing crear suscripción...")
    try:
        subscription_data = {
            "customer_email": "test@qaviongen.com",
            "plan_type": "professional",
            "billing_cycle": "monthly",
            "custom_id": "test-001"
        }
        
        response = requests.post(
            f"{BASE_URL}/create-subscription",
            json=subscription_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Suscripción creada: {result['subscription_id']}")
            print(f"✅ URL de aprobación: {result['approval_url'][:50]}...")
            return True
        else:
            print(f"❌ Error creando suscripción: {response.status_code}")
            print(f"❌ Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """🚀 Ejecutar todos los tests"""
    print("🧪 INICIANDO TEST SUITE Q-AVIOGEN PAYPAL")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_server_health),
        ("Planes Disponibles", test_plans_endpoint),
        ("Revenue Projection", test_revenue_projection),
        ("Crear Suscripción", test_create_subscription)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE TESTS")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{len(results)} tests pasaron")
    
    if passed == len(results):
        print("🚀 ¡PayPal integration LISTA para producción!")
        print("💰 ¡En camino a €15K en el primer mes!")
    else:
        print("⚠️  Revisa los errores antes de pasar a producción")

if __name__ == "__main__":
    print("🧪 Q-AVIOGEN PayPal Test Suite")
    print("Asegúrate de que el servidor esté ejecutándose en puerto 8001")
    print("Ejecuta: python start_paypal_server.py")
    input("\nPresiona Enter cuando el servidor esté listo...")
    
    run_all_tests()
