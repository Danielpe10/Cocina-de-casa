# Cocina de Casa — AI Restaurant Operator
### AMD Developer Hackathon: ACT II — Track 3 (Unicorn Track)

## 1. El problema

Miles de restaurantes familiares e independientes en EE.UU. (y en LATAM) operan con
recursos mínimos: un dueño, quizás un empleado, sin equipo de marketing ni sistemas.
Reciben pedidos por WhatsApp mensaje a mensaje, publican en redes cuando se acuerdan,
y pierden ventas por no responder a tiempo o por quedarse sin inventario sin avisar.

Contratar un community manager o un sistema de POS enterprise no es viable
económicamente para este segmento. El resultado: horas del dueño perdidas en tareas
repetitivas que un agente de IA puede hacer solo.

## 2. La solución — Cocina de Casa

Un **operador de restaurante autónomo basado en agentes de IA**, ya funcionando en
producción para un restaurante colombiano real en Winston-Salem, NC:

- **Agente de pedidos 24/7**: el cliente escribe por WhatsApp en lenguaje natural
  ("una bandeja paisa para las 6pm, pago con Zelle"), el agente interpreta el pedido,
  genera un ID único, descuenta inventario y notifica al dueño — sin intervención humana.
- **8 agentes programados**: reseteo diario de menú, publicaciones bilingües automáticas
  en Facebook/Instagram, broadcasts de marketing a clientes regulares y nuevos, alertas
  de inventario bajo, mensajes de urgencia ("¡se están agotando!"), y resumen diario al dueño.
- **Multi-canal real**: WhatsApp (Meta Cloud API) + Facebook + Instagram, todo orquestado
  desde un solo backend Flask + APScheduler.

Ya no es una demo: es un sistema que un negocio real usa todos los días.

## 3. Por qué esto es "Unicorn Track" y no un demo de un fin de semana

- **Producto, no prototipo**: arquitectura modular (`agents/ordering`, `agents/social`,
  `agents/inventory`, `agents/scheduler`...) pensada para escalar a más restaurantes.
- **Modelo de negocio claro**: SaaS vertical para restaurantes independientes —
  precio por suscripción mensual, sin fricción de setup (WhatsApp es el canal que
  el cliente final ya usa).
- **Mercado grande y desatendido**: cientos de miles de restaurantes familiares en
  EE.UU. sin presupuesto para herramientas enterprise de IA.

## 4. Uso de infraestructura AMD

Para el hackathon, migramos el cerebro del agente de Google Gemini a **Fireworks AI**,
corriendo modelos abiertos (**Gemma**) alojados en hardware AMD:

- Todo el razonamiento del agente (parseo de pedidos, generación de respuestas,
  copy de marketing bilingüe) pasa por **Fireworks AI API** en lugar de un
  proveedor cerrado.
- Compute de la aplicación (Flask + scheduler, contenedor Docker) corre sobre
  **AMD Developer Cloud**.
- Esto nos hace elegibles también para el premio adicional **"Best AMD-Hosted
  Gemma Project"**.

## 5. Qué se entrega

- Repo público en GitHub, containerizado (Docker), con README de setup/uso.
- Demo desplegada y accesible (URL pública).
- Video de presentación mostrando el flujo real: pedido por WhatsApp → confirmación →
  notificación al dueño → post automático en redes.

## 6. Roadmap post-hackathon (para el pitch de "market potential")

- Onboarding self-service para nuevos restaurantes (multi-tenant).
- Dashboard web para el dueño (hoy todo es vía WhatsApp).
- Integración de pagos (Stripe/Zelle automatizado) y reportes de ventas.
