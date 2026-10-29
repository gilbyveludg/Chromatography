Hola, Claude. Vengo de trabajar este material en otra sesión y quiero continuar aquí. Te adjunto un .zip con todo; ábrelo y léelo antes de responder.

## Quién soy y para qué
Soy profesor de Nutrición Molecular (CUCEI–UdG / ITESO, otoño 2026). Mis alumnos son de **Ingeniería en Alimentos y Biotecnología**, no nutriólogos: los ejemplos deben ir hacia alimentos, procesos y laboratorio más que hacia la clínica. Escríbeme siempre en español.

## Temario que SÍ hemos visto («Del Genoma Crudo a la Clínica»)
1. Ómicas y dogma central; tipos de variantes (SNP sinónimo, missense, nonsense, indels, CNV); hiper e hiporrespondedores.
2. Nutrigenética: TAS2R38 (PAV/AVI, receptores T2R en el intestino), OR6A2 (cilantro), OR2M7 (espárragos), CYP1A2 (cafeína), APOE ε4 × alcohol, ALDH2 (acetaldehído), PKU (PAH) frente a lactasa (MCM6/LCT, −13910T y −22018A, metilación del promotor), MTHFR, FTO rs9939609; hipolactasia frente a malabsorción e intolerancia.
3. Purificación de DNA (fenol-cloroformo, salting-out, columnas de sílice bind-wash-elute, SPRI) y PCR de **punto final** (no vimos PCR digital ni qPCR); Alu PV92 en CDH13 (alelo + ≈ 731 pb, alelo − ≈ 416 pb); UCSC In-Silico PCR, BLAST, Primer-BLAST, GWAS Catalog.
4. Antioxidantes: DPPH (517 nm), TAC/FRAP (593 nm), catalasa (240 nm), SOD (560 nm); % de inhibición con resta del blanco e IC₅₀; troubleshooting (pigmentos, DPPH degradado por la luz, catalasa fuera de rango).

**No** vimos diseños de estudio avanzados (aleatorización mendeliana, ensayos cruzados), PCR digital ni conceptos como splicing a detalle. Evita esos términos.

## Lo que ya está hecho (en el .zip)
- **Preexamen** (3 h, práctica): `Preexamen_..._con_clave.docx` y su presentación de revisión.
- **Examen real** (lo que estamos afinando): `Examen_..._con_clave.docx` / `.pdf`. Estructura: 4 bloques con pesos 30/30/20/20, 2 horas en línea en Canvas, 29 reactivos, 100 puntos, aviso de **prohibido usar IA** y declaración de integridad (0 pts). Al final del Word está la clave con la justificación de cada reactivo y por qué fallan las otras opciones.
- `banco_examen.py`: el banco del examen en Python (fuente de verdad). `generar_qti.py` lo convierte al .zip QTI para importar en Canvas; `figuras_examen.py` genera las 5 gráficas de datos simulados del bloque 1.

## Criterios que ya acordamos
- Preguntas de **pensamiento crítico**: interpretar datos, detectar errores, decidir con evidencia; nada que se responda de memoria.
- Preferir **gráficas o geles simulados** y casos con datos sobre preguntas teóricas largas.
- Lenguaje sencillo; dar contexto cuando se use un término técnico (p. ej., explicar qué es el PROP).
- Casos y números distintos a los vistos en clase; las respuestas correctas repartidas entre A, B, C y D.
- Requisitos del examen: al menos 2 ejercicios con secuencias, 1 cálculo de IC₅₀ con tabla de absorbancias (restando el blanco) y 1 lectura de gel de PV92.

## Pendiente
- Revisar si E1-2 (habla de splicing) y E1-7 (GWAS e IMC) son demasiado avanzadas; quizá cambiarlas por gráficas.
- Revisar los bloques 2 a 4 con el mismo criterio.
- Después: presentación con las respuestas explicadas del examen, para revisarlo con el grupo.

Para empezar: lee el examen y dime en una lista breve qué reactivos te parece que aún usan conceptos que no vimos o que son poco claros para ingenieros en alimentos. No cambies nada todavía.
