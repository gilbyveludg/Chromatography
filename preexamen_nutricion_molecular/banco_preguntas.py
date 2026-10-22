# -*- coding: utf-8 -*-
"""Banco de reactivos del preexamen de Nutrición Molecular (Otoño 2026).

Unidades cubiertas:
  I.   Polimorfismos y nutrigenética (Dry Lab 1: PCR in silico, PCR-RFLP)
  II.  Estrés oxidativo y antioxidantes (DPPH, TAC/FRAP, catalasa, SOD, Nrf2)
  III. Epigenética y nutrición (metilación, ciclo de un carbono, histonas, miRNAs)

Cada reactivo es un dict; `generar_qti.py` lo convierte a QTI 1.2 para Canvas.
Los casos y valores son distintos a los ejemplos vistos en clase.
"""

TITULO = "Preexamen · Nutrición Molecular (Unidades I–III)"

DESCRIPCION = """
<p><strong>Preexamen de práctica.</strong> Está pensado para resolverse en <strong>3 horas</strong>, igual que el examen.
Cubre las unidades vistas hasta ahora:</p>
<ol>
<li>Polimorfismos y nutrigenética (Dry Lab 1: PCR <em>in silico</em>, PCR-RFLP, frecuencias alélicas).</li>
<li>Estrés oxidativo y antioxidantes (DPPH, TAC/FRAP, catalasa, SOD, Nrf2).</li>
<li>Epigenética y nutrición (metilación del DNA, ciclo de un carbono, histonas, miRNAs, evidencia humana).</li>
</ol>
<p>Casi ninguna pregunta se responde de memoria: piden interpretar datos, detectar errores y justificar con el mecanismo.
Al enviar verás la retroalimentación de cada reactivo; léela aunque hayas acertado.</p>
"""

# Distribución sugerida del tiempo (minutos), se muestra en las instrucciones.
TIEMPOS = [
    ("I. Opción múltiple razonada (25)", 50),
    ("II. Selección múltiple (6)", 18),
    ("III. Relación de columnas (3)", 12),
    ("IV. Cadenas mecanísticas (3)", 12),
    ("V. Cálculos (7)", 30),
    ("VI. Respuesta extendida (4)", 48),
    ("Revisión final", 10),
]


def _tabla(encabezados, filas):
    th = "".join(f"<th style='border:1px solid #999;padding:4px 8px'>{h}</th>" for h in encabezados)
    trs = "".join(
        "<tr>" + "".join(f"<td style='border:1px solid #999;padding:4px 8px'>{c}</td>" for c in fila) + "</tr>"
        for fila in filas
    )
    return f"<table style='border-collapse:collapse;margin:8px 0'><tr>{th}</tr>{trs}</table>"


INSTRUCCIONES = (
    "<h3>Instrucciones</h3>"
    "<ul>"
    "<li>Tiempo límite: <strong>180 minutos</strong>. Puedes usar calculadora; no necesitas otras fuentes.</li>"
    "<li>Reactivos de cálculo: escribe solo el número, con punto decimal y sin unidades.</li>"
    "<li>Respuesta extendida: se califica el razonamiento (mecanismo, uso de los datos, límites de la evidencia), no la extensión.</li>"
    "<li>Puedes repetir el preexamen; Canvas conserva tu mejor intento.</li>"
    "</ul>"
    "<p><strong>Distribución sugerida del tiempo</strong></p>"
    + _tabla(["Sección", "Minutos"], [(s, m) for s, m in TIEMPOS])
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


def mc(titulo, texto, opciones, correcta, fb, puntos=1.6):
    REACTIVOS.append({"type": "mc", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correcta, "fb": fb, "points": puntos})


def ma(titulo, texto, opciones, correctas, fb, puntos=2.0):
    REACTIVOS.append({"type": "ma", "title": titulo, "text": texto, "choices": opciones,
                      "correct": correctas, "fb": fb, "points": puntos})


def matching(titulo, texto, pares, distractores, fb, puntos=3.0):
    REACTIVOS.append({"type": "matching", "title": titulo, "text": texto, "pairs": pares,
                      "distractors": distractores, "fb": fb, "points": puntos})


def dropdowns(titulo, texto, blancos, fb, puntos=3.0):
    REACTIVOS.append({"type": "dropdowns", "title": titulo, "text": texto, "blanks": blancos,
                      "fb": fb, "points": puntos})


def numerical(titulo, texto, respuesta, tolerancia, fb, puntos=2.0):
    REACTIVOS.append({"type": "numerical", "title": titulo, "text": texto, "answer": respuesta,
                      "tol": tolerancia, "fb": fb, "points": puntos})


def essay(titulo, texto, fb, puntos=4.0):
    REACTIVOS.append({"type": "essay", "title": titulo, "text": texto, "fb": fb, "points": puntos})


header(INSTRUCCIONES)

# ===========================================================================
# SECCIÓN I · OPCIÓN MÚLTIPLE RAZONADA
# ===========================================================================
header("<h3>Sección I · Opción múltiple razonada</h3>"
       "<p>25 reactivos, 1.6 puntos cada uno. Elige la opción <em>mejor justificada</em>; "
       "varias pueden sonar correctas, pero solo una resiste el análisis.</p>")

# ---- Unidad I: polimorfismos y nutrigenética ------------------------------

mc("I-1 · Nutrigenética o nutrigenómica",
   "<p>El estudio A da 2 g/día de EPA+DHA a 40 voluntarios y mide por RNA-seq qué genes inflamatorios cambian en sus linfocitos. "
   "El estudio B compara cuánto bajan los triglicéridos con la misma dosis entre portadores y no portadores de una variante de <em>FADS1</em>.</p>"
   "<p>¿Cuál clasificación es correcta?</p>",
   ["A es nutrigenómica (efecto del nutriente sobre la expresión); B es nutrigenética (efecto del genotipo sobre la respuesta al nutriente).",
    "A es nutrigenética y B es nutrigenómica, porque B mide un gen y A mide miles.",
    "Ambos son nutrigenómica, porque los dos usan un nutriente como intervención.",
    "Ambos son nutrigenética, porque en los dos hay variación genética entre voluntarios."],
   0,
   "<p><strong>Correcta: A nutrigenómica, B nutrigenética.</strong> La pregunta clave es en qué dirección va la flecha: "
   "nutriente → expresión génica (nutrigenómica) o genotipo → respuesta al nutriente (nutrigenética). "
   "El número de genes medidos no define la disciplina, y que haya variación entre voluntarios no convierte un estudio en nutrigenético si el genotipo no es la variable de estudio.</p>")

mc("I-2 · Primer-BLAST sin producto",
   "<p>Un equipo quiere verificar la especificidad de unos primers que amplifican un polimorfismo de inserción Alu situado en un "
   "<strong>intrón</strong> del gen <em>LPL</em>. Corren Primer-BLAST con la base de datos por defecto (<em>Refseq mRNA</em>) "
   "y el resultado es «No target templates were found». ¿Qué concluyes?</p>",
   ["Los primers están mal diseñados y deben rediseñarse antes de seguir.",
    "El resultado era esperable: la base de mRNA no contiene intrones; hay que repetir con <em>Refseq representative genomes</em> de <em>Homo sapiens</em>.",
    "El Alu no existe en humanos modernos, por eso no aparece en ninguna base.",
    "Los primers solo funcionarán con cDNA, así que hay que hacer RT-PCR."],
   1,
   "<p><strong>Correcta: la base de mRNA no tiene intrones.</strong> Un mRNA maduro ya perdió los intrones por splicing, así que un amplicón "
   "intrónico no puede encontrarse ahí. Antes de culpar al diseño hay que preguntarse si la base de datos contiene la secuencia buscada. "
   "Hacer RT-PCR sería justo lo contrario: el cDNA tampoco tiene intrones.</p>")

mc("I-3 · Lectura de un gel PCR-RFLP (MTHFR C677T)",
   "<p>El polimorfismo <em>MTHFR</em> C677T se genotipa amplificando un fragmento de 198 pb y digiriéndolo con <em>Hin</em>fI. "
   "El alelo T crea un sitio de corte, de modo que el fragmento T se corta en 175 + 23 pb; el alelo C queda sin cortar.</p>"
   "<p>En un gel de agarosa al 3 % un carril muestra bandas de <strong>198 pb y 175 pb</strong> y no se ve banda de 23 pb. ¿Cuál es el genotipo más probable?</p>",
   ["CC, porque la banda de 23 pb no aparece y por lo tanto no hubo corte.",
    "TT, porque la banda de 175 pb indica que hubo corte.",
    "CT: hay producto sin cortar (C) y producto cortado (T); la banda de 23 pb es demasiado pequeña y tenue para verse en agarosa.",
    "No se puede asignar genotipo: la ausencia de la banda de 23 pb invalida la digestión."],
   2,
   "<p><strong>Correcta: CT.</strong> El heterocigoto da las bandas de ambos alelos: 198 (C, sin cortar) y 175 + 23 (T). "
   "Un fragmento de 23 pb casi no se tiñe y suele correr fuera del intervalo útil del gel, así que su ausencia no prueba que no hubo corte. "
   "Si fuera TT faltaría la banda de 198 pb (salvo digestión incompleta, que se controla con una muestra de genotipo conocido).</p>")

mc("I-4 · Un heterocigoto que se lee como homocigoto",
   "<p>En el polimorfismo ACE I/D, el alelo D da ~190 pb y el alelo I ~490 pb. Un grupo genotipa 60 personas y reporta 0 heterocigotos I/D, "
   "aunque en esa población se esperaban cerca de la mitad. ¿Cuál es la explicación técnica más probable y su solución?</p>",
   ["El alelo I es letal en heterocigosis; el resultado es biológicamente correcto.",
    "La banda D, más corta, se amplifica preferentemente y algunos I/D se leen como D/D; se confirma con un segundo par de primers específicos de la inserción.",
    "La enzima de restricción no cortó; hay que digerir con otra enzima.",
    "El gel tenía demasiada agarosa; con un gel al 0.5 % aparecerían los heterocigotos."],
   1,
   "<p><strong>Correcta: amplificación preferencial del alelo corto.</strong> En la PCR, el fragmento corto compite con ventaja y puede ocultar al largo. "
   "Por eso en investigación los D/D se confirman con un primer que solo hibrida dentro de la inserción. "
   "ACE I/D no usa enzima de restricción (se distingue por tamaño), y un gel muy diluido empeoraría la resolución.</p>")

mc("I-5 · Hardy–Weinberg como control de calidad",
   "<p>En 200 estudiantes se genotipó un SNP: 98 AA, 22 AG y 80 GG. La frecuencia de A es 0.545. "
   "Bajo equilibrio de Hardy–Weinberg se esperarían ~99 heterocigotos, y se observaron 22. ¿Qué interpretación es más sólida?</p>",
   ["La población está en equilibrio, porque las frecuencias alélicas suman 1.",
    "El déficit tan grande de heterocigotos sugiere un problema de genotipado (pérdida de un alelo, mala lectura del gel) o una muestra mezclada de poblaciones; hay que revisarlo antes de interpretar.",
    "El alelo G confiere una ventaja selectiva que se manifestó en una generación.",
    "Es esperable: los heterocigotos siempre son minoría en cualquier población."],
   1,
   "<p><strong>Correcta: revisar el genotipado o la estructura de la muestra.</strong> Que p + q = 1 es cierto por definición, no prueba equilibrio. "
   "Un exceso de homocigotos tan marcado rara vez es biológico en una muestra de estudiantes: suele indicar error técnico (como en ACE I/D) o mezcla de subpoblaciones (efecto Wahlund). "
   "Con p ≈ 0.5, los heterocigotos esperados son la clase más frecuente, no la minoría.</p>")

mc("I-6 · La trampa de la hebra",
   "<p>Un gen de receptor del gusto está en la hebra (−) del cromosoma. El alelo funcional, en la secuencia codificante, es <strong>C</strong>. "
   "Ensembl reporta los alelos sobre la hebra (+): G = 0.71 y C = 0.29 en la población MXL. Un alumno escribe que el alelo funcional tiene frecuencia 0.29 en MXL. ¿Qué pasó?</p>",
   ["Nada; Ensembl siempre reporta la hebra codificante.",
    "Confundió la hebra: la C codificante corresponde a la G de la hebra (+), así que la frecuencia del alelo funcional es 0.71.",
    "La frecuencia correcta es 0.50, porque en un SNP bialélico cada alelo vale la mitad.",
    "Debe sumar ambas frecuencias porque el gen está en las dos hebras."],
   1,
   "<p><strong>Correcta: complementar la base.</strong> En un gen de la hebra (−), la base codificante es el complemento de la que se lee en la hebra (+): C ↔ G. "
   "Es la misma trampa que vimos con TAS2R38: confundir la hebra invierte la frecuencia reportada.</p>")

# ---- Unidad II: estrés oxidativo y antioxidantes ---------------------------

mc("II-1 · Curva que no llega al 50 %",
   "<p>Un extracto de cáscara de mango alcanza solo <strong>38 % de inhibición</strong> de DPPH a la concentración máxima probada (200 µg/mL). "
   "Un alumno ajusta una recta y extrapola una IC<sub>50</sub> de 290 µg/mL. ¿Qué es lo correcto?</p>",
   ["Reportar IC<sub>50</sub> = 290 µg/mL, porque la recta tiene buen R².",
    "No extrapolar: reportar «IC<sub>50</sub> > 200 µg/mL» junto con el 38 % a 200 µg/mL, o repetir con concentraciones mayores.",
    "Reportar IC<sub>50</sub> = 200 µg/mL, porque es la máxima concentración probada.",
    "Concluir que el extracto no tiene actividad antioxidante."],
   1,
   "<p><strong>Correcta: no extrapolar.</strong> La relación dosis–respuesta no es lineal y suele aplanarse; una recta fuera del intervalo medido inventa un dato. "
   "Un 38 % sí es actividad, solo que menor que la necesaria para estimar la IC<sub>50</sub> con los datos disponibles.</p>")

mc("II-2 · Inhibición negativa con jamaica",
   "<p>Con un extracto concentrado de jamaica, la absorbancia a 517 nm de «muestra + DPPH» resulta <strong>mayor</strong> que la del control, "
   "y el cálculo da −12 % de inhibición. ¿Cuál es la causa más probable?</p>",
   ["La jamaica es prooxidante y genera más radical DPPH•.",
    "Las antocianinas absorben cerca de 520 nm y suman su color a la lectura; falta restar un blanco de muestra (extracto sin DPPH).",
    "El DPPH se degradó por la luz.",
    "El espectrofotómetro se calibró a una longitud de onda equivocada."],
   1,
   "<p><strong>Correcta: interferencia de color.</strong> Los pigmentos rojos absorben en la misma región que el DPPH•. "
   "El blanco de muestra corrige esa absorbancia propia. Un DPPH degradado haría <em>bajar</em> el control, no subir la muestra; y el DPPH• no se «genera» a partir del extracto.</p>")

mc("II-3 · Dos ensayos, dos rankings",
   "<p>El extracto A tiene mejor IC<sub>50</sub> en DPPH; el extracto B da más µmol TE/g en FRAP. ¿Cuál afirmación es la más defendible?</p>",
   ["A es mejor antioxidante, porque DPPH usa un radical y FRAP no.",
    "B es mejor antioxidante, porque FRAP es más reproducible.",
    "Ninguno es «mejor» en absoluto: los ensayos difieren en mecanismo (HAT/SET), disolvente, pH y tiempo, y favorecen compuestos distintos; por eso se reportan al menos dos ensayos.",
    "Los resultados son contradictorios, así que al menos uno de los ensayos está mal hecho."],
   2,
   "<p><strong>Correcta: ningún ensayo mide «la» capacidad antioxidante.</strong> FRAP trabaja a pH 3.6 y solo mide transferencia de electrón; DPPH es mixto y en metanol. "
   "Rankings distintos son esperables y no indican error.</p>")

mc("II-4 · Lo que FRAP no ve",
   "<p>Una bebida rica en glutatión (un tiol) da un valor de FRAP mucho menor de lo que su contenido de tioles haría esperar. ¿Por qué?</p>",
   ["El glutatión no es antioxidante.",
    "FRAP detecta mal los tioles y trabaja a pH ácido (3.6), lejos del fisiológico; un ensayo como ABTS o CUPRAC lo reflejaría mejor.",
    "El glutatión aumenta la absorbancia a 593 nm y anula la señal.",
    "FRAP solo mide antioxidantes liposolubles."],
   1,
   "<p><strong>Correcta: selectividad del ensayo.</strong> FRAP responde a cualquier reductor capaz de reducir Fe³⁺-TPTZ en esas condiciones, pero reacciona poco con tioles. "
   "Esto ilustra por qué un solo ensayo puede subestimar a ciertos compuestos.</p>")

mc("II-5 · Más SOD no siempre es mejor",
   "<p>Un ratón transgénico sobreexpresa SOD1 cinco veces, sin cambios en catalasa ni glutatión peroxidasa. "
   "Tras un reto oxidativo muestra <strong>más</strong> daño lipídico que el silvestre. ¿Cuál es la explicación más coherente?</p>",
   ["La SOD1 en exceso consume el H₂O₂ y deja sin sustrato a la catalasa.",
    "La SOD convierte el superóxido en H₂O₂ más rápido de lo que este se elimina; el H₂O₂ acumulado, con Fe²⁺, genera radical hidroxilo (Fenton).",
    "La SOD1 es prooxidante por sí misma porque contiene cobre.",
    "El transgén silenció a la catalasa por metilación."],
   1,
   "<p><strong>Correcta: desbalance entre los dos pasos de la cascada.</strong> O₂•⁻ → (SOD) → H₂O₂ → (catalasa/GPx) → H₂O. "
   "Acelerar solo el primer paso cambia una especie reactiva por otra; el •OH de Fenton es el más dañino. "
   "No hay datos que apoyen un silenciamiento epigenético.</p>")

mc("II-6 · SOD fuera de intervalo",
   "<p>En el ensayo de SOD con NBT, un homogenado de hígado sin diluir da <strong>96 % de inhibición</strong>. ¿Qué haces?</p>",
   ["Reportar 96 % como actividad máxima.",
    "Calcular las unidades directamente: si 50 % = 1 U, entonces 96 % ≈ 1.92 U.",
    "Diluir el homogenado y repetir hasta quedar entre 20 y 80 % de inhibición, y obtener el volumen que da 50 % a partir de la curva.",
    "Aumentar la concentración de NBT para que vuelva a aparecer el color."],
   2,
   "<p><strong>Correcta: diluir.</strong> La relación entre inhibición y cantidad de enzima no es lineal y se satura cerca del 100 %; "
   "ahí la inhibición ya no distingue entre mucha y muchísima enzima. Por eso no se escala proporcionalmente. "
   "Cambiar el NBT altera la competencia por el superóxido y la definición de la unidad.</p>")

mc("II-7 · Catalasa que se aplana",
   "<p>Al medir catalasa (caída de A<sub>240</sub>), la absorbancia baja casi a cero en los primeros 10 s y luego se queda plana. ¿Qué indica y cómo se corrige?</p>",
   ["La enzima está inactiva; hay que preparar un homogenado nuevo.",
    "Hay demasiada enzima; diluir el homogenado y usar solo el tramo inicial (cinética de primer orden).",
    "El H₂O₂ estaba contaminado con plástico; cambiar a cubeta de vidrio común.",
    "Es el comportamiento normal; reportar el ΔA total entre 0 y 60 s."],
   1,
   "<p><strong>Correcta: demasiada enzima.</strong> La catalasa casi no se satura y agota rápidamente el H₂O₂; si el sustrato se acaba, la pendiente deja de reflejar la actividad. "
   "El vidrio común absorbe en el UV: se necesita cuarzo o cubeta UV.</p>")

mc("II-8 · TAC sérica que sube por otra razón",
   "<p>Tras 8 semanas tomando un jugo de frutas con fructosa añadida, la capacidad antioxidante total (TAC) del suero sube 25 %. "
   "También subió el ácido úrico sérico. ¿Qué conclusión es más prudente?</p>",
   ["El jugo mejoró el estado antioxidante, porque la TAC subió.",
    "No se puede atribuir el aumento de TAC a los antioxidantes del jugo: el ácido úrico aporta buena parte de la TAC plasmática y la fructosa lo eleva; hay que medir enzimas y un marcador de daño.",
    "La TAC sérica no tiene relación con el ácido úrico.",
    "El aumento de ácido úrico demuestra que el jugo es prooxidante."],
   1,
   "<p><strong>Correcta: confusor metabólico.</strong> El urato es uno de los principales contribuyentes a la TAC del plasma, y el metabolismo hepático de la fructosa lo incrementa. "
   "Un aumento de TAC no equivale a menos estrés oxidativo; se confirma con enzimas (SOD, catalasa) y daño (MDA/TBARS).</p>")

mc("II-9 · Polifenoles: tubo frente a organismo",
   "<p>La quercetina tiene una IC<sub>50</sub> excelente en DPPH, pero su concentración plasmática tras una comida rara vez supera el rango micromolar bajo "
   "y circula mayoritariamente conjugada. Aun así, algunos estudios reportan más expresión de enzimas antioxidantes en tejido. ¿Qué mecanismo reconcilia ambas observaciones?</p>",
   ["Neutralización directa de radicales en el plasma, porque basta una concentración baja.",
    "Activación de Nrf2: los polifenoles o sus metabolitos modifican a Keap1, Nrf2 se acumula y aumenta la transcripción de enzimas antioxidantes; el efecto depende de la señalización, no de la estequiometría.",
    "Los polifenoles se convierten en SOD dentro del hígado.",
    "La quercetina inhibe la catalasa y así aumenta la señal de H₂O₂."],
   1,
   "<p><strong>Correcta: señalización vía Nrf2.</strong> Una molécula a concentración baja no puede neutralizar estequiométricamente un flujo continuo de radicales, pero sí puede activar un factor de transcripción "
   "que amplifica la respuesta. Esta es la razón por la que medimos los dos lados: la actividad química del extracto y las enzimas del organismo.</p>")

# ---- Unidad III: epigenética y nutrición ----------------------------------

mc("III-1 · El diseño de la Hambruna Holandesa",
   "<p>En el estudio de la Hambruna Holandesa (1944–45), cada persona expuesta se comparó con un hermano o hermana <strong>del mismo sexo</strong> no expuesto. ¿Qué gana el diseño con esa elección?</p>",
   ["Elimina por completo cualquier confusión.",
    "Controla parcialmente el fondo genético y el ambiente familiar compartido, y el sexo, que también influyen en la metilación; así la diferencia es más atribuible a la exposición prenatal.",
    "Permite estudiar herencia transgeneracional.",
    "Asegura que ambos hermanos tengan exactamente el mismo genotipo."],
   1,
   "<p><strong>Correcta: control parcial de genética, familia y sexo.</strong> Los hermanos comparten en promedio la mitad de las variantes (no todo el genotipo) y gran parte del ambiente familiar. "
   "Recordemos que hay variantes (mQTL) que cambian la metilación cercana, así que controlar la genética importa. Ningún diseño observacional elimina toda la confusión.</p>")

mc("III-2 · ¿Por qué IGF2?",
   "<p>¿Por qué un gen impreso como <em>IGF2</em> es un buen candidato para registrar exposiciones periconcepcionales?</p>",
   ["Porque solo se expresa en el adulto mayor.",
    "Porque su marca de metilación resiste la ola de desmetilación del embrión preimplantación y se establece en una ventana muy temprana, así que una perturbación en ese momento puede dejar huella duradera.",
    "Porque su secuencia cambia con la dieta materna.",
    "Porque todos los genes impresos se expresan desde los dos alelos."],
   1,
   "<p><strong>Correcta: resiste la reprogramación.</strong> Las improntas se colocan en los gametos y se mantienen tras la fecundación; por eso registran exposiciones muy tempranas. "
   "En los genes impresos solo se expresa el alelo de un progenitor (IGF2: paterno), y la dieta no cambia la secuencia.</p>")

mc("III-3 · Ratón agouti",
   "<p>Dos crías de la misma camada tienen genotipo <em>A<sup>vy</sup>/a</em>; una es amarilla y obesa, otra café y delgada. "
   "¿Por qué esto se considera evidencia epigenética y no genética?</p>",
   ["Porque tienen distinto número de copias del gen agouti.",
    "Porque comparten genotipo pero difieren en la metilación del retrotransposón IAP río arriba de agouti, que determina si el gen se expresa de forma ectópica.",
    "Porque una heredó el alelo de la madre y la otra del padre.",
    "Porque la dieta materna mutó el IAP en una de ellas."],
   1,
   "<p><strong>Correcta: mismo genotipo, distinta metilación.</strong> IAP hipometilado → agouti ectópico → amarillo y obeso; IAP metilado → café (pseudoagouti). "
   "Los donadores de metilo en la dieta materna desplazan la distribución hacia el café; el bisfenol A la desplaza hacia el amarillo.</p>")

mc("III-4 · Potencial de metilación",
   "<p>Ratas alimentadas sin folato ni colina muestran hipometilación global del DNA hepático. ¿Cuál es el mecanismo más directo?</p>",
   ["El folato se incorpora como base en el DNA y al faltar se pierde la metilación.",
    "Cae la remetilación de homocisteína: baja el SAM y sube el SAH; el SAH inhibe a las DNMT, así que el cociente SAM/SAH (potencial de metilación) disminuye.",
    "La colina se une a las colas de histonas y sin ella el DNA se desenrolla.",
    "La falta de folato activa a las enzimas TET, que eliminan todos los metilos."],
   1,
   "<p><strong>Correcta: SAM ↓, SAH ↑.</strong> El folato (vía 5-metil-THF y metionina sintasa) y la colina (vía betaína y BHMT) remetilan la homocisteína. "
   "El SAH no es inerte: inhibe a las metiltransferasas, por eso importa el cociente y no solo el SAM.</p>")

mc("III-5 · Dos tejidos en Gambia",
   "<p>En el estudio de Gambia, la metilación de epialelos metaestables se midió en sangre y en folículo piloso de los bebés. "
   "¿Por qué medir dos tejidos fortalece la conclusión?</p>",
   ["Porque así se duplica el tamaño de muestra.",
    "Porque provienen de capas embrionarias distintas (mesodermo y ectodermo): si ambos cambian igual, la marca se estableció antes de la diferenciación, en el embrión temprano, y es sistémica.",
    "Porque el folículo piloso no tiene DNA metilado y sirve de control negativo.",
    "Porque la sangre refleja la dieta del bebé y el pelo la de la madre."],
   1,
   "<p><strong>Correcta: origen embrionario distinto.</strong> Una marca presente en tejidos de linajes diferentes apunta a un evento previo a la gastrulación, "
   "lo que coincide con la ventana periconcepcional en que cambió la dieta materna.</p>")

mc("III-6 · Gemelos que divergen",
   "<p>Los gemelos monocigóticos mayores difieren más en metilación que los jóvenes. ¿Qué diseño distinguiría mejor entre el efecto del estilo de vida y el azar (deriva epigenética)?</p>",
   ["Comparar un solo par de gemelos de 50 años.",
    "Seguir a muchos pares en el tiempo y relacionar cuánto difieren en hábitos (dieta, tabaco, ejercicio) con cuánto difieren en metilación: si la divergencia es igual con o sin diferencias de hábitos, predomina el azar.",
    "Secuenciar el genoma de ambos gemelos para encontrar mutaciones.",
    "Medir la metilación solo en recién nacidos."],
   1,
   "<p><strong>Correcta: diseño longitudinal con exposición medida.</strong> Hay tres fuentes de variación: genética (mQTL), ambiental y estocástica. "
   "En gemelos MZ la genética está controlada; para separar ambiente y azar hay que medir las diferencias de exposición y ver si predicen la divergencia.</p>")

mc("III-7 · Una diferencia que podría ser genética",
   "<p>Un estudio transversal encuentra que los vegetarianos tienen 8 % menos metilación en un CpG que los omnívoros, y concluye que la dieta vegetariana desmetila ese sitio. "
   "Ese CpG está a 300 pb de un SNP común, y el estudio no genotipó a los participantes. ¿Cuál es la crítica más importante?</p>",
   ["El efecto es muy pequeño para ser real.",
    "El SNP podría ser un mQTL: si su frecuencia difiere entre los grupos (por ascendencia, por ejemplo), explicaría la diferencia sin que la dieta intervenga.",
    "La metilación no se puede medir en un solo CpG.",
    "Los vegetarianos consumen más folato, así que deberían tener más metilación, no menos."],
   1,
   "<p><strong>Correcta: posible confusión genética.</strong> No toda diferencia de metilación es dietaria; un estudio serio considera el genotipo. "
   "Además, al ser transversal, no establece temporalidad. La opción D asume un mecanismo sin datos que lo respalden.</p>")

mc("III-8 · Metionina y H3K4me3",
   "<p>Restringir metionina bajó el SAM y la marca H3K4me3 en pocas horas, y la marca se recuperó al restaurar la metionina. ¿Qué implica esa reversibilidad?</p>",
   ["Que las marcas de histonas son irrelevantes para la expresión génica.",
    "Que algunas marcas responden de forma dinámica al estado nutricional del adulto, porque las metiltransferasas dependen del SAM disponible; no todo efecto epigenético es una huella permanente del desarrollo.",
    "Que la metionina modifica la secuencia del DNA de forma reversible.",
    "Que H3K4me3 es una marca de represión."],
   1,
   "<p><strong>Correcta: el metabolismo alimenta la cromatina en tiempo real.</strong> Las HAT usan acetil-CoA y las metiltransferasas usan SAM. "
   "H3K4me3 marca promotores activos (las de represión son H3K9me3 y H3K27me3).</p>")

mc("III-9 · Anti-miR-33",
   "<p><em>miR-33a</em> está en un intrón de <em>SREBF2</em> y reprime a <em>ABCA1</em>. Si en ratones se administra un oligonucleótido que inhibe a miR-33, ¿qué se espera?</p>",
   ["Menos ABCA1 y menos HDL.",
    "Más ABCA1, más eflujo de colesterol y más HDL plasmático.",
    "Menos síntesis de colesterol, porque se inhibe a SREBF2.",
    "Ningún cambio, porque los miRNAs no regulan genes de lípidos."],
   1,
   "<p><strong>Correcta: se libera la represión de ABCA1.</strong> Inhibir el miRNA no apaga a su gen hospedero; solo deja de reprimir sus blancos. "
   "Más ABCA1 → más eflujo de colesterol hacia apoA-I → más HDL, como se observó en ratones.</p>")

mc("III-10 · miRNAs de la dieta",
   "<p>Un estudio reportó un miRNA del arroz en suero humano que reprimía un gen hepático en ratón; un estudio posterior, con controles más estrictos, "
   "no detectó miRNAs vegetales en plasma de humanos, ratones ni abejas tras la ingesta. ¿Cuál es la postura más rigurosa?</p>",
   ["Aceptar el primer estudio porque se publicó antes.",
    "Aceptar el segundo porque tiene más especies.",
    "Considerar la hipótesis no establecida: hay que comparar sensibilidad del método, controles de contaminación y reproducibilidad independiente antes de aceptarla.",
    "Concluir que los miRNAs no existen en plantas."],
   2,
   "<p><strong>Correcta: hipótesis abierta.</strong> En ciencia una afirmación extraordinaria necesita replicación independiente. "
   "Las secuencias contaminantes de reactivos y la amplificación de cantidades mínimas son fuentes conocidas de falsos positivos en este tipo de estudios.</p>")

# ===========================================================================
# SECCIÓN II · SELECCIÓN MÚLTIPLE
# ===========================================================================
header("<h3>Sección II · Selección múltiple</h3>"
       "<p>6 reactivos, 2 puntos cada uno. Marca <strong>todas</strong> las opciones correctas; Canvas da crédito parcial y descuenta las marcadas de más.</p>")

ma("SM-1 · Leer el patrón enzimático",
   "<p>Ratas con dieta alta en fructosa + extracto vegetal, comparadas con el grupo que solo recibió fructosa:</p>"
   + _tabla(["Marcador hepático", "Cambio"],
            [("SOD (U/mg proteína)", "↑ 60 %"), ("Catalasa (U/mg proteína)", "sin cambio"), ("TBARS (nmol MDA/mg)", "↑ 35 %")])
   + "<p>Selecciona las afirmaciones bien sustentadas.</p>",
   ["Puede estar acumulándose H₂O₂, porque se produce más de lo que la catalasa elimina.",
    "El aumento de TBARS es coherente con más peroxidación lipídica, posiblemente por Fenton.",
    "El extracto demostró ser antioxidante <em>in vivo</em>, porque elevó la SOD.",
    "Antes de concluir convendría medir glutatión peroxidasa o glutatión, la otra vía de eliminación del H₂O₂.",
    "Más SOD siempre indica mejor estado redox."],
   [0, 1, 3],
   "<p><strong>Correctas: 1, 2 y 4.</strong> SOD alta con catalasa igual y más daño lipídico es el patrón de desbalance, no de protección. "
   "Una enzima elevada puede ser señal de más estrés, no de mejor salud. La GPx también elimina H₂O₂ y no se midió.</p>")

ma("SM-2 · De la IC<sub>50</sub> a la recomendación",
   "<p>Un extracto de semilla de aguacate tiene IC<sub>50</sub> = 12 µg/mL en DPPH, más baja que la del ácido ascórbico en el mismo ensayo. "
   "Una empresa quiere anunciar que «protege tus células mejor que la vitamina C». ¿Qué objeciones son válidas?</p>",
   ["DPPH es un radical nitrogenado artificial; no representa a las especies reactivas fisiológicas.",
    "El ensayo no considera absorción, metabolismo ni concentración alcanzada en el tejido.",
    "Una IC<sub>50</sub> baja indica menor actividad que la vitamina C.",
    "Haría falta evidencia en un modelo biológico (enzimas, marcadores de daño) y, para la afirmación en humanos, estudios en humanos.",
    "Basta con repetir el DPPH por triplicado para sostener la afirmación."],
   [0, 1, 3],
   "<p><strong>Correctas: 1, 2 y 4.</strong> La IC<sub>50</sub> baja sí indica mayor actividad <em>en el tubo</em> (la opción 3 es falsa). "
   "El problema es extrapolar del tubo a la célula; la replicación técnica no resuelve un problema de validez.</p>")

ma("SM-3 · Gen × nutriente",
   "<p>En un estudio, las personas <em>MTHFR</em> 677TT tuvieron menos metilación genómica que las CC, pero la diferencia se concentró en las TT con folato bajo. "
   "¿Qué afirmaciones se desprenden?</p>",
   ["Es una interacción gen–nutriente: el efecto del genotipo depende del estado de folato.",
    "Las personas TT con buen estado de folato pueden tener una metilación similar a la de las CC.",
    "El genotipo TT causa hipometilación en cualquier condición dietaria.",
    "Una recomendación razonable es asegurar un buen aporte de folato (y de riboflavina, cofactor de MTHFR) en personas TT.",
    "Las personas CC no necesitan folato."],
   [0, 1, 3],
   "<p><strong>Correctas: 1, 2 y 4.</strong> La interacción implica que el genotipo no es destino; la dieta modula su efecto. "
   "MTHFR usa FAD (derivado de la riboflavina). El folato es esencial para todos, no solo para TT.</p>")

ma("SM-4 · ¿Transgeneracional o intergeneracional?",
   "<p>¿Cuáles escenarios cumplirían el criterio de herencia <strong>transgeneracional</strong> verdadera?</p>",
   ["Una gestante (F0) se expone a hambruna y su hijo (F1) tiene diabetes a los 50 años.",
    "Una gestante (F0) se expone y el efecto aparece en sus bisnietos (F3), que nunca estuvieron expuestos.",
    "Una gestante (F0) se expone y el efecto aparece en sus nietos (F2).",
    "Un macho (F0) se expone antes de la concepción y el efecto aparece en sus nietos (F2).",
    "Una madre lactante cambia su dieta y su bebé tiene otra microbiota."],
   [1, 3],
   "<p><strong>Correctas: 2 y 4.</strong> Si la gestante se expone, también se exponen el feto (F1) y sus células germinales (F2). "
   "Solo la F3 por vía materna, o la F2 por vía paterna, no tuvieron exposición directa. La lactancia es una exposición directa del bebé.</p>")

ma("SM-5 · PCR in silico de una inserción Alu",
   "<p>Para un polimorfismo de inserción Alu, UCSC In-Silico PCR sobre GRCh38 devuelve un producto de 352 pb que cae en un intrón. "
   "El genoma de referencia no tiene la inserción, y el Alu mide ~300 pb. Selecciona las afirmaciones correctas.</p>",
   ["El alelo (+) daría una banda de ~650 pb.",
    "Un heterocigoto mostraría dos bandas, ~352 y ~650 pb.",
    "El producto de 352 pb corresponde al alelo (+).",
    "Como cae en un intrón, no se espera que cambie la secuencia de la proteína.",
    "Por estar en un gen, este polimorfismo necesariamente altera un rasgo nutricional."],
   [0, 1, 3],
   "<p><strong>Correctas: 1, 2 y 4.</strong> La referencia no tiene el Alu, así que 352 pb es el alelo (−); el (+) mide ~352 + 300. "
   "Una inserción intrónica puede ser un marcador neutro (como PV92 en CDH13); estar dentro de un gen no basta para afirmar un efecto.</p>")

ma("SM-6 · Evidencia humana en epigenética",
   "<p>Selecciona las afirmaciones respaldadas por la evidencia revisada en clase.</p>",
   ["Una sola sesión de ejercicio redujo la metilación de promotores como PGC-1α en músculo esquelético.",
    "El tabaquismo materno se asocia con diferencias de metilación en miles de CpG del recién nacido, y muchas persisten en la infancia.",
    "Los tests comerciales de «edad epigenética» están validados para tomar decisiones clínicas individuales.",
    "Relojes como GrimAge se asocian con mortalidad, pero esa asociación no demuestra que bajar la «edad epigenética» prolongue la vida.",
    "La metilación medida en sangre refleja siempre la del músculo o el hígado."],
   [0, 1, 3],
   "<p><strong>Correctas: 1, 2 y 4.</strong> Los relojes son predictores poblacionales, no diagnósticos individuales; y la metilación es específica de tejido, "
   "así que la sangre no siempre representa a otros órganos.</p>")

# ===========================================================================
# SECCIÓN III · RELACIÓN DE COLUMNAS
# ===========================================================================
header("<h3>Sección III · Relación de columnas</h3>"
       "<p>3 reactivos, 3 puntos cada uno. Cada columna derecha tiene una opción que no corresponde a nada.</p>")

matching("RC-1 · Estudio → hallazgo",
         "<p>Relaciona cada estudio con su hallazgo principal.</p>",
         [("Ratón A<sup>vy</sup> con madre suplementada con folato, B12, colina y betaína",
           "Más metilación del IAP y más crías de pelaje café"),
          ("Personas concebidas durante la Hambruna Holandesa",
           "Menos metilación de IGF2 seis décadas después"),
          ("Gambia rural, estación de lluvias frente a seca",
           "La dieta materna en la concepción predijo la metilación de epialelos metaestables en el bebé"),
          ("Portadores MTHFR 677TT con folato bajo",
           "Menor contenido de 5mC genómica que los CC"),
          ("Restricción de metionina en células y en hígado de ratón",
           "Caída rápida y reversible de H3K4me3"),
          ("Sesión aguda de ejercicio",
           "Hipometilación de promotores de PGC-1α y PDK4 en músculo")],
         ["Aumento de HDL al inhibir un miRNA"],
         "<p><strong>Clave:</strong> agouti → IAP; Hambruna → IGF2; Gambia → epialelos metaestables; MTHFR → 5mC genómica; "
         "metionina → H3K4me3; ejercicio → PGC-1α. El distractor (HDL y miRNA) corresponde a miR-33.</p>")

matching("RC-2 · Ensayo → lectura",
         "<p>Relaciona cada ensayo con lo que se lee en él.</p>",
         [("DPPH", "Disminución de absorbancia a 517 nm"),
          ("FRAP", "Aumento de absorbancia a 593 nm al formarse Fe²⁺-TPTZ"),
          ("Catalasa (Aebi)", "Caída de A₂₄₀ por desaparición del H₂O₂"),
          ("SOD con NBT", "Menor formación de formazán a 560 nm"),
          ("TBARS", "Producto de la peroxidación lipídica (MDA) como marcador de daño")],
         ["Concentración directa de radical hidroxilo en el tejido"],
         "<p><strong>Clave:</strong> solo FRAP sube con más antioxidante; DPPH, catalasa y SOD se leen como disminución de señal. "
         "El •OH vive nanosegundos y no se mide directamente con estos ensayos.</p>")

matching("RC-3 · Herramienta → para qué sirve en el Dry Lab",
         "<p>Relaciona cada herramienta con su uso.</p>",
         [("UCSC In-Silico PCR", "Obtener el amplicón y sus coordenadas a partir de dos primers"),
          ("UCSC Genome Browser (pista GENCODE)", "Ver si el amplicón cae en exón o intrón y en qué gen"),
          ("Primer-BLAST con genoma de referencia", "Verificar que los primers amplifican un solo producto"),
          ("NEBcutter", "Predecir qué enzima corta un producto y el tamaño de los fragmentos"),
          ("Ensembl (Population genetics)", "Consultar frecuencias alélicas por población de 1000 Genomas")],
         ["Medir la expresión del gen en el tejido de un paciente"],
         "<p><strong>Clave:</strong> ninguna de estas herramientas mide expresión en una muestra; todas trabajan sobre secuencias de referencia o bases de datos.</p>")

# ===========================================================================
# SECCIÓN IV · CADENAS MECANÍSTICAS
# ===========================================================================
header("<h3>Sección IV · Cadenas mecanísticas</h3>"
       "<p>3 reactivos, 3 puntos cada uno. Completa cada eslabón; un eslabón equivocado rompe la lógica del resto.</p>")

dropdowns("CM-1 · Ciclo de un carbono",
          "<p>El folato de la dieta se convierte en 5,10-metilen-THF y la enzima [c1], que usa como cofactor [c2], lo reduce a 5-metil-THF. "
          "La metionina sintasa, dependiente de [c3], transfiere ese metilo a la homocisteína para formar metionina, precursora del [c4]. "
          "Una vía alterna de remetilación usa [c5], derivada de la colina. Tras donar su metilo se forma [c6], que inhibe a las metiltransferasas.</p>",
          {"c1": (["MTHFR", "DNMT1", "BHMT", "TET"], 0),
           "c2": (["FAD (riboflavina)", "biotina", "vitamina K", "hierro hemo"], 0),
           "c3": (["vitamina B12", "vitamina C", "vitamina D", "tiamina"], 0),
           "c4": (["SAM", "acetil-CoA", "NADPH", "glutatión"], 0),
           "c5": (["betaína", "glicina", "taurina", "creatina"], 0),
           "c6": (["SAH", "5mC", "homocisteína oxidada", "metilmalonato"], 0)},
          "<p><strong>Cadena:</strong> MTHFR (FAD/riboflavina) → 5-metil-THF → metionina sintasa (B12) → metionina → SAM → SAH. "
          "La betaína (BHMT) es la vía alterna. El cociente SAM/SAH es el potencial de metilación.</p>")

dropdowns("CM-2 · Butirato: un metabolito, dos destinos",
          "<p>La fibra fermentable llega al colon, donde bacterias como [b1] producen butirato. En el colonocito normal, el butirato se [b2] "
          "y alimenta a las [b3], lo que aumenta la acetilación de histonas. En la célula tumoral, que obtiene energía principalmente por [b4], "
          "el butirato [b5] y actúa como inhibidor de [b6], frenando la proliferación.</p>",
          {"b1": (["<em>Faecalibacterium prausnitzii</em>", "<em>Lactobacillus delbrueckii</em> subsp. <em>bulgaricus</em>",
                   "<em>Streptococcus thermophilus</em>", "<em>Escherichia coli</em>"], 0),
           "b2": (["oxida a acetil-CoA en la mitocondria", "convierte en SAM", "excreta sin cambios", "polimeriza en glucógeno"], 0),
           "b3": (["histona acetiltransferasas (HAT)", "DNA metiltransferasas", "enzimas TET", "Dicer"], 0),
           "b4": (["glucólisis aeróbica (efecto Warburg)", "β-oxidación de butirato", "cetogénesis", "fosforilación oxidativa exclusiva"], 0),
           "b5": (["se acumula en el núcleo", "se oxida más rápido", "se convierte en folato", "no logra entrar a la célula"], 0),
           "b6": (["histona desacetilasas (HDAC)", "catalasa", "MTHFR", "metionina sintasa"], 0)},
          "<p><strong>Cadena:</strong> <em>F. prausnitzii</em> → butirato → (normal) acetil-CoA → HAT; (tumoral, Warburg) se acumula → inhibe HDAC. "
          "<em>L. bulgaricus</em> y <em>S. thermophilus</em> son homofermentativos lácticos: producen lactato, no butirato.</p>")

dropdowns("CM-3 · Genotipar un SNP con PCR-RFLP",
          "<p>Un SNP no cambia el [r1] del amplicón, así que en el gel los dos alelos se ven iguales. Para distinguirlos se usa un primer con una base "
          "[r2] cerca de su extremo 3', que crea un sitio de restricción solo en uno de los alelos. Por ese cambio, UCSC In-Silico PCR [r3] el producto. "
          "Después de digerir, el homocigoto sin sitio muestra [r4] banda(s) y el heterocigoto muestra [r5].</p>",
          {"r1": (["tamaño", "color", "número de copias", "contenido de GC visible"], 0),
           "r2": (["modificada a propósito", "metilada", "eliminada", "duplicada"], 0),
           "r3": (["puede no encontrar", "siempre encuentra", "duplica", "corta"], 0),
           "r4": (["una", "dos", "tres", "cero"], 0),
           "r5": (["las bandas de ambos alelos (sin cortar y cortadas)", "solo las bandas cortadas", "una banda intermedia", "ninguna banda"], 0)},
          "<p><strong>Cadena:</strong> mismo tamaño → primer con base modificada crea el sitio → UCSC exige coincidencia perfecta en el extremo 3' y puede no dar producto "
          "→ homocigoto sin sitio = 1 banda; heterocigoto = banda sin cortar + fragmentos cortados (como TAS2R38 con <em>Hae</em>III).</p>")

# ===========================================================================
# SECCIÓN V · CÁLCULOS
# ===========================================================================
header("<h3>Sección V · Cálculos</h3>"
       "<p>7 reactivos, 2 puntos cada uno. Escribe solo el número. Haz el cálculo en papel: en el examen se pide el procedimiento.</p>")

numerical("C-1 · DPPH con blanco de muestra",
          "<p>Un extracto de flor de cempasúchil (pigmentado) se prueba a 100 µg/mL:</p>"
          + _tabla(["Lectura", "A<sub>517</sub>"],
                   [("Control (DPPH + metanol)", "0.910"), ("Muestra + DPPH", "0.502"), ("Blanco de muestra (extracto sin DPPH)", "0.048")])
          + "<p>Calcula el porcentaje de inhibición (una cifra decimal).</p>",
          50.1, 0.5,
          "<p>A muestra corregida = 0.502 − 0.048 = 0.454. "
          "% = (0.910 − 0.454) / 0.910 × 100 = <strong>50.1 %</strong>. "
          "Sin restar el blanco obtendrías 44.8 %: el pigmento haría parecer al extracto menos activo.</p>")

numerical("C-2 · IC<sub>50</sub> por interpolación",
          "<p>Porcentaje de inhibición de DPPH (ya corregido) de un extracto de nopal:</p>"
          + _tabla(["µg/mL", "% inhibición"], [("10", "22"), ("25", "38"), ("50", "57"), ("100", "79")])
          + "<p>Estima la IC<sub>50</sub> por interpolación lineal entre los dos puntos que rodean al 50 % (µg/mL, una cifra decimal).</p>",
          40.8, 0.5,
          "<p>El 50 % está entre 25 µg/mL (38 %) y 50 µg/mL (57 %). "
          "IC<sub>50</sub> = 25 + (50 − 38)/(57 − 38) × (50 − 25) = 25 + 0.632 × 25 = <strong>40.8 µg/mL</strong>. "
          "Interpolar entre puntos vecinos es razonable; extrapolar fuera de los datos no.</p>")

numerical("C-3 · FRAP: de absorbancia a µmol TE/g",
          "<p>Curva de Trolox en FRAP: A = 0.0025·C + 0.015 (C en µM). Se extraen 250 mg de cacao en 25 mL; el extracto se diluye 1:20 y da A<sub>593</sub> = 0.440.</p>"
          "<p>Calcula la capacidad antioxidante en µmol de equivalentes de Trolox por gramo (µmol TE/g).</p>",
          340.0, 3.0,
          "<p>1) C = (0.440 − 0.015)/0.0025 = 170 µM en la dilución. "
          "2) × 20 = 3,400 µM = 3.40 µmol/mL en el extracto. "
          "3) 3.40 µmol/mL × 25 mL = 85 µmol en 0.25 g → <strong>340 µmol TE/g</strong>. "
          "Errores típicos: olvidar el factor de dilución (17 µmol TE/g) o normalizar dos veces.</p>")

numerical("C-4 · Actividad específica de catalasa",
          "<p>Homogenado de hígado: ΔA<sub>240</sub>/min = 0.0654 (tramo inicial), cubeta de 1 cm, volumen total 3.0 mL, volumen de muestra 0.10 mL, "
          "proteína 2.5 mg/mL. ε<sub>240</sub>(H₂O₂) = 43.6 M⁻¹ cm⁻¹. 1 U = 1 µmol de H₂O₂ por minuto.</p>"
          "<p>Calcula la actividad específica en U/mg de proteína.</p>",
          18.0, 0.3,
          "<p>U/mL = (0.0654 / 43.6) × 1000 × (3.0/0.10) = 0.0015 × 1000 × 30 = 45.0 U/mL. "
          "Actividad específica = 45.0 / 2.5 = <strong>18.0 U/mg</strong>. "
          "El factor 1000 convierte mol/L a µmol/mL; el cociente de volúmenes corrige la dilución en la cubeta.</p>")

numerical("C-5 · Unidades de SOD",
          "<p>Ensayo de SOD con NBT. Blanco (reacción completa sin muestra): ΔA<sub>560</sub>/min = 0.080. "
          "Con 10 µL de muestra: ΔA/min = 0.052. Con varios volúmenes se construyó la curva, y el 50 % de inhibición se alcanza con <strong>16 µL</strong> de muestra. "
          "Proteína de la muestra: 5.0 mg/mL. Definición: 1 U = cantidad de enzima que inhibe el 50 %.</p>"
          "<p>Calcula la actividad específica en U/mg de proteína.</p>",
          12.5, 0.2,
          "<p>Con 10 µL la inhibición es (0.080 − 0.052)/0.080 = 35 %, dentro del intervalo útil, pero las unidades salen del volumen que da 50 %: "
          "1 U en 0.016 mL → 62.5 U/mL; 62.5 / 5.0 = <strong>12.5 U/mg</strong>. "
          "No se escala el 35 % de forma proporcional porque la relación no es lineal.</p>")

numerical("C-6 · Frecuencia alélica",
          "<p>Se genotipó TAS2R38 (PAV = catador, AVI = no catador) en 80 estudiantes: 22 PAV/PAV, 38 PAV/AVI y 20 AVI/AVI.</p>"
          "<p>Calcula la frecuencia del alelo PAV (dos cifras decimales).</p>",
          0.51, 0.01,
          "<p>Alelos PAV = 2 × 22 + 38 = 82, de 2 × 80 = 160 alelos. p = 82/160 = <strong>0.51</strong>. "
          "Heterocigotos esperados en equilibrio: 2pq × 80 = 2 × 0.5125 × 0.4875 × 80 ≈ 40, muy cerca de los 38 observados.</p>")

numerical("C-7 · Potencial de metilación",
          "<p>En hígado de ratas control: SAM = 90 nmol/g y SAH = 30 nmol/g. Tras 6 semanas sin folato ni colina: SAM = 60 nmol/g y SAH = 40 nmol/g.</p>"
          "<p>¿En qué porcentaje <strong>disminuyó</strong> el cociente SAM/SAH? (Escribe un número positivo.)</p>",
          50.0, 1.0,
          "<p>Control: 90/30 = 3.0. Deficiente: 60/40 = 1.5. Disminución = (3.0 − 1.5)/3.0 × 100 = <strong>50 %</strong>. "
          "Fíjate que el SAM solo bajó 33 %: el aumento de SAH, inhibidor de las metiltransferasas, agrava el efecto.</p>")

# ===========================================================================
# SECCIÓN VI · RESPUESTA EXTENDIDA
# ===========================================================================
header("<h3>Sección VI · Respuesta extendida</h3>"
       "<p>4 reactivos, 4 puntos cada uno, ~12 minutos cada uno. Se califica con la rúbrica que aparece en la retroalimentación: "
       "mecanismo correcto, uso explícito de los datos, límites de la evidencia y propuesta concreta.</p>")

RUBRICA = (
    "<p><strong>Rúbrica (4 pts):</strong> 1 pt mecanismo correcto y en orden; 1 pt usa los datos del caso de forma explícita; "
    "1 pt identifica al menos una limitación o confusor relevante; 1 pt propone un siguiente paso concreto y justificado.</p>"
)

essay("RE-1 · ¿Mejoró el estado redox?",
      "<p>Ratas Wistar durante 10 semanas. Valores medios por grupo (n = 8):</p>"
      + _tabla(["Grupo", "SOD (U/mg)", "Catalasa (U/mg)", "TBARS (nmol MDA/mg)", "TAC sérica (mM TE)", "Ácido úrico (mg/dL)"],
               [("Control", "12.1", "35.2", "1.10", "1.05", "3.1"),
                ("Alta en fructosa (AF)", "15.8", "22.4", "2.05", "1.38", "5.9"),
                ("AF + extracto de jamaica", "17.9", "33.0", "1.30", "1.41", "5.6")])
      + "<p>a) Interpreta el patrón del grupo AF frente al control. b) ¿Qué cambió con el extracto y qué mecanismo lo explicaría? "
        "c) Un compañero concluye que la fructosa es antioxidante porque subió la TAC. Responde con los datos. d) Propón un experimento o medición que haga falta.</p>",
      "<p><strong>Respuesta modelo.</strong> a) En AF la SOD sube pero la catalasa cae: se produce más H₂O₂ del que se elimina; las TBARS casi se duplican, coherente con daño lipídico (Fenton). "
      "b) Con el extracto la catalasa se recupera (33.0) y las TBARS bajan (1.30); SOD y catalasa altas juntas sugieren una respuesta adaptativa coordinada, compatible con activación de Nrf2 por los polifenoles. "
      "c) La TAC sube en AF a la par del ácido úrico (3.1 → 5.9), que aporta buena parte de la TAC plasmática y se eleva con el metabolismo de la fructosa; la TAC alta no indica menos estrés, y las TBARS muestran lo contrario. "
      "d) Medir GPx/glutatión, expresión de Nrf2 o de sus blancos (NQO1, HO-1), y hacer estadística entre grupos (ANOVA con post hoc) con la dispersión, no solo medias; caracterizar el extracto (DPPH y un segundo ensayo).</p>"
      + RUBRICA)

essay("RE-2 · «Lo que comió tu abuela decide tu diabetes»",
      "<p>Un portal de salud publica: <em>«Ya está demostrado: lo que comió tu abuela determina si tendrás diabetes, porque la dieta se hereda en tus genes».</em></p>"
      "<p>a) Corrige el error conceptual de «se hereda en tus genes». b) Distingue efecto intergeneracional y transgeneracional con el esquema F0–F1–F2–F3. "
      "c) Usa dos estudios vistos en clase para decir qué sí está demostrado y qué no. d) Diseña en términos generales qué estudio haría falta para sostener el titular.</p>",
      "<p><strong>Respuesta modelo.</strong> a) Las exposiciones no cambian la secuencia; lo que puede transmitirse son marcas epigenéticas (metilación, histonas, RNAs), y aun eso es discutido en humanos. "
      "b) Si la gestante (F0) se expone, también se exponen el feto (F1) y sus células germinales (F2): un efecto en F1 o F2 es intergeneracional. Transgeneracional verdadero requiere F3 por vía materna (o F2 por vía paterna). "
      "c) Hambruna Holandesa: menor metilación de IGF2 seis décadas después en los expuestos periconcepcionalmente (efecto en F1, ventana crítica). Agouti: la dieta materna cambia la metilación del IAP y el fenotipo de las crías (modelo animal). "
      "Ninguno demuestra transmisión a nietos no expuestos en humanos ni que la marca cause diabetes. "
      "d) Cohorte multigeneracional con exposición materna documentada, metilación medida en varias generaciones y tejidos, control del genotipo (mQTL) y del ambiente compartido (dieta y nivel socioeconómico familiar), con el desenlace (diabetes) en F3.</p>"
      + RUBRICA)

essay("RE-3 · Caso de nutrigenética: homocisteína alta",
      "<p>Mujer de 34 años que planea embarazarse. Homocisteína 19 µmol/L (referencia &lt; 15), folato sérico bajo, B12 normal. "
      "El laboratorio genotipó <em>MTHFR</em> C677T por PCR-RFLP con <em>Hin</em>fI: su carril muestra <strong>solo una banda de 175 pb</strong> (no se distingue la de 23 pb).</p>"
      "<p>a) Asigna el genotipo y justifica con la lógica del ensayo. b) Explica con el ciclo de un carbono por qué su homocisteína está alta. "
      "c) ¿Qué recomendación nutricional harías y por qué el genotipo no es destino? d) Señala una limitación del ensayo y una de la interpretación.</p>",
      "<p><strong>Respuesta modelo.</strong> a) TT: todo el producto de 198 pb se cortó (175 + 23); no queda banda sin cortar del alelo C. "
      "b) La variante 677T produce una MTHFR termolábil con menor actividad → menos 5-metil-THF → la metionina sintasa (B12) remetila menos homocisteína → se acumula homocisteína y baja el SAM. Con folato bajo el efecto se intensifica (interacción gen–nutriente). "
      "c) Asegurar folato (alimentos y el suplemento de ácido fólico indicado antes del embarazo), riboflavina (FAD, cofactor de MTHFR) y B12 adecuada; en el estudio de clase las TT con buen folato se parecían a las CC. Revalorar homocisteína tras la intervención. "
      "d) Ensayo: una digestión incompleta podría confundir TT y CT si quedara algo de 198 pb, por eso se incluyen controles de genotipo conocido. "
      "Interpretación: el genotipo explica solo parte de la variación de homocisteína (influyen dieta, función renal y otras variantes); no justifica por sí solo un tratamiento distinto al que recibiría cualquier persona con folato bajo.</p>"
      + RUBRICA)

essay("RE-4 · Análisis de una afirmación comercial",
      "<p>Una marca vende cápsulas de extracto de germinado de brócoli con este texto: <em>«El sulforafano reprograma tus genes, neutraliza los radicales libres "
      "y, según nuestro test de saliva, reduce tu edad epigenética 10 años en 3 meses».</em></p>"
      "<p>Evalúa cada una de las tres afirmaciones con lo visto en las unidades II y III. Para cada una di qué parte tiene sustento mecanístico, qué evidencia falta "
      "y qué tipo de estudio la respaldaría.</p>",
      "<p><strong>Respuesta modelo.</strong> «Reprograma tus genes»: hay sustento mecanístico parcial. Los metabolitos del sulforafano (SFN-cisteína, SFN-NAC) inhibieron HDAC y aumentaron la acetilación en el promotor de P21 en líneas celulares de cáncer de colon; "
      "eso no cambia la secuencia ni demuestra efecto en personas que consumen la cápsula. Faltan biodisponibilidad, dosis alcanzada en tejido y ensayos en humanos. "
      "«Neutraliza radicales»: el sulforafano actúa sobre todo de forma indirecta: es un electrófilo que modifica Keap1, activa Nrf2 e induce enzimas citoprotectoras; no es principalmente un antioxidante estequiométrico, así que la afirmación describe mal el mecanismo. "
      "«Reduce la edad epigenética 10 años»: los relojes (Horvath, GrimAge) son predictores poblacionales; un test comercial no está validado para decisiones individuales, la metilación es específica de tejido (saliva no es hígado o colon) y un cambio en el reloj no demuestra más salud ni más vida. "
      "Para respaldarlo haría falta un ensayo aleatorizado y controlado con placebo, reloj validado, tejido justificado, tamaño de muestra suficiente y desenlaces clínicos, no solo el marcador.</p>"
      + RUBRICA)
