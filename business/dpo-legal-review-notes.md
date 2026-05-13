# Notas de revisión legal/DPO externa — Kiosk Biometric Verification

Documento de preparación para revisión profesional. No constituye asesoramiento jurídico.

## 1. Checklist prioritario para abogado/DPO

- Confirmar clasificación sectorial ante normativa de tabaco/vending: máquina expendedora, sistema auxiliar, terminal asistido u otra categoría.
- Validar quién será responsable del tratamiento, encargado, subencargado o corresponsable según el modelo comercial.
- Determinar bases jurídicas art. 6 RGPD para verificación documental, auditoría, seguridad, soporte e incidencias.
- Si hay biometría, determinar si aplica art. 9 RGPD y qué excepción podría sostenerse; no asumir consentimiento explícito si no hay alternativa real.
- Evaluar necesidad, idoneidad y proporcionalidad frente a alternativas menos intrusivas.
- Redactar DPIA/EIPD antes de cualquier piloto con datos reales.
- Decidir si procede consulta previa AEPD si queda alto riesgo residual tras medidas.
- Revisar información al usuario, rutas de ejercicio de derechos y gestión de reclamaciones/falsos rechazos.
- Revisar contratos art. 28 RGPD, subencargados, transferencias internacionales, soporte remoto y acceso a logs.
- Revisar obligaciones AI Act si el módulo de liveness/matching/decisión automatizada encaja como sistema de IA sujeto a obligaciones.

## 2. Punto crítico: HMAC, anonimización y seudonimización

Criterio prudente de trabajo: los logs HMAC no deben presentarse como anónimos por defecto. Deben tratarse como seudonimizados si existe cualquier posibilidad razonable de reidentificación mediante claves, secretos, granularidad temporal, terminal, TPV, CCTV, turnos, incidencias o acceso de proveedor/operador.

Preguntas para validación:

1. ¿Es necesario generar token por operación o bastan logs no correlables?
2. ¿Qué entradas se usan para el HMAC? ¿Incluyen DNI, fecha nacimiento, número de documento, foto hash u otro atributo estable?
3. ¿Quién conserva la clave/secreto y durante cuánto tiempo?
4. ¿Puede recalcularse el token a posteriori?
5. ¿Se puede vincular el evento con TPV, producto, CCTV o turno del empleado?
6. ¿Qué granularidad temporal es estrictamente necesaria?
7. ¿Puede destruirse la clave para convertir logs antiguos en no vinculables?
8. ¿Se pretende usar logs para inspección individual o solo métricas agregadas?

## 3. Decisiones que no debería tomar el equipo sin revisión externa

- Activar biometría real en piloto.
- Contactar reguladores con una afirmación de legalidad cerrada.
- Calificar logs como anónimos fuera del RGPD.
- Definir retención larga por conveniencia técnica.
- Integrar TPV/CCTV con verificación de edad sin nuevo análisis.
- Usar consentimiento biométrico sin alternativa manual/documental equivalente.

## 4. Entregables recomendados de revisión externa

- Memo sectorial tabaco/vending.
- Informe RGPD/DPIA v0.1.
- Dictamen breve sobre biometría y art. 9 RGPD.
- Matriz responsable/encargado/subencargados.
- Política de retención y logs.
- Texto de información al usuario y señalización.
- Recomendación documentada sobre consulta previa AEPD.
