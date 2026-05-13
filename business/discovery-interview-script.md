# Guion de entrevistas de discovery

**Proyecto:** verificación segura de mayoría de edad para venta asistida, semi-automatizada o automatizada en sectores regulados.  
**Audiencias:** estancos, asociaciones, integradores de kioscos/vending, proveedores de identidad/biometría y expertos legales.  
**Objetivo:** validar problema, restricciones, disposición a colaborar y criterios de piloto antes de construir hardware o contactar formalmente a reguladores.

> Este guion es para conversaciones exploratorias. No vender, no prometer legalidad, no pedir datos personales de clientes, no realizar pruebas con menores ni datos reales. Pendiente de validación por abogado/DPO antes de cualquier piloto real.

---

## 1. Principios de la entrevista

- Escuchar más que explicar.
- No liderar la respuesta con “biometría” o “tabaco autónomo”.
- Presentar el proyecto como **capa de cumplimiento y verificación de edad**, basada primero en documento/eID y no en biometría como reclamo principal.
- Preguntar por problemas reales, no por opiniones abstractas.
- Separar claramente interés comercial, viabilidad operativa y riesgo regulatorio.
- Cerrar siempre con permiso para seguimiento y posibles recomendaciones de contacto.
- Si se toman notas, no recoger nombres de clientes ni casos identificables; anonimizar entrevistas y almacenar solo datos de contacto profesional necesarios.

Duración ideal: 25–35 minutos.

---

## 2. Apertura sugerida

Hola, gracias por dedicarme este tiempo.

Estoy validando un proyecto técnico de verificación segura de mayoría de edad para entornos de venta automatizada o semi-automatizada en sectores regulados. El caso inicial que estoy estudiando es el estanco, porque exige control estricto de edad y cumplimiento normativo.

No estoy vendiendo una solución cerrada ni asumiendo que sea legalmente desplegable. Precisamente quiero entender mejor los límites reales: operación diaria, regulación, aceptación del cliente, costes y qué tendría que demostrarse antes de plantear un piloto.

¿Te parece bien si te hago unas preguntas sobre cómo funciona hoy el control de edad y qué problemas ves en una solución de este tipo?

---

## 3. Bloque A — contexto del entrevistado

1. ¿Cuál es tu relación con el sector?  
   - Estanquero/a.
   - Asociación.
   - Vending/kioscos.
   - Tecnología de identidad.
   - Legal/RGPD.
   - Otro.

2. ¿Qué tipo de operaciones gestionas o conoces mejor?  
   - Venta presencial.
   - Vending.
   - Autoservicio.
   - TPV/stock.
   - Compliance/regulación.

3. ¿Cuánta exposición tienes a controles de edad o venta restringida?

Notas:

- Rol:
- Tamaño/volumen aproximado:
- Nivel de decisión:
- Posible contacto posterior:

---

## 4. Bloque B — problema actual

4. ¿Cómo se controla actualmente que no se vende a menores?

5. ¿En qué situaciones se vuelve más difícil controlar la edad?  
   - Horas punta.
   - Personal nuevo.
   - Clientes habituales jóvenes.
   - Máquinas/vending.
   - Compra por terceros.
   - Presión o conflicto con el cliente.

6. ¿Ha habido inspecciones, sanciones o preocupación real por este tema en el sector?

7. ¿Qué evidencia se conserva hoy para demostrar que se ha actuado correctamente?

8. ¿El control de edad es un problema frecuente, ocasional o más bien teórico?

9. Si pudieras mejorar una cosa del proceso actual, ¿cuál sería?

Señales a observar:

- Dolor económico o legal real.
- Miedo a sanciones.
- Falta de proceso documentado.
- Rechazo a añadir fricción al cliente.
- Necesidad de no ralentizar la venta.

---

## 5. Bloque C — reacción al concepto

Explicación breve:

> La idea es un módulo que verifica mayoría de edad antes de permitir una operación en un terminal. Podría usar documento oficial/eID —por ejemplo DNIe/NFC cuando sea viable—, registrar una evidencia técnica minimizada sin identificadores directos y bloquear la venta si la verificación falla. La biometría, si se estudiara, sería solo 1:1, transitoria y sujeta a DPIA/revisión legal; no reconocimiento masivo ni almacenamiento de plantillas. Los logs HMAC se tratarían prudentemente como seudónimos hasta que un DPO/abogado confirme otra cosa.

10. ¿Qué primera reacción te genera este enfoque?

11. ¿Lo verías más útil como herramienta asistida por personal o como terminal autónomo?

12. ¿Dónde tendría más sentido instalarlo?  
   - Dentro de estanco.
   - Zona visible/supervisada.
   - Máquina externa.
   - Back-office/herramienta para empleado.
   - Otro.

13. ¿Qué parte te parece más valiosa?  
   - Verificación documental.
   - Registro de auditoría.
   - Bloqueo automático.
   - Reducción de responsabilidad.
   - Rapidez operativa.
   - Imagen de cumplimiento.

14. ¿Qué parte te genera más rechazo o preocupación?

15. ¿Qué tendría que ser verdad para que lo consideraras viable?

---

## 6. Bloque D — operación y experiencia de usuario

16. ¿Cuánto tiempo máximo podría durar una verificación sin molestar al cliente?

17. ¿Qué ocurre hoy si un cliente no lleva documento o se niega a mostrarlo?

18. ¿Sería aceptable que el sistema bloquee la operación y derive al personal?

19. ¿Qué nivel de intervención humana sería razonable?

20. ¿Cómo debería explicarse al cliente para no parecer invasivo?

21. ¿Qué idioma/accesibilidad serían necesarios?

22. ¿Qué incidencias operativas te preocupan más?  
   - Fallos de lectura.
   - Falsos rechazos.
   - Clientes enfadados.
   - Lentitud.
   - Mantenimiento.
   - Higiene/uso de cámara o lector.
   - Coste de soporte.

---

## 7. Bloque E — datos, privacidad y confianza

23. ¿Qué nivel de sensibilidad crees que tendría el cliente ante lectura de documento?

24. ¿Y ante una comprobación facial 1:1 si no se guarda la imagen?

25. ¿Cambiaría tu percepción si existiera alternativa manual?

26. ¿Qué garantías necesitarías ver por escrito?  
   - No almacenar datos personales.
   - Informe RGPD/DPIA y validación DPO/abogado.
   - Proveedor certificado.
   - Auditoría externa.
   - Criterio regulatorio.
   - Seguro/responsabilidad.

27. ¿Quién crees que debería ser responsable si el sistema falla?

28. ¿Te preocuparía que los logs técnicos, aunque no incluyan nombre o DNI, pudieran vincularse a clientes concretos mediante hora, TPV, CCTV o incidencias?

---

## 8. Bloque F — compra, precio y adopción

29. Si el problema estuviera resuelto legalmente, ¿quién decidiría comprar o probar una solución así?

30. ¿Qué modelo tendría más sentido?

- Compra de equipo.
- Cuota mensual por terminal.
- Pago por verificación.
- Servicio incluido por fabricante/integrador.
- Asociación/central de compras.

31. ¿Qué rango de precio mensual sería razonable para un estanco pequeño?

32. ¿Qué coste inicial sería asumible para una prueba?

33. ¿Qué objeciones bloquearían la compra?

34. ¿Qué evidencia pedirías antes de probarlo?

35. ¿Conoces negocios que serían más abiertos a probar tecnología de este tipo?

Notas sobre pricing:

- Umbral bajo:
- Umbral razonable:
- Umbral imposible:
- Decisor:
- Prescriptor:

---

## 9. Bloque G — piloto

36. ¿Aceptarías ver una demo simulada sin datos reales?

37. ¿Tendría sentido un piloto no comercial, sin dispensar producto real?

38. ¿Qué condiciones mínimas exigirías para un piloto?

39. ¿Durante cuánto tiempo debería probarse para obtener conclusiones?

40. ¿Qué métricas serían relevantes?

- Tiempo medio de verificación.
- Tasa de fallos.
- Reacción de clientes.
- Intervenciones manuales.
- Incidencias técnicas.
- Percepción de seguridad.
- Reducción de riesgo operativo.

41. ¿Qué haría que el piloto fuera claramente un éxito?

42. ¿Qué haría que se descartara inmediatamente?

---

## 10. Bloque H — regulación y contactos

43. ¿Qué organismo o asociación crees que debería consultarse primero?

44. ¿Conoces precedentes de automatización o autoservicio en estancos?

45. ¿Qué límites regulatorios crees que son más críticos?

46. ¿Qué documentación daría confianza a la hora de hablar con el Comisionado o con una asociación?

47. ¿Me recomendarías hablar con alguien más para contrastar esto?

48. ¿Puedo mencionarte como persona que me orientó, o prefieres que no?

---

## 11. Cierre

Muchas gracias. Me llevo sobre todo [resumir 2–3 aprendizajes].

Como próximos pasos estoy preparando documentación legal-producto, matriz RGPD y preguntas regulatorias. Si tiene sentido, ¿podría enviarte una versión resumida para pedir feedback, sin compromiso?

¿Hay algo importante que no te haya preguntado?

---

## 12. Plantilla de notas post-entrevista

**Fecha:**  
**Entrevistado / organización:**  
**Tipo:** estanco / asociación / integrador / legal / proveedor / otro  
**Nivel de interés:** alto / medio / bajo  
**Nivel de riesgo percibido:** alto / medio / bajo

### Aprendizajes clave

1.
2.
3.

### Dolor real detectado

- [ ] Sí, fuerte
- [ ] Sí, moderado
- [ ] Débil
- [ ] No validado

Descripción:

### Objeciones principales

1.
2.
3.

### Señales de compra/piloto

- [ ] Pediría demo
- [ ] Presentaría a otro contacto
- [ ] Aceptaría piloto
- [ ] Solo curiosidad
- [ ] Rechazo claro

Notas:

### Requisitos antes de avanzar

- Legal:
- RGPD:
- Técnico:
- Operativo:
- Precio:

### Frases textuales útiles

> 

> 

### Próximo paso

- [ ] Enviar resumen
- [ ] Enviar one-pager
- [ ] Pedir contacto referido
- [ ] Invitar a demo
- [ ] No continuar

Fecha de seguimiento:

---

## 13. Criterios de decisión tras 5 entrevistas

Continuar si aparecen al menos 3 de estas señales:

- Existe preocupación real por sanciones o venta a menores.
- El flujo asistido/semi-asistido se percibe viable.
- Hay interés en demo o piloto.
- El precio estimado no se percibe imposible.
- Un actor sectorial recomienda hablar con otro decisor.
- La auditoría minimizada sin identificadores directos se valora positivamente.

Pivotar si:

- La biometría genera rechazo fuerte, pero la verificación documental interesa.
- El estanco no quiere hardware, pero integradores/vending sí.
- El caso tabaco bloquea, pero otros sectores regulados muestran interés.

Pausar si:

- Nadie percibe problema real.
- La regulación se ve inviable sin excepción clara.
- El coste operativo supera ampliamente la disposición a pagar.
- No hay camino razonable hacia piloto no comercial.

## 14. Límites de privacidad durante discovery

- No solicitar ni registrar datos de clientes finales, menores, documentos reales ni imágenes.
- No probar cámaras, documentos o biometría en entrevistas exploratorias.
- Si se documentan ejemplos de incidentes, redactarlos sin datos identificables.
- Informar al entrevistado de que el proyecto no está legalmente validado y que cualquier piloto requeriría revisión abogado/DPO, DPIA/EIPD y autorización/criterio sectorial cuando proceda.
- Separar notas comerciales de cualquier dato regulatorio sensible; conservar solo lo necesario para seguimiento profesional.
