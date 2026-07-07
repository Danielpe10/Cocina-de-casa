# Guion — Video de presentación (60-90 seg)
### AMD Developer Hackathon Act II — Track 3 (Unicorn Track)

Formato sugerido: screen recording + voz en off. Duración total: ~75 segundos.

---

**[0:00–0:08] Hook — el problema**
Pantalla: foto/video del restaurante real (Cocina de Casa, Winston-Salem).
Voz en off:
> "Miles de restaurantes familiares reciben sus pedidos por WhatsApp, mensaje a mensaje,
> sin equipo de marketing ni sistemas. Nosotros les dimos un empleado que nunca duerme."

**[0:08–0:15] Presentación del producto**
Pantalla: logo/título "Cocina de Casa — AI Restaurant Operator".
Voz en off:
> "Cocina de Casa es un operador de restaurante autónomo, corriendo en producción
> hoy mismo, construido sobre Gemma en AMD Developer Cloud vía Fireworks AI."

**[0:15–0:35] Demo — flujo de pedido (la parte más importante)**
Pantalla: grabación real de WhatsApp.
1. Cliente escribe: *"Quiero una bandeja paisa para las 6pm, entrega en 123 Main St, pago con Zelle"*
2. El agente responde confirmando el pedido con ID **CDC-00X**.
3. Corte a notificación que le llega al dueño con el resumen completo.
Voz en off:
> "El agente entiende el pedido en lenguaje natural, genera un ID único,
> descuenta el inventario automáticamente y notifica al dueño al instante — cero intervención humana."

**[0:35–0:50] Demo — automatización de marketing**
Pantalla: post generado automáticamente en Facebook/Instagram (bilingüe ES/EN),
y el mensaje de "¡se están agotando!" enviado por WhatsApp.
Voz en off:
> "Y no se detiene ahí: ocho agentes programados publican en redes, avisan cuando
> el inventario está bajo, y generan urgencia de venta — todo el día, todos los días."

**[0:50–1:05] Stack técnico / uso de AMD**
Pantalla: diagrama simple (usar el mismo diagrama de las slides): WhatsApp/Meta → Flask →
agents/llm.py → Fireworks AI (Gemma) → AMD Developer Cloud.
Voz en off:
> "Todo el razonamiento del agente corre sobre Gemma, alojado en hardware AMD
> a través de Fireworks AI. La aplicación completa está containerizada y lista
> para desplegar en AMD Developer Cloud."

**[1:05–1:15] Cierre — mercado y visión**
Pantalla: slide de cierre con el nombre del proyecto y "Built for AMD Developer Hackathon Act II".
Voz en off:
> "Esto ya es un negocio real. La visión: llevarlo a cientos de restaurantes
> independientes que hoy no pueden pagar por IA. Gracias."

---

## Shot list / checklist de grabación
- [ ] Captura de pantalla del chat de WhatsApp real (pedido → confirmación)
- [ ] Captura de la notificación al dueño
- [ ] Captura del post automático en Facebook/Instagram
- [ ] Captura del mensaje de "últimas unidades"
- [ ] Diagrama de arquitectura (mismo de las slides, slide 5)
- [ ] Slide de cierre con logo/nombre del proyecto

## Notas de producción
- Grabar el flujo end-to-end en un número de WhatsApp de prueba antes de grabar el video final.
- Subtítulos en inglés recomendados (el jurado internacional puede no hablar español).
- Mantenerlo bajo 90 segundos — los jueces revisan muchos proyectos.
