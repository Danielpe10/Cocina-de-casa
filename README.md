# 🍽️ Cocina de Casa — Sistema de IA

**Restaurante colombiano · Winston-Salem, NC**

Sistema completo de automatización con IA: recibe pedidos por WhatsApp, publica en Facebook/Instagram y gestiona el negocio 24/7 en piloto automático.

---

## ¿Qué hace el sistema?

### 🤖 Agente de pedidos (siempre activo)
El cliente escribe por WhatsApp:
```
"Quiero una bandeja paisa para las 6pm, entrega en 123 Main St, pago con Zelle"
```
El sistema:
1. Entiende el pedido con Google Gemini
2. Genera un ID único: **CDC-001**
3. Descuenta del inventario automáticamente
4. Confirma al cliente con resumen completo
5. Notifica al papá al instante con todos los detalles

### ⏰ 8 tareas automáticas (Eastern Time)

| Hora | Agente |
|------|--------|
| 09:00 | Reset del menú con cantidades frescas |
| 09:15 | Post bilingüe (ES+EN) a Facebook e Instagram |
| 09:30 | Broadcast del menú a clientes regulares por WhatsApp |
| 11:00 | Alerta de inventario bajo al dueño |
| 14:00 | "¡Se están agotando!" — urgencia en los últimos platos |
| 16:00 | Broadcast de tarde a clientes nuevos |
| 19:30 | "Últimos pedidos del día" |
| 20:30 | Resumen del día al papá por WhatsApp |

### 🍴 Menú base
| Plato | Precio |
|-------|--------|
| Bandeja Paisa | $16 |
| Sancocho | $14 |
| Arroz con Pollo | $13 |
| Frijoles | $12 |
| Empanadas | $8 |
| Arepas | $5 |
| Arroz con leche | $5 |
| Jugos | $4 |

---

## 🏗️ Arquitectura

```
cocina-de-casa/
├── main.py              # Arranque: Flask + APScheduler
├── config.py            # Variables de entorno
├── webhook.py           # Webhook WhatsApp + endpoints HTTP
├── agents/
│   ├── llm.py           # Google Gemini (gemini-1.5-flash)
│   ├── ordering.py      # Lógica de pedidos, CDC-XXX, notificaciones
│   ├── scheduler.py     # 8 tareas programadas (APScheduler)
│   ├── broadcast.py     # Broadcasts a clientes regulares y nuevos
│   ├── social.py        # Facebook + Instagram (Meta Graph API)
│   ├── menu.py          # Reset diario, stock, formatos ES/EN
│   ├── inventory.py     # Alertas de bajo stock, urgencia
│   └── whatsapp.py      # Cliente Meta WhatsApp Cloud API
└── data/
    ├── menu.json        # Menú con cantidades disponibles
    ├── orders.json      # Historial de pedidos
    └── customers.json   # Regulares y nuevos leads
```

**Stack:** Python 3.11+ · Flask · APScheduler · Google Gemini · Meta Cloud API

---

## 🚀 Instalación

### 1. Clonar el repo
```bash
git clone https://github.com/Danielpe10/cocina-de-casa.git
cd cocina-de-casa
git checkout claude/proxy-scope-limitation-UVXNw
```

### 2. Entorno virtual
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 3. Variables de entorno
```bash
cp .env.example .env
```
Edita `.env` con tus credenciales:

```env
# Meta WhatsApp Cloud API
WHATSAPP_TOKEN=tu_token_permanente
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=cualquier_string_secreto

# Meta Graph API (Facebook + Instagram)
META_PAGE_ACCESS_TOKEN=tu_page_access_token
FACEBOOK_PAGE_ID=tu_page_id
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu_ig_account_id

# Google Gemini
GEMINI_API_KEY=tu_gemini_api_key

# Número WhatsApp del dueño (solo dígitos, sin +)
OWNER_WHATSAPP=13365550001
```

### 4. Correr el sistema
```bash
python main.py
```

El servidor arranca en `http://localhost:8080`.

---

## 🔗 Configurar el Webhook de WhatsApp

1. Exponer el servidor con [ngrok](https://ngrok.com): `ngrok http 8080`
2. En [Meta Developer Console](https://developers.facebook.com) → tu app → WhatsApp → Configuration
3. **Webhook URL:** `https://TU-URL.ngrok.io/webhook`
4. **Verify Token:** el mismo que pusiste en `WHATSAPP_VERIFY_TOKEN`
5. Suscribir al evento: `messages`

Para producción usa un servidor con HTTPS fijo (Railway, Render, VPS).

---

## 🌐 Endpoints HTTP

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/webhook` | GET | Verificación Meta |
| `/webhook` | POST | Recibe mensajes WhatsApp |
| `/health` | GET | Estado del servidor |
| `/menu` | GET | Ver menú actual con stock |
| `/orders` | GET | Historial de pedidos del día |

---

## 📦 Deploy en producción (Railway recomendado)

```bash
# Procfile para Railway/Render
web: gunicorn webhook:app --bind 0.0.0.0:$PORT
```

O para correr el sistema completo con scheduler:
```bash
web: python main.py
```

Configura las mismas variables de `.env` como **Environment Variables** en tu plataforma.

---

## 🔑 ¿Dónde obtener las credenciales?

| Credencial | Dónde obtenerla |
|---|---|
| `WHATSAPP_TOKEN` | [Meta Developer](https://developers.facebook.com) → App → WhatsApp → API Setup |
| `WHATSAPP_PHONE_NUMBER_ID` | Mismo lugar, junto al token |
| `META_PAGE_ACCESS_TOKEN` | Meta Business Suite → Configuración → Acceso a la API |
| `FACEBOOK_PAGE_ID` | URL de tu página de Facebook |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Meta Business Suite → Instagram |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com) → Get API Key |

---

*Hecho con IA para Cocina de Casa — Winston-Salem, NC 🇨🇴*
