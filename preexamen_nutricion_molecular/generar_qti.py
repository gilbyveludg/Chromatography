# -*- coding: utf-8 -*-
"""Genera el paquete QTI 1.2 (formato de exportación de Canvas) de un banco de reactivos.

Uso:  python3 generar_qti.py [ruta/al/banco.py]
      (sin argumento usa banco_preguntas.py de esta carpeta: el preexamen)
Salida, junto al banco:
  <ARCHIVO_ZIP del banco>  -> Canvas: Configuración > Importar contenido del curso > Paquete QTI .zip
  clave_docente.md         -> respuestas y retroalimentación para el docente

El banco puede definir CANVAS (dict) para cambiar la configuración del cuestionario.
"""
import hashlib
import importlib.util
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape


def _cargar_banco():
    ruta = os.environ.get("BANCO") or (sys.argv[1] if __name__ == "__main__" and len(sys.argv) > 1 else None)
    ruta = os.path.abspath(ruta or os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco_preguntas.py"))
    spec = importlib.util.spec_from_file_location("banco", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo, os.path.dirname(ruta)


banco, AQUI = _cargar_banco()
ZIP_SALIDA = os.path.join(AQUI, getattr(banco, "ARCHIVO_ZIP", "preexamen_nutricion_molecular_qti.zip"))
CLAVE_SALIDA = os.path.join(AQUI, "clave_docente.md")

# Configuración de Canvas: por defecto, cuestionario de práctica (preexamen).
CANVAS = {
    "quiz_type": "practice_quiz",
    "time_limit": 180,
    "allowed_attempts": -1,  # ilimitados: es material de estudio
    "show_correct_answers": "true",
    "hide_results": "",
    "one_question_at_a_time": "false",
    "cant_go_back": "false",
    "scoring_policy": "keep_highest",
}
CANVAS.update(getattr(banco, "CANVAS", {}))
LIMITE_MIN = CANVAS["time_limit"]


def ident(*partes):
    return "g" + hashlib.md5("|".join(map(str, partes)).encode()).hexdigest()


QUIZ_ID = ident(getattr(banco, "ID_CUESTIONARIO", "preexamen-nutricion-molecular-2026"))
META_ID = ident(QUIZ_ID, "meta")


def texto_plano(html):
    return re.sub(r"<[^>]+>", "", html)


IMAGENES = []  # rutas relativas al banco de las imágenes usadas en los reactivos


def _con_imagenes(html):
    """Registra las imágenes locales y las apunta a la carpeta de archivos del curso en Canvas."""
    def cambiar(m):
        ruta = m.group(2)
        if ruta not in IMAGENES:
            IMAGENES.append(ruta)
        return f"src={m.group(1)}%24IMS-CC-FILEBASE%24/{ruta}{m.group(1)}"
    return re.sub(r"src=(['\"])(?!https?:|%24|\$)([^'\"]+)\1", cambiar, html)


def mat(contenido, html=True):
    tipo = "text/html" if html else "text/plain"
    if html:
        contenido = _con_imagenes(contenido)
    return f'<material><mattext texttype="{tipo}">{escape(contenido)}</mattext></material>'


def metadatos(tipo, puntos, ids_respuesta=""):
    campos = [("question_type", tipo), ("points_possible", f"{puntos:.2f}"),
              ("original_answer_ids", ids_respuesta), ("assessment_question_identifierref", ident("aq", tipo, puntos, ids_respuesta))]
    filas = "".join(f"<qtimetadatafield><fieldlabel>{k}</fieldlabel><fieldentry>{v}</fieldentry></qtimetadatafield>" for k, v in campos)
    return f"<itemmetadata><qtimetadata>{filas}</qtimetadata></itemmetadata>"


SALIDA = '<outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>'
FB_GENERAL = ('<respcondition continue="Yes"><conditionvar><other/></conditionvar>'
              '<displayfeedback feedbacktype="Response" linkrefid="general_fb"/></respcondition>')


def bloque_fb(fb):
    return f'<itemfeedback ident="general_fb"><flow_mat>{mat(fb)}</flow_mat></itemfeedback>'


def item(n, r):
    t = r["type"]
    iid = ident("item", n, r.get("title", ""))
    titulo = escape(r.get("title", f"Bloque {n}"), {'"': "&quot;"})

    if t == "header":
        return (f'<item ident="{iid}" title="Instrucciones">{metadatos("text_only_question", 0)}'
                f'<presentation>{mat(r["text"])}</presentation></item>')

    if t in ("mc", "ma"):
        ids = [str(1000 * n + i) for i in range(len(r["choices"]))]
        card = "Single" if t == "mc" else "Multiple"
        etiquetas = "".join(f'<response_label ident="{i}">{mat(c)}</response_label>' for i, c in zip(ids, r["choices"]))
        pres = (f'<presentation>{mat(r["text"])}<response_lid ident="response1" rcardinality="{card}">'
                f'<render_choice>{etiquetas}</render_choice></response_lid></presentation>')
        if t == "mc":
            cond = f'<varequal respident="response1">{ids[r["correct"]]}</varequal>'
        else:
            partes = [f'<varequal respident="response1">{i}</varequal>' if k in r["correct"]
                      else f'<not><varequal respident="response1">{i}</varequal></not>' for k, i in enumerate(ids)]
            cond = "<and>" + "".join(partes) + "</and>"
        proc = (f'<resprocessing>{SALIDA}{FB_GENERAL}<respcondition continue="No"><conditionvar>{cond}</conditionvar>'
                f'<setvar action="Set" varname="SCORE">100</setvar></respcondition></resprocessing>')
        tipo = "multiple_choice_question" if t == "mc" else "multiple_answers_question"
        return f'<item ident="{iid}" title="{titulo}">{metadatos(tipo, r["points"], ",".join(ids))}{pres}{proc}{bloque_fb(r["fb"])}</item>'

    if t == "matching":
        derechas = [d for _, d in r["pairs"]] + r["distractors"]
        der_ids = [str(1000 * n + 500 + i) for i in range(len(derechas))]
        etiquetas = "".join(f'<response_label ident="{i}">{mat(texto_plano(d), html=False)}</response_label>'
                            for i, d in zip(der_ids, derechas))
        lids, conds = "", ""
        peso = 100.0 / len(r["pairs"])
        izq_ids = []
        for k, (izq, _) in enumerate(r["pairs"]):
            rid = str(1000 * n + k)
            izq_ids.append(rid)
            lids += f'<response_lid ident="response_{rid}">{mat(texto_plano(izq), html=False)}<render_choice>{etiquetas}</render_choice></response_lid>'
            conds += (f'<respcondition><conditionvar><varequal respident="response_{rid}">{der_ids[k]}</varequal></conditionvar>'
                      f'<setvar varname="SCORE" action="Add">{peso:.2f}</setvar></respcondition>')
        pres = f'<presentation>{mat(r["text"])}{lids}</presentation>'
        proc = f'<resprocessing>{SALIDA}{FB_GENERAL}{conds}</resprocessing>'
        return f'<item ident="{iid}" title="{titulo}">{metadatos("matching_question", r["points"], ",".join(izq_ids))}{pres}{proc}{bloque_fb(r["fb"])}</item>'

    if t == "dropdowns":
        lids, conds, todos = "", "", []
        peso = 100.0 / len(r["blanks"])
        for b, (opciones, correcta) in r["blanks"].items():
            ids = [ident(iid, b, i)[:12] for i in range(len(opciones))]
            todos += ids
            etiquetas = "".join(f'<response_label ident="{i}">{mat(texto_plano(o), html=False)}</response_label>' for i, o in zip(ids, opciones))
            lids += f'<response_lid ident="response_{b}">{mat(b, html=False)}<render_choice>{etiquetas}</render_choice></response_lid>'
            conds += (f'<respcondition><conditionvar><varequal respident="response_{b}">{ids[correcta]}</varequal></conditionvar>'
                      f'<setvar varname="SCORE" action="Add">{peso:.2f}</setvar></respcondition>')
        pres = f'<presentation>{mat(r["text"])}{lids}</presentation>'
        proc = f'<resprocessing>{SALIDA}{FB_GENERAL}{conds}</resprocessing>'
        return f'<item ident="{iid}" title="{titulo}">{metadatos("multiple_dropdowns_question", r["points"], ",".join(todos))}{pres}{proc}{bloque_fb(r["fb"])}</item>'

    if t == "numerical":
        a, tol = r["answer"], r["tol"]
        pres = (f'<presentation>{mat(r["text"])}<response_str ident="response1" rcardinality="Single">'
                f'<render_fib fibtype="Decimal"><response_label ident="answer1"/></render_fib></response_str></presentation>')
        cond = (f'<or><varequal respident="response1">{a}</varequal><and><vargte respident="response1">{a - tol:.4f}</vargte>'
                f'<varlte respident="response1">{a + tol:.4f}</varlte></and></or>')
        proc = (f'<resprocessing>{SALIDA}{FB_GENERAL}<respcondition continue="No"><conditionvar>{cond}</conditionvar>'
                f'<setvar action="Set" varname="SCORE">100</setvar></respcondition></resprocessing>')
        return f'<item ident="{iid}" title="{titulo}">{metadatos("numerical_question", r["points"], str(1000 * n))}{pres}{proc}{bloque_fb(r["fb"])}</item>'

    if t == "essay":
        pres = (f'<presentation>{mat(r["text"])}<response_str ident="response1" rcardinality="Single">'
                f'<render_fib><response_label ident="answer1" rshuffle="No"/></render_fib></response_str></presentation>')
        proc = (f'<resprocessing>{SALIDA}{FB_GENERAL}<respcondition continue="No"><conditionvar><other/></conditionvar></respcondition></resprocessing>')
        return f'<item ident="{iid}" title="{titulo}">{metadatos("essay_question", r["points"])}{pres}{proc}{bloque_fb(r["fb"])}</item>'

    raise ValueError(t)


def puntos_totales():
    return round(sum(r.get("points", 0) for r in banco.REACTIVOS), 2)


def evaluacion_xml():
    items = "".join(item(n, r) for n, r in enumerate(banco.REACTIVOS, start=1))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">'
            f'<assessment ident="{QUIZ_ID}" title="{escape(banco.TITULO)}"><qtimetadata>'
            f'<qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>{'unlimited' if CANVAS['allowed_attempts'] == -1 else CANVAS['allowed_attempts']}</fieldentry></qtimetadatafield>'
            f'<qtimetadatafield><fieldlabel>qmd_timelimit</fieldlabel><fieldentry>{LIMITE_MIN}</fieldentry></qtimetadatafield>'
            f'</qtimetadata><section ident="root_section">{items}</section></assessment></questestinterop>\n')


def meta_xml():
    campos = {
        "title": escape(banco.TITULO),
        "description": escape(banco.DESCRIPCION.strip()),
        "shuffle_answers": "true",
        "scoring_policy": CANVAS["scoring_policy"],
        "hide_results": CANVAS["hide_results"],
        "quiz_type": CANVAS["quiz_type"],
        "points_possible": f"{puntos_totales():.1f}",
        "require_lockdown_browser": "false",
        "require_lockdown_browser_for_results": "false",
        "require_lockdown_browser_monitor": "false",
        "lockdown_browser_monitor_data": "",
        "show_correct_answers": CANVAS["show_correct_answers"],
        "anonymous_submissions": "false",
        "could_be_locked": "false",
        "time_limit": str(LIMITE_MIN),
        "allowed_attempts": str(CANVAS["allowed_attempts"]),
        "one_question_at_a_time": CANVAS["one_question_at_a_time"],
        "cant_go_back": CANVAS["cant_go_back"],
        "available": "false",
        "one_time_results": "false",
        "show_correct_answers_last_attempt": "false",
        "only_visible_to_overrides": "false",
        "module_locked": "false",
    }
    cuerpo = "".join(f"<{k}>{v}</{k}>" for k, v in campos.items())
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<quiz identifier="{QUIZ_ID}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">'
            f'{cuerpo}<assignment_group_identifierref></assignment_group_identifierref></quiz>\n')


def manifiesto_xml():
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<manifest identifier="{ident(QUIZ_ID, "manifest")}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" '
            'xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd '
            'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd '
            'http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">'
            '<metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion>'
            '<imsmd:lom><imsmd:general><imsmd:title><imsmd:string>'
            f'{escape(banco.TITULO)}</imsmd:string></imsmd:title></imsmd:general></imsmd:lom></metadata>'
            '<organizations/><resources>'
            f'<resource identifier="{QUIZ_ID}" type="imsqti_xmlv1p2"><file href="{QUIZ_ID}/{QUIZ_ID}.xml"/>'
            f'<dependency identifierref="{META_ID}"/></resource>'
            f'<resource identifier="{META_ID}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" '
            f'href="{QUIZ_ID}/assessment_meta.xml"><file href="{QUIZ_ID}/assessment_meta.xml"/></resource>'
            + "".join(f'<resource identifier="{ident("img", r)}" type="webcontent" href="{escape(r)}"><file href="{escape(r)}"/></resource>' for r in IMAGENES)
            + '</resources></manifest>\n')


def clave_md():
    lineas = [f"# Clave docente · {banco.TITULO}", "",
              f"Puntaje total: **{puntos_totales():g}** · Tiempo: **{LIMITE_MIN} min** · No se entrega a los alumnos.", ""]
    for r in banco.REACTIVOS:
        t = r["type"]
        if t == "header":
            m = re.search(r"<h3>(.*?)</h3>", r["text"])
            if m and m.group(1) != "Instrucciones":
                lineas += [f"## {texto_plano(m.group(1))}", ""]
            continue
        lineas.append(f"### {texto_plano(r['title'])} ({r['points']:g} pts)")
        if t == "mc":
            lineas.append(f"- Respuesta: **{chr(65 + r['correct'])}**: {texto_plano(r['choices'][r['correct']])}")
        elif t == "ma":
            letras = ", ".join(chr(65 + i) for i in r["correct"])
            lineas.append(f"- Respuestas: **{letras}**")
        elif t == "matching":
            for izq, der in r["pairs"]:
                lineas.append(f"- {texto_plano(izq)} → {texto_plano(der)}")
        elif t == "dropdowns":
            lineas.append("- " + "; ".join(f"[{b}] {texto_plano(o[c])}" for b, (o, c) in r["blanks"].items()))
        elif t == "numerical":
            lineas.append(f"- Respuesta: **{r['answer']:g}** (se acepta ± {r['tol']:g})")
        lineas += [f"- {texto_plano(r['fb'])}", ""]
    return "\n".join(lineas) + "\n"


def main():
    with zipfile.ZipFile(ZIP_SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        evaluacion = evaluacion_xml()  # primero: registra las imágenes que usa
        z.writestr("imsmanifest.xml", manifiesto_xml())
        z.writestr(f"{QUIZ_ID}/{QUIZ_ID}.xml", evaluacion)
        for ruta in IMAGENES:
            z.write(os.path.join(AQUI, ruta), ruta)
        z.writestr(f"{QUIZ_ID}/assessment_meta.xml", meta_xml())
    with open(CLAVE_SALIDA, "w", encoding="utf-8") as f:
        f.write(clave_md())
    n = sum(1 for r in banco.REACTIVOS if r["type"] != "header")
    print(f"{n} reactivos · {puntos_totales():g} puntos · {ZIP_SALIDA}")


if __name__ == "__main__":
    main()
