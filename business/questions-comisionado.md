# Preguntas para el Comisionado para el Mercado de Tabacos

**Documento preparatorio — no enviar sin revisión legal previa. Pendiente de validación por abogado/DPO.**  
**Proyecto:** sistema de verificación segura de mayoría de edad para terminales de autoservicio en entornos regulados.  
**Caso de consulta:** posible uso dentro de expendedurías de tabaco autorizadas en España.

---

## 1. Objetivo de la consulta

Solicitar criterio preliminar sobre la viabilidad regulatoria de integrar una capa tecnológica de verificación de mayoría de edad en un terminal de autoservicio ubicado dentro de un estanco autorizado, manteniendo controles de supervisión, trazabilidad y bloqueo de venta ante verificación fallida.

El objetivo no es solicitar autorización de despliegue inmediato, sino entender:

- Cómo se clasificaría el dispositivo o sistema.
- Qué requisitos serían aplicables.
- Qué documentación debería prepararse antes de un piloto.
- Qué límites existen en materia de supervisión, venta automatizada y control de acceso por menores.

---

## 2. Descripción breve del sistema a consultar

Sistema modular de verificación de mayoría de edad para venta asistida, semi-automatizada o automatizada en sectores regulados.

Características previstas:

- Verificación documental mediante lectura de documento oficial/DNIe/NFC/chip o equivalente.
- Validación de mayoría de edad antes de permitir la operación.
- Posible comparación facial 1:1 transitoria contra el documento, solo si es legalmente viable.
- Sin reconocimiento facial 1:N.
- Sin almacenamiento de imágenes, plantillas biométricas ni datos identificativos en logs.
- Registro de auditoría minimizado, sin identificadores directos, para acreditar que se realizó la verificación; a efectos RGPD se trataría de forma prudente como seudonimizado salvo validación externa de anonimización.
- Bloqueo automático de la venta si la verificación no se completa correctamente.
- Posible operación asistida por personal del estanco en una primera fase.

---

## 3. Preguntas prioritarias

### A. Clasificación del sistema

1. ¿Un terminal de autoservicio ubicado dentro de una expendeduría autorizada y controlado por su titular se consideraría una **máquina expendedora de tabaco**, una extensión del punto de venta, un sistema auxiliar o una categoría distinta?

2. Si el terminal realiza dispensación automática del producto después de la verificación, ¿requeriría autorización previa, homologación, inscripción o comunicación específica ante el Comisionado?

3. ¿La clasificación cambia si el terminal no dispensa producto, sino que solo realiza verificación de edad y genera una autorización para que el personal complete la venta?

4. ¿Existen criterios publicados o precedentes sobre terminales de autoservicio dentro de estancos autorizados?

### B. Ubicación y supervisión

5. ¿El sistema podría instalarse exclusivamente dentro de una expendeduría autorizada bajo responsabilidad del titular?

6. ¿Sería obligatoria la presencia o supervisión directa de personal durante la operación del terminal?

7. En caso de operación semi-asistida, ¿qué nivel de intervención humana sería suficiente: supervisión visual, validación manual final, desbloqueo por empleado o atención solo ante incidencias?

8. ¿Existen restricciones sobre horario de funcionamiento del terminal si se encuentra dentro del local autorizado?

### C. Control de mayoría de edad

9. ¿Qué estándar de verificación de mayoría de edad se considera aceptable para una operación asistida, semi-automatizada o automatizada dentro de un estanco?

10. ¿Sería aceptable una verificación basada en documento oficial electrónico/NFC o DNIe, siempre que la venta se bloquee ante error o duda?

11. ¿El Comisionado exige o recomienda mecanismos concretos para impedir el acceso de menores a compra automatizada?

12. ¿Qué documentación debería conservar el titular para demostrar que se ha realizado el control de mayoría de edad sin almacenar datos personales innecesarios?

### D. Biometría y alternativas

13. Desde el punto de vista sectorial del tabaco, ¿existe alguna prohibición o requisito específico respecto al uso de comparación facial 1:1 como refuerzo del control de identidad/edad?

14. ¿Sería preferible, desde el criterio del Comisionado, un sistema basado solo en documento oficial y supervisión humana, dejando la biometría como módulo opcional sujeto a RGPD/AEPD?

15. Si la biometría se procesara únicamente de forma transitoria y sin almacenamiento, ¿afectaría a la autorización del sistema o solo al análisis de protección de datos?

### E. Auditoría e inspección

16. ¿Qué evidencia puede requerir una inspección para comprobar que el terminal no permite ventas a menores?

17. ¿Un registro de auditoría minimizado —fecha/hora, terminal, resultado de verificación y, solo si fuera imprescindible, token HMAC tratado inicialmente como seudónimo— podría ser suficiente para acreditar funcionamiento del control, o serían necesarios datos adicionales?

18. ¿Deben registrarse también los intentos fallidos de verificación?

19. ¿Durante cuánto tiempo debería conservarse la evidencia técnica de control de edad, si no existe una obligación específica, y qué nivel de agregación/minimización sería aceptable?

### F. Fallos, incidencias y responsabilidad

20. ¿Debe el terminal operar siempre en modo *fail-closed*, bloqueando la venta ante cualquier fallo de lectura, validación o comunicación?

21. ¿Qué protocolo se esperaría ante incidencias: registro interno, comunicación al Comisionado, retirada temporal del equipo, revisión técnica?

22. En caso de error del sistema, ¿la responsabilidad recaería íntegramente en el titular de la expendeduría, en el proveedor tecnológico, o dependería del modelo contractual?

### G. Piloto o prueba controlada

23. ¿Sería posible realizar una prueba piloto sin ventas reales, usando transacciones simuladas dentro de un entorno privado o estanco colaborador?

24. ¿Qué documentación debería presentarse para solicitar criterio o autorización sobre un piloto limitado?

25. ¿Debe consultarse primero al Comisionado, o sería recomendable obtener previamente informe de abogado especializado y evaluación RGPD/DPIA?

26. ¿Existe un canal formal específico para consultas técnicas sobre este tipo de solución?

---

## 4. Preguntas de seguimiento según respuesta

Si el Comisionado considera el sistema máquina expendedora:

- ¿Qué normativa técnica concreta debe cumplir?
- ¿Qué procedimiento de autorización/modelo aplica?
- ¿Qué requisitos de ubicación, supervisión y bloqueo de menores son obligatorios?

Si lo considera sistema auxiliar dentro de estanco:

- ¿Qué límites funcionales no debe superar para no ser considerado máquina expendedora?
- ¿Puede integrarse con TPV o gestión de stock?
- ¿Debe quedar la entrega física del producto en manos del personal?

Si no existe criterio definido:

- ¿Qué información adicional permitiría emitir una orientación preliminar?
- ¿Puede presentarse una memoria técnica y funcional para valoración?
- ¿Conviene involucrar a una asociación sectorial o a otros organismos?

---

## 5. Documentación sugerida para acompañar una consulta formal

No enviar todo en una primera toma de contacto salvo que lo soliciten. Preparar:

1. Nota conceptual de 1–2 páginas.
2. Diagrama del flujo de usuario.
3. Descripción de controles de edad y bloqueo.
4. Matriz preliminar de datos/RGPD.
5. Especificación de auditoría minimizada, indicando que los registros HMAC se tratarán inicialmente como seudónimos salvo evaluación de anonimización validada.
6. Protocolo de fallos e incidencias.
7. Declaración de que no se almacenan datos biométricos ni identificadores directos en logs; pendiente de validar si los logs son seudónimos o anónimos.
8. Pregunta expresa sobre clasificación regulatoria.

---

## 6. Tono recomendado para la comunicación

- Exploratorio y prudente.
- No afirmar que el sistema es legalmente desplegable.
- No enfatizar “biometría” ni “venta autónoma” como titulares principales.
- Presentar el producto como refuerzo de cumplimiento y prevención de venta a menores.
- Pedir orientación sobre requisitos antes de avanzar a piloto.

Frase recomendada:

> Estamos analizando si una solución de verificación segura de mayoría de edad, integrada dentro de una expendeduría autorizada y con bloqueo automático ante fallo, podría encajar regulatoriamente como sistema auxiliar o requeriría tratamiento como máquina expendedora/autorización específica.

## 7. Nota de alcance para no mezclar competencias

La consulta al Comisionado debería limitarse al encaje sectorial: clasificación del sistema, requisitos de venta, supervisión, evidencia de control de edad, autorización/modelo y piloto. Las cuestiones de RGPD, biometría, base jurídica, DPIA/EIPD, anonimización de logs y consulta previa AEPD deben prepararse con abogado/DPO y, si procede, con la AEPD. Conviene no pedir al Comisionado que valide protección de datos, aunque sí explicar que se está trabajando con enfoque privacy-by-design.
