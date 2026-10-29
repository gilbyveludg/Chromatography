# -*- coding: utf-8 -*-
"""Banco de reactivos del EXAMEN «Del Genoma Crudo a la Clínica» (Nutrición Molecular, Otoño 2026).

Misma estructura y pesos que el preexamen, con reactivos nuevos y acotado a 2 horas en línea:
  1. Opción múltiple: fundamentos moleculares y ómicos ............. 30 %
  2. Casos clínicos y diagnóstico nutrigenético ..................... 30 %
  3. Bioinformática, PCR in silico e interpretación de geles ......... 20 %
  4. Cálculo químico-enzimático, capacidad antioxidante y troubleshooting 20 %

Generar (desde la carpeta del preexamen, que tiene los generadores):
  python3 ../preexamen_nutricion_molecular/generar_qti.py banco_examen.py
  BANCO=banco_examen.py python3 ../preexamen_nutricion_molecular/exportar_json.py examen.json
  node ../preexamen_nutricion_molecular/generar_word.js examen.json Examen_..._con_clave.docx
"""

TITULO = "Examen · Del Genoma Crudo a la Clínica (Nutrición Molecular)"
PIE = "Examen · Del Genoma Crudo a la Clínica"
ARCHIVO_ZIP = "examen_nutricion_molecular_qti.zip"
ID_CUESTIONARIO = "examen-nutricion-molecular-2026"

# Examen calificado: 2 horas, un intento, sin mostrar respuestas ni retroalimentación al enviar.
CANVAS = {
    "quiz_type": "assignment",
    "time_limit": 120,
    "allowed_attempts": 1,
    "show_correct_answers": "false",
    "hide_results": "always",
    "one_question_at_a_time": "false",
    "cant_go_back": "false",
    "scoring_policy": "keep_highest",
}

DESCRIPCION = """
<p><strong>Examen individual en línea · 2 horas · 100 puntos.</strong></p>
<p><strong>No está permitido usar inteligencia artificial</strong> (ChatGPT, Gemini, Copilot, Claude, traductores con IA, extensiones o apps que generen respuestas),
ni consultar a otras personas. Puedes usar calculadora y una tabla del código genético.</p>
<p>Las preguntas piden razonar con los datos de cada caso: una respuesta genérica, aunque suene correcta, no obtiene el puntaje.</p>
"""

TIEMPOS = [
    ("Bloque 1 · Opción múltiple (10 reactivos, 30 pts)", 20),
    ("Bloque 2 · Casos clínicos (7 reactivos, 30 pts)", 40),
    ("Bloque 3 · Bioinformática y geles (6 reactivos, 20 pts)", 25),
    ("Bloque 4 · Cálculo y troubleshooting (6 reactivos, 20 pts)", 25),
    ("Revisión final", 10),
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
    "<li>Tiempo límite: <strong>120 minutos</strong> y <strong>un solo intento</strong>. Canvas envía el examen automáticamente al terminar el tiempo.</li>"
    "<li><strong>Uso de inteligencia artificial prohibido.</strong> Cualquier respuesta generada o reescrita con IA, o copiada de otra persona, se anula y se reporta conforme al reglamento.</li>"
    "<li>Permitido: calculadora y tabla del código genético. No necesitas otras fuentes.</li>"
    "<li>Cálculos: escribe solo el número, con punto decimal y sin unidades.</li>"
    "<li>Selección múltiple: marca todas las correctas; se da crédito parcial y se descuentan las marcadas de más.</li>"
    "<li>Casos de respuesta extendida: escribe con tus palabras y usa los datos del caso; se califica el razonamiento, no la extensión.</li>"
    "</ul>"
    "<p><strong>Distribución sugerida del tiempo</strong></p>"
    + _tabla(["Bloque", "Minutos"], [(s, m) for s, m in TIEMPOS])
)

REACTIVOS = []


def header(texto):
    REACTIVOS.append({"type": "header", "text": texto})


def mc(titulo, texto, opciones, correcta, fb, puntos=3.0):
    REACTIVOS.append({"type": "mc", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correcta, "fb": fb, "points": puntos})


def ma(titulo, texto, opciones, correctas, fb, puntos=4.0):
    REACTIVOS.append({"type": "ma", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correctas, "fb": fb, "points": puntos})


def matching(titulo, texto, pares, distractores, fb, puntos=4.0):
    REACTIVOS.append({"type": "matching", "title": titulo, "text": texto, "pairs": pares,
                      "distractors": distractores, "fb": fb, "points": puntos})


def dropdowns(titulo, texto, blancos, fb, puntos=4.0):
    REACTIVOS.append({"type": "dropdowns", "title": titulo, "text": texto, "blanks": blancos,
                      "fb": fb, "points": puntos})


def numerical(titulo, texto, respuesta, tolerancia, fb, puntos=3.0):
    REACTIVOS.append({"type": "numerical", "title": titulo, "text": texto, "answer": respuesta,
                      "tol": tolerancia, "fb": fb, "points": puntos})


def essay(titulo, texto, fb, puntos=7.0):
    REACTIVOS.append({"type": "essay", "title": titulo, "text": texto, "fb": fb, "points": puntos})


def _fb(correcta, porque, demas):
    items = "".join(f"<li>{d}</li>" for d in demas)
    return (f"<p><strong>Correcta: {correcta}</strong> {porque}</p>"
            f"<p><strong>Por qué no las demás:</strong></p><ul>{items}</ul>")


header(INSTRUCCIONES)

# Declaración de integridad (0 puntos, obligatoria para empezar).
REACTIVOS.append({
    "type": "mc", "title": "Declaración de integridad académica", "points": 0.0,
    "text": "<p>Declaro que resolveré este examen de forma individual, <strong>sin usar herramientas de inteligencia artificial</strong> "
            "ni ayuda de otras personas, y que las respuestas escritas son de mi autoría. Entiendo que incumplir esta declaración anula el examen.</p>",
    "choices": ["Sí, lo declaro y acepto estas condiciones."], "correct": 0,
    "fb": "<p>Reactivo sin valor. Sirve como registro de la declaración de cada alumno.</p>",
})

# ===========================================================================
# BLOQUE 1 · FUNDAMENTOS MOLECULARES Y ÓMICOS (30 pts)
# ===========================================================================
header("<h3>Bloque 1 · Fundamentos moleculares y ómicos (30 %)</h3>"
       "<p>10 reactivos de opción múltiple, 3 puntos cada uno. Elige la opción mejor justificada.</p>")

mc("E1-1 · Probar que una variante actúa en cis",
   "<p>Se quiere demostrar que el alelo −13910T aumenta la transcripción de <em>LCT</em> en el propio cromosoma que lo porta (efecto en <em>cis</em>) y no por un factor general del individuo. "
   "Se dispone de biopsias intestinales de adultos heterocigotos C/T que también son heterocigotos para un SNP sinónimo dentro del exón de <em>LCT</em>. ¿Qué medición lo demuestra mejor?</p>",
   ["Secuenciar el genoma completo de cada persona.",
    "Medir la expresión específica de alelo: comparar, dentro de la misma biopsia, cuánto mRNA de LCT proviene del cromosoma con T y cuánto del cromosoma con C, usando el SNP exónico como marcador.",
    "Medir la lactasa total en heces.",
    "Comparar la actividad de lactasa entre personas C/C y T/T de distintas familias."],
   1,
   _fb("expresión específica de alelo.", "Dentro de una misma célula ambos cromosomas comparten el mismo ambiente (factores de transcripción, dieta, edad); si el cromosoma con T produce más mRNA que el de C, la diferencia solo puede deberse a la secuencia en cis.",
       ["«Secuenciar el genoma»: describe las variantes, no mide su efecto en la expresión.",
        "«Lactasa en heces»: no es una medición válida de la expresión intestinal y no separa los alelos.",
        "«Comparar C/C y T/T»: muestra asociación entre personas, pero mezcla diferencias de edad, dieta, ascendencia y daño de mucosa; no aísla el efecto en cis."]))

mc("E1-2 · ¿Cuál variante preocupa más?",
   "<p>En el gen de una enzima metabólica se encuentran dos variantes en un paciente: (1) un missense que cambia un residuo de la superficie, poco conservado entre especies, Lys→Arg; "
   "(2) un cambio sinónimo en el último nucleótido de un exón, junto al sitio donador de splicing. ¿Cuál razonamiento es el más sólido?</p>",
   ["La 1 es más grave porque todo missense cambia la proteína y todo sinónimo es neutro.",
    "La 2 puede ser más dañina: aunque no cambia el aminoácido, puede alterar el reconocimiento del sitio de splicing y causar salto de exón; la 1 es un cambio conservador (ambos básicos) en un sitio poco conservado.",
    "Ambas son igual de graves porque las dos están en el mismo gen.",
    "Ninguna puede tener efecto porque ninguna es nonsense."],
   1,
   _fb("el contexto pesa más que la etiqueta.", "La clasificación por efecto en el aminoácido es solo el primer filtro; la posición (borde de exón), el tipo de cambio químico (Lys→Arg conserva la carga) y la conservación evolutiva cambian el pronóstico.",
       ["«Todo sinónimo es neutro»: ignora splicing, estabilidad del mRNA y uso de codones.",
        "«Mismo gen, misma gravedad»: el efecto depende de la posición y del tipo de cambio, no solo del gen.",
        "«Solo los nonsense tienen efecto»: missense y cambios de splicing también pueden ser patogénicos."]))

mc("E1-3 · Una CNV que el genotipado no ve",
   "<p>Un estudio genotipa el SNP más cercano al locus <em>AMY1</em> con una PCR de punto final y no encuentra asociación con la actividad de amilasa salival. "
   "Otro estudio en la misma población, con PCR digital, encuentra que el número de copias de <em>AMY1</em> (de 2 a 14) sí se asocia. ¿Cuál es la explicación más probable?</p>",
   ["El segundo estudio se equivocó porque usó una técnica más nueva.",
    "La variación relevante es el número de copias del gen; un ensayo diseñado para leer las bases de un SNP no cuantifica cuántas copias hay, así que no captura el efecto de dosis.",
    "La amilasa salival no depende del DNA.",
    "La PCR de punto final siempre detecta CNV si se corre un gel."],
   1,
   _fb("se midió el tipo de variante equivocado.", "La pregunta biológica (dosis génica) exige un método cuantitativo del número de copias (PCR digital o qPCR relativa, arreglos de CNV).",
       ["«Técnica más nueva = error»: la técnica correcta es la que mide la variable relevante.",
        "«No depende del DNA»: la asociación con el número de copias muestra lo contrario.",
        "«Punto final detecta CNV»: la PCR de punto final llega a una meseta y no es cuantitativa."]))

mc("E1-4 · Cómo identificar respondedores de verdad",
   "<p>Un grupo quiere clasificar a 40 personas como hiper o hiporrespondedoras del LDL a la grasa saturada. ¿Cuál diseño separa mejor la respuesta individual verdadera del ruido?</p>",
   ["Una sola medición de LDL después de 4 semanas de dieta alta en grasa saturada.",
    "Un ensayo cruzado: cada persona pasa por dieta control y dieta alta en grasa saturada en orden aleatorio, con lavado entre fases y mediciones repetidas de LDL en cada fase; idealmente repitiendo el reto.",
    "Preguntar a cada persona si siente que la grasa le sube el colesterol.",
    "Comparar a las personas de LDL más alto con las de LDL más bajo en una sola toma."],
   1,
   _fb("cruzado con mediciones repetidas.", "Cada persona es su propio control y las mediciones repetidas permiten estimar la variabilidad intraindividual; solo así una diferencia grande se interpreta como respuesta y no como ruido o regresión a la media.",
       ["«Una sola medición»: no hay comparación con la condición control de la misma persona.",
        "«Preguntar»: la percepción no mide el LDL.",
        "«Comparar extremos en una toma»: confunde nivel basal con respuesta a la dieta."]))

mc("E1-5 · Un AVI/AVI que percibe el amargo",
   "<p>Una estudiante con genotipo <em>TAS2R38</em> AVI/AVI califica el PROP como «muy amargo», con un puntaje similar al de compañeros PAV/PAV. ¿Cuál interpretación es la más rigurosa?</p>",
   ["El genotipado debe estar mal, porque AVI/AVI siempre es no catador.",
    "TAS2R38 explica gran parte de la variación en la percepción de PROP, pero no toda: influyen otros genes de receptores, la densidad de papilas fungiformes, la técnica de la prueba y factores de atención. Antes de dudar del genotipo, conviene repetir la prueba con controles.",
    "Los AVI/AVI son en realidad «supertasters».",
    "La percepción del amargo no tiene relación con TAS2R38."],
   1,
   _fb("un gen mayor no es el único determinante.", "Es un caso de penetrancia incompleta de un rasgo de gran efecto; la excepción obliga a revisar método y otros factores, no a negar la asociación.",
       ["«Genotipo mal»: es una posibilidad a verificar, no la conclusión automática.",
        "«AVI/AVI son supertasters»: invierte la relación promedio.",
        "«Sin relación»: la asociación TAS2R38–PROP es de las más robustas de la nutrigenética."]))

mc("E1-6 · Tamiz neonatal: PKU sí, lactasa no",
   "<p>¿Por qué se tamiza fenilcetonuria (<em>PAH</em>) en todos los recién nacidos, pero no se tamiza el genotipo de persistencia de lactasa?</p>",
   ["Porque la lactasa no tiene base genética.",
    "Porque PKU es una enfermedad de gran efecto con daño neurológico irreversible si no se trata desde las primeras semanas y con un tratamiento eficaz (restricción de fenilalanina); la no persistencia de lactasa es común, aparece después del destete y se maneja según síntomas.",
    "Porque la PKU es más frecuente que la no persistencia de lactasa.",
    "Porque el genotipo de lactasa no se puede determinar con PCR."],
   1,
   _fb("criterios de tamizaje: gravedad, ventana de intervención y tratamiento eficaz.", "Un tamiz poblacional se justifica cuando detectar antes cambia el desenlace de forma importante.",
       ["«Sin base genética»: la persistencia de lactasa tiene base genética clara.",
        "«PKU más frecuente»: es al revés; la no persistencia es el estado mayoritario en el mundo.",
        "«No se puede genotipar»: se genotipa fácilmente; el problema no es técnico."]))

mc("E1-7 · Del GWAS a la persona",
   "<p>En un GWAS de 500 000 personas, cada alelo A de <em>FTO</em> rs9939609 se asocia con +0.35 kg/m² de IMC (p = 10⁻⁸⁰). Una persona AA pregunta si su IMC alto «es culpa del gen». ¿Qué respuesta es más correcta?</p>",
   ["Sí: con un p tan pequeño, el gen explica su IMC.",
    "El p indica que la asociación es real en la población, pero el efecto por persona es pequeño (≈ 0.7 kg/m² en AA frente a TT); su IMC depende sobre todo de muchos otros genes y del ambiente, y el genotipo no predice bien el IMC de un individuo.",
    "No: si el efecto es pequeño, la asociación es falsa.",
    "Sí: los AA siempre tienen IMC mayor que los TT."],
   1,
   _fb("certeza estadística no es poder predictivo individual.", "Con muestras enormes, efectos diminutos dan p minúsculos; la utilidad clínica se mide con el tamaño del efecto y la capacidad de predicción, no con el p.",
       ["«p pequeño = explica su IMC»: confunde significancia con magnitud.",
        "«Efecto pequeño = asociación falsa»: un efecto puede ser pequeño y real.",
        "«Siempre mayor»: hay enorme superposición entre genotipos."]))

mc("E1-8 · MTHFR en un país que fortifica",
   "<p>En una población con fortificación obligatoria de harinas con ácido fólico, la diferencia de homocisteína entre personas <em>MTHFR</em> TT y CC es mucho menor que en una población sin fortificación. ¿Qué explica mejor este hallazgo?</p>",
   ["La fortificación cambió el genotipo de la población.",
    "Es una interacción gen–ambiente: con folato abundante, la enzima termolábil TT recibe suficiente sustrato y se estabiliza, así que el efecto del genotipo se atenúa; con folato bajo, el efecto se hace evidente.",
    "Las personas TT dejaron de absorber ácido fólico.",
    "La homocisteína no depende del folato."],
   1,
   _fb("el ambiente modifica el efecto del genotipo.", "El mismo genotipo tiene distinta expresión fenotípica según el estado de folato (y de riboflavina): es el ejemplo clásico de interacción gen–nutriente.",
       ["«Cambió el genotipo»: la dieta no modifica la secuencia.",
        "«Dejaron de absorber»: no hay evidencia de ese mecanismo; el folato aumenta.",
        "«No depende del folato»: el folato es el donador de metilo para remetilar la homocisteína."]))

mc("E1-9 · ALDH2 como experimento natural",
   "<p>Varios estudios usan el genotipo <em>ALDH2</em> rs671 para estimar el efecto causal del alcohol sobre la presión arterial: los portadores de ALDH2*2 beben menos por el rubor y tienen presión más baja. ¿Por qué este diseño (aleatorización mendeliana) fortalece la inferencia causal?</p>",
   ["Porque el genotipo se asigna al azar en la concepción, antes de los hábitos; así no está confundido por nivel socioeconómico o tabaco, y si el genotipo que reduce el consumo también reduce la presión, apoya que el alcohol eleva la presión.",
    "Porque ALDH2 controla directamente la presión arterial.",
    "Porque elimina la necesidad de medir el consumo de alcohol.",
    "Porque demuestra que el acetaldehído baja la presión."],
   0,
   _fb("el genotipo actúa como una aleatorización natural.", "La lógica requiere que el gen afecte la presión solo a través del consumo de alcohol; esa suposición debe discutirse, pero el diseño evita la confusión típica de los estudios observacionales.",
       ["«ALDH2 controla la presión»: si así fuera, se violaría el supuesto central del diseño.",
        "«No hay que medir el alcohol»: hay que verificar que el genotipo sí cambia el consumo.",
        "«El acetaldehído baja la presión»: la menor presión se explica por beber menos."]))

mc("E1-10 · Genotipo o fenotipo metabólico",
   "<p>Para individualizar la recomendación de café, ¿qué indicador refleja mejor la actividad real de CYP1A2 de una persona: su genotipo rs762551 o el cociente paraxantina/cafeína en plasma 4–6 h después de una dosis estándar?</p>",
   ["El genotipo, porque no cambia con el tiempo.",
    "El cociente metabólico, porque integra el genotipo con factores que inducen o inhiben a CYP1A2 (tabaquismo, anticonceptivos orales, algunos fármacos, embarazo); el genotipo solo predice una parte de esa actividad.",
    "Ninguno, porque la cafeína no se metaboliza en el hígado.",
    "Ambos dan exactamente la misma información."],
   1,
   _fb("el fenotipo metabólico integra genes y ambiente.", "El tabaco induce fuertemente a CYP1A2 y los anticonceptivos orales la inhiben; dos personas con el mismo genotipo pueden metabolizar la cafeína muy distinto.",
       ["«No cambia con el tiempo»: es estable, pero no captura inducción ni inhibición.",
        "«No se metaboliza en el hígado»: CYP1A2 hepática hace la mayor parte de su metabolismo.",
        "«Misma información»: el genotipo es una causa parcial; el cociente es el resultado medido."]))

# ===========================================================================
# BLOQUE 2 · CASOS CLÍNICOS (30 pts)
# ===========================================================================
header("<h3>Bloque 2 · Casos clínicos y diagnóstico nutrigenético (30 %)</h3>"
       "<p>4 casos de opción múltiple (3 pts c/u), 1 de selección múltiple (4 pts) y 2 casos de respuesta extendida (7 pts c/u).</p>")

mc("E2-1 · «Es cultural, no genético»",
   "<p>Un chef afirma que el rechazo al cilantro por su sabor «a jabón» es puramente cultural. En una cohorte, una variante cercana al receptor olfatorio <em>OR6A2</em> se asocia con esa percepción, "
   "pero explica solo una parte pequeña de la variación, y la percepción también cambia con la exposición repetida y con el machacado de las hojas. ¿Qué conclusión es la más equilibrada?</p>",
   ["El chef tiene razón: si el efecto genético es pequeño, no existe.",
    "Es un rasgo multifactorial: hay un componente genético real (receptor que detecta aldehídos del cilantro) y componentes ambientales (exposición, preparación que modifica los aldehídos); ninguno lo explica solo.",
    "Es 100 % genético: quien tiene la variante nunca podrá tolerar el cilantro.",
    "La variante cambia la composición química del cilantro."],
   1,
   _fb("genes y ambiente contribuyen.", "Los datos muestran ambos componentes; rechazar uno por la existencia del otro es un falso dilema.",
       ["«Efecto pequeño = no existe»: una contribución modesta sigue siendo real.",
        "«100 % genético»: los datos de exposición y preparación lo contradicen.",
        "«Cambia la química del cilantro»: la variante está en quien percibe, no en la planta."]))

mc("E2-2 · Cafeína antes de competir",
   "<p>Una ciclista toma 6 mg/kg de cafeína antes de cada prueba porque «todos los estudios muestran que mejora el rendimiento». Su genotipo <em>CYP1A2</em> rs762551 es C/C. "
   "En un ensayo con atletas, la cafeína mejoró el tiempo en A/A, tuvo poco efecto en A/C y lo empeoró en C/C. ¿Qué recomendación es la más defendible?</p>",
   ["Mantener la dosis: el promedio de la literatura es positivo.",
    "Explicar que el efecto ergogénico promedio puede no aplicarse a su genotipo; probar de forma controlada (con y sin cafeína, en orden aleatorio) dosis menores o ninguna, y vigilar efectos adversos y sueño.",
    "Duplicar la dosis para compensar el metabolismo lento.",
    "Prohibirle la cafeína para siempre por riesgo cardiaco inmediato."],
   1,
   _fb("individualizar con evidencia y prueba controlada.", "El promedio de un grupo esconde respuestas opuestas por genotipo; la mejor decisión combina la evidencia por genotipo con una prueba individual controlada.",
       ["«Mantener la dosis»: ignora que el promedio no representa a todos los genotipos.",
        "«Duplicar»: en metabolizadores lentos aumenta la exposición y los efectos adversos.",
        "«Prohibir para siempre»: exagera; la recomendación es ajustar y evaluar."]))

mc("E2-3 · C/C pero toma leche sin problema",
   "<p>Una mujer mexicana de ascendencia indígena tiene genotipo <em>MCM6</em> −13910 C/C (no persistencia según el marcador europeo) y refiere tomar un vaso de leche al día sin síntomas. ¿Cuál explicación es la menos probable?</p>",
   ["Puede portar otra variante de persistencia no incluida en la prueba, porque −13910T es característica de poblaciones europeas.",
    "Puede tener hipolactasia y aun así tolerar una dosis moderada de lactosa, gracias a la adaptación de su microbiota colónica y a que la toma con alimentos.",
    "Puede tener malabsorción sin intolerancia: la lactosa no se absorbe por completo, pero no le causa síntomas con esa dosis.",
    "El genotipo C/C le causa alergia a la leche que todavía no se ha manifestado."],
   3,
   _fb("la «alergia» es la explicación menos probable.", "La alergia a la leche es una reacción inmunológica a sus proteínas y no tiene relación con el genotipo de lactasa; las otras tres opciones son explicaciones plausibles.",
       ["Otra variante de persistencia: es plausible; hay variantes distintas en poblaciones africanas, de Medio Oriente y americanas, y los paneles comerciales suelen usar solo −13910.",
        "Tolerancia con hipolactasia: es plausible; la dosis, la comida y la microbiota modulan los síntomas.",
        "Malabsorción sin intolerancia: es plausible; son niveles distintos (enzima, absorción, síntomas)."]))

mc("E2-4 · Rubor con ALDH2 «normal»",
   "<p>Un paciente presenta rubor, palpitaciones y náuseas al beber una cerveza desde hace una semana. Su genotipo <em>ALDH2</em> rs671 es G/G (*1/*1). Hace 10 días inició un antibiótico para una infección dental. ¿Qué haces primero?</p>",
   ["Repetir el genotipado, porque debe ser ALDH2*2.",
    "Revisar el fármaco: algunos medicamentos (p. ej., metronidazol) producen una reacción tipo disulfiram que inhibe el metabolismo del acetaldehído; un genotipo normal no excluye causas adquiridas.",
    "Concluir que desarrolló una mutación nueva en ALDH2.",
    "Indicar que beba más para generar tolerancia."],
   1,
   _fb("buscar la causa adquirida.", "El cuadro aparece de forma aguda y coincide con el inicio del antibiótico; el genotipo describe la predisposición heredada, no excluye inhibiciones farmacológicas.",
       ["«Repetir el genotipo»: el inicio reciente apunta a otra causa antes que a un error de laboratorio.",
        "«Mutación nueva»: una mutación germinal no aparece en una semana.",
        "«Beber más»: aumenta la exposición al acetaldehído y es peligroso con el fármaco."]))

ma("E2-5 · Evaluar un reporte comercial",
   "<p>Un reporte nutrigenético de venta directa al consumidor afirma lo siguiente. Selecciona las afirmaciones que <strong>están respaldadas</strong> por la evidencia vista en el curso.</p>",
   ["«Por su genotipo APOE ε4, su LDL tiende a responder más a la grasa saturada y al colesterol dietario.»",
    "«Por su genotipo FTO AA, ninguna dieta le funcionará para perder peso.»",
    "«Por su genotipo ALDH2*1/*2, el alcohol le genera más acetaldehído en sangre y saliva, y beber se asocia con mayor riesgo de cáncer de esófago.»",
    "«Por su genotipo TAS2R38 PAV/PAV, es probable que perciba más amargas las crucíferas.»",
    "«Por su genotipo MTHFR TT, debe evitar todo alimento con ácido fólico.»"],
   [0, 2, 3],
   "<p><strong>Por qué son correctas:</strong> APOE ε4 se asocia con mayor respuesta del LDL a la grasa y al colesterol dietarios; ALDH2*2 acumula acetaldehído y aumenta el riesgo de cáncer de esófago al beber; PAV se asocia con mayor percepción del amargor de los glucosinolatos.</p>"
   "<p><strong>Por qué no las demás:</strong> los portadores de FTO AA responden a las intervenciones de forma similar a los TT; y en MTHFR TT el folato es justamente lo que atenúa el efecto del genotipo.</p>")

essay("E2-6 · Caso: intolerancia de inicio reciente",
      "<p>Hombre de 31 años que siempre tomó leche sin molestias. Hace 6 semanas tuvo una gastroenteritis por rotavirus; desde entonces presenta distensión y diarrea con cualquier lácteo. Resultados:</p>"
      + _tabla(["Estudio", "Resultado"],
               [("Genotipo <em>MCM6</em> −13910", "T/T"),
                ("Prueba de H₂ espirado (25 g de lactosa)", "Aumento de 46 ppm (positiva ≥ 20), con síntomas"),
                ("Anticuerpos para enfermedad celíaca", "Negativos"),
                ("Coprocultivo actual", "Negativo")])
      + "<p>a) ¿Cómo es posible que un T/T tenga malabsorción e intolerancia? Distingue hipolactasia primaria y secundaria. "
        "b) Explica qué dice y qué no dice su genotipo sobre la expresión de LCT. "
        "c) ¿Qué pronóstico esperas y por qué? "
        "d) Propón un manejo nutricional temporal y un criterio para reintroducir lácteos. "
        "e) ¿Qué error cometería alguien que interpretara solo el genotipo?</p>",
      "<p><strong>Respuesta modelo.</strong> a) Tiene hipolactasia secundaria: la gastroenteritis dañó el epitelio de las vellosidades, donde está la lactasa en el borde en cepillo; aunque su genotipo mantiene la transcripción de LCT, los enterocitos dañados expresan menos enzima. La primaria se debe a la caída programada de la expresión tras el destete (genotipo de no persistencia). "
      "b) T/T indica que el potenciador de MCM6 sostiene la transcripción de LCT en el adulto (persistencia); no protege contra la pérdida de enterocitos maduros ni garantiza actividad si la mucosa está dañada. "
      "c) Buen pronóstico: al regenerarse el epitelio (semanas a pocos meses), la actividad de lactasa debería recuperarse, porque la causa es transitoria. "
      "d) Reducir temporalmente la lactosa (deslactosados, yogur, quesos madurados, lactasa exógena), mantener calcio y proteína, y reintroducir en dosis crecientes al desaparecer los síntomas; si persisten más de 2–3 meses, repetir la prueba de H₂ y buscar otras causas. "
      "e) Concluir que «no puede ser intolerante» por ser T/T y descartar los síntomas, o etiquetarlo de forma permanente; el genotipo informa la causa primaria, no el estado actual de la mucosa.</p>"
      "<p><strong>Rúbrica (7 pts):</strong> 2 primaria vs. secundaria con mecanismo; 1.5 qué dice y qué no dice el genotipo; 1 pronóstico justificado; 1.5 manejo con criterio de reintroducción; 1 error de interpretación.</p>")

essay("E2-7 · Caso: un hallazgo que no se buscó",
      "<p>Mujer de 38 años, ascendencia coreana, IMC 29, LDL 171 mg/dL. Quiere un plan de alimentación «según sus genes». Su reporte:</p>"
      + _tabla(["Gen (variante)", "Genotipo"],
               [("<em>APOE</em>", "ε4/ε4"),
                ("<em>ALDH2</em> rs671", "*1/*2"),
                ("<em>CYP1A2</em> rs762551", "C/C"),
                ("<em>TAS2R38</em>", "PAV/PAV"),
                ("<em>FTO</em> rs9939609", "A/A")])
      + "<p>a) Propón tres recomendaciones nutricionales prioritarias y justifícalas con un mecanismo. "
        "b) El genotipo APOE ε4/ε4 también se asocia con un riesgo mucho mayor de enfermedad de Alzheimer, y ella no pidió esa información. ¿Qué dilema ético plantea y cómo lo manejarías? "
        "c) Su gusto por las verduras es bajo: ¿cómo usarías el resultado de TAS2R38 sin convertirlo en una excusa? "
        "d) Señala dos limitaciones de basar el plan solo en este reporte.</p>",
      "<p><strong>Respuesta modelo.</strong> a) 1) Reducir grasa saturada y colesterol dietario y aumentar fibra soluble: en ε4 el LDL responde más a la dieta y su LDL ya está alto. "
      "2) Evitar o limitar mucho el alcohol: con ALDH2*2 acumula acetaldehído (carcinógeno) y en ε4 el alcohol se asocia con LDL más alto. "
      "3) Moderar la cafeína (1–2 tazas): metabolizadora lenta (C/C). FTO A/A: actividad física regular, que atenúa su efecto y ayuda al peso. "
      "b) Es un hallazgo incidental de alto impacto, sin tratamiento preventivo específico y con carga emocional; respeta su derecho a decidir si quiere saberlo (derecho a no saber). Manejo: no revelarlo de forma casual, ofrecer asesoría genética antes de comunicarlo, explicar que es riesgo y no diagnóstico, y cuidar la confidencialidad. "
      "c) Explicar que percibe más el amargor de las crucíferas; usar preparaciones que lo reduzcan, combinarlas con grasas saludables o sabores que lo compensen, exposición repetida y otras verduras menos amargas; el genotipo orienta la estrategia, no justifica omitir verduras. "
      "d) Las variantes explican una fracción pequeña del riesgo; la evidencia de dietas guiadas por genotipo frente a una dieta saludable es limitada; muchas asociaciones vienen de poblaciones europeas y pueden no aplicar igual a su ascendencia; el plan debe integrar historia clínica, hábitos y laboratorio.</p>"
      "<p><strong>Rúbrica (7 pts):</strong> 2.5 tres recomendaciones priorizadas con mecanismo; 2 manejo ético del hallazgo incidental; 1 uso constructivo de TAS2R38; 1.5 dos limitaciones pertinentes.</p>")

# ===========================================================================
# BLOQUE 3 · BIOINFORMÁTICA, PCR IN SILICO Y GELES (20 pts)
# ===========================================================================
header("<h3>Bloque 3 · Bioinformática, PCR <em>in silico</em> e interpretación de geles (20 %)</h3>"
       "<p>6 reactivos. Ten a mano la tabla del código genético.</p>")

mc("E3-1 · Leer la variante de ALDH2",
   "<p>Fragmento <strong>ilustrativo</strong> de la secuencia codificante de <em>ALDH2</em>, en marco de lectura, con el codón 504 entre corchetes:</p>"
   f"<p>Alelo *1: {_seq('5′-… GCA [GAA] TAC …-3′')}<br>Alelo *2: {_seq('5′-… GCA [AAA] TAC …-3′')}</p>"
   "<p>¿Qué cambio ocurre y qué consecuencia funcional es coherente con lo que sabes de ALDH2*2?</p>",
   ["G→A en la primera posición; Glu→Lys (missense); la subunidad mutante reduce la actividad del tetrámero completo, por eso un heterocigoto ya acumula acetaldehído.",
    "G→A en la primera posición; Glu→Glu (sinónimo); no hay consecuencia funcional.",
    "G→A que crea un codón de paro; la enzima se trunca.",
    "G→A en la tercera posición; Glu→Asp (missense conservador) sin efecto."],
   0,
   _fb("GAA (Glu) → AAA (Lys): missense con efecto dominante negativo.", "El cambio de un residuo ácido por uno básico altera la estructura; como ALDH2 funciona como tetrámero, las subunidades *2 contaminan los tetrámeros mixtos.",
       ["«Sinónimo»: AAA codifica lisina, no glutamato.",
        "«Codón de paro»: AAA no es paro (TAA, TAG, TGA).",
        "«Tercera posición, Glu→Asp»: el cambio está en la primera base, y Asp sería GAT o GAC."]))

dropdowns("E3-2 · Clasificar variantes en una secuencia",
          "<p>Marco de lectura abierto ilustrativo (posiciones contadas desde la A del ATG):</p>"
          f"<p>{_seq('5′-ATG AAA CCG TAC TGT GGA CTT TAA-3′')}<br>Proteína: Met-Lys-Pro-Tyr-Cys-Gly-Leu-Stop</p>"
          "<p>c.6A&gt;G → [w1]<br>c.12C&gt;G → [w2]<br>c.14G&gt;A → [w3]<br>c.20delT → [w4]<br>c.7_9dupCCG → [w5]</p>"
          "<p>De las cinco, la que con mayor probabilidad elimina la función de la proteína desde ese punto es: [w6]</p>",
          {"w1": (["sinónima (Lys→Lys)", "missense (Lys→Arg)", "nonsense", "indel con corrimiento del marco"], 0),
           "w2": (["nonsense (Tyr→Stop)", "sinónima (Tyr→Tyr)", "missense (Tyr→Cys)", "indel sin corrimiento del marco"], 0),
           "w3": (["missense (Cys→Tyr)", "sinónima (Cys→Cys)", "nonsense", "missense (Cys→Trp)"], 0),
           "w4": (["indel con corrimiento del marco", "indel sin corrimiento del marco", "sinónima", "CNV"], 0),
           "w5": (["inserción sin corrimiento del marco (Pro adicional)", "indel con corrimiento del marco", "nonsense", "sinónima"], 0),
           "w6": (["c.12C>G", "c.6A>G", "c.7_9dupCCG", "c.14G>A"], 0)},
          "<p><strong>Clave:</strong> c.6A&gt;G: AAA→AAG, ambos Lys (sinónima). c.12C&gt;G: TAC→TAG, paro (nonsense). c.14G&gt;A: TGT→TAT, Cys→Tyr (missense). "
          "c.20delT: se pierde 1 nt de CTT y se corre el marco desde el codón 7. c.7_9dupCCG: se duplica un codón completo (una Pro más) sin correr el marco. "
          "La de mayor pérdida de función es la nonsense temprana (codón 4); el frameshift de c.20delT ocurre casi al final del marco.</p>"
          "<p><strong>Distractores:</strong> Lys→Arg requeriría AGA/AGG; Tyr→Cys requeriría TGC/TGT; Cys→Trp requeriría TGG; una CNV implica un segmento grande, no 1 nt.</p>")

GEL = (
    "<p>Gel de agarosa al 2 % con productos de PCR de PV92 (alelo + con Alu ≈ 731 pb; alelo − sin Alu ≈ 416 pb). "
    "M = marcador de 100 pb. «▬» indica banda; «tenue», banda débil; «barrido», mancha continua sin bandas definidas.</p>"
    + _tabla(["Tamaño (pb)", "M", "Carril 1", "Carril 2", "Carril 3", "Carril 4", "Carril 5", "Carril 6 (sin DNA)"],
             [("1000", "▬", "", "", "", "barrido", "", ""),
              ("≈ 730", "▬ (700)", "", "▬", "▬ tenue", "barrido", "▬", ""),
              ("500", "▬", "", "", "", "barrido", "", ""),
              ("≈ 420", "▬ (400)", "▬", "", "▬", "barrido", "▬", "▬"),
              ("100", "▬", "", "", "", "barrido", "", "")])
)

matching("E3-3 · Lectura de gel: Alu PV92",
         GEL + "<p>Asigna la interpretación de cada carril.</p>",
         [("Carril 1", "Homocigoto −/− (sin inserción)"),
          ("Carril 2", "Homocigoto +/+ (inserción en ambos cromosomas)"),
          ("Carril 3", "Heterocigoto +/−; la banda larga se ve débil por amplificación preferencial del alelo corto"),
          ("Carril 4", "DNA degradado o exceso de templado: repetir extracción o diluir; no se genotipa"),
          ("Carril 5", "Heterocigoto +/−"),
          ("Carril 6", "Contaminación: el control sin DNA amplificó; los resultados de toda la corrida no son confiables")],
         ["Homocigoto +/+ con una tercera inserción"],
         "<p><strong>Clave:</strong> 1 = −/− (solo 416); 2 = +/+ (solo 731); 3 = +/− aunque la banda de 731 sea débil: el alelo corto se amplifica con ventaja, pero la presencia de ambas bandas define al heterocigoto; "
         "4 = barrido sin bandas definidas: DNA degradado o demasiado templado; 5 = +/−; 6 = el control sin DNA debe salir limpio, y una banda de 416 indica contaminación con DNA o productos de PCR: se invalida la corrida. "
         "Pensamiento crítico clave: el carril 6 cambia la interpretación de todos los demás; los genotipos 1, 3 y 5 podrían estar contaminados.</p>")

mc("E3-4 · Elegir y evaluar la extracción",
   "<p>Un proyecto colectará 300 hisopados bucales en escuelas y genotipará varios SNPs. El laboratorio tiene campana de extracción limitada. "
   "En una prueba piloto, el DNA extraído por salting-out dio A<sub>260/280</sub> = 1.52. ¿Cuál es la mejor decisión?</p>",
   ["Cambiar a fenol-cloroformo para todas las muestras, porque da el DNA más puro.",
    "La relación 1.52 sugiere proteína residual: ajustar la precipitación de proteínas (más sal o centrifugado, sin arrastrar la interfase) o usar columnas de sílice o perlas SPRI, que escalan bien, no requieren solventes orgánicos y dan DNA apto para PCR.",
    "Ignorar el valor: cualquier DNA sirve para PCR.",
    "Aumentar el volumen de DNA en la PCR para compensar la impureza."],
   1,
   _fb("diagnóstico de pureza más elección del método según el contexto.", "Para muchas muestras y sin campana, los métodos de fase sólida (sílice o SPRI) son más seguros y reproducibles; el valor bajo de 260/280 señala proteína y se corrige en el paso de precipitación.",
       ["«Fenol-cloroformo»: es tóxico, requiere campana y es lento para 300 muestras; además puede arrastrar fenol.",
        "«Cualquier DNA sirve»: los contaminantes pueden inhibir la polimerasa.",
        "«Más DNA en la PCR»: también aumenta el inhibidor y puede empeorar el resultado."]))

mc("E3-5 · Lo que dice el genoma de referencia",
   "<p>Al correr los cebadores de PV92 en UCSC In-Silico PCR (GRCh38) se obtiene un solo producto de 416 pb. Un alumno concluye que «la población humana es −/− para PV92». ¿Cuál es el error de razonamiento?</p>",
   ["Ninguno: UCSC refleja a toda la población.",
    "El genoma de referencia es una secuencia compuesta que representa un solo alelo en cada sitio; que tenga el alelo − no informa la frecuencia poblacional, que se obtiene genotipando muestras o consultando bases poblacionales.",
    "UCSC In-Silico PCR solo funciona con mRNA.",
    "El producto de 416 pb corresponde al alelo +."],
   1,
   _fb("la referencia no es una población.", "La herramienta predice el producto sobre una secuencia de referencia; la variación entre personas se estudia genotipando o con bases de datos poblacionales.",
       ["«Refleja a toda la población»: es exactamente el error.",
        "«Solo mRNA»: UCSC In-Silico PCR trabaja sobre el genoma ensamblado.",
        "«416 = alelo +»: sin el Alu el producto es de 416 pb; con él, unos 300 pb más."]))

mc("E3-6 · Interpretar una entrada del GWAS Catalog",
   "<p>En el GWAS Catalog, una variante intergénica aparece asociada al consumo de café con «mapped genes: <em>CYP1A1</em> – <em>CYP1A2</em>», OR por alelo = 1.05 y p = 2 × 10⁻³⁰, en una muestra de 120 000 europeos. "
   "¿Qué conclusión es la más rigurosa?</p>",
   ["La variante causa que las personas tomen café.",
    "Existe una asociación robusta pero de efecto pequeño; la variante probablemente marca una región regulatoria del locus CYP1A1–CYP1A2 (metabolismo de cafeína), y su efecto y frecuencia podrían diferir en poblaciones no europeas.",
    "Como el OR es casi 1, la asociación es falsa.",
    "Los genes asignados son siempre los genes efectores."],
   1,
   _fb("robusta, pequeña, plausible y dependiente de la población.", "El p refleja certeza estadística por el tamaño de muestra; el OR indica efecto pequeño; la ubicación intergénica sugiere regulación; y la transferibilidad entre poblaciones debe verificarse.",
       ["«Causa el consumo»: una asociación no prueba causalidad ni mecanismo.",
        "«OR ≈ 1 = falsa»: un efecto pequeño puede ser real, y aquí es muy significativo.",
        "«Gen asignado = efector»: es la etiqueta de proximidad, no una demostración funcional."]))

# ===========================================================================
# BLOQUE 4 · CÁLCULO Y TROUBLESHOOTING (20 pts)
# ===========================================================================
header("<h3>Bloque 4 · Cálculo químico-enzimático, capacidad antioxidante y troubleshooting (20 %)</h3>"
       "<p>3 cálculos, 2 de opción múltiple (2.5 pts c/u) y 1 de selección múltiple (5 pts). Escribe solo el número en los cálculos.</p>"
       "<p>Fórmulas: % inhibición = [A<sub>control</sub> − (A<sub>muestra</sub> − A<sub>blanco</sub>)] / A<sub>control</sub> × 100. "
       "Catalasa: U/mL = (ΔA<sub>240</sub>/min) / (43.6 × l) × 1000 × (V<sub>total</sub>/V<sub>muestra</sub>).</p>")

numerical("E4-1 · Inhibición de DPPH con blanco",
          "<p>Extracto de flor de cempasúchil a 40 µg/mL:</p>"
          + _tabla(["Lectura", "A<sub>517</sub>"],
                   [("Control (DPPH + metanol)", "0.874"), ("Muestra + DPPH", "0.521"), ("Blanco de muestra (extracto sin DPPH)", "0.044")])
          + "<p>Calcula el porcentaje de inhibición (una cifra decimal).</p>",
          45.4, 0.5,
          "<p>A corregida = 0.521 − 0.044 = 0.477. % = (0.874 − 0.477)/0.874 × 100 = <strong>45.4 %</strong>. Sin restar el blanco saldría 40.4 %.</p>")

numerical("E4-2 · IC<sub>50</sub> con tabla de absorbancias",
          "<p>Extracto de cáscara de tuna roja. A<sub>517</sub> del control (DPPH + metanol) = 0.912.</p>"
          + _tabla(["µg/mL", "A muestra + DPPH", "A blanco de muestra"],
                   [("5", "0.756", "0.008"), ("15", "0.553", "0.015"), ("30", "0.374", "0.027"), ("60", "0.231", "0.049")])
          + "<p>Calcula el % de inhibición de cada concentración (restando el blanco) y estima la IC<sub>50</sub> por interpolación lineal entre los dos puntos que rodean al 50 % "
            "(µg/mL, una cifra decimal).</p>",
          21.4, 0.5,
          "<p>% corregidos: 5 → 18.0; 15 → 41.0; 30 → 62.0; 60 → 80.0. El 50 % está entre 15 y 30 µg/mL. "
          "IC<sub>50</sub> = 15 + (50 − 41.0)/(62.0 − 41.0) × 15 = <strong>21.4 µg/mL</strong>. Sin restar el blanco se obtendría ≈ 23.1 µg/mL.</p>",
          puntos=4.0)

numerical("E4-3 · Actividad específica de catalasa",
          "<p>Homogenado de riñón: ΔA<sub>240</sub>/min = 0.0327 (tramo inicial), cubeta de cuarzo de 1 cm, volumen total 3.0 mL, volumen de muestra 0.10 mL, proteína 1.5 mg/mL. "
          "ε<sub>240</sub>(H₂O₂) = 43.6 M⁻¹ cm⁻¹; 1 U = 1 µmol de H₂O₂ por minuto. Calcula la actividad en U/mg de proteína.</p>",
          15.0, 0.3,
          "<p>U/mL = 0.0327/43.6 × 1000 × (3.0/0.10) = 0.00075 × 1000 × 30 = 22.5 U/mL. Actividad específica = 22.5/1.5 = <strong>15.0 U/mg</strong>.</p>")

mc("E4-4 · Comparar IC<sub>50</sub> entre laboratorios",
   "<p>Tu extracto de jamaica dio IC<sub>50</sub> = 35 µg/mL con DPPH 0.1 mM y 30 min de reacción. Un artículo reporta IC<sub>50</sub> = 12 µg/mL para jamaica usando DPPH 0.05 mM y 60 min. "
   "¿Puedes concluir que tu extracto es casi tres veces menos potente?</p>",
   ["Sí: la IC<sub>50</sub> es una propiedad fija del extracto.",
    "No directamente: la IC<sub>50</sub> depende de la concentración de DPPH (con menos radical se necesita menos extracto) y del tiempo de reacción; para comparar hay que usar las mismas condiciones o un patrón común (p. ej., expresar en equivalentes de Trolox medido en paralelo).",
    "No, porque la jamaica no tiene antioxidantes.",
    "Sí, porque el artículo fue publicado y tu experimento no."],
   1,
   _fb("la IC₅₀ depende de las condiciones del ensayo.", "Menos DPPH y más tiempo favorecen una IC₅₀ menor; un patrón medido en paralelo permite comparar entre laboratorios.",
       ["«Propiedad fija»: depende de concentración del radical, disolvente y tiempo.",
        "«Sin antioxidantes»: la jamaica es rica en antocianinas y otros polifenoles.",
        "«Publicado = correcto»: la publicación no elimina la diferencia de condiciones."]),
   puntos=2.5)

mc("E4-5 · Una lectura fuera de la curva",
   "<p>En FRAP, la curva de Trolox va de 0 a 500 µM (A<sub>593</sub> de 0.01 a 1.30). Un extracto sin diluir da A<sub>593</sub> = 2.45. Un compañero extrapola la recta y reporta 940 µM. ¿Qué es lo correcto?</p>",
   ["Aceptar el valor: la recta se puede extender indefinidamente.",
    "Diluir el extracto (p. ej., 1:5), volver a leer para que caiga dentro de la curva y multiplicar por el factor de dilución; a absorbancias tan altas la respuesta deja de ser lineal.",
    "Reportar 500 µM, el máximo de la curva.",
    "Restar el blanco de reactivo y reportar el resultado así."],
   1,
   _fb("diluir y repetir, nunca extrapolar.", "Fuera del intervalo calibrado no se sabe si la relación sigue siendo lineal, y a absorbancias altas casi nunca lo es.",
       ["«Extender la recta»: supone una linealidad que no se verificó.",
        "«Reportar 500 µM»: subestima la muestra; solo indica que supera el patrón más alto.",
        "«Restar el blanco»: es necesario, pero no resuelve que la lectura esté fuera de la curva."]),
   puntos=2.5)

ma("E4-6 · Integrar los ensayos de un experimento",
   "<p>Ratas con dieta alta en fructosa, con o sin un extracto de chile ancho, frente a un control:</p>"
   + _tabla(["Marcador", "Fructosa", "Fructosa + extracto"],
            [("SOD hepática (U/mg)", "↑ 40 %", "↑ 45 %"),
             ("Catalasa hepática (U/mg)", "↓ 35 %", "≈ control"),
             ("TBARS (MDA)", "↑ 70 %", "↑ 15 %"),
             ("TAC sérica", "↑ 25 %", "↑ 28 %"),
             ("Ácido úrico sérico", "↑ 50 %", "↑ 48 %")])
   + "<p>Selecciona las interpretaciones bien sustentadas.</p>",
   ["Con fructosa sola hay un desbalance: más H₂O₂ producido (SOD alta) que eliminado (catalasa baja), coherente con más peroxidación (TBARS).",
    "El extracto recuperó la catalasa y redujo la peroxidación, lo que sugiere un efecto protector; un mecanismo posible es la inducción de enzimas antioxidantes (p. ej., vía Nrf2).",
    "El aumento de TAC en ambos grupos demuestra que la fructosa es antioxidante.",
    "Como la TAC sube igual en ambos grupos y el ácido úrico también, la TAC no sirve aquí para distinguir el efecto del extracto.",
    "Como la SOD está alta en ambos grupos, el extracto no tuvo ningún efecto."],
   [0, 1, 3],
   "<p><strong>Por qué son correctas:</strong> el patrón de la fructosa sola es de desbalance con daño; con extracto, la catalasa se normaliza y las TBARS bajan casi a control; y la TAC se mueve con el ácido úrico (la fructosa lo eleva), así que no discrimina entre grupos.</p>"
   "<p><strong>Por qué no las demás:</strong> la TAC alta se explica por urato, no por un efecto antioxidante de la fructosa; y juzgar el extracto solo por la SOD ignora la recuperación de la catalasa y la caída de las TBARS.</p>",
   puntos=5.0)


def _barajar():
    """Baraja las opciones de mc/ma con semilla fija para que la letra correcta no sea siempre la misma."""
    import random
    for r in REACTIVOS:
        if r["type"] not in ("mc", "ma") or len(r["choices"]) < 2:
            continue
        rng = random.Random(r["title"] + "0")  # semilla elegida para repartir A–D por igual
        orden = list(range(len(r["choices"])))
        rng.shuffle(orden)
        r["choices"] = [r["choices"][i] for i in orden]
        if r["type"] == "mc":
            r["correct"] = orden.index(r["correct"])
        else:
            r["correct"] = sorted(orden.index(i) for i in r["correct"])


_barajar()
