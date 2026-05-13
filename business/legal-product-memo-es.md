# Memo legal-producto — Kiosk Biometric Verification

**Documento de trabajo para revisión legal, regulatoria y de partners.**  
**Proyecto:** capa segura de verificación de mayoría de edad para flujos asistidos, semi-asistidos o automatizados en sectores regulados.  
**Caso inicial:** entornos autorizados de venta de tabaco en España, especialmente estancos.  
**Estado:** prueba de concepto técnica y dossier de validación; no desplegado comercialmente.  
**Pendiente de validación por abogado/DPO:** todo criterio jurídico, base de legitimación, clasificación sectorial, retención y calificación de logs debe revisarse antes de tratar datos reales.

> Este documento no constituye asesoramiento jurídico. Su objetivo es describir el producto, acotar riesgos y preparar una conversación ordenada con abogados, reguladores, asociaciones sectoriales y posibles socios tecnológicos.

---

## 1. Resumen ejecutivo

El proyecto propone una **capa de verificación de edad e identidad** para terminales de autoservicio, kioscos o máquinas automatizadas —preferentemente en una primera fase asistida o semi-asistida— en entornos regulados. La primera hipótesis de validación se centra en estancos españoles, por ser un caso exigente donde la venta a menores está prohibida y donde el operador necesita controles trazables.

La recomendación estratégica actual es **no presentar el producto como “kiosco autónomo de tabaco”**, sino como:

> Sistema de verificación segura de mayoría de edad, basado principalmente en documento oficial/DNIe/NFC cuando sea viable, con privacidad desde el diseño, trazabilidad auditable y posible integración en entornos de venta autorizados.

La solución se ha diseñado para minimizar datos personales: lectura conceptual de documento/chip, validación criptográfica, cálculo de edad, posible comparación facial 1:1 transitoria y registro de auditoría con HMAC u otros mecanismos de minimización, evitando identificadores directos. El diseño objetivo evita almacenar imágenes, plantillas biométricas, embeddings faciales, DNI/NIE o datos identificativos en los logs. No obstante, por prudencia, los logs HMAC deben tratarse inicialmente como **datos personales seudonimizados** si el responsable o proveedor conserva claves, sales, secretos, granularidad temporal o medios razonables para vincularlos con una operación/persona; solo deberían calificarse como anónimos tras una evaluación documentada de anonimización y riesgo de reidentificación.

La hipótesis de producto más prudente para una primera validación es un **flujo asistido o semi-asistido dentro de un estanco autorizado**, con comportamiento *fail-closed* —si la verificación no es concluyente, no se completa la venta— y posibilidad de intervención humana.

---

## 2. Qué hace el sistema

### 2.1 Funciones principales

El sistema pretende realizar, de forma modular:

1. **Inicio de sesión de compra/verificación** en terminal o kiosco.
2. **Lectura de documento oficial compatible** mediante DNIe/NFC/ICAO 9303 o equivalente, en fase de prototipo simulada.
3. **Validación criptográfica conceptual** del documento frente a anclas de confianza oficiales en una implementación productiva.
4. **Extracción mínima de datos necesarios** para determinar mayoría de edad.
5. **Cálculo de edad** con reglas deterministas y control de casos límite.
6. **Opcional: prueba de vivacidad y comparación facial 1:1** contra la foto del documento/chip, de forma transitoria, si supera revisión legal y DPIA.
7. **Decisión de autorización/rechazo** de la operación.
8. **Registro de auditoría minimizado**, sin identificadores directos, para demostrar que el flujo de control se ejecutó.
9. **Borrado seguro de buffers sensibles** al finalizar cada sesión, incluyendo rutas de error.

### 2.2 Qué no hace el sistema

El sistema, en su diseño actual, **no** pretende:

- Identificar personas mediante reconocimiento facial 1:N.
- Crear listas de clientes, historiales personales o perfiles de consumo.
- Almacenar imágenes faciales, plantillas biométricas o embeddings.
- Guardar números de documento, nombre, fecha de nacimiento completa o dirección en logs.
- Sustituir obligaciones regulatorias del estanquero/concesionario.
- Permitir venta si la verificación falla o queda incompleta.
- Operar comercialmente sin validación legal previa.

---

## 3. Encaje regulatorio a validar

### 3.1 Tabaco y estancos

Puntos clave pendientes de criterio:

- Si el terminal sería considerado **máquina expendedora de tabaco**, extensión de punto de venta, sistema auxiliar dentro de estanco o categoría distinta.
- Si requiere autorización previa de modelo/dispositivo o inscripción específica.
- Qué grado de supervisión humana es obligatorio.
- Si puede operar exclusivamente dentro de locales autorizados y bajo responsabilidad del titular de la expendeduría.
- Qué evidencia debe conservarse para acreditar controles de mayoría de edad.

La consulta prioritaria debe dirigirse al **Comisionado para el Mercado de Tabacos**, idealmente después de revisión por abogado especializado.

### 3.2 Protección de datos y biometría

El uso de biometría para verificar que la persona presente coincide con el documento puede implicar tratamiento de datos biométricos de categoría especial cuando se utilice para identificación o autenticación inequívoca. La AEPD ha adoptado una posición exigente sobre biometría: incluso en escenarios 1:1 y aunque el tratamiento sea transitorio, debe justificarse base del art. 6 RGPD, una excepción válida del art. 9 RGPD cuando aplique, necesidad, idoneidad, proporcionalidad y ausencia de alternativas menos intrusivas.

Principios de diseño recomendados:

- **Minimización:** procesar solo lo imprescindible.
- **Limitación de finalidad:** verificar mayoría de edad para una operación concreta.
- **No persistencia biométrica:** no almacenar plantillas, imágenes ni embeddings.
- **Alternativas menos intrusivas:** valorar DNIe/documento, identidad digital, validación asistida o credenciales de edad antes de biometría.
- **DPIA/EIPD presumiblemente necesaria antes de cualquier piloto con datos reales:** por biometría, documentos oficiales, decisión automatizada, posible uso en espacios abiertos al público y riesgo de exclusión; confirmarlo y documentarlo con DPO/abogado.
- **Consulta previa AEPD:** no es un trámite inicial automático; procede si, tras la DPIA y medidas mitigadoras, persiste alto riesgo residual que no pueda reducirse adecuadamente.

### 3.3 AI Act y sistemas biométricos

Antes de despliegue comercial debe revisarse si los componentes de vivacidad, matching facial o decisión automatizada entran en categorías de alto riesgo o requieren obligaciones específicas bajo el Reglamento de IA.

Documentación mínima a preparar:

- Finalidad exacta del sistema.
- Métricas de precisión y sesgo.
- Evaluación PAD/liveness.
- Supervisión humana.
- Registro de eventos e incidentes.
- Gestión de proveedores y cambios de modelo.

---

## 4. Roles y responsabilidades preliminares

| Rol | Posible responsable | Pendiente de definir |
|---|---|---|
| Responsable de la venta | Titular del estanco/concesionario | Confirmar con Comisionado |
| Responsable del tratamiento | A determinar: titular del estanco, sociedad explotadora, proveedor o corresponsables | Depende de quién decida fines y medios; documentar art. 26 si hay corresponsabilidad |
| Encargado del tratamiento | Proveedor tecnológico si trata datos por cuenta del responsable | Contrato art. 28 RGPD, instrucciones, subencargados, auditoría y transferencias |
| Subencargados | SDK biométrico, cloud, mantenimiento, hardware | Mapa de proveedores requerido |
| Responsable de seguridad operativa | Operador + proveedor | SLA, incidentes, soporte |
| Responsable de auditoría/regulatorio | Operador | Evidencias aceptadas por autoridad |

La arquitectura contractual debe evitar ambigüedades: quién decide finalidades, quién accede a datos, quién responde ante inspecciones, y quién soporta fallos del sistema.

---

## 5. Datos tratados y retención propuesta

Diseño recomendado:

- Datos del documento: lectura solo en memoria durante la sesión.
- Fecha de nacimiento o atributo de mayoría de edad: procesado transitorio; no persistir dato bruto.
- Imagen facial/documento: transitoria; borrado inmediato.
- Resultado de verificación: conservar solo estado mínimo necesario.
- Auditoría: token HMAC o identificador técnico minimizado, fecha/hora, resultado técnico, terminal y versión de software, sin identificadores directos. Clasificación prudente: **seudónimo**, no anónimo, salvo informe específico que demuestre irreversibilidad práctica, separación efectiva de claves, agregación suficiente y ausencia de enlaces razonables con TPV/CCTV/turnos/horarios.
- Incidentes: registro técnico separado, evitando datos identificativos salvo necesidad legal explícita.

La retención de logs debe fijarse con criterio legal. Como hipótesis inicial: conservar logs técnicos minimizados, sin identificadores directos, durante el plazo proporcional para inspección, soporte e incidencias, y revisar si existe obligación sectorial específica. A efectos prudentes, tratarlos como seudonimizados salvo informe de anonimización.

---

## 6. Modelo MVP recomendado

### Opción recomendada para primera fase

**Herramienta asistida/semi-asistida dentro de estanco autorizado.**

Ventajas:

- Menor fricción regulatoria que una máquina completamente autónoma.
- Mantiene responsabilidad y supervisión humana.
- Permite validar utilidad operativa sin forzar el caso más restrictivo.
- Facilita pilotos no comerciales o con transacciones simuladas.

### Opción a aplazar

**Terminal completamente autónomo de venta de tabaco.**

Debe aplazarse hasta disponer de:

- Criterio jurídico/regulatorio preliminar.
- DPIA madura.
- Partner hardware.
- Protocolo de supervisión e incidentes.
- Evidencia de demanda comercial.

---

## 7. Riesgos principales

| Riesgo | Impacto | Mitigación propuesta |
|---|---:|---|
| Clasificación como máquina expendedora regulada | Alto | Consulta al Comisionado antes de piloto real |
| Biometría considerada desproporcionada | Alto | Diseñar alternativa sin biometría; usar 1:1 transitorio solo si se justifica |
| Falta de base jurídica clara | Alto | Revisión legal RGPD + sectorial antes de tratar datos reales |
| Venta indebida a menor por fallo técnico | Muy alto | Fail-closed, supervisión, pruebas, auditoría, seguro |
| Coste hardware/SDK superior al mercado objetivo | Medio-alto | Validar precio con estancos e integradores antes de construir |
| Dependencia de proveedor biométrico | Medio | Arquitectura modular y evaluación de varios proveedores |
| Rechazo social por biometría | Medio-alto | Transparencia, minimización, alternativas manuales, piloto limitado |

---

## 8. Decisiones pendientes antes de contactar a terceros

1. Definir si el primer MVP se presenta como **asistido/semi-asistido** o como **terminal automatizado**.
2. Confirmar si se incluye biometría en la narrativa inicial o se mantiene como módulo opcional sujeto a DPIA.
3. Preparar lista formal de preguntas al Comisionado.
4. Preparar matriz RGPD y flujo de datos.
5. Definir documentación mínima para entrevistas con estancos.
6. Identificar abogado/DPO adecuado para primera revisión.

---

## 9. Próxima acción recomendada

Antes de cualquier contacto externo:

1. Revisar este memo.
2. Revisar `questions-comisionado.md`.
3. Revisar `rgpd-data-matrix.md`.
4. Validar con un especialista legal si el enfoque de consulta es prudente.
5. Solo entonces iniciar conversaciones exploratorias, sin prometer despliegue ni legalidad confirmada.

## 10. Nota de prudencia legal / DPO

Pendiente de validación por abogado/DPO antes de cualquier piloto con datos reales:

- Confirmar base jurídica del art. 6 RGPD para verificación documental, logs y seguridad.
- Confirmar si existe excepción aplicable del art. 9 RGPD para biometría; no asumir que el consentimiento explícito será válido si no hay alternativa real equivalente.
- Documentar análisis de necesidad y proporcionalidad frente a opciones menos intrusivas: control manual, DNIe/eID sin rostro, credencial de mayoría de edad o verificación asistida.
- Tratar logs HMAC como seudonimizados por defecto y aplicar obligaciones RGPD hasta que exista evaluación robusta de anonimización.
- Validar roles responsable/encargado/corresponsables y contratos antes de seleccionar proveedores.
- Preparar DPIA/EIPD y, si queda alto riesgo residual, valorar consulta previa a la AEPD conforme al art. 36 RGPD.
