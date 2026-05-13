# Plan de lanzamiento en España — Kiosk Biometric Verification

Hoja de ruta práctica para llevar el proyecto desde prueba de concepto de portfolio hacia una validación real en España.

**Nota:** documento operativo, no asesoramiento jurídico. Pendiente de validación por abogado/DPO antes de contactar reguladores o tratar datos reales.

## Posicionamiento estratégico

En esta fase **no conviene presentar el proyecto como “kiosco biométrico autónomo para tabaco”**. Es más prudente, defendible y financiable posicionarlo como:

> Capa segura de verificación de mayoría de edad para retail regulado, privacy-by-design, basada principalmente en verificación documental/eID — especialmente DNIe/NFC cuando sea viable — con auditabilidad respetuosa con la privacidad y comparación biométrica 1:1 transitoria solo si supera revisión legal y DPIA.

Este enfoque reduce fricción regulatoria, evita sobredimensionar la biometría y deja margen para pivotar si la AEPD, el Comisionado o un DPO consideran que la biometría no es proporcional.

---

## 1. Vías de financiación

### Encaje prioritario

#### ENISA Emprendedoras Digitales

- Préstamo participativo para pymes digitales lideradas por mujeres.
- Rango orientativo: 25.000 € – 1.500.000 €.
- Requiere sociedad en España, plan de negocio viable, innovación, cofinanciación/fondos propios alineados con el importe solicitado y capacidad razonable de devolución.
- Mejor momento: después de tener validación legal inicial, cartas de interés y plan financiero básico.

URL: https://www.enisa.es/es/financia-tu-empresa/lineas-de-financiacion/d/emprendedoras-digitales

#### INCIBE Emprende

- Encaje fuerte si el proyecto se presenta como ciberseguridad, identidad digital, prevención de fraude y cumplimiento normativo en retail regulado.
- Puede ser una vía previa a ENISA porque aporta incubación/aceleración, mentores, visibilidad y ecosistema.
- Programas o entidades colaboradoras relevantes pueden incluir Wayra, Tetuan Valley, IMMUNE, MadFinTech u otras iniciativas vinculadas a INCIBE.

URLs:
- https://www.incibe.es/emprendimiento
- https://www.wayra.es/programa-ciberseguridad-02

#### CDTI NEOTEC 2026

- Encaje potencial si el proyecto demuestra tecnología propia, no solo integración de biometría de terceros.
- Ángulo más sólido: verificación privacy-preserving, evaluación de liveness/PAD, flujo DNIe/NFC, auditoría minimizada, procesamiento seguro en edge y arquitectura verificable.
- Mejor para una fase posterior, cuando la novedad técnica y la estructura societaria estén más maduras.

URLs:
- https://www.cdti.es/ayudas/ayudas-neotec-2026
- https://www.ciencia.gob.es/Convocatorias/2026/NEOTEC2026.html

#### Comunidad de Madrid — Innova / startups tecnológicas

- Posible encaje para empresas innovadoras de base tecnológica o pymes con alta intensidad innovadora.
- Conviene monitorizarlo junto con iniciativas de Madrid Innovation.

URL: https://www.comunidad.madrid/inversion-empresa/innova

### Vías complementarias

#### Premio Emprendedoras Madrid

- Útil para visibilidad, validación, contactos y posible impulso institucional para un proyecto liderado por mujer.

URL: https://www.madridinnovation.es/iniciativas/premio-emprendedoras-madrid-2026/

#### EIC Accelerator / Unión Europea

- No es la primera vía. Puede ser interesante más adelante si existe piloto, tracción, componente deep tech defendible y escalabilidad europea.

URL: https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en

#### ICO Empresas y Emprendedores

- Más útil para financiar hardware, pilotos o despliegue cuando ya haya contratos, ingresos o compromisos de clientes.

URL: https://www.ico.es/ico-empresas-y-emprendedores

#### Business angels / inversión semilla privada

- Útil después de validar viabilidad legal e interés del sector.
- Canales: AEBAN, WA4STEAM, South Summit, Wayra, SeedRocket, IESE BAN y redes deep tech/ciberseguridad.

URL: https://aeban.es/

---

## 2. Validación legal y regulatoria

### Punto principal: Comisionado para el Mercado de Tabacos

Cuestiones a resolver:

- Si el dispositivo se considera máquina expendedora de tabaco, sistema auxiliar dentro de un estanco autorizado u otra categoría.
- Si, en caso de dispensar producto automáticamente, necesita autorización previa de modelo.
- Qué controles técnicos se exigen para impedir el acceso de menores.
- Si es necesaria vigilancia humana directa, permanente o semipermanente.
- Si una capa de verificación de edad puede utilizarse como sistema adicional de cumplimiento dentro de un establecimiento autorizado.

Fuentes relevantes:
- Circular 1/2025 / BOE: https://www.boe.es/buscar/act.php?id=BOE-A-2025-25914
- Sede del Comisionado: https://sede.cmt.gob.es/default.aspx
- Ley 28/2005: https://boe.es/buscar/act.php?id=BOE-A-2005-21261

### RGPD / AEPD / biometría

El tratamiento biométrico es de alto riesgo y puede considerarse categoría especial según finalidad e implementación. El proyecto debe superar análisis de idoneidad, necesidad, proporcionalidad y minimización.

Diseño recomendado para reducir riesgo:

- Priorizar DNIe/NFC/verificación documental como núcleo de prueba de edad.
- Usar comparación facial 1:1 solo de forma transitoria contra la foto del documento/chip, si queda jurídicamente justificado.
- No usar reconocimiento facial 1:N.
- No usar estimación facial de edad como prueba única.
- No almacenar imágenes, plantillas biométricas ni embeddings.
- Mantener solo logs mínimos de auditoría mediante HMAC u otros mecanismos equivalentes, sin identificadores directos. Tratar esos logs como seudónimos por defecto, no anónimos, hasta evaluación específica de anonimización y reidentificación.
- Implementar comportamiento fail-closed: si la verificación no es concluyente, no hay venta.
- Realizar una DPIA/EIPD antes de cualquier piloto con datos reales y cerrar base jurídica, excepción art. 9 si hay biometría, roles y retención.
- Si la DPIA deja alto riesgo residual no mitigado, preparar consulta previa a la AEPD conforme al art. 36 RGPD; no usarla como sustituto de una DPIA madura.

Referencia AEPD:
- https://www.aepd.es/prensa-y-comunicacion/notas-de-prensa/la-aepd-publica-una-guia-sobre-la-utilizacion-de-datos

### AI Act / sistemas biométricos

Antes de cualquier despliegue comercial debe revisarse si el sistema entra en categorías de alto riesgo relacionadas con IA, biometría, identificación o categorización. En su caso, preparar documentación sobre:

- Limitación de finalidad.
- Precisión y sesgos.
- Validación de liveness/PAD.
- Supervisión humana.
- Trazabilidad.
- Gestión de incidencias.

---

## 3. Contactos y partners recomendados

### Sector / validación

- Comisionado para el Mercado de Tabacos.
- Unión de Estanqueros: https://union-estanqueros.com/
- Asociaciones locales de estanqueros en Madrid.
- 3–5 estancos con mentalidad tecnológica para entrevistas de descubrimiento.

### Legal / privacidad

- DPO o despacho especializado en RGPD, biometría e IA.
- Posibles firmas para un primer memo legal: ECIJA, Cuatrecasas, Garrigues, Across Legal u otras equivalentes.
- AEPD solo después de preparar una DPIA seria, no con una idea inmadura.

### Partners tecnológicos

- Proveedores españoles de biometría/eID: Veridas, FacePhi, Mobbeel.
- Fabricantes e integradores de kioscos/vending: Azkoyen, Jofemar, GM Vending u operadores similares.
- Especialistas en NFC/DNIe y PC/SC.
- Expertos en ISO/IEC 30107-3, PAD y liveness.

### Financiación / ecosistema

- INCIBE Emprende.
- Wayra.
- Tetuan Valley.
- Madrid Innovation.
- South Summit.
- AEBAN.
- WA4STEAM.

---

## 4. Hoja de ruta 30/60/90 días

### Días 0–30: base de validación

Objetivo: confirmar si el proyecto es jurídicamente plausible y si el sector tiene interés real.

Acciones:

1. Convertir el material del repositorio en un dossier de validación claro.
2. Preparar un memo legal/producto de 3 páginas: qué verifica el sistema, qué no almacena, quién es responsable y qué ocurre ante fallos.
3. Preparar preguntas formales para el Comisionado.
4. Crear matriz RGPD: tipos de datos, finalidad, base jurídica preliminar, posible art. 9 RGPD, retención, roles responsable/encargado/corresponsables, transferencias, subencargados y disparadores de DPIA.
5. Entrevistar a 5 estancos o contactos del sector.
6. Monitorizar/contactar programas como INCIBE Emprende y Madrid Innovation.
7. Definir si el primer MVP será:
   - herramienta de verificación asistida dentro de un estanco, o
   - terminal de venta automatizada tipo vending.

Decisión recomendada: empezar con **verificación asistida o semiasistida**, no con vending totalmente autónomo.

### Días 31–60: MVP y prueba de interés

Objetivo: hacer el proyecto concreto sin crear exposición legal innecesaria.

Acciones:

1. Construir una demo MVP con flujo documental/NFC o lector simulado.
2. Añadir pantallas explícitas de fail-closed y ruta de revisión manual.
3. Redactar DPIA/EIPD v0.1 con DPO o abogado, incluyendo análisis de alternativas menos intrusivas y criterio sobre logs HMAC seudónimos/anónimos.
4. Contactar al menos con un integrador/fabricante de kioscos o vending.
5. Intentar obtener 2–3 cartas de interés de estancos o contactos sectoriales.
6. Preparar materiales para ENISA:
   - plan de empresa,
   - previsión financiera a 3 años,
   - uso de fondos,
   - plan de cofinanciación,
   - roadmap,
   - mitigación de riesgos legales.
7. Definir hipótesis de pricing:
   - fee de instalación/integración,
   - cuota mensual SaaS de cumplimiento,
   - soporte y mantenimiento.

### Días 61–90: preparación para piloto

Objetivo: decidir si se avanza, se pivota o se pausa.

Acciones:

1. Ejecutar una demo privada o piloto no comercial en entorno controlado.
2. Buscar criterio preliminar por escrito del Comisionado o de asesoría especializada.
3. Revisar DPIA/análisis legal y decidir:
   - continuar con biometría 1:1 transitoria solo si necesidad, proporcionalidad y base jurídica están justificadas,
   - pivotar a DNIe/eID + validación manual,
   - o separar la biometría como módulo opcional.
4. Solicitar la vía de financiación más adecuada según ventana activa: INCIBE, ENISA, Comunidad de Madrid, aceleradora o inversión privada.
5. Preparar paquete para financiación/inversores:
   - deck,
   - one-pager,
   - vídeo demo,
   - memo legal,
   - LOIs/cartas de interés,
   - presupuesto MVP,
   - mapa regulatorio.
6. Decidir si constituir sociedad ya o esperar a feedback regulatorio más claro.

---

## 5. Riesgos y bloqueantes principales

- La AEPD puede considerar la biometría desproporcionada si bastan controles documentales o manuales.
- El Comisionado puede clasificar el sistema como máquina expendedora y exigir autorización de modelo.
- La venta totalmente autónoma de tabaco puede estar limitada por requisitos de supervisión.
- La responsabilidad por venta a menores debe estar extremadamente controlada.
- Hardware, certificación, SDKs biométricos y revisión legal pueden ser caros para estancos pequeños.
- NEOTEC/CDTI exige tecnología propia real, no solo integración de componentes comerciales.
- Un piloto real es difícil sin cobertura legal previa.
- Los proveedores biométricos pueden imponer licencias, restricciones o costes por verificación.

---

## 6. Entregables inmediatos

1. `legal-product-memo-es.md` — memo de 3 páginas para abogados, reguladores y partners.
2. `questions-comisionado.md` — borrador de preguntas formales para viabilidad regulatoria, pendiente de revisión antes de enviar.
3. `rgpd-data-matrix.md` — primera matriz de datos orientada a DPIA/EIPD.
4. `funding-shortlist.md` — tabla priorizada de financiación con encaje, requisitos y siguiente acción.
5. `discovery-interview-script.md` — guion de entrevista para estancos y partners.

Recomendación: revisar estos cinco documentos junto con este plan antes de contactar a terceros. El objetivo es transmitir seriedad, prudencia regulatoria y claridad de ejecución desde la primera conversación.

## 7. Puertas de control legal/DPO antes de avanzar

No pasar a piloto con datos reales hasta completar, como mínimo:

- Informe preliminar abogado/DPO sobre encaje tabaco/vending y protección de datos.
- Definición documentada de responsable, encargado, subencargados y posibles corresponsables.
- DPIA/EIPD con análisis de necesidad, proporcionalidad, riesgos, mitigaciones y decisión sobre consulta previa AEPD.
- Decisión expresa sobre biometría: excluirla, hacerla opcional, o justificarla con base art. 6 + excepción art. 9 y alternativa real.
- Política de retención y borrado automático de logs, con clasificación prudente como seudónimos salvo evaluación de anonimización.
- Protocolo de información al usuario, ejercicio de derechos, incidencias, falsos rechazos y escalado humano.
