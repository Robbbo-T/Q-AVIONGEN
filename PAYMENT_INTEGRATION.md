# 💳 SISTEMA DE PAGOS E INTEGRACIÓN FREEMIUM

## 🔐 Integración de Pagos (Stripe + PayPal)

### **Configuración Stripe**

```javascript
// stripe-config.js
const stripe = Stripe('pk_live_xxxxxxxxxxxxxxxxxxxxx'); // Clave pública

const pricingPlans = {
    free: {
        id: 'free',
        name: 'Plan Gratuito',
        price: 0,
        features: {
            videos_per_month: 3,
            max_duration_seconds: 30,
            resolution: '720p',
            watermark: true,
            voice_type: 'basic',
            support: 'community',
            storage_gb: 1,
            exports: ['mp4_720p'],
            api_calls: 0
        }
    },
    base: {
        id: 'price_1234567890', // Stripe Price ID
        name: 'Plan Base',
        price: 49,
        currency: 'eur',
        interval: 'month',
        features: {
            videos_per_month: 20,
            max_duration_seconds: 120,
            resolution: '1080p',
            watermark: false,
            voice_type: 'professional',
            support: 'email',
            storage_gb: 10,
            exports: ['mp4_1080p', 'webm', 'mov'],
            api_calls: 1000
        }
    },
    plus: {
        id: 'price_0987654321',
        name: 'Plan Plus',
        price: 149,
        currency: 'eur',
        interval: 'month',
        features: {
            videos_per_month: 100,
            max_duration_seconds: 300,
            resolution: '4k',
            watermark: false,
            voice_type: 'premium',
            support: 'chat',
            storage_gb: 50,
            exports: ['mp4_4k', 'webm', 'mov', 'avi'],
            api_calls: 10000,
            custom_branding: true,
            multiple_languages: true
        }
    },
    pro: {
        id: 'price_1122334455',
        name: 'Plan Pro',
        price: 299,
        currency: 'eur',
        interval: 'month',
        features: {
            videos_per_month: -1, // Ilimitado
            max_duration_seconds: 900,
            resolution: '8k',
            watermark: false,
            voice_type: 'custom',
            support: 'phone',
            storage_gb: 200,
            exports: ['mp4_8k', 'webm', 'mov', 'avi', 'prores'],
            api_calls: -1, // Ilimitado
            custom_branding: true,
            multiple_languages: true,
            white_label: true,
            priority_processing: true
        }
    }
};

// Función para crear sesión de checkout
async function createCheckoutSession(planId, userId) {
    const plan = pricingPlans[planId];
    
    const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card', 'paypal'],
        line_items: [{
            price: plan.id,
            quantity: 1,
        }],
        mode: 'subscription',
        success_url: 'https://q-aviogen.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url: 'https://q-aviogen.com/pricing',
        customer_email: userId + '@customer.domain',
        metadata: {
            user_id: userId,
            plan_id: planId
        },
        subscription_data: {
            trial_period_days: 14, // 14 días gratis para todos los planes
            metadata: {
                user_id: userId,
                plan_id: planId
            }
        },
        allow_promotion_codes: true // Permite códigos promocionales
    });
    
    return session;
}
```

### **Backend Node.js (Express) para Webhook de Stripe**

```javascript
// server.js
const express = require('express');
const stripe = require('stripe')('sk_live_xxxxxxxxxxxxxxxxxxxxx');
const app = express();

// Webhook endpoint para Stripe
app.post('/webhook/stripe', express.raw({type: 'application/json'}), (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = 'whsec_xxxxxxxxxxxxxxxxxxxxx';
    
    let event;
    
    try {
        event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    } catch (err) {
        console.log(`Webhook signature verification failed.`, err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }
    
    switch (event.type) {
        case 'checkout.session.completed':
            const session = event.data.object;
            handleSuccessfulPayment(session);
            break;
            
        case 'invoice.payment_succeeded':
            const invoice = event.data.object;
            handleSubscriptionRenewal(invoice);
            break;
            
        case 'customer.subscription.deleted':
            const subscription = event.data.object;
            handleSubscriptionCancellation(subscription);
            break;
            
        default:
            console.log(`Unhandled event type ${event.type}`);
    }
    
    res.json({received: true});
});

// Función para manejar pagos exitosos
async function handleSuccessfulPayment(session) {
    const userId = session.metadata.user_id;
    const planId = session.metadata.plan_id;
    
    // Actualizar usuario en base de datos
    await updateUserPlan(userId, planId);
    
    // Enviar email de bienvenida
    await sendWelcomeEmail(userId, planId);
    
    // Activar funcionalidades del plan
    await activatePlanFeatures(userId, planId);
}

// Función para actualizar plan de usuario
async function updateUserPlan(userId, planId) {
    const plan = pricingPlans[planId];
    
    // Aquí actualizarías tu base de datos
    const user = await database.users.update(userId, {
        plan: planId,
        plan_features: plan.features,
        subscription_active: true,
        trial_ends_at: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 días
        subscription_starts_at: new Date(),
        videos_used_this_month: 0,
        last_billing_date: new Date()
    });
    
    console.log(`Usuario ${userId} actualizado al plan ${planId}`);
}
```

---

## 🎯 **SISTEMA DE LIMITACIONES FREEMIUM**

### **Middleware de Validación de Límites**

```javascript
// limits-middleware.js
class FreemiumLimits {
    constructor(userPlan) {
        this.plan = pricingPlans[userPlan] || pricingPlans.free;
    }
    
    // Verificar si puede crear video
    canCreateVideo(userStats) {
        const { videos_used_this_month } = userStats;
        const limit = this.plan.features.videos_per_month;
        
        if (limit === -1) return { allowed: true }; // Ilimitado
        
        return {
            allowed: videos_used_this_month < limit,
            used: videos_used_this_month,
            limit: limit,
            remaining: limit - videos_used_this_month
        };
    }
    
    // Verificar duración de video
    canCreateVideoDuration(requestedDuration) {
        const maxDuration = this.plan.features.max_duration_seconds;
        
        return {
            allowed: requestedDuration <= maxDuration,
            requested: requestedDuration,
            max_allowed: maxDuration,
            exceeds_by: Math.max(0, requestedDuration - maxDuration)
        };
    }
    
    // Verificar llamadas API
    canMakeAPICall(userStats) {
        const { api_calls_this_month } = userStats;
        const limit = this.plan.features.api_calls;
        
        if (limit === -1) return { allowed: true }; // Ilimitado
        
        return {
            allowed: api_calls_this_month < limit,
            used: api_calls_this_month,
            limit: limit,
            remaining: limit - api_calls_this_month
        };
    }
    
    // Obtener opciones de exportación
    getExportOptions() {
        return this.plan.features.exports;
    }
    
    // Verificar si debe incluir marca de agua
    shouldIncludeWatermark() {
        return this.plan.features.watermark;
    }
}

// Uso del middleware
app.post('/api/videos/create', async (req, res) => {
    const user = await getUser(req.userId);
    const limits = new FreemiumLimits(user.plan);
    
    // Verificar límite de videos
    const videoCheck = limits.canCreateVideo(user.stats);
    if (!videoCheck.allowed) {
        return res.status(403).json({
            error: 'LIMIT_EXCEEDED',
            message: `Ha alcanzado el límite de videos (${videoCheck.used}/${videoCheck.limit})`,
            upgrade_required: true,
            suggested_plans: ['base', 'plus', 'pro']
        });
    }
    
    // Verificar duración
    const durationCheck = limits.canCreateVideoDuration(req.body.duration);
    if (!durationCheck.allowed) {
        return res.status(403).json({
            error: 'DURATION_EXCEEDED',
            message: `Duración excede límite del plan (${durationCheck.requested}s > ${durationCheck.max_allowed}s)`,
            upgrade_required: true,
            max_duration: durationCheck.max_allowed
        });
    }
    
    // Proceder con la creación del video
    const video = await createVideo({
        ...req.body,
        watermark: limits.shouldIncludeWatermark(),
        resolution: limits.plan.features.resolution,
        voice_type: limits.plan.features.voice_type
    });
    
    res.json({ video, remaining_videos: videoCheck.remaining });
});
```

---

## 📊 **DASHBOARD DE FACTURACIÓN**

### **Componente React para Billing**

```jsx
// BillingDashboard.jsx
import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('pk_live_xxxxxxxxxxxxxxxxxxxxx');

function BillingDashboard({ user }) {
    const [usage, setUsage] = useState(null);
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetchUsageData();
        fetchInvoices();
    }, []);
    
    const fetchUsageData = async () => {
        const response = await fetch('/api/usage/current');
        const data = await response.json();
        setUsage(data);
        setLoading(false);
    };
    
    const handleUpgrade = async (planId) => {
        const stripe = await stripePromise;
        
        const response = await fetch('/api/billing/create-checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ planId, userId: user.id })
        });
        
        const session = await response.json();
        
        const result = await stripe.redirectToCheckout({
            sessionId: session.id
        });
        
        if (result.error) {
            alert(result.error.message);
        }
    };
    
    const UsageCard = ({ title, used, limit, unit }) => {
        const percentage = limit === -1 ? 0 : (used / limit) * 100;
        const isUnlimited = limit === -1;
        
        return (
            <div className="usage-card">
                <h4>{title}</h4>
                <div className="usage-stats">
                    <span className="current">{used}</span>
                    {!isUnlimited && <span className="limit">/ {limit} {unit}</span>}
                    {isUnlimited && <span className="unlimited">Ilimitado</span>}
                </div>
                {!isUnlimited && (
                    <div className="progress-bar">
                        <div 
                            className={`progress-fill ${percentage > 80 ? 'warning' : ''}`}
                            style={{ width: `${Math.min(percentage, 100)}%` }}
                        />
                    </div>
                )}
                {percentage > 90 && (
                    <button onClick={() => handleUpgrade('plus')} className="upgrade-btn">
                        Actualizar Plan
                    </button>
                )}
            </div>
        );
    };
    
    if (loading) return <div>Cargando...</div>;
    
    return (
        <div className="billing-dashboard">
            <h2>Estado de la Cuenta</h2>
            
            <div className="plan-info">
                <h3>Plan Actual: {user.plan_name}</h3>
                <p>Próxima facturación: {user.next_billing_date}</p>
                {user.trial_ends_at && (
                    <p className="trial-notice">
                        Período de prueba termina: {user.trial_ends_at}
                    </p>
                )}
            </div>
            
            <div className="usage-grid">
                <UsageCard 
                    title="Videos Creados"
                    used={usage.videos_used}
                    limit={usage.videos_limit}
                    unit="videos"
                />
                <UsageCard 
                    title="Almacenamiento"
                    used={usage.storage_used_gb}
                    limit={usage.storage_limit_gb}
                    unit="GB"
                />
                <UsageCard 
                    title="Llamadas API"
                    used={usage.api_calls_used}
                    limit={usage.api_calls_limit}
                    unit="llamadas"
                />
            </div>
            
            <div className="billing-actions">
                <button onClick={() => handleUpgrade('plus')}>
                    Actualizar Plan
                </button>
                <button onClick={() => window.open('/api/billing/portal')}>
                    Gestionar Facturación
                </button>
            </div>
        </div>
    );
}
```

---

## 🎯 **ONBOARDING FREEMIUM**

### **Flujo de Onboarding Inteligente**

```javascript
// onboarding.js
class OnboardingFlow {
    constructor(user) {
        this.user = user;
        this.steps = this.getStepsForPlan(user.plan);
    }
    
    getStepsForPlan(plan) {
        const baseSteps = [
            {
                id: 'welcome',
                title: 'Bienvenido a Q-AVIOGEN',
                component: 'WelcomeStep',
                required: true
            },
            {
                id: 'first_video',
                title: 'Cree su primer video',
                component: 'FirstVideoStep',
                required: true
            }
        ];
        
        if (plan === 'free') {
            baseSteps.push({
                id: 'free_limitations',
                title: 'Conozca las limitaciones del plan gratuito',
                component: 'FreeLimitationsStep',
                required: true
            });
        }
        
        if (plan !== 'free') {
            baseSteps.push({
                id: 'advanced_features',
                title: 'Explore funciones avanzadas',
                component: 'AdvancedFeaturesStep',
                required: false
            });
        }
        
        return baseSteps;
    }
    
    // Mostrar notificación inteligente según uso
    getSmartNotification(userStats) {
        const { videos_used, videos_limit, plan } = userStats;
        
        if (plan === 'free') {
            if (videos_used === 0) {
                return {
                    type: 'welcome',
                    title: '¡Comience ahora!',
                    message: 'Cree su primer video gratis. Tiene 3 videos disponibles este mes.',
                    action: 'Crear Video',
                    priority: 'high'
                };
            }
            
            if (videos_used === 2) {
                return {
                    type: 'limit_warning',
                    title: '¡Solo queda 1 video!',
                    message: 'Ha usado 2 de 3 videos gratuitos. Actualice para acceso ilimitado.',
                    action: 'Ver Planes',
                    priority: 'high'
                };
            }
            
            if (videos_used >= videos_limit) {
                return {
                    type: 'limit_reached',
                    title: 'Límite alcanzado',
                    message: 'Ha usado todos sus videos gratuitos. Actualice para continuar.',
                    action: 'Actualizar Ahora',
                    priority: 'critical'
                };
            }
        }
        
        return null;
    }
}
```

---

## 📈 **MÉTRICAS Y ANALYTICS FREEMIUM**

### **Tracking de Conversión**

```javascript
// analytics.js
class FreemiumAnalytics {
    static trackUserAction(userId, action, metadata = {}) {
        const event = {
            user_id: userId,
            action: action,
            timestamp: new Date(),
            metadata: metadata
        };
        
        // Enviar a sistema de analytics
        this.sendToAnalytics(event);
        
        // Triggers automáticos basados en comportamiento
        this.checkConversionTriggers(userId, action, metadata);
    }
    
    static checkConversionTriggers(userId, action, metadata) {
        switch (action) {
            case 'video_created':
                if (metadata.attempt_number === 1) {
                    // Primera vez creando video - mostrar valor
                    this.triggerEmail(userId, 'first_video_success');
                }
                break;
                
            case 'limit_reached':
                // Usuario alcanzó límite - ofrecer upgrade
                this.triggerUpgradeOffer(userId, 'limit_reached');
                break;
                
            case 'video_download_attempted':
                if (metadata.plan === 'free' && metadata.duration > 30) {
                    // Intentó descargar video largo - upsell
                    this.triggerUpgradeOffer(userId, 'long_video_attempted');
                }
                break;
                
            case 'quality_upgrade_clicked':
                // Usuario interesado en mejor calidad
                this.triggerDemo(userId, 'quality_comparison');
                break;
        }
    }
    
    static triggerUpgradeOffer(userId, reason) {
        const offers = {
            'limit_reached': {
                discount: 30,
                message: 'Actualice ahora y obtenga 30% de descuento',
                valid_hours: 24
            },
            'long_video_attempted': {
                discount: 20,
                message: 'Videos más largos disponibles en Plan Base',
                valid_hours: 48
            }
        };
        
        const offer = offers[reason];
        if (offer) {
            this.createPersonalizedOffer(userId, offer);
        }
    }
}

// Uso en la aplicación
FreemiumAnalytics.trackUserAction(user.id, 'video_created', {
    duration: 45,
    plan: user.plan,
    attempt_number: 1,
    watermark_included: true
});
```

---

## 🎯 **ESTRATEGIA DE RETENCIÓN FREEMIUM**

### **Email Sequences Automáticos**

```javascript
// email-automation.js
const emailSequences = {
    free_user_onboarding: [
        {
            day: 0,
            subject: '¡Bienvenido a Q-AVIOGEN! Su primer video le espera',
            template: 'welcome_free',
            trigger: 'signup'
        },
        {
            day: 1,
            subject: '¿Ya creó su primer video? Aquí tiene plantillas listas',
            template: 'first_video_reminder',
            condition: 'videos_created == 0'
        },
        {
            day: 3,
            subject: 'Vea lo que puede lograr con Q-AVIOGEN (ejemplos reales)',
            template: 'success_stories',
            condition: 'videos_created >= 1'
        },
        {
            day: 7,
            subject: 'Solo quedan X videos este mes - ¿necesita más?',
            template: 'mid_month_check',
            condition: 'videos_used >= 2'
        },
        {
            day: 14,
            subject: 'Oferta especial: 50% descuento en Plan Base',
            template: 'upgrade_offer',
            condition: 'videos_used >= 2'
        }
    ],
    
    limit_reached: [
        {
            immediate: true,
            subject: 'Ha alcanzado su límite - Actualice ahora con 40% descuento',
            template: 'limit_reached_upgrade'
        },
        {
            day: 1,
            subject: '¿Perdió oportunidades por el límite? Solución aquí',
            template: 'post_limit_value'
        }
    ]
};
```

Este sistema completo proporciona:

1. **💳 Integración completa de pagos** con Stripe y PayPal
2. **🔒 Sistema robusto de limitaciones** freemium
3. **📊 Dashboard de facturación** profesional
4. **🎯 Onboarding inteligente** basado en el plan
5. **📈 Analytics y conversión** automática
6. **📧 Email marketing** automatizado

¿Desea que implemente alguna parte específica o que cree más detalles sobre algún componente?
