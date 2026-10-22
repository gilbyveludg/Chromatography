# -*- coding: utf-8 -*-
"""Banco de reactivos del preexamen «Del Genoma Crudo a la Clínica» (Nutrición Molecular, Otoño 2026).

Cuatro bloques con el peso del examen:
  1. Opción múltiple: fundamentos moleculares y ómicos ............. 30 %
  2. Casos clínicos y diagnóstico nutrigenético ..................... 30 %
  3. Bioinformática, PCR in silico e interpretación de geles ......... 20 %
  4. Cálculo químico-enzimático, capacidad antioxidante y troubleshooting 20 %

Cada reactivo es un dict; `generar_qti.py` lo convierte a QTI 1.2 para Canvas y
`exportar_json.py` + `generar_word.js` producen el Word con la clave.
Los casos y valores son distintos a los ejemplos vistos en clase.
"""

TITULO = "Preexamen · Del Genoma Crudo a la Clínica (Nutrición Molecular)"

DESCRIPCION = """
<p><strong>Preexamen de práctica.</strong> Tiene la misma estructura y duración que el examen (<strong>3 horas</strong>), con casos y datos distintos.</p>
<ol>
<li>Bloque 1 · Opción múltiple: fundamentos moleculares y ómicos (30 %).</li>
<li>Bloque 2 · Casos clínicos y diagnóstico nutrigenético (30 %).</li>
<li>Bloque 3 · Bioinformática, PCR <em>in silico</em> e interpretación de geles (20 %).</li>
<li>Bloque 4 · Cálculo químico-enzimático, capacidad antioxidante y troubleshooting (20 %).</li>
</ol>
<p>Casi ninguna pregunta se responde de memoria: piden interpretar datos, detectar errores y justificar con el mecanismo.
Al enviar verás la retroalimentación de cada reactivo; léela aunque hayas acertado.</p>
"""

TIEMPOS = [
    ("Bloque 1 · Opción múltiple (15 reactivos, 30 pts)", 30),
    ("Bloque 2 · Casos clínicos (10 reactivos, 30 pts)", 55),
    ("Bloque 3 · Bioinformática y geles (9 reactivos, 20 pts)", 40),
    ("Bloque 4 · Cálculo y troubleshooting (10 reactivos, 20 pts)", 40),
    ("Revisión final", 15),
]


def _tabla(encabezados, filas):
    th = "".join(f"<th style='border:1px solid #999;padding:4px 8px'>{h}</th>" for h in encabezados)
    trs = "".join(
        "<tr>" + "".join(f"<td style='border:1px solid #999;padding:4px 8px'>{c}</td>" for c in fila) + "</tr>"
        for fila in filas
    )
    return f"<table style='border-collapse:collapse;margin:8px 0'><tr>{th}</tr>{trs}</table>"


def _seq(texto):
    return f"<code>{texto}</code>"


INSTRUCCIONES = (
    "<h3>Instrucciones</h3>"
    "<ul>"
    "<li>Tiempo límite: <strong>180 minutos</strong>. Puedes usar calculadora y una tabla del código genético; no necesitas otras fuentes.</li>"
    "<li>Reactivos de cálculo: escribe solo el número, con punto decimal y sin unidades.</li>"
    "<li>Selección múltiple: marca todas las correctas; Canvas da crédito parcial y descuenta las marcadas de más.</li>"
    "<li>Casos de respuesta extendida: se califica el razonamiento (mecanismo, uso de los datos, límites de la evidencia y propuesta), no la extensión.</li>"
    "<li>Puedes repetir el preexamen; Canvas conserva tu mejor intento.</li>"
    "</ul>"
    "<p><strong>Distribución sugerida del tiempo</strong></p>"
    + _tabla(["Bloque", "Minutos"], [(s, m) for s, m in TIEMPOS])
)

# ---------------------------------------------------------------------------
# Tipos: header, mc, ma, matching, dropdowns, numerical, essay
# mc:        choices (list[str]), correct (int)
# ma:        choices (list[str]), correct (list[int])
# matching:  pairs (list[(izq, der)]), distractors (list[str])
# dropdowns: text con [clave], blanks {clave: (opciones, índice_correcto)}
# numerical: answer, tol (margen absoluto)
# essay:     text; fb lleva la respuesta modelo y la rúbrica
# ---------------------------------------------------------------------------

REACTIVOS = []


def header(texto):
    REACTIVOS.append({"type": "header", "text": texto})


def mc(titulo, texto, opciones, correcta, fb, puntos=2.0):
    REACTIVOS.append({"type": "mc", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correcta, "fb": fb, "points": puntos})


def ma(titulo, texto, opciones, correctas, fb, puntos=3.0):
    REACTIVOS.append({"type": "ma", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correctas, "fb": fb, "points": puntos})


def matching(titulo, texto, pares, distractores, fb, puntos=3.0):
    REACTIVOS.append({"type": "matching", "title": titulo, "text": texto, "pairs": pares,
                      "distractors": distractores, "fb": fb, "points": puntos})


def dropdowns(titulo, texto, blancos, fb, puntos=2.0):
    REACTIVOS.append({"type": "dropdowns", "title": titulo, "text": texto, "blanks": blancos,
                      "fb": fb, "points": puntos})


def numerical(titulo, texto, respuesta, tolerancia, fb, puntos=2.0):
    REACTIVOS.append({"type": "numerical", "title": titulo, "text": texto, "answer": respuesta,
                      "tol": tolerancia, "fb": fb, "points": puntos})


def essay(titulo, texto, fb, puntos=6.0):
    REACTIVOS.append({"type": "essay", "title": titulo, "text": texto, "fb": fb, "points": puntos})


def _fb(correcta, porque, demas):
    """Retroalimentación: la correcta con su justificación y por qué fallan las demás."""
    items = "".join(f"<li>{d}</li>" for d in demas)
    return (f"<p><strong>Correcta: {correcta}</strong> {porque}</p>"
            f"<p><strong>Por qué no las demás:</strong></p><ul>{items}</ul>")


header(INSTRUCCIONES)

# ===========================================================================
# BLOQUE 1 · OPCIÓN MÚLTIPLE: FUNDAMENTOS MOLECULARES Y ÓMICOS (30 pts)
# ===========================================================================
header("<h3>Bloque 1 · Fundamentos moleculares y ómicos (30 %)</h3>"
       "<p>15 reactivos de opción múltiple, 2 puntos cada uno. Elige la opción <em>mejor justificada</em>.</p>")

mc("B1-1 · ¿Qué capa ómica responde la pregunta?",
   "<p>Un equipo quiere saber si un yogur fermentado cambia, a las 2 horas de consumirlo, las concentraciones plasmáticas de ácidos grasos de cadena corta, "
   "aminoácidos y ácidos biliares. ¿Qué enfoque responde de forma más directa esa pregunta?</p>",
   ["Genómica del voluntario (secuenciación de su DNA).",
    "Transcriptómica de leucocitos (RNA-seq).",
    "Metabolómica plasmática (LC-MS o RMN).",
    "Epigenómica de leucocitos (metilación de CpG)."],
   2,
   _fb("metabolómica.", "La pregunta es sobre moléculas pequeñas circulantes a muy corto plazo; la metabolómica las mide directamente y es la capa más cercana al fenotipo y a la dieta.",
       ["Genómica: el DNA del voluntario no cambia en 2 horas; describe el potencial, no la respuesta aguda.",
        "Transcriptómica: mide RNA mensajero, un paso intermedio; un cambio de transcritos no informa la concentración de metabolitos.",
        "Epigenómica: la metilación cambia en escalas más largas y tampoco cuantifica metabolitos."]))

mc("B1-2 · Dogma central y regulación",
   "<p>En adultos con genotipo de no persistencia de lactasa, el promotor de <em>LCT</em> en el epitelio intestinal se hipermetila con la edad y baja el mRNA de lactasa. "
   "¿Qué afirmación describe mejor ese fenómeno dentro del dogma central?</p>",
   ["Es una mutación adquirida del gen <em>LCT</em> que cambia la proteína.",
    "Es una regulación epigenética: la secuencia no cambia, pero la metilación del promotor reduce la transcripción (DNA → RNA); se detectaría con epigenómica y transcriptómica.",
    "Es un cambio postraduccional de la lactasa que la inactiva.",
    "Es un cambio en el código genético que hace que el ribosoma no lea el mRNA de lactasa."],
   1,
   _fb("regulación epigenética de la transcripción.", "La metilación de CpG en promotores reduce el acceso de la maquinaria transcripcional sin alterar la secuencia. El efecto aparece como menos mRNA y menos proteína.",
       ["«Mutación adquirida»: la secuencia de LCT no cambia; la metilación es una marca química sobre la citosina.",
        "«Cambio postraduccional»: actuaría sobre la proteína ya formada; aquí lo que baja es el mRNA.",
        "«Cambio en el código genético»: el código es universal; la lectura del mRNA no es el paso afectado."]))

mc("B1-3 · Un SNP sinónimo",
   "<p>Un SNP cambia el codón CTG por CTA; ambos codifican leucina. Un alumno afirma que, por ser sinónimo, «no puede tener ningún efecto biológico». ¿Cuál es la mejor respuesta?</p>",
   ["Tiene razón: si el aminoácido no cambia, la proteína es idéntica y no hay efecto posible.",
    "No necesariamente: un cambio sinónimo puede alterar sitios de splicing, la estabilidad del mRNA o la velocidad de traducción por uso de codones, aunque la mayoría son neutros.",
    "Es incorrecto porque todo SNP sinónimo es en realidad un nonsense.",
    "Un SNP sinónimo siempre cambia la proteína porque modifica el marco de lectura."],
   1,
   _fb("puede tener efecto, aunque casi siempre es neutro.", "«Sinónimo» describe solo el efecto sobre el aminoácido. El mRNA sí cambia, y eso puede afectar procesamiento o traducción.",
       ["«No hay efecto posible»: confunde la secuencia proteica con todo lo que hace el mRNA.",
        "«Es un nonsense»: nonsense significa crear un codón de paro; CTA codifica leucina.",
        "«Cambia el marco de lectura»: una sustitución de una base no corre el marco; eso lo hacen los indels que no son múltiplos de 3."]))

mc("B1-4 · Nonsense frente a missense",
   "<p>Dos pacientes tienen variantes en el codón 120 de una enzima de 450 aminoácidos: el paciente 1 tiene CAG→CAT (Gln→His) y el paciente 2 tiene CAG→TAG. "
   "¿Qué predicción es más razonable?</p>",
   ["Ambas variantes tienen el mismo efecto porque afectan el mismo codón.",
    "La del paciente 2 introduce un codón de paro prematuro; lo esperable es una proteína truncada o un mRNA degradado por NMD, con pérdida de función más grave que el cambio Gln→His.",
    "La del paciente 1 es más grave porque His tiene carga.",
    "La del paciente 2 es sinónima, porque TAG también codifica glutamina."],
   1,
   _fb("nonsense con pérdida de función.", "TAG es codón de paro. Un paro en el codón 120 de 450 elimina casi toda la proteína y suele activar el decaimiento del mRNA mediado por nonsense (NMD).",
       ["«Mismo efecto»: el codón es el mismo, pero el cambio resultante es distinto (missense vs. nonsense).",
        "«His es más grave»: un missense puede ser grave o neutro según el sitio; no hay base para suponerlo peor que perder la proteína.",
        "«TAG codifica glutamina»: TAG es uno de los tres codones de paro."]))

mc("B1-5 · Indels y marco de lectura",
   "<p>En un exón se encuentran dos deleciones distintas: una de 1 nucleótido y otra de 3 nucleótidos. ¿Qué consecuencia es más probable para cada una?</p>",
   ["Ambas corren el marco de lectura.",
    "La de 1 nt corre el marco (cambia todos los aminoácidos siguientes y suele crear un paro prematuro); la de 3 nt elimina un aminoácido sin correr el marco.",
    "La de 3 nt corre el marco y la de 1 nt no.",
    "Ninguna afecta la proteína porque los indels solo ocurren en intrones."],
   1,
   _fb("la de 1 nt es frameshift; la de 3 nt es in-frame.", "El ribosoma lee de 3 en 3; quitar un número de bases que no es múltiplo de 3 desplaza la lectura.",
       ["«Ambas corren el marco»: 3 nt es un codón completo.",
        "«Al revés»: invierte la regla del múltiplo de 3.",
        "«Solo en intrones»: los indels pueden ocurrir en cualquier región; en exones tienen el mayor efecto."]))

mc("B1-6 · Variación en número de copias (CNV)",
   "<p>Las poblaciones con dietas tradicionalmente altas en almidón tienden a tener más copias del gen de amilasa salival <em>AMY1</em>, y el número de copias se asocia con la cantidad de amilasa en saliva. ¿Qué tipo de variante es y qué ilustra?</p>",
   ["Un SNP missense que mejora la enzima.",
    "Una CNV: el número de copias del gen cambia la dosis de proteína, un ejemplo de variación genética asociada a la dieta.",
    "Un indel que corre el marco de lectura de AMY1.",
    "Una mutación somática adquirida por comer almidón."],
   1,
   _fb("CNV con efecto de dosis.", "Más copias del gen → más transcripción total → más enzima. Es un ejemplo clásico de variación estructural relacionada con la dieta.",
       ["«SNP missense»: un SNP cambia una base; aquí lo que varía es cuántas copias del gen hay.",
        "«Indel frameshift»: un frameshift anularía la proteína, no la aumentaría.",
        "«Mutación somática por comer almidón»: la dieta no crea copias génicas en el individuo; la diferencia es heredada y poblacional."]))

mc("B1-7 · Hiporrespondedores e hiperrespondedores",
   "<p>En un ensayo, 30 adultos agregan 300 mg/día de colesterol dietario durante 4 semanas. El LDL cambia en promedio +6 mg/dL, pero un tercio sube más de 20 mg/dL y otro tercio no cambia. ¿Qué concepto describe mejor estos resultados?</p>",
   ["Error de medición: todos deberían responder igual.",
    "Respuesta interindividual a la dieta: hay hiperrespondedores e hiporrespondedores, en parte por variación genética (p. ej., APOE) y en parte por otros factores.",
    "El promedio de +6 mg/dL describe bien a todos los participantes.",
    "Los hiporrespondedores no absorben colesterol."],
   1,
   _fb("variabilidad interindividual.", "El promedio oculta subgrupos con respuestas muy distintas; la nutrigenética busca qué variantes explican parte de esa heterogeneidad.",
       ["«Error de medición»: puede contribuir, pero una dispersión sistemática en subgrupos es justamente lo que define respondedores.",
        "«El promedio describe a todos»: es la falacia que este concepto corrige.",
        "«No absorben colesterol»: es una sobreinterpretación; la respuesta depende de absorción, síntesis endógena y depuración de LDL."]))

mc("B1-8 · Haplotipos de TAS2R38",
   "<p>¿Qué describe correctamente los haplotipos PAV y AVI de <em>TAS2R38</em>?</p>",
   ["Son dos genes distintos del cromosoma 7.",
    "Son combinaciones de tres SNPs missense (posiciones 49, 262 y 296 de la proteína); PAV forma un receptor funcional (catador de PTC/PROP, «supertaster» en el curso) y AVI uno poco funcional (no catador).",
    "PAV es una deleción y AVI una inserción Alu.",
    "AVI es el haplotipo catador porque tiene valina."],
   1,
   _fb("tres SNPs missense en un mismo haplotipo.", "Pro-Ala-Val en las posiciones 49, 262 y 296 (PAV) da un receptor sensible; Ala-Val-Ile (AVI) da un receptor con muy baja sensibilidad a tioureas como PTC y PROP.",
       ["«Dos genes»: es un mismo gen con alelos distintos.",
        "«Deleción/inserción»: son sustituciones de una base.",
        "«AVI catador»: es al revés; AVI es el haplotipo no catador."]))

mc("B1-9 · Receptores T2R fuera de la boca",
   "<p>Los receptores de sabor amargo T2R también se expresan en células enteroendocrinas del intestino. ¿Qué papel fisiológico es el más aceptado?</p>",
   ["Permiten «saborear» el alimento en el intestino de forma consciente.",
    "Detectan compuestos amargos en la luz intestinal y estimulan la liberación de hormonas como GLP-1 o CCK, que informan al cerebro (eje intestino-cerebro) sobre saciedad y motilidad.",
    "Degradan los compuestos amargos antes de su absorción.",
    "Solo existen en roedores; en humanos no hay T2R extraorales."],
   1,
   _fb("quimiosensores que liberan hormonas intestinales.", "La señal no es una percepción consciente: activa vías endocrinas y vagales hacia el sistema nervioso central.",
       ["«Saborear de forma consciente»: la percepción consciente del sabor ocurre en la lengua y la corteza gustativa.",
        "«Degradan los compuestos»: los receptores detectan, no metabolizan.",
        "«Solo roedores»: hay evidencia de T2R extraorales en humanos (intestino, vía aérea)."]))

mc("B1-10 · Monogénico frente a regulatorio común",
   "<p>¿Qué comparación entre fenilcetonuria (<em>PAH</em>) y persistencia de lactasa (<em>MCM6</em>/<em>LCT</em>) es correcta?</p>",
   ["Ambas son rasgos poligénicos de efecto pequeño.",
    "PKU es monogénica, recesiva, de gran efecto y con variantes casi siempre raras y codificantes; la persistencia de lactasa depende de variantes comunes en un potenciador regulatorio que cambia la expresión de LCT en el adulto.",
    "PKU se debe a una variante del potenciador de PAH y la persistencia de lactasa a una nonsense de LCT.",
    "En ambas la dieta no influye en el fenotipo."],
   1,
   _fb("gran efecto codificante frente a variante regulatoria común.", "En PKU la pérdida de función de la fenilalanina hidroxilasa es casi determinante; en lactasa, la variante cambia cuándo y cuánto se expresa una enzima normal.",
       ["«Ambas poligénicas»: PKU es el modelo de enfermedad monogénica.",
        "«Al revés»: invierte el tipo de variante de cada caso.",
        "«La dieta no influye»: en ambos casos la dieta es central (restricción de Phe en PKU; consumo de lactosa en hipolactasia)."]))

mc("B1-11 · ¿Dónde está la variante −13910?",
   "<p>La variante −13910C&gt;T (rs4988235), asociada a persistencia de lactasa en europeos, se localiza en el intrón 13 del gen <em>MCM6</em>, unos 14 kb río arriba de <em>LCT</em>. ¿Cómo actúa?</p>",
   ["Cambia un aminoácido de la proteína MCM6.",
    "Forma parte de un potenciador: el alelo T favorece la unión de factores de transcripción (como Oct-1) y mantiene la transcripción de <em>LCT</em> en el adulto, sin cambiar la secuencia de la lactasa.",
    "Cambia un aminoácido de la lactasa y la hace más activa.",
    "Elimina el gen MCM6, lo que libera a LCT."],
   1,
   _fb("potenciador regulatorio a distancia.", "Un intrón de un gen vecino puede contener elementos que regulan a otro gen; por eso el «gen asignado» en una base de datos no siempre es el gen efector.",
       ["«Cambia un aminoácido de MCM6»: los intrones no se traducen.",
        "«Cambia un aminoácido de la lactasa»: la variante no está en LCT y la enzima es la misma; cambia su cantidad.",
        "«Elimina MCM6»: es un SNP, no una deleción del gen."]))

mc("B1-12 · Hipolactasia, malabsorción e intolerancia",
   "<p>¿Cuál conjunto de definiciones es correcto?</p>",
   ["Son sinónimos.",
    "Hipolactasia: baja actividad de lactasa en el borde en cepillo. Malabsorción: la lactosa no se absorbe por completo (se demuestra, p. ej., con prueba de hidrógeno espirado). Intolerancia: aparición de síntomas tras ingerir lactosa.",
    "Intolerancia es la causa genética, malabsorción el síntoma e hipolactasia la prueba de laboratorio.",
    "Hipolactasia es una alergia a la proteína de la leche."],
   1,
   _fb("son tres niveles distintos: enzima, absorción y síntomas.", "Una persona puede tener hipolactasia y malabsorción sin síntomas (sin intolerancia), según la dosis de lactosa y su microbiota.",
       ["«Sinónimos»: confundirlos lleva a diagnósticos erróneos.",
        "«Intolerancia = causa genética»: la genética explica la hipolactasia; la intolerancia es clínica.",
        "«Alergia a la proteína»: la alergia a proteínas de leche es inmunológica y distinta de la hipolactasia."]))

mc("B1-13 · MTHFR C677T",
   "<p>¿Qué describe correctamente la variante <em>MTHFR</em> C677T?</p>",
   ["Es nonsense: produce una enzima truncada sin actividad.",
    "Es missense (Ala222Val): produce una enzima termolábil con menor actividad; con folato bajo, los homocigotos TT tienden a tener homocisteína más alta.",
    "Es sinónima y no tiene efecto.",
    "Aumenta la actividad de MTHFR y baja la homocisteína."],
   1,
   _fb("missense termolábil con interacción gen–folato.", "El efecto del genotipo depende del estado de folato (y de riboflavina, precursora del FAD que usa MTHFR).",
       ["«Nonsense»: no crea codón de paro.",
        "«Sinónima»: cambia alanina por valina.",
        "«Aumenta la actividad»: la reduce."]))

mc("B1-14 · FTO rs9939609",
   "<p>¿Qué afirmación sobre el alelo A de <em>FTO</em> rs9939609 está mejor sustentada?</p>",
   ["Cada copia del alelo A se asocia con más masa grasa y mayor riesgo de obesidad, con un efecto modesto (del orden de 1–1.5 kg por alelo) que se atenúa en personas físicamente activas.",
    "Los homocigotos AA desarrollan obesidad con certeza.",
    "Es una variante nonsense que elimina la proteína FTO.",
    "Explica la mayor parte de la variación del IMC en la población."],
   0,
   _fb("asociación real pero de efecto pequeño.", "Es la variante común de mayor efecto descrita para IMC, pero explica una fracción mínima de la varianza y su efecto se modifica con la actividad física.",
       ["«Obesidad con certeza»: es un factor de riesgo probabilístico.",
        "«Nonsense»: está en un intrón y actúa por mecanismos regulatorios.",
        "«La mayor parte de la variación»: el IMC es poligénico y muy influido por el ambiente."]))

mc("B1-15 · ALDH2 y acetaldehído",
   "<p>¿Por qué los portadores del alelo <em>ALDH2</em>*2 (rs671, Glu504Lys) presentan rubor facial tras beber alcohol?</p>",
   ["Porque metabolizan el etanol más lento y se acumula etanol.",
    "Porque la enzima ALDH2 mutante, que actúa como tetrámero, pierde actividad (efecto dominante negativo); el acetaldehído se acumula y causa vasodilatación.",
    "Porque tienen alergia al alcohol.",
    "Porque producen más ALDH2 y oxidan el acetaldehído demasiado rápido."],
   1,
   _fb("acumulación de acetaldehído por pérdida de función dominante negativa.", "Basta una copia de ALDH2*2 para reducir mucho la actividad, porque las subunidades mutantes contaminan el tetrámero.",
       ["«Se acumula etanol»: el paso afectado es acetaldehído → acetato, después de ADH.",
        "«Alergia»: no es un mecanismo inmunológico.",
        "«Más ALDH2»: es al revés; la actividad baja."]))

# ===========================================================================
# BLOQUE 2 · CASOS CLÍNICOS Y DIAGNÓSTICO NUTRIGENÉTICO (30 pts)
# ===========================================================================
header("<h3>Bloque 2 · Casos clínicos y diagnóstico nutrigenético (30 %)</h3>"
       "<p>6 casos de opción múltiple (2 pts c/u), 2 de selección múltiple (3 pts c/u) y 2 casos de respuesta extendida (6 pts c/u).</p>")

mc("B2-1 · Niño que rechaza el brócoli",
   "<p>Un niño de 8 años con genotipo <em>TAS2R38</em> PAV/PAV rechaza brócoli, col y coles de Bruselas. Su madre pide un «suplemento para que le guste». ¿Qué recomendación es la mejor fundamentada?</p>",
   ["No hay nada que hacer: su genotipo le impedirá comer crucíferas toda la vida.",
    "Explicar que percibe más intenso el amargor de los glucosinolatos; usar exposición repetida, cocciones que reducen el amargor y combinaciones con grasas o sabores dulces/salados, y asegurar otras fuentes de verduras.",
    "Indicar un suplemento de PROP para desensibilizar el receptor.",
    "Cambiar el diagnóstico a alergia alimentaria."],
   1,
   _fb("intervención conductual y culinaria informada por el genotipo.", "El genotipo explica una mayor sensibilidad, no una imposibilidad; la aceptación de alimentos se modifica con exposición y preparación.",
       ["«No hay nada que hacer»: el genotipo es un factor, no un destino.",
        "«Suplemento de PROP»: no existe evidencia de desensibilización así, y PROP es un compuesto de prueba.",
        "«Alergia»: rechazo por sabor no es una reacción inmunológica."]))

mc("B2-2 · «El cilantro sabe a jabón»",
   "<p>Una paciente dice que el cilantro le sabe a jabón y lo evita en todas las salsas. Su prueba genética muestra el alelo de riesgo en una variante cercana a <em>OR6A2</em>. ¿Qué interpretación es la mejor?</p>",
   ["Tiene una enfermedad del gusto que requiere tratamiento.",
    "OR6A2 codifica un receptor olfatorio que detecta aldehídos presentes en el cilantro; su variante se asocia a percibir ese olor como «jabonoso». Es una variación normal; basta sustituir el cilantro por otras hierbas sin consecuencias nutricionales relevantes.",
    "Debe forzarse a comer cilantro porque su genotipo es un error.",
    "El sabor a jabón se debe a que el cilantro contiene detergente."],
   1,
   _fb("variación normal de un receptor olfatorio.", "La percepción del sabor de las hierbas depende mucho del olfato; el cilantro contiene aldehídos con notas jabonosas que algunas personas perciben con más intensidad.",
       ["«Enfermedad»: es variación común, no patología.",
        "«Forzarlo»: no hay beneficio nutricional que lo justifique.",
        "«Contiene detergente»: son aldehídos naturales de la planta."]))

mc("B2-3 · Orina después de espárragos",
   "<p>Dos hermanos comen espárragos. Uno nota un olor sulfuroso en su orina y el otro asegura que no huele nada. ¿Qué explicación es más completa?</p>",
   ["El hermano que no huele nada no produce los compuestos azufrados.",
    "Hay variación en dos pasos: producir los compuestos azufrados y percibirlos. Una variante cercana a <em>OR2M7</em> se asocia a anosmia específica para ese olor; para saber cuál paso falla, habría que pedirle que huela la orina del hermano.",
    "Ambos deberían tener el mismo fenotipo porque son hermanos.",
    "Es un signo de insuficiencia renal."],
   1,
   _fb("distinguir producción de percepción.", "Es una buena lección de diseño: una sola observación («no huelo nada») tiene dos explicaciones posibles, y un experimento simple las separa.",
       ["«No produce»: posible, pero no es la única explicación; podría producirlos y no percibirlos.",
        "«Mismo fenotipo por ser hermanos»: comparten en promedio la mitad de las variantes.",
        "«Insuficiencia renal»: es un fenómeno común y benigno."]))

mc("B2-4 · Café y metabolismo lento",
   "<p>Hombre de 42 años, presión arterial limítrofe, toma 4 tazas de café al día. Su genotipo <em>CYP1A2</em> rs762551 es C/C («metabolizador lento»). ¿Qué recomendación es más coherente con la evidencia?</p>",
   ["Ninguna: el café es igual para todos.",
    "Considerar reducir a 1–2 tazas/día: en metabolizadores lentos la cafeína permanece más tiempo en circulación, y se ha descrito mayor riesgo cardiovascular con consumo alto en ese genotipo; vigilar presión arterial.",
    "Aumentar el café porque los metabolizadores lentos se benefician más de la cafeína.",
    "Suspender toda fuente de cafeína de inmediato porque su genotipo es patogénico."],
   1,
   _fb("moderar la dosis según el metabolismo.", "CYP1A2 hace la mayor parte del metabolismo de la cafeína; la variante condiciona cuánto tiempo está expuesto el organismo a la misma dosis.",
       ["«Igual para todos»: ignora la variabilidad farmacocinética documentada.",
        "«Aumentar el café»: el beneficio descrito con café se observa sobre todo en metabolizadores rápidos.",
        "«Suspender de inmediato, genotipo patogénico»: es una variante común, no una enfermedad; la recomendación es de moderación."]))

mc("B2-5 · Rubor y «tolerancia»",
   "<p>Una estudiante de ascendencia japonesa (<em>ALDH2</em>*1/*2) se pone roja al beber. Dice que «va a entrenar su tolerancia» bebiendo más seguido hasta que deje de ponerse roja. ¿Qué le explicas?</p>",
   ["Es buena idea: la tolerancia elimina el riesgo.",
    "El rubor es una señal de acumulación de acetaldehído, un carcinógeno; en portadores de ALDH2*2 beber con frecuencia se asocia con mayor riesgo de cáncer de esófago, aunque el rubor disminuya. Conviene reducir el consumo.",
    "Su genotipo la protege de cualquier daño por alcohol.",
    "Debe tomar antihistamínicos para quitarse el rubor y seguir bebiendo."],
   1,
   _fb("el rubor es la alarma, no el problema.", "Quitar la señal (por adaptación o fármacos) no elimina la exposición al acetaldehído en la mucosa.",
       ["«La tolerancia elimina el riesgo»: el acetaldehído sigue acumulándose.",
        "«La protege»: el efecto aversivo puede reducir el consumo, pero si bebe, su riesgo es mayor.",
        "«Antihistamínicos»: enmascaran la señal y facilitan beber más."]))

mc("B2-6 · APOE ε4 y alcohol",
   "<p>Hombre de 50 años, <em>APOE</em> ε3/ε4, LDL 168 mg/dL, bebe 3 cervezas diarias. Su cuñado (ε2/ε3) bebe lo mismo y tiene LDL de 110 mg/dL. ¿Qué interpretación se apoya en la evidencia de interacción gen–dieta?</p>",
   ["El alcohol baja el LDL en todos por igual.",
    "En portadores de ε4 se ha descrito que el consumo de alcohol se asocia con LDL más alto, mientras que en portadores de ε2 se asocia con LDL más bajo; en este paciente, reducir el alcohol es una medida razonable junto con el resto del tratamiento.",
    "La diferencia entre ambos se debe solo al alcohol.",
    "El genotipo ε4 obliga a iniciar estatinas sin cambios de estilo de vida."],
   1,
   _fb("interacción APOE × alcohol sobre LDL.", "El mismo hábito puede asociarse con efectos opuestos según el genotipo; por eso la recomendación individual considera ambos.",
       ["«Baja el LDL en todos»: es justamente lo que la interacción contradice.",
        "«Solo al alcohol»: beben lo mismo; la diferencia sugiere el genotipo (y otros factores).",
        "«Estatinas sin estilo de vida»: el genotipo no sustituye la evaluación clínica ni elimina la intervención dietaria."]))

ma("B2-7 · Interpretar un reporte de FTO",
   "<p>Mujer de 29 años, IMC 33, <em>FTO</em> rs9939609 AA. Un laboratorio comercial le recomienda «una dieta especial para su genotipo FTO». Selecciona las afirmaciones bien sustentadas.</p>",
   ["Su genotipo se asocia con mayor riesgo de obesidad, pero no la determina.",
    "La actividad física atenúa el efecto del alelo A sobre el IMC.",
    "Las personas AA pierden en promedio un peso similar a las TT en intervenciones de dieta y ejercicio, así que el genotipo no es una razón para no intentarlo.",
    "Una «dieta para FTO» tiene eficacia superior demostrada frente a una dieta saludable estándar.",
    "Si fuera TT, no tendría riesgo de obesidad."],
   [0, 1, 2],
   "<p><strong>Por qué son correctas:</strong> FTO aumenta el riesgo de forma modesta; la actividad física lo atenúa, y los metaanálisis no muestran peor respuesta a la pérdida de peso en portadores del alelo A.</p>"
   "<p><strong>Por qué no las demás:</strong> no hay evidencia sólida de que una dieta «para FTO» sea superior a una dieta saludable estándar; y ser TT no elimina el riesgo, porque el IMC es poligénico y ambiental.</p>")

ma("B2-8 · Un hiperrespondedor que quizá no lo es",
   "<p>En consulta, una paciente sube su LDL de 120 a 150 mg/dL tras dos semanas comiendo 3 huevos diarios, y la etiquetan como «hiperrespondedora genética». Selecciona las afirmaciones correctas.</p>",
   ["Una sola medición antes y después no basta: el LDL varía entre días, y parte del cambio podría ser variabilidad intraindividual.",
    "Para clasificarla habría que repetir mediciones o repetir el reto dietario.",
    "El genotipo APOE (p. ej., ε4) es uno de los factores asociados con mayor respuesta del LDL al colesterol dietario.",
    "Si es hiperrespondedora, todos sus familiares también lo serán.",
    "Los hiporrespondedores no tienen ninguna base genética."],
   [0, 1, 2],
   "<p><strong>Por qué son correctas:</strong> Clasificar respondedores exige separar la respuesta real del ruido de medición; APOE es uno de los moduladores conocidos.</p>"
   "<p><strong>Por qué no las demás:</strong> los familiares comparten solo parte de las variantes y del ambiente; y tanto la hiper como la hiporrespuesta tienen componentes genéticos.</p>")

essay("B2-9 · Caso: «la leche me cae mal»",
      "<p>Mujer de 24 años con distensión, gases y diarrea 1–2 horas después de tomar un vaso grande de leche. Tolera queso madurado y yogur. Resultados:</p>"
      + _tabla(["Estudio", "Resultado"],
               [("Genotipo <em>MCM6</em> −13910", "C/C"),
                ("Genotipo <em>MCM6</em> −22018", "G/G"),
                ("Prueba de H₂ espirado con 25 g de lactosa", "Aumento de 38 ppm sobre el basal (positiva ≥ 20 ppm), con síntomas"),
                ("Anticuerpos para enfermedad celíaca", "Negativos")])
      + "<p>a) Usa correctamente los términos hipolactasia, malabsorción e intolerancia para describir su caso. "
        "b) Explica el mecanismo molecular de su genotipo (potenciador de MCM6, expresión de LCT y metilación del promotor con la edad). "
        "c) ¿Por qué tolera queso madurado y yogur? d) Propón un manejo nutricional y di qué riesgo nutricional hay que vigilar. "
        "e) Señala una limitación de usar solo el genotipo para diagnosticar.</p>",
      "<p><strong>Respuesta modelo.</strong> a) Genotipo C/C y G/G de no persistencia → hipolactasia del adulto (probable); la prueba de H₂ positiva demuestra malabsorción; los síntomas durante la prueba confirman intolerancia. "
      "b) Los alelos −13910T y −22018A, en un potenciador del intrón 13 de MCM6, mantienen la transcripción de LCT en el adulto; con C/C y G/G la expresión de lactasa declina tras el destete, y en el epitelio se acumula metilación del promotor de LCT que refuerza el silenciamiento. La enzima es normal; cambia su cantidad. "
      "c) El queso madurado tiene muy poca lactosa (queda en el suero y se fermenta) y el yogur tiene bacterias con β-galactosidasa que la hidrolizan parcialmente, además de vaciamiento gástrico más lento. "
      "d) No eliminar todos los lácteos: fraccionar la lactosa (dosis pequeñas con comidas), usar productos deslactosados, yogur y quesos madurados, o lactasa exógena; vigilar el aporte de calcio y vitamina D. "
      "e) El genotipo indica la predisposición, no los síntomas; hay personas C/C sin intolerancia con dosis habituales, y otras variantes de persistencia en poblaciones no europeas no se detectan con −13910; además los síntomas podrían tener otras causas (por eso se descartó celiaquía).</p>"
      "<p><strong>Rúbrica (6 pts):</strong> 1.5 terminología correcta de los tres niveles; 1.5 mecanismo regulatorio y epigenético; 1 explicación de la tolerancia a fermentados; 1 manejo con vigilancia de calcio/vitamina D; 1 limitación del genotipo.</p>")

essay("B2-10 · Caso: reporte nutrigenético integrado",
      "<p>Hombre de 45 años, IMC 31, LDL 162 mg/dL, presión 138/88 mmHg. Toma 4 tazas de café y 3–4 cervezas al día; sedentario. Su reporte comercial incluye:</p>"
      + _tabla(["Gen (variante)", "Genotipo"],
               [("<em>CYP1A2</em> rs762551", "A/C"),
                ("<em>APOE</em>", "ε3/ε4"),
                ("<em>ALDH2</em> rs671", "G/G (ALDH2*1/*1)"),
                ("<em>FTO</em> rs9939609", "A/T"),
                ("<em>MTHFR</em> C677T", "C/C")])
      + "<p>a) Interpreta cada resultado en una o dos líneas (qué implica y qué no). "
        "b) Ordena por prioridad tres recomendaciones y justifica cada una con un mecanismo. "
        "c) Explica por qué un resultado «normal» en ALDH2 no significa que el alcohol sea seguro para él. "
        "d) Menciona dos limitaciones de este tipo de reportes.</p>",
      "<p><strong>Respuesta modelo.</strong> a) CYP1A2 A/C: portador del alelo C, metabolismo de cafeína más lento que A/A; con presión limítrofe conviene moderar el café. "
      "APOE ε3/ε4: mayor LDL y mayor respuesta del LDL a grasa y colesterol dietarios; además, en ε4 el alcohol se asocia con LDL más alto. "
      "ALDH2*1/*1: oxida el acetaldehído con normalidad; no tiene rubor que lo «avise». FTO A/T: un alelo de riesgo, efecto modesto y atenuable con actividad física. MTHFR C/C: sin la variante termolábil; no requiere medidas específicas. "
      "b) 1) Reducir el alcohol: actúa sobre LDL (interacción con ε4), presión, peso y riesgo de cáncer. 2) Actividad física regular y patrón dietario con menos grasa saturada: baja LDL (relevante en ε4), atenúa el efecto de FTO y ayuda a la presión. 3) Bajar a 1–2 tazas de café: menor exposición a cafeína dada su metabolización más lenta y su presión limítrofe. "
      "c) Sin la variante, el acetaldehído no se acumula de forma aguda, pero el etanol sigue siendo tóxico (hígado, presión, cáncer, LDL en ε4) y la falta de rubor puede facilitar beber más. "
      "d) Las variantes explican una fracción pequeña del riesgo y casi todas provienen de asociaciones (GWAS), no de pruebas de causalidad individual; la evidencia de que dietas guiadas por genotipo sean superiores a una dieta saludable estándar es limitada; y los reportes suelen no considerar la ascendencia de la persona.</p>"
      "<p><strong>Rúbrica (6 pts):</strong> 2 interpretación correcta de los cinco genotipos; 2 priorización con mecanismo; 1 argumento sobre ALDH2 normal; 1 dos limitaciones pertinentes.</p>")

# ===========================================================================
# BLOQUE 3 · BIOINFORMÁTICA, PCR IN SILICO E INTERPRETACIÓN DE GELES (20 pts)
# ===========================================================================
header("<h3>Bloque 3 · Bioinformática, PCR <em>in silico</em> e interpretación de geles (20 %)</h3>"
       "<p>9 reactivos. Ten a mano la tabla del código genético.</p>")

mc("B3-1 · Leer una variante en la secuencia (MTHFR)",
   "<p>Fragmento <strong>ilustrativo</strong> de la secuencia codificante de <em>MTHFR</em>, en marco de lectura, con el codón 222 entre corchetes:</p>"
   f"<p>Referencia: {_seq('5′-… GGA [GCC] GAC …-3′')}<br>Paciente: {_seq('5′-… GGA [GTC] GAC …-3′')}</p>"
   "<p>¿Qué cambio ocurre y cómo se clasifica?</p>",
   ["C→T en la primera posición del codón; Ala→Ser; missense.",
    "C→T en la segunda posición del codón; Ala→Val; missense (corresponde a C677T).",
    "C→T en la segunda posición; Ala→Ala; sinónimo.",
    "C→T que crea un codón de paro; nonsense."],
   1,
   _fb("GCC (Ala) → GTC (Val), cambio en la segunda base del codón: missense.", "Es la variante C677T: alanina 222 por valina, que vuelve termolábil a la enzima.",
       ["«Primera posición, Ala→Ser»: la primera base (G) no cambió; Ser sería TCC o AGC.",
        "«Sinónimo»: GTC codifica valina, no alanina.",
        "«Nonsense»: GTC no es codón de paro (TAA, TAG, TGA)."]))

dropdowns("B3-2 · Clasificar variantes en una secuencia",
          "<p>Marco de lectura abierto ilustrativo (los números indican la posición del nucleótido desde la A del ATG):</p>"
          f"<p>{_seq('5′-ATG GCT TGG CAG GAA CTG AAA TAA-3′')}<br>"
          "Proteína: Met-Ala-Trp-Gln-Glu-Leu-Lys-Stop</p>"
          "<p>Clasifica cada variante:</p>"
          "<p>c.6T&gt;C → [v1]<br>c.9G&gt;A → [v2]<br>c.14A&gt;T → [v3]<br>c.17delT → [v4]<br>c.10_12delCAG → [v5]</p>",
          {"v1": (["sinónima (Ala→Ala)", "missense (Ala→Pro)", "nonsense", "indel con corrimiento del marco"], 0),
           "v2": (["nonsense (Trp→Stop)", "sinónima (Trp→Trp)", "missense (Trp→Cys)", "indel sin corrimiento del marco"], 0),
           "v3": (["missense (Glu→Val)", "sinónima (Glu→Glu)", "nonsense", "missense (Glu→Asp)"], 0),
           "v4": (["indel con corrimiento del marco", "indel sin corrimiento del marco", "sinónima", "nonsense directo en ese codón"], 0),
           "v5": (["indel sin corrimiento del marco (pierde Gln)", "indel con corrimiento del marco", "nonsense", "CNV"], 0)},
          "<p><strong>Clave:</strong> c.6T&gt;C: GCT→GCC, ambos Ala (sinónima). c.9G&gt;A: TGG→TGA, paro (nonsense). c.14A&gt;T: GAA→GTA, Glu→Val (missense). "
          "c.17delT: se pierde 1 nt de CTG y se corre el marco desde el codón 6. c.10_12delCAG: se pierde el codón 4 completo (Gln) sin correr el marco.</p>"
          "<p><strong>Distractores:</strong> Ala→Pro requeriría CCT; Trp tiene un solo codón (TGG), así que no hay cambio sinónimo posible; Glu→Asp requeriría GAT o GAC; una CNV es un cambio en el número de copias de un segmento grande, no la pérdida de 3 nt.</p>",
          puntos=3.0)

GEL = (
    "<p>Gel de agarosa al 2 % con productos de PCR de PV92 (alelo + con Alu ≈ 731 pb; alelo − sin Alu ≈ 416 pb). "
    "M = marcador de 100 pb. «▬» indica banda y «▬ tenue» una banda débil.</p>"
    + _tabla(["Tamaño (pb)", "M", "Carril 1", "Carril 2", "Carril 3", "Carril 4", "Carril 5", "Carril 6"],
             [("1000", "▬", "", "", "", "", "", ""),
              ("≈ 730", "▬ (700)", "▬", "▬", "", "", "", ""),
              ("500", "▬", "", "", "", "", "", ""),
              ("≈ 420", "▬ (400)", "", "▬", "▬", "", "▬", ""),
              ("100", "▬", "", "", "", "", "", ""),
              ("&lt; 80", "", "", "", "", "", "▬ tenue", "")])
    + "<p>El carril 6 es el control sin DNA.</p>"
)

matching("B3-3 · Lectura de gel: Alu PV92",
         GEL + "<p>Asigna el genotipo o la interpretación de cada carril.</p>",
         [("Carril 1", "Homocigoto +/+ (inserción en ambos cromosomas)"),
          ("Carril 2", "Heterocigoto +/−"),
          ("Carril 3", "Homocigoto −/− (sin inserción)"),
          ("Carril 4", "Sin producto: no se puede genotipar; repetir la PCR"),
          ("Carril 5", "Homocigoto −/−; la banda menor de 80 pb son dímeros de cebador"),
          ("Carril 6", "Control negativo correcto: confirma que no hubo contaminación")],
         ["Heterocigoto con dos inserciones Alu distintas"],
         "<p><strong>Clave:</strong> 1 = +/+ (solo 731); 2 = +/− (731 y 416); 3 = −/− (solo 416); 4 = sin banda en una muestra: falla de extracción o de PCR, no se asigna genotipo; "
         "5 = −/− con dímeros de cebador (artefacto de &lt; 100 pb que no corresponde a ningún alelo); 6 = control sin DNA limpio. "
         "El distractor no tiene sentido: en un locus hay a lo sumo un sitio de inserción por cromosoma, y el gel solo muestra dos tamaños posibles.</p>",
         puntos=3.0)

numerical("B3-4 · Frecuencia alélica a partir del gel del grupo",
          "<p>El grupo completo (30 estudiantes) genotipó PV92: 12 son +/+, 10 son +/− y 8 son −/−. "
          "Calcula la frecuencia del alelo + (dos cifras decimales).</p>",
          0.57, 0.01,
          "<p>Alelos + = 2 × 12 + 10 = 34 de 60 alelos → p = 34/60 = <strong>0.57</strong>. "
          "Con Hardy–Weinberg se esperarían 2pq × 30 ≈ 14.7 heterocigotos y se observaron 10: hay un déficit que con n = 30 puede ser azar, "
          "pero que también podría indicar heterocigotos mal leídos (amplificación preferencial del alelo corto).</p>")

dropdowns("B3-5 · El ciclo térmico de la PCR",
          "<p>En cada ciclo, la mezcla se calienta a [p1] para separar las hebras; luego se baja a una temperatura de alineamiento que se elige [p2]; "
          "finalmente se sube a [p3], donde la [p4] extiende los cebadores en dirección [p5].</p>",
          {"p1": (["94–95 °C", "72 °C", "55 °C", "37 °C"], 0),
           "p2": (["unos grados por debajo de la Tm de los cebadores", "siempre a 72 °C", "por encima de 95 °C", "igual a la temperatura ambiente"], 0),
           "p3": (["72 °C", "95 °C", "4 °C", "60 °C fijos para cualquier enzima"], 0),
           "p4": (["Taq polimerasa", "transcriptasa reversa", "ligasa", "enzima de restricción"], 0),
           "p5": (["5′→3′", "3′→5′", "en ambas direcciones a la vez", "del extremo 3′ del molde al 5′ del cebador"], 0)},
          "<p><strong>Clave:</strong> 94–95 °C (desnaturalización) → alineamiento unos grados bajo la Tm de los cebadores → 72 °C, temperatura óptima de la Taq, que sintetiza 5′→3′. "
          "Si el alineamiento es demasiado bajo aparecen productos inespecíficos y dímeros; si es demasiado alto, el cebador no se une y no hay producto.</p>")

dropdowns("B3-6 · Columna de sílice: bind-wash-elute",
          "<p>El lisado se mezcla con un buffer que contiene sales caotrópicas de [s1] y se agrega [s2]; en esas condiciones el DNA se une a la sílice. "
          "Los lavados con buffer etanólico eliminan [s3]. Antes de eluir se hace un [s4], porque el etanol residual [s5]. "
          "Finalmente el DNA se eluye con [s6].</p>",
          {"s1": (["guanidina", "sodio a baja concentración", "magnesio", "Tris"], 0),
           "s2": (["etanol", "fenol", "agua destilada", "SDS"], 0),
           "s3": (["sales, proteínas y otros contaminantes", "el DNA unido", "la sílice", "los cebadores de PCR"], 0),
           "s4": (["centrifugado en seco (dry spin)", "lavado con agua", "calentamiento a 95 °C", "agregado de fenol"], 0),
           "s5": (["inhibe la PCR y dificulta la elución", "mejora el rendimiento", "es necesario para la elución", "protege al DNA de las nucleasas"], 0),
           "s6": (["buffer de baja fuerza iónica (TE o agua, pH ≈ 8)", "buffer con guanidina concentrada", "etanol al 70 %", "cloroformo"], 0)},
          "<p><strong>Clave:</strong> las sales de guanidina deshidratan el DNA y rompen la capa de agua de la sílice, y el etanol favorece la unión; el lavado etanólico quita sales y proteínas sin despegar el DNA; "
          "el dry spin elimina el etanol, que inhibe la polimerasa y evita que el DNA se rehidrate; un buffer de baja fuerza iónica a pH ligeramente básico rehidrata el DNA y lo libera.</p>")

mc("B3-7 · Comparar métodos de extracción",
   "<p>Un DNA extraído con columna de sílice da A<sub>260/280</sub> = 1.84 y A<sub>260/230</sub> = 0.55, y la PCR falla. ¿Cuál es la explicación más probable y qué harías?</p>",
   ["Contaminación con proteínas; repetir con fenol-cloroformo.",
    "Arrastre de sales de guanidina (absorben cerca de 230 nm) por un lavado insuficiente; repetir el lavado etanólico, hacer el dry spin y volver a eluir, o purificar con perlas SPRI.",
    "Contaminación con RNA; agregar RNasa y la PCR funcionará.",
    "El DNA está demasiado puro; diluirlo en agua."],
   1,
   _fb("arrastre de guanidina.", "Una relación 260/280 cercana a 1.8 indica poca proteína; la relación 260/230 muy baja señala sales caotrópicas u otros compuestos que absorben a 230 nm y que inhiben la polimerasa.",
       ["«Proteínas»: bajarían la relación 260/280 (por debajo de ~1.7). Fenol-cloroformo, además, añade el riesgo de arrastrar fenol (absorbe ~270 nm).",
        "«RNA»: subiría la relación 260/280 hacia ~2.0 y no explica el 260/230 bajo.",
        "«Demasiado puro»: no existe ese problema; los valores indican contaminación."]))

mc("B3-8 · Herramientas in silico",
   "<p>Un equipo diseña cebadores para genotipar <em>ALDH2</em> rs671. UCSC In-Silico PCR da un producto de 214 pb en el cromosoma 12, pero Primer-BLAST con el genoma de referencia reporta además un segundo producto de 214 pb en otro cromosoma. ¿Qué interpretación y acción son correctas?</p>",
   ["Ningún problema: UCSC ya confirmó el producto, así que Primer-BLAST se equivoca.",
    "Los cebadores pueden amplificar también una secuencia muy parecida (un parálogo o pseudogén); como el producto es del mismo tamaño, el gel no lo distinguiría y podría falsear el genotipo. Hay que rediseñar al menos un cebador en una región única y verificarlo con BLAST.",
    "El segundo producto es el alelo variante de rs671.",
    "Primer-BLAST solo funciona con mRNA, así que hay que ignorarlo."],
   1,
   _fb("riesgo de amplificación inespecífica.", "UCSC exige coincidencia casi perfecta y puede no reportar sitios con desapareamientos; Primer-BLAST evalúa la especificidad contra todo el genoma permitiendo algunos desapareamientos.",
       ["«Primer-BLAST se equivoca»: las herramientas son complementarias; UCSC no está diseñada para buscar todos los sitios parecidos.",
        "«Es el alelo variante»: un SNP no se ubica en otro cromosoma; ambos alelos se amplifican en el mismo locus.",
        "«Solo con mRNA»: Primer-BLAST permite elegir el genoma de referencia como base de datos."]))

mc("B3-9 · Leer el GWAS Catalog",
   "<p>En el GWAS Catalog, rs4988235 aparece asociado a «lactase persistence» y a niveles de calcio, con «mapped gene: <em>MCM6</em>» y p = 3 × 10⁻²⁰⁰. Un alumno concluye que <em>MCM6</em> codifica la lactasa y que la variante causa directamente cambios de calcio. ¿Cuál es la mejor corrección?</p>",
   ["El alumno tiene razón: el gen asignado es siempre el gen que codifica el fenotipo.",
    "El «mapped gene» es el gen donde cae la variante, no necesariamente el gen efector: la variante está en un potenciador de MCM6 que regula LCT. Además, una asociación muy significativa no demuestra causalidad directa; el efecto en calcio puede ser indirecto (consumo de lácteos).",
    "Un valor p tan pequeño prueba que el efecto es grande.",
    "El GWAS Catalog solo incluye variantes missense."],
   1,
   _fb("gen asignado ≠ gen efector, y asociación ≠ causalidad.", "El umbral de significancia genómica es p &lt; 5 × 10⁻⁸; un p muy pequeño indica alta certeza estadística (por tamaños de muestra enormes), no un efecto grande ni un mecanismo.",
       ["«Gen asignado = gen del fenotipo»: es el error que la variante de lactasa ilustra mejor.",
        "«p pequeño = efecto grande»: el p depende también del tamaño de muestra; el efecto se lee en el OR o beta.",
        "«Solo missense»: la mayoría de las variantes de GWAS son no codificantes."]))

# ===========================================================================
# BLOQUE 4 · CÁLCULO QUÍMICO-ENZIMÁTICO, CAPACIDAD ANTIOXIDANTE Y TROUBLESHOOTING (20 pts)
# ===========================================================================
header("<h3>Bloque 4 · Cálculo químico-enzimático, capacidad antioxidante y troubleshooting (20 %)</h3>"
       "<p>5 cálculos, 4 de opción múltiple (1.5 pts c/u) y 1 de selección múltiple. Escribe solo el número en los cálculos; en el examen se pide el procedimiento.</p>"
       "<p>Fórmulas: % inhibición = [A<sub>control</sub> − (A<sub>muestra</sub> − A<sub>blanco</sub>)] / A<sub>control</sub> × 100. "
       "Catalasa: U/mL = (ΔA<sub>240</sub>/min) / (43.6 × l) × 1000 × (V<sub>total</sub>/V<sub>muestra</sub>).</p>")

numerical("B4-1 · Porcentaje de inhibición de DPPH",
          "<p>Extracto de jamaica a 50 µg/mL:</p>"
          + _tabla(["Lectura", "A<sub>517</sub>"],
                   [("Control (DPPH + metanol)", "0.950"), ("Muestra + DPPH", "0.512"), ("Blanco de muestra (extracto sin DPPH)", "0.037")])
          + "<p>Calcula el porcentaje de inhibición (una cifra decimal).</p>",
          50.0, 0.5,
          "<p>A muestra corregida = 0.512 − 0.037 = 0.475. % = (0.950 − 0.475)/0.950 × 100 = <strong>50.0 %</strong>. "
          "Sin restar el blanco saldría 46.1 %: las antocianinas absorben cerca de 517 nm y harían parecer al extracto menos activo.</p>")

TABLA_IC50 = _tabla(["µg/mL", "A muestra + DPPH", "A blanco de muestra"],
                    [("10", "0.681", "0.012"), ("20", "0.557", "0.020"), ("40", "0.405", "0.035"), ("80", "0.264", "0.062")])

numerical("B4-2 · IC<sub>50</sub> con tabla de absorbancias",
          "<p>Extracto de cáscara de granada. A<sub>517</sub> del control (DPPH + metanol) = 0.880.</p>" + TABLA_IC50
          + "<p>Calcula el % de inhibición de cada concentración (restando el blanco) y estima la IC<sub>50</sub> por interpolación lineal entre los dos puntos que rodean al 50 % "
            "(µg/mL, una cifra decimal).</p>",
          31.6, 0.6,
          "<p>% corregidos: 10 → 24.0; 20 → 39.0; 40 → 58.0; 80 → 77.0. El 50 % está entre 20 y 40 µg/mL. "
          "IC<sub>50</sub> = 20 + (50 − 39.0)/(58.0 − 39.0) × 20 = <strong>31.6 µg/mL</strong>. "
          "Sin restar el blanco se obtendría ≈ 35.4 µg/mL: el error sobreestima la IC<sub>50</sub> y subestima la potencia.</p>",
          puntos=3.0)

numerical("B4-3 · Capacidad antioxidante por FRAP",
          "<p>Curva de Trolox en FRAP: A<sub>593</sub> = 0.0031·C + 0.008 (C en µM). Se extraen 0.5 g de amaranto en 10 mL; el extracto se diluye 1:10 y da A<sub>593</sub> = 0.597. "
          "Calcula la capacidad antioxidante en µmol de equivalentes de Trolox por gramo (µmol TE/g).</p>",
          38.0, 0.5,
          "<p>1) C = (0.597 − 0.008)/0.0031 = 190 µM en la dilución. 2) × 10 = 1,900 µM = 1.90 µmol/mL en el extracto. "
          "3) 1.90 × 10 mL = 19 µmol en 0.5 g → <strong>38 µmol TE/g</strong>. En FRAP la absorbancia sube con más poder reductor.</p>")

numerical("B4-4 · Actividad específica de catalasa",
          "<p>Homogenado de hígado: ΔA<sub>240</sub>/min = 0.0436 (tramo inicial), cubeta de cuarzo de 1 cm, volumen total 3.0 mL, volumen de muestra 0.05 mL, proteína 3.0 mg/mL. "
          "ε<sub>240</sub>(H₂O₂) = 43.6 M⁻¹ cm⁻¹; 1 U = 1 µmol de H₂O₂ descompuesto por minuto. Calcula la actividad en U/mg de proteína.</p>",
          20.0, 0.3,
          "<p>U/mL = 0.0436/43.6 × 1000 × (3.0/0.05) = 0.001 × 1000 × 60 = 60 U/mL. Actividad específica = 60/3.0 = <strong>20 U/mg</strong>.</p>")

numerical("B4-5 · Unidades de SOD",
          "<p>Ensayo de SOD con NBT (lectura del formazán a 560 nm). Blanco (reacción completa sin muestra): ΔA/min = 0.090. Con 15 µL de muestra: ΔA/min = 0.054. "
          "Con la curva de varios volúmenes, el 50 % de inhibición se alcanza con <strong>25 µL</strong>. Proteína: 4.0 mg/mL. 1 U = cantidad que inhibe el 50 %. "
          "Calcula la actividad en U/mg de proteína.</p>",
          10.0, 0.2,
          "<p>Con 15 µL la inhibición es (0.090 − 0.054)/0.090 = 40 %, pero las unidades salen del volumen que da 50 %: 1 U en 0.025 mL = 40 U/mL; 40/4.0 = <strong>10 U/mg</strong>. "
          "No se escala el 40 % proporcionalmente porque la relación no es lineal.</p>")

mc("B4-6 · Inhibición negativa",
   "<p>Con un extracto concentrado de betabel, la absorbancia de «muestra + DPPH» a 517 nm es mayor que la del control y el cálculo da −15 % de inhibición. ¿Qué pasó?</p>",
   ["El betabel es prooxidante y genera DPPH•.",
    "Las betalaínas del betabel absorben cerca de 517 nm y suman su color; falta restar el blanco de muestra (extracto sin DPPH), o diluir el extracto.",
    "El DPPH se degradó por la luz.",
    "La IC<sub>50</sub> del betabel es negativa."],
   1,
   _fb("interferencia de pigmentos.", "Es el mismo problema de las antocianinas: el color propio del extracto se lee como si fuera DPPH• sin reaccionar.",
       ["«Genera DPPH•»: el radical solo viene del reactivo; un extracto no lo crea.",
        "«DPPH degradado»: bajaría la absorbancia del control, no subiría la de la muestra.",
        "«IC<sub>50</sub> negativa»: una concentración no puede ser negativa; el resultado es un artefacto."]),
   puntos=1.5)

mc("B4-7 · Un control que baja",
   "<p>Durante la sesión, la A<sub>517</sub> del control de DPPH bajó de 0.92 (9:00 h) a 0.71 (11:30 h). El frasco quedó destapado junto a la ventana. ¿Qué haces?</p>",
   ["Nada: el control no se usa en el cálculo.",
    "El DPPH se degradó por la luz; preparar reactivo fresco, protegerlo de la luz y leer un control junto a cada serie de muestras. Los datos calculados con el control de 0.92 para muestras leídas más tarde están sesgados.",
    "Ajustar todas las muestras con el control de las 9:00 h.",
    "El control bajó porque el metanol se contaminó con antioxidantes del laboratorio."],
   1,
   _fb("degradación fotoquímica del DPPH.", "El control es el denominador del cálculo; si cambia durante la sesión, todas las inhibiciones calculadas con un control viejo quedan mal.",
       ["«No se usa»: es el término A<sub>control</sub> de la fórmula.",
        "«Usar el de las 9:00»: precisamente introduce el sesgo.",
        "«Metanol contaminado»: es mucho menos probable que la luz, con el frasco destapado junto a la ventana."]),
   puntos=1.5)

mc("B4-8 · Catalasa fuera de rango",
   "<p>Al iniciar el ensayo de catalasa, la A<sub>240</sub> inicial (antes de agregar muestra) es 1.85. ¿Cuál es la causa más probable y la corrección?</p>",
   ["Es lo esperado; con más absorbancia el ensayo es más sensible.",
    "El H₂O₂ está demasiado concentrado o se usó una cubeta de plástico que absorbe en el UV; verificar la concentración de H₂O₂ por A<sub>240</sub>, diluirlo y usar cubeta de cuarzo.",
    "La catalasa ya está actuando.",
    "Falta agregar más H₂O₂."],
   1,
   _fb("fuera del intervalo lineal del espectrofotómetro.", "Por encima de ~1 de absorbancia la lectura pierde linealidad; además el plástico común absorbe a 240 nm.",
       ["«Más sensible»: a esas absorbancias la relación con la concentración ya no es lineal.",
        "«La catalasa ya actúa»: aún no se agregó muestra.",
        "«Más H₂O₂»: subiría todavía más la absorbancia."]),
   puntos=1.5)

mc("B4-9 · ¿Cuál extracto es más potente?",
   "<p>Tres extractos dieron IC<sub>50</sub> en DPPH: A = 18 µg/mL, B = 65 µg/mL y C = «no alcanzó 50 % a 200 µg/mL». ¿Qué conclusión es correcta?</p>",
   ["B es el más potente porque su IC<sub>50</sub> es mayor.",
    "A es el más potente en este ensayo porque necesita menos extracto para inhibir el 50 %; para C se reporta IC<sub>50</sub> &gt; 200 µg/mL, sin extrapolar.",
    "C es el más potente porque no se pudo medir.",
    "A es el mejor antioxidante para el organismo."],
   1,
   _fb("menor IC<sub>50</sub> = mayor potencia en el ensayo.", "La IC<sub>50</sub> es una concentración: cuanto menos extracto se necesita, más activo es.",
       ["«B porque es mayor»: es el error más frecuente; invierte la lógica.",
        "«C porque no se pudo medir»: no alcanzar 50 % indica menor actividad en ese intervalo.",
        "«Mejor para el organismo»: DPPH es un ensayo químico in vitro; no considera absorción ni metabolismo."]),
   puntos=1.5)

ma("B4-10 · Leer los ensayos en conjunto",
   "<p>Ratas con dieta alta en grasa durante 8 semanas, frente al control:</p>"
   + _tabla(["Marcador", "Cambio"],
            [("SOD hepática (U/mg)", "↑ 55 %"), ("Catalasa hepática (U/mg)", "↓ 30 %"), ("TBARS (MDA)", "↑ 80 %"), ("TAC sérica", "↑ 20 %, con ácido úrico ↑ 45 %")])
   + "<p>Selecciona las interpretaciones bien sustentadas.</p>",
   ["Se produce más H₂O₂ del que se elimina; el H₂O₂ acumulado puede generar radical hidroxilo por Fenton, coherente con el aumento de TBARS.",
    "El aumento de TAC sérica no indica menos estrés oxidativo: el ácido úrico aporta buena parte de la TAC plasmática.",
    "Más SOD significa que el estado antioxidante mejoró.",
    "Conviene confirmar con otra vía de eliminación de H₂O₂ (glutatión peroxidasa) antes de concluir.",
    "La TAC alta demuestra que la dieta alta en grasa es antioxidante."],
   [0, 1, 3],
   "<p><strong>Por qué son correctas:</strong> SOD alta con catalasa baja es un desbalance: cambia una especie reactiva (O₂•⁻) por otra (H₂O₂) que no se elimina; las TBARS confirman daño lipídico.</p>"
   "<p><strong>Por qué no las demás:</strong> una enzima elevada puede indicar más estrés, no mejor salud; y una TAC alta explicada por urato no es evidencia de efecto antioxidante.</p>")


def _barajar():
    """Baraja las opciones de mc/ma con semilla fija para que la letra correcta no sea siempre la misma
    en el Word impreso (Canvas además las baraja por alumno)."""
    import random
    for r in REACTIVOS:
        if r["type"] not in ("mc", "ma"):
            continue
        rng = random.Random(r["title"])
        orden = list(range(len(r["choices"])))
        rng.shuffle(orden)
        r["choices"] = [r["choices"][i] for i in orden]
        if r["type"] == "mc":
            r["correct"] = orden.index(r["correct"])
        else:
            r["correct"] = sorted(orden.index(i) for i in r["correct"])


_barajar()
