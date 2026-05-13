# Matriz RGPD de datos — Kiosk Biometric Verification

**Documento de trabajo para DPIA / EIPD v0.1.**  
**Estado:** preliminar, pendiente de revisión por DPO/abogado especializado.  
**Pendiente de validación por abogado/DPO:** bases jurídicas, excepción del art. 9 RGPD si hay biometría, roles de tratamiento, retención, necesidad/proporcionalidad y eventual consulta previa AEPD.  
**Principio rector:** verificar mayoría de edad con la mínima exposición de datos personales posible.

> Este documento no sustituye una Evaluación de Impacto relativa a la Protección de Datos. Sirve como mapa inicial para identificar datos, finalidades, bases jurídicas, riesgos y medidas de minimización.

---

## 1. Alcance del tratamiento

El sistema se plantea como una capa de verificación para autorizar o bloquear una operación en un terminal de autoservicio o flujo semi-asistido.

El tratamiento se limita idealmente a una sesión concreta:

1. Usuario inicia verificación.
2. Sistema lee o valida documento/atributo de edad.
3. Opcionalmente realiza prueba de vivacidad y comparación 1:1.
4. Decide si la operación puede continuar.
5. Borra datos sensibles.
6. Registra evidencia técnica minimizada, sin identificadores directos.

No se persigue identificar al cliente para marketing, perfilado, fidelización ni seguimiento de hábitos de compra.

---

## 2. Supuestos de diseño privacy-by-design

- No reconocimiento facial 1:N.
- No almacenamiento de imágenes faciales.
- No almacenamiento de plantillas biométricas ni embeddings.
- No almacenamiento de DNI/NIE, nombre, dirección o fecha de nacimiento completa en logs.
- Procesamiento local/edge preferente frente a envío a cloud.
- Logs minimizados mediante HMAC y sal/clave rotatoria. Tratarlos inicialmente como **seudonimizados**: no calificarlos como anónimos mientras exista clave/secreto, granularidad temporal, ID de terminal o posibilidad razonable de enlace con TPV, CCTV, turnos, incidencias o registros del operador.
- Separación entre logs técnicos, logs de seguridad e información comercial.
- Modo *fail-closed*: ante duda, error o falta de lectura, no se autoriza la operación.
- Información clara al usuario antes de iniciar la verificación.
- Alternativa o asistencia humana a evaluar cuando sea posible.

---

## 3. Matriz de datos

| Dato / categoría | Origen | Finalidad | Base jurídica preliminar | Persistencia propuesta | Riesgo | Medidas |
|---|---|---|---|---|---|---|
| Datos del documento leídos por NFC/DNIe/eID o equivalente | Documento oficial del usuario | Validar autenticidad y extraer atributo de edad | Pendiente: obligación legal / interés legítimo / consentimiento u otra base según diseño | Solo memoria durante sesión | Alto | Lectura mínima, cifrado en memoria si aplica, borrado seguro |
| Fecha de nacimiento o atributo de mayoría de edad | Documento | Calcular si el usuario es mayor de edad | Pendiente de análisis legal | No almacenar; convertir a resultado mayor/no mayor | Alto | Minimización, no logs de fecha completa |
| Fotografía del chip/documento | Documento | Comparación 1:1 contra rostro vivo, si procede | Posible categoría especial; requiere análisis específico | Solo memoria durante sesión | Muy alto | No persistir, DPIA, revisión proporcionalidad |
| Imagen facial capturada en cámara | Cámara local | Vivacidad y comparación 1:1 opcional | Posible categoría especial; requiere base del art. 6 RGPD y excepción del art. 9 si aplica, a validar | Solo memoria durante sesión | Muy alto | Procesamiento local, no templates persistentes, borrado inmediato |
| Resultado de liveness/PAD | Motor biométrico | Evitar suplantación con foto/vídeo | Igual que biometría si vinculado a identidad | Resultado técnico efímero o log agregado no personal | Alto | No guardar imagen ni score identificable salvo justificación |
| Embedding/template facial | Motor biométrico | Matching 1:1 transitorio | Categoría especial si permite identificación | No almacenar | Muy alto | Generar en memoria, borrar tras decisión, prohibir exportación |
| Resultado de verificación | Sistema | Autorizar/bloquear operación | Necesario para cumplimiento/seguridad | Log mínimo: aprobado/rechazado/error | Medio | Sin identificadores directos; granularidad controlada |
| Token HMAC o identificador técnico minimizado | Sistema | Auditoría sin identificación directa y detección de abuso/incidencias | Interés legítimo / cumplimiento, pendiente de ponderación | Conservación proporcional y documentada | Medio-alto | Considerar dato seudonimizado por defecto; separación de claves, rotación, control de acceso, evitar granularidad excesiva, revisar riesgo de enlace con TPV/CCTV/horarios |
| Fecha y hora de operación | Sistema | Auditoría, inspección, soporte | Interés legítimo / cumplimiento | Conservación proporcional | Bajo-medio | Asociar solo a token no reversible |
| ID terminal / versión software | Sistema | Trazabilidad técnica | Interés legítimo / seguridad | Conservación proporcional | Bajo | Sin vinculación personal directa |
| Código de error/fallo | Sistema | Soporte, seguridad, mejora | Interés legítimo / seguridad | Conservación proporcional | Bajo-medio | Evitar mensajes que incluyan identificadores o datos personales innecesarios |
| Datos de pago | TPV/proveedor de pago | Cobro | Responsable/proveedor separado | Según normativa pagos/fiscal | Alto | Separación lógica; no mezclar con biometría |
| Producto comprado | TPV/stock | Venta, stock, obligaciones comerciales | Ejecución venta / obligaciones fiscales | Según sistema comercial | Medio | Separar de verificación de identidad |
| Grabación CCTV del local | Local/operador si existe | Seguridad física | Fuera del sistema; base propia | Según política local | Alto | No integrar salvo necesidad explícita |

---

## 4. Bases jurídicas — hipótesis a validar

La base jurídica no debe cerrarse sin asesoramiento. Opciones a analizar:

### Obligación legal

Podría aplicar parcialmente si el operador debe impedir venta a menores, pero no debe darse por suficiente para cualquier medio técnico. Debe confirmarse si la norma habilita el tratamiento concreto y si es suficientemente clara y específica, especialmente para biometría.

### Interés legítimo

Podría justificar controles técnicos y auditoría antifraude si supera ponderación, pero es delicado para biometría y no basta por sí solo para categorías especiales.

### Consentimiento explícito

Podría plantearse para biometría, pero debe ser libre, específico, informado, inequívoco y explícito cuando proceda. En un contexto donde la verificación condiciona la compra, existe riesgo de que no sea libre si no hay alternativa real, equivalente y no penalizadora.

### Interés público / requisito legal específico

Solo aplicable si existe norma habilitante clara. No asumir sin informe legal.

**Conclusión preliminar:** diseñar el MVP para poder operar con verificación documental y/o asistida sin biometría obligatoria, y tratar la biometría como módulo opcional sujeto a DPIA y criterio legal.

---

## 5. DPIA / EIPD — disparadores claros

La DPIA/EIPD debe planificarse antes de cualquier piloto con datos reales y presumirse necesaria —pendiente de confirmación formal por DPO/abogado— por:

- Tratamiento de datos biométricos o potencialmente biométricos.
- Decisión automatizada con impacto sobre acceso a una compra legalmente restringida.
- Posible uso en espacio físico abierto al público.
- Datos de documentos oficiales.
- Trazabilidad y auditoría de operaciones reguladas.
- Riesgo de exclusión, falsos rechazos o sesgos biométricos.

Contenido mínimo de la DPIA:

1. Descripción sistemática del tratamiento.
2. Finalidades y necesidad.
3. Evaluación de proporcionalidad.
4. Alternativas menos intrusivas.
5. Análisis de riesgos para derechos y libertades.
6. Medidas técnicas y organizativas.
7. Pruebas de precisión, sesgo y seguridad.
8. Gestión de proveedores/subencargados.
9. Procedimiento de atención de derechos.
10. Decisión documentada sobre consulta previa a AEPD si queda alto riesgo residual pese a las medidas.

---

## 6. Medidas técnicas y organizativas iniciales

### Minimización y arquitectura

- Procesamiento local siempre que sea viable.
- No enviar biometría a cloud sin necesidad justificada.
- Separar módulo de verificación de módulo de pago/stock.
- No conservar identificadores personales tras la sesión.
- Logs técnicos sin identificadores directos por defecto.

### Seguridad

- Cifrado de datos en tránsito y reposo cuando exista persistencia.
- Gestión segura de claves HMAC y rotación de sales.
- Control de acceso por roles para paneles de auditoría.
- Registro de cambios de configuración.
- Pruebas de seguridad antes de piloto.
- Actualizaciones firmadas y control de integridad del software del terminal.

### Operación

- Protocolo de fallo cerrado.
- Retirada temporal del terminal ante incidencias críticas.
- Registro de incidentes de seguridad y privacidad.
- Formación del personal del estanco.
- Señalización e información al usuario antes del tratamiento.

---

## 7. Derechos de las personas

Debe definirse cómo atender:

- Derecho de información.
- Acceso, supresión, limitación u oposición cuando proceda.
- Reclamaciones por falsos rechazos.
- Retirada de consentimiento si se usa biometría basada en consentimiento.
- Alternativa humana o procedimiento manual, si el modelo lo permite.

Dado que el sistema busca no conservar identificadores directos ni datos brutos, habrá que explicar claramente qué datos no se pueden recuperar porque no se almacenan.

---

## 8. Retención preliminar

| Categoría | Retención recomendada preliminar |
|---|---|
| Imágenes/documento/biometría | 0; borrado inmediato al finalizar sesión |
| Embeddings/templates | 0; prohibida persistencia |
| Resultado mayor/no mayor en memoria | Solo duración de sesión |
| Log minimizado de verificación | Plazo proporcional a inspección/soporte; definir legalmente; revisar si hay obligación sectorial y fijar borrado automático |
| Logs técnicos de error | Plazo corto, revisable; sin identificadores directos |
| Incidentes de seguridad | Según obligación legal y política de seguridad |
| Datos de pago/fiscales | Fuera de esta matriz; según normativa aplicable |

---

## 9. Riesgos residuales a resolver

- Validez de base jurídica para biometría.
- Proporcionalidad frente a alternativas menos intrusivas.
- Sesgo/falsos rechazos por edad, género, origen étnico, discapacidad o iluminación.
- Capacidad real de explicar el tratamiento al usuario en pantalla.
- Dependencia de proveedores biométricos.
- Posible reidentificación si se cruzan logs minimizados o seudonimizados con CCTV, TPV u horarios.
- Aceptación social y reputacional.

---

## 10. Decisiones antes de piloto con datos reales

1. ¿Habrá biometría en el piloto o solo verificación documental/simulada?
2. ¿Quién será responsable del tratamiento?
3. ¿Qué proveedor actuará como encargado/subencargado?
4. ¿Dónde se procesan los datos: local, cloud UE, terceros países?
5. ¿Qué alternativa existe si el usuario no acepta biometría?
6. ¿Qué logs son necesarios para inspección y cuáles pueden eliminarse?
7. ¿Debe consultarse previamente a la AEPD?
8. ¿Qué protocolo se seguirá ante falsos positivos/falsos negativos?

---

## 11. Próximo paso recomendado

Usar esta matriz como anexo para una revisión legal inicial. La decisión prudente es diseñar primero una versión **sin biometría obligatoria**, basada en verificación documental —preferentemente DNIe/NFC/eID cuando sea viable— y supervisión, y mantener la comparación facial 1:1 como hipótesis sujeta a justificación, DPIA y validación jurídica.

## 12. Criterio específico sobre anonimización, HMAC y seudonimización

Pendiente de validación por abogado/DPO.

Para este proyecto no conviene afirmar que un HMAC convierte automáticamente los logs en anónimos. Un registro con HMAC puede seguir siendo dato personal seudonimizado si:

- el responsable o encargado conserva la clave/secreto o puede recalcular tokens;
- el token se genera a partir de atributos relativamente estables o repetibles;
- la fecha/hora, terminal, producto, TPV, CCTV, turno o incidencia permiten inferir quién fue la persona;
- existe acceso interno o contractual a fuentes auxiliares que permitan reidentificación razonable;
- el objetivo del log es demostrar una operación individual, no solo estadísticas agregadas.

Diseño recomendado:

1. Minimizar el token: si no es imprescindible correlacionar sesiones, no generar identificador de persona/documento.
2. Preferir logs de evento no vinculables: terminal, versión, resultado y ventana temporal menos granular cuando sea suficiente.
3. Separar claves HMAC del entorno operativo y limitar acceso; rotación con destrucción verificable.
4. Documentar una prueba de anonimización si se pretende tratar los logs fuera del RGPD.
5. Mientras no exista esa prueba, aplicar RGPD completo: base jurídica, información, retención, derechos, seguridad y contrato de encargo.
