# Kiosk Biometric Verification

[![Tests](https://github.com/Ana-lopez-web/kiosk-biometric-verification/actions/workflows/tests.yml/badge.svg)](https://github.com/Ana-lopez-web/kiosk-biometric-verification/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://github.com/Ana-lopez-web/kiosk-biometric-verification)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success)](#roadmap)

> 🇬🇧 Also available in [English](README.md).

Diseño e implementación, en formato prueba de concepto, de un módulo de verificación biométrica de identidad concebido para integrarse en un **modelo de máquina expendedora de productos del tabaco homologable** al amparo del marco regulatorio español — la [Circular 1/2025](https://www.boe.es/diario_boe/) del *Comisionado para el Mercado de Tabacos* (entrada en vigor: 2 de enero de 2026) — para su despliegue en los locales autorizados por el artículo 25.Dos del [Real Decreto 1199/1999](https://www.boe.es/buscar/act.php?id=BOE-A-1999-15028) (hostelería, hoteles, tiendas de conveniencia en estaciones de servicio, salas de juego y quioscos de prensa).

El proyecto abarca el diseño nuclear de una solución de venta automatizada regulada y restringida por razón de edad: un flujo de verificación en Python con interfaces mockeables para las comprobaciones criptográficas y biométricas, una suite de tests con pytest, y materiales documentales sobre marco regulatorio, RGPD y planificación de proyecto.

> **Estado**: proyecto personal de principio a fin, en fase activa de consulta regulatoria. Los componentes software son funcionales; la integración con hardware (lectores NFC físicos, cámaras con sensor de profundidad) queda fuera del alcance actual. Véase [Roadmap](#roadmap).

---

## Por qué este proyecto

El mercado del tabaco en España está fuertemente regulado. La venta manual está reservada a los expendedores autorizados (*estancos*), pero la venta automatizada a través de máquinas expendedoras se permite — con condiciones estrictas — en la relación cerrada de locales del artículo 25.Dos del RD 1199/1999. Dichas máquinas requieren autorización modelo a modelo, conforme al procedimiento que la *Circular 1/2025* (15 de diciembre de 2025) consolida y moderniza.

Este proyecto explora cómo podría ser un modelo de máquina expendedora tecnológicamente avanzado y conforme: verificación segura de edad mediante lectura del chip NFC del DNIe y comparación biométrica facial 1:1, plena conformidad con el RGPD, registros de auditoría anonimizados y trazables, y un encaje regulatorio claro y alineado con el procedimiento vigente de autorización de modelo.

El objetivo no fue solo escribir código, sino recorrer el camino completo desde el concepto hasta una entrega que pudiera presentarse de forma realista ante el regulador — reflejando cómo trabajo en posiciones técnicas: responsabilidad, atención al detalle y documentación rigurosa.

---

## Escenarios de despliegue

### Escenario principal — Locales autorizados (artículo 25.Dos del RD 1199/1999)

Modelo homologado instalado en los establecimientos donde la normativa española permite actualmente las máquinas expendedoras de tabaco: hostelería (bares, restaurantes), hoteles y similares, tiendas de conveniencia en estaciones de servicio, salas de juego y quioscos de prensa. El sistema de verificación biométrica se plantea como **refuerzo técnico** de la obligación legal del titular del establecimiento de controlar y supervisar la máquina, reduciendo el riesgo de ventas inadvertidas a menores.

### Escenario secundario — Herramienta de cumplimiento en el interior del estanco

Como variante, el mismo módulo software podría desplegarse como **herramienta de apoyo al cumplimiento normativo** en el interior de los estancos, ayudando (sin sustituir) al expendedor a verificar la mayoría de edad del comprador. Se plantea como instrumento interno, no como máquina expendedora, y su admisibilidad forma parte de la consulta regulatoria abierta (véase [`docs/regulatory/`](docs/regulatory)).

---

## Contenido del repositorio

### `src/biometric_verification.py`

Módulo Python con el flujo de verificación, diseñado para ser totalmente testeable:

- **Interfaz de lectura NFC mockeable**, conforme a los conceptos de la norma ICAO 9303 MRTD.
- **Interfaz de validación criptográfica mockeable**, prevista para validar contra el ancla de confianza FNMT-RCM en la implementación de producción.
- **Interfaz de detección de vida mockeable**, alineada con la norma ISO/IEC 30107-3.
- **Comparación facial 1:1** mediante distancia coseno contra la fotografía extraída del chip.
- **Cálculo de edad** con tratamiento correcto de años bisiestos.
- **Registro de auditoría anonimizado** con HMAC y rotación diaria de sal (sin almacenamiento de PII).
- **Borrado seguro de memoria** con sobrescritura de `bytearray` y `numpy.fill(0)` en todos los caminos del flujo, incluidos los de excepción.

### `tests/test_biometric_verification.py`

Suite de tests unitarios con `pytest`, `pytest-cov`, `freezegun` y `unittest.mock`. **51 tests, 94 % de cobertura de líneas**, organizados en siete clases:

- `TestSecureWipe` — borrado de buffers, incluidos arrays RGB completos.
- `TestCalculateAge` — fechas de nacimiento extremas, años bisiestos, congelación determinista de la fecha.
- `TestFaceMatcher` — propiedades de la distancia coseno, vectores cero, límites del umbral.
- `TestAuditLogger` — determinismo diario, rotación de sal, verificación de ausencia de PII.
- `TestBiometricSessionFlow` — los siete desenlaces posibles de la sesión, con aserciones negativas.
- `TestPrivacyGuarantees` — el borrado se ejecuta en todos los caminos; los recursos se liberan en caso de fallo.
- Tablas parametrizadas de regresión para invariantes de desenlace y casos límite de edad.

Para ejecutar los tests:

```bash
pip install -r requirements.txt
pytest --cov=src
```

> Fuera de alcance (declarado explícitamente): tests de integración con hardware, calibración del SDK biométrico conforme a la ISO/IEC 19795, evaluación completa de PAD conforme a la ISO/IEC 30107-3 (requiere kit físico de ataques y laboratorio acreditado).

### `demo_session.py`

Demo simulada que ejecuta sesiones aprobadas y rechazadas sin hardware físico.

```bash
python demo_session.py
```

### `mockups/kiosk-flow.html`

Mockup conceptual de pantalla táctil en un único archivo HTML que cubre el flujo del cliente: bienvenida, catálogo, verificación biométrica, pago y confirmación. Sin frameworks, sin paso de build — basta con abrirlo en cualquier navegador.

### `docs/architecture.md`

Nota de arquitectura técnica con el flujo de verificación, los componentes implementados, los elementos fuera de alcance y un checklist de endurecimiento para producción.

### `docs/regulatory/`

Materiales de encaje regulatorio:

- Mapeo del diseño técnico contra el artículo 4 de la Ley 28/2005, el artículo 25.Dos del RD 1199/1999 y la Circular 1/2025 del *Comisionado para el Mercado de Tabacos*.
- Versión anonimizada del escrito formal de consulta presentado al *Comisionado*.

### `.github/workflows/tests.yml`

Workflow de GitHub Actions que ejecuta automáticamente la suite de tests en Python 3.11 y 3.12.

### `business/`

Paquete de validación de negocio que posiciona el proyecto como sistema seguro de verificación de edad para venta automatizada en sectores regulados. Incluye one-pager, esquema de pitch deck, dossier regulatorio, mapa de contactos, plan de vídeo demo y presupuesto del MVP.

---

## Marco regulatorio

El proyecto se ancla en las siguientes normas españolas y de la Unión Europea:

- **Ley 13/1998**, de 4 de mayo, de Ordenación del Mercado de Tabacos.
- **Ley 28/2005**, de 26 de diciembre, de medidas sanitarias frente al tabaquismo (art. 4 — máquinas expendedoras; art. 9 — prohibición de publicidad; art. 19 — régimen sancionador).
- **Real Decreto 1199/1999**, de 9 de julio, que desarrolla la Ley 13/1998 (art. 25.Dos — relación de locales en los que se permiten máquinas expendedoras de tabaco, en la redacción dada por el RD 1676/2011).
- **Circular 1/2025**, de 15 de diciembre, del *Comisionado para el Mercado de Tabacos*, sobre el procedimiento de autorización, modificación o alteración de modelos de máquinas expendedoras y funcionamiento del Registro de Máquinas Expendedoras (BOE de 17 de diciembre de 2025; en vigor desde el 2 de enero de 2026).
- **Real Decreto-ley 17/2017**, de 17 de noviembre, por el que se transpone la Directiva 2014/40/UE relativa a los productos del tabaco.
- **Reglamento (UE) 2016/679** (RGPD) y **Ley Orgánica 3/2018** de protección de datos — en particular el artículo 9 (categorías especiales de datos personales, incluidos los datos biométricos) y el artículo 36 (consulta previa al organismo supervisor).
- **Reglamento Delegado (UE) 2018/574** relativo a la trazabilidad de los productos del tabaco.

---

## Roadmap

| Hito | Estado |
|---|---|
| Módulo POC + 94 % de cobertura | ✅ Hecho |
| Mockups del flujo de cliente | ✅ Hecho |
| Documentación de arquitectura y encaje regulatorio | ✅ Hecho |
| Consulta formal al *Comisionado para el Mercado de Tabacos* | 🟡 En preparación |
| Borrador de Evaluación de Impacto en Protección de Datos (EIPD) | ⏳ Pendiente |
| Consulta previa a la AEPD (art. 36 RGPD), si procede | ⏳ Pendiente |
| MVP de hardware (lector NFC + cámara con profundidad + dispensación) | ⏳ Pendiente |
| Procedimiento de autorización del modelo (Circular 1/2025) | ⏳ Pendiente |
| Piloto en local autorizado | ⏳ Pendiente |

---

## Stack tecnológico

- **Lenguaje**: Python 3.11+
- **Tests**: pytest, pytest-cov, freezegun, unittest.mock
- **Concepto de lectura NFC**: interfaz estilo PC/SC (dependencia `pyscard` mantenida para la integración prevista)
- **Concepto criptográfico**: biblioteca estándar + paquete `cryptography` para la validación X.509 prevista contra FNMT-RCM
- **Procesado de imagen**: numpy, Pillow
- **Prototipo de UI**: HTML5 + CSS en archivo único
- **CI**: GitHub Actions sobre Python 3.11 y 3.12

---

## Decisiones de diseño que merecen subrayarse

- **Privacidad por diseño, no por añadido.** Los datos biométricos se borran en todos los caminos, incluidos los de excepción. Los registros de auditoría usan HMAC con sal de rotación diaria y no almacenan PII. El flujo de consentimiento es multicapa y revocable.
- **Validación criptográfica contra fuente autoritativa.** El diseño de producción contempla la validación contra los certificados raíz de FNMT-RCM, no una autocomprobación cerrada.
- **Basado en estándares, no improvisado.** La detección de vida se enmarca en la ISO/IEC 30107-3 y la lectura NFC en la ICAO 9303. Allí donde el ensayo con hardware queda fuera de alcance, se documenta explícitamente en vez de obviarlo.
- **El encaje regulatorio como entregable de primer orden.** El escrito de consulta cubre el régimen de licencias, los estándares de verificación de edad, las precintas fiscales, la trazabilidad, los protocolos post-incidente y las interacciones con el RGPD, y está estructurado para alinearse con el procedimiento de la Circular 1/2025.

---

## Qué demuestra este proyecto

- Autonomía técnica de principio a fin en un alcance no trivial.
- Capacidad para trabajar a lo largo de toda la cadena de entrega: análisis de requisitos, prototipado, implementación, pruebas, encaje regulatorio, documentación de cumplimiento y validación de negocio temprana.
- Rigor en las decisiones de privacidad y seguridad, aplicado a lo largo del código y no como añadido posterior.
- Hábitos claros de documentación — del tipo que se traducen directamente en soporte operativo, gestión de incidentes y trabajo procedimental.
- Capacidad para traducir un prototipo técnico en un paquete de validación de negocio para mercados regulados.

---

## Seguridad

Véase [SECURITY.md](SECURITY.md) para la política de divulgación responsable y el canal de notificación.

---

## Licencia

Publicado bajo [Licencia MIT](LICENSE) con fines de portafolio y educativos. El código se proporciona "tal cual", sin garantía de ningún tipo. La documentación regulatoria y de RGPD es ilustrativa y **no debe** utilizarse para un despliegue real sin asesoramiento jurídico cualificado.

---

## Autora

**Ana López Fernández** — Técnica de Soporte Informático, CFGS ASIR (especialidad Ciberseguridad).
[LinkedIn](https://www.linkedin.com/in/ana-lopez-fernandez-evanda/) · Madrid, España.
