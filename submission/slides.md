# Slide Deck — Cocina de Casa
### AMD Developer Hackathon Act II — Track 3 (Unicorn Track)

Sugerencia: 8 slides, formato 16:9. Contenido listo para pegar en Google Slides / Canva / Pitch.

---

## Slide 1 — Portada
**Cocina de Casa**
*AI Restaurant Operator*
Built on Gemma + AMD Developer Cloud (via Fireworks AI)
[Nombre del equipo] · AMD Developer Hackathon Act II · Track 3

---

## Slide 2 — El problema
**Los restaurantes independientes no pueden pagar por IA enterprise**
- Miles de restaurantes familiares operan con 1-2 personas, sin equipo de marketing ni POS.
- Pedidos gestionados manualmente por WhatsApp, mensaje a mensaje.
- Publicaciones en redes irregulares → menos ventas.
- Inventario sin control → se agotan platos sin avisar a tiempo.

---

## Slide 3 — La solución
**Un operador de restaurante autónomo, ya en producción**
- Agente de pedidos 24/7 por WhatsApp (lenguaje natural → pedido estructurado).
- 8 agentes programados: menú, marketing bilingüe, broadcasts, alertas de inventario.
- Multi-canal: WhatsApp + Facebook + Instagram, un solo backend.
- No es una demo — corre hoy para un restaurante real en Winston-Salem, NC.

---

## Slide 4 — Demo (capturas reales)
[Insertar 2-3 capturas de pantalla reales]
1. Cliente pide por WhatsApp → confirmación con ID de pedido
2. Notificación instantánea al dueño
3. Post automático bilingüe en Instagram/Facebook

---

## Slide 5 — Arquitectura y uso de AMD
```
WhatsApp / Meta Graph API
        │
     Flask + APScheduler  ← containerizado (Docker)
        │
   agents/llm.py
        │
  Fireworks AI API
        │
  Gemma (hospedado en AMD Developer Cloud)
```
- Razonamiento del agente: **Gemma vía Fireworks AI**, hardware AMD.
- Aplicación completa: **containerizada**, lista para AMD Developer Cloud.
- Elegible para el premio **"Best AMD-Hosted Gemma Project"**.

---

## Slide 6 — Modelo de negocio / mercado
- **SaaS vertical** para restaurantes independientes: suscripción mensual.
- Canal de entrada = WhatsApp (cero fricción, el cliente final ya lo usa).
- Mercado: cientos de miles de restaurantes familiares en EE.UU. y LATAM sin
  presupuesto para herramientas enterprise de IA.
- Validación real: ya operando con ingresos reales para un restaurante.

---

## Slide 7 — Roadmap
- Onboarding self-service multi-tenant (hoy es single-restaurant).
- Dashboard web para el dueño (hoy 100% vía WhatsApp).
- Pagos integrados (Stripe) + reportes de ventas automáticos.
- Expandir el agente de pedidos con más idiomas y canales (Telegram, SMS).

---

## Slide 8 — Cierre
**Cocina de Casa**
De un restaurante familiar a una plataforma para miles.
Construido con Gemma en AMD Developer Cloud.
[Link al repo] · [Link a la demo]
