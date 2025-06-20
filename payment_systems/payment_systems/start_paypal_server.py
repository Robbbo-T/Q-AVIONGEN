"""
🚀 Q-AVIOGEN PayPal Server Startup
Ejecutar para iniciar el servidor PayPal
"""

import uvicorn
import os
from pathlib import Path

# Cargar variables de entorno
from dotenv import load_dotenv

# Cargar .env desde payment_systems
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

if __name__ == "__main__":
    print("🚀 Iniciando servidor PayPal Q-AVIOGEN...")
    print("🌐 Documentación: http://localhost:8001/docs")
    print("💰 Revenue Dashboard: http://localhost:8001/revenue/dashboard")
    
    uvicorn.run(
        "paypal_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
