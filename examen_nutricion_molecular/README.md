# Examen · Del Genoma Crudo a la Clínica (Nutrición Molecular)

Examen calificado en Canvas, **2 horas en línea**, con la misma estructura y pesos que el preexamen y reactivos nuevos de pensamiento crítico. Incluye aviso de **prohibición de uso de IA** y una declaración de integridad (0 pts) que el alumno acepta al iniciar.

## Archivos

| Archivo | Para qué |
|---|---|
| `examen_nutricion_molecular_qti.zip` | Paquete QTI 1.2 para importar en Canvas. |
| `Examen_Genoma_Crudo_a_la_Clinica_con_clave.docx` / `.pdf` | El examen completo y, al final, la clave con la justificación de cada reactivo y las rúbricas. Solo para el docente. |
| `Examen_Genoma_Crudo_a_la_Clinica_sin_respuestas.pdf` | Solo el examen, sin clave (para revisar o imprimir). |
| `clave_docente.md` | Clave en texto. |
| `banco_examen.py` | Banco de reactivos; se edita aquí. |

## Estructura (100 puntos, 120 min)

| Bloque | Reactivos | Puntos | Min sugeridos |
|---|---|---|---|
| 1. Fundamentos moleculares y ómicos (opción múltiple) | 10 | 30 | 20 |
| 2. Casos clínicos (4 OM, 1 selección múltiple, 2 respuesta extendida) | 7 | 30 | 40 |
| 3. Bioinformática, secuencias y gel de PV92 | 6 | 20 | 25 |
| 4. Cálculo (DPPH, IC₅₀, catalasa) y troubleshooting | 6 | 20 | 25 |

Las 2 preguntas de respuesta extendida se califican a mano con la rúbrica incluida.

## Configuración de Canvas incluida

Cuestionario calificado, 120 min, **un intento**, opciones barajadas, sin mostrar respuestas ni retroalimentación al enviar. Tras importarlo conviene revisar en Canvas: grupo de tareas, fechas de disponibilidad y, si el curso lo tiene, LockDown Browser.

## Regenerar

Los generadores están en `../preexamen_nutricion_molecular/`:

```bash
python3 ../preexamen_nutricion_molecular/generar_qti.py banco_examen.py
BANCO=banco_examen.py python3 ../preexamen_nutricion_molecular/exportar_json.py examen.json
node ../preexamen_nutricion_molecular/generar_word.js examen.json Examen_Genoma_Crudo_a_la_Clinica_con_clave.docx
```
