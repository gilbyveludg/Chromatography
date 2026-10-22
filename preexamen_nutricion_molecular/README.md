# Preexamen · Del Genoma Crudo a la Clínica (Nutrición Molecular)

Cuestionario de práctica para Canvas, pensado para 3 horas, con la estructura del examen:

1. **Bloque 1 · Fundamentos moleculares y ómicos** (30 %): ómicas, tipos de variantes, respuesta interindividual, TAS2R38, PKU vs. lactasa, MTHFR, FTO, ALDH2.
2. **Bloque 2 · Casos clínicos y diagnóstico nutrigenético** (30 %): TAS2R38, OR6A2, OR2M7, CYP1A2, ALDH2, APOE × alcohol, FTO, hipolactasia/malabsorción/intolerancia.
3. **Bloque 3 · Bioinformática, PCR in silico y geles** (20 %): lectura de secuencias, gel de Alu PV92, ciclo de PCR, columnas de sílice, UCSC/BLAST/Primer-BLAST, GWAS Catalog.
4. **Bloque 4 · Cálculo y troubleshooting** (20 %): DPPH con blanco, IC₅₀ con tabla de absorbancias, FRAP, catalasa, SOD y errores de laboratorio.

Los casos y valores son distintos a los ejemplos de clase.

## Archivos

| Archivo | Para qué |
|---|---|
| `preexamen_nutricion_molecular_qti.zip` | Paquete QTI 1.2 listo para importar en Canvas. |
| `Preexamen_Genoma_Crudo_a_la_Clinica_con_clave.docx` | Word: el examen completo y, al final, la clave con la justificación de cada reactivo y las rúbricas. |
| `clave_docente.md` | Respuestas, retroalimentación y rúbricas. No se entrega a los alumnos. |
| `banco_preguntas.py` | Banco de reactivos; se edita aquí. |
| `generar_qti.py` | Regenera el .zip y la clave: `python3 generar_qti.py`. |
| `exportar_json.py`, `generar_word.js` | Regeneran el Word: `python3 exportar_json.py banco.json && node generar_word.js banco.json Preexamen_Genoma_Crudo_a_la_Clinica_con_clave.docx`. |

## Importar en Canvas

Curso → **Configuración** → **Importar contenido del curso** → tipo **Paquete QTI .zip** → subir el .zip → **Importar**.
El cuestionario aparece en *Cuestionarios* sin publicar.

Configuración incluida: cuestionario de práctica, 180 min, intentos ilimitados (se conserva el mejor), respuestas barajadas y respuestas correctas visibles al enviar. Todo se puede cambiar en Canvas tras importarlo.

## Estructura (100 puntos)

| Bloque | Reactivos | Puntos | Min sugeridos |
|---|---|---|---|
| 1. Opción múltiple: fundamentos | 15 | 30 | 30 |
| 2. Casos clínicos (6 OM, 2 selección múltiple, 2 respuesta extendida) | 10 | 30 | 55 |
| 3. Bioinformática, secuencias y geles | 9 | 20 | 40 |
| 4. Cálculo y troubleshooting | 10 | 20 | 40 |

Las 2 preguntas de respuesta extendida se califican a mano con la rúbrica incluida.

| Sección | Reactivos | Puntos | Min sugeridos |
|---|---|---|---|
| I. Opción múltiple razonada | 25 | 40 | 50 |
| II. Selección múltiple | 6 | 12 | 18 |
| III. Relación de columnas | 3 | 9 | 12 |
| IV. Cadenas mecanísticas (menús desplegables) | 3 | 9 | 12 |
| V. Cálculos (numéricos con tolerancia) | 7 | 14 | 30 |
| VI. Respuesta extendida (calificación manual) | 4 | 16 | 48 |

Las letras de la clave siguen el orden del banco; como Canvas baraja las opciones, el alumno las verá en otro orden.
