# 💳 Q-AVIOGEN - Setup Legal, Fiscal y Pagos

## 🏦 Checklist Configuración Empresarial

### 📋 **URGENTE - Semana 1 (Días 1-7)**

#### 🏛️ **Setup Legal (Día 5)**
- [ ] **Decidir estructura**: ¿Autónomo o crear SL?
  - Autónomo: Más simple, menos costos
  - SL: Más profesional para B2B, limita responsabilidad
- [ ] **Alta en Hacienda**: Obtener número fiscal/CIF
- [ ] **Registro actividad**: Código CNAE para software empresarial
- [ ] **Seguridad Social**: Alta como autónomo (si aplica)

#### 💳 **Sistema de Pagos (Día 6)**
- [ ] **Cuenta bancaria business**: Separar ingresos del negocio
- [ ] **Stripe Account**: Configurar pagos internacionales
  - Soporte tarjetas Visa/MC/Amex
  - Suscripciones mensuales/anuales
  - Webhooks para automatización
- [ ] **PayPal Business**: Alternativa para empresas
- [ ] **Wire Transfer info**: Para clientes enterprise

#### 📊 **Facturación Automática (Día 7)**
- [ ] **Software contable**: Holded, Quipu, o Factusol
- [ ] **Templates de facturas**: Diseño profesional
- [ ] **Numeración automática**: Secuencial y legal
- [ ] **IVA configuration**: 21% España, exento EU B2B con válido VAT

---

## 💰 Configuración Stripe (Crítico para Revenue)

### 🔧 **Stripe Setup Técnico**
```javascript
// Productos y precios en Stripe
const products = [
  {
    name: "Q-AVIOGEN Personal",
    price: 49, // EUR/month
    currency: "eur",
    interval: "month"
  },
  {
    name: "Q-AVIOGEN Professional", 
    price: 149,
    currency: "eur",
    interval: "month"
  },
  {
    name: "Q-AVIOGEN Business",
    price: 499,
    currency: "eur", 
    interval: "month"
  },
  {
    name: "Q-AVIOGEN Enterprise",
    price: 2000,
    currency: "eur",
    interval: "month"
  }
];
```

### 🔗 **Integración con FastAPI**
```python
import stripe
from fastapi import FastAPI, HTTPException

stripe.api_key = "sk_live_..." # Tu Stripe secret key

@app.post("/create-subscription")
async def create_subscription(customer_email: str, price_id: str):
    try:
        # Crear customer
        customer = stripe.Customer.create(
            email=customer_email,
            metadata={"source": "q-aviogen-signup"}
        )
        
        # Crear suscripción
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_id}],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"]
        )
        
        return {
            "subscription_id": subscription.id,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 🌍 Configuración International

### 🇪🇺 **IVA Europeo**
- **España B2C**: 21% IVA siempre
- **EU B2B**: 0% si cliente tiene VAT válido  
- **Non-EU**: 0% IVA (pero puede tener impuestos locales)

### 💱 **Monedas Múltiples**
- **EUR**: Mercado europeo principal
- **USD**: Mercado americano (gran potencial aeroespacial)
- **GBP**: Reino Unido post-Brexit

### 📝 **Templates de Facturas**
```
FACTURA Nº: FAC-2025-001
Fecha: 23/06/2025

DE:
[Tu Nombre/Empresa]
[Dirección]
[Código Postal, Ciudad]
CIF/NIF: [Tu número fiscal]

PARA:
[Cliente]
[Dirección Cliente]
VAT/CIF: [Número cliente]

CONCEPTO: Suscripción Q-AVIOGEN Professional - Julio 2025
IMPORTE: 149,00 EUR
IVA (21%): 31,29 EUR
TOTAL: 180,29 EUR

Forma de pago: Domiciliación bancaria
Vencimiento: Al recibo
```

---

## 🚀 Marketplace Billing (Más Fácil)

### ☁️ **Azure Marketplace**
- **Microsoft maneja el billing**: Ellos cobran, te pagan
- **Comisión**: ~20% pero sin gestión de pagos
- **Moneda**: USD principalmente
- **Facturación**: Microsoft factura al cliente

### 🔶 **AWS Marketplace**  
- **Similar a Azure**: AWS maneja cobros
- **Comisión**: ~20-30% dependiendo del modelo
- **Ventaja**: Acceso directo a clientes enterprise

### 🔵 **Google Cloud Marketplace**
- **Menor comisión**: ~15% típicamente  
- **Menor alcance**: Pero clientes más técnicos

---

## ⚡ Plan de Implementación Pagos

### **Día 5 (27 Jun): Setup Legal**
- [ ] Decidir estructura empresarial
- [ ] Iniciar trámites fiscales
- [ ] Abrir cuenta bancaria business

### **Día 6 (28 Jun): Stripe + PayPal**
- [ ] Crear cuentas Stripe y PayPal
- [ ] Configurar productos y precios
- [ ] Implementar webhook handlers
- [ ] Test de pagos funcionando

### **Día 7 (29 Jun): Facturación**
- [ ] Software contable configurado
- [ ] Templates de facturas diseñados
- [ ] Sistema automático funcionando
- [ ] Test factura completo

### **Día 15 (15 Jul): Marketplace Billing**
- [ ] Azure Marketplace billing configurado
- [ ] AWS Marketplace payments setup
- [ ] GCP billing integration

---

## 💡 Tips Importantes

### 🔒 **Seguridad Pagos**
- **SSL Certificate**: Obligatorio para Stripe
- **PCI Compliance**: Stripe lo maneja por ti
- **Webhooks Security**: Verificar signatures
- **API Keys**: Nunca en frontend, solo backend

### 💸 **Optimización Revenue**
- **Annual Discounts**: 2 meses gratis en anual
- **Free Trial**: 14 días para reducir fricción
- **Upgrades**: Botones prominentes para upgrade
- **Failed Payments**: Retry automático + email

### 📊 **Métricas Críticas**
- **MRR**: Monthly Recurring Revenue
- **Churn Rate**: % cancelaciones mensuales
- **LTV**: Lifetime Value por cliente
- **CAC**: Customer Acquisition Cost

---

**🎯 RESULTADO ESPERADO**: Sistema completo de pagos funcionando para recibir los $15K en el primer mes.

**⚠️ SIN ESTO NO HAY REVENUE**: Los pagos son la parte MÁS crítica del plan de 30 días.

*Prioridad máxima: Días 5-7 del plan*
