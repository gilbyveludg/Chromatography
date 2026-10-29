# -*- coding: utf-8 -*-
"""Convierte un banco de reactivos a JSON estructurado para generar el Word (generar_word.js) y la presentación.

Uso: python3 exportar_json.py salida.json  (el banco se elige con la variable BANCO; sin ella, el del preexamen)
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

from generar_qti import AQUI, banco, puntos_totales, LIMITE_MIN


class Bloques(HTMLParser):
    """Pasa un fragmento HTML a bloques: párrafos y listas con runs, y tablas."""

    def __init__(self):
        super().__init__()
        self.bloques, self.runs, self.estilo = [], [], set()
        self.tabla = self.fila = self.celda = None
        self.lista, self.encabezado = None, False

    def _vaciar(self):
        if self.runs and any(r["t"].strip() for r in self.runs):
            b = {"tipo": "p", "runs": self.runs}
            if self.lista:
                b["lista"] = self.lista
            if self.encabezado:
                b["h"] = True
            self.bloques.append(b)
        self.runs = []

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "li", "h3"):
            self._vaciar()
            self.encabezado = tag == "h3"
        elif tag in ("ul", "ol"):
            self._vaciar()
            self.lista = "bullet" if tag == "ul" else "num"
        elif tag == "table":
            self._vaciar()
            self.tabla = []
        elif tag == "tr":
            self.fila = []
        elif tag in ("td", "th"):
            self.celda = []
        elif tag in ("strong", "b", "th"):
            self.estilo.add("b")
        elif tag in ("em", "i"):
            self.estilo.add("i")
        elif tag in ("sub", "sup"):
            self.estilo.add(tag)
        elif tag == "code":
            self.estilo.add("m")
        elif tag == "img":
            self._vaciar()
            a = dict(attrs)
            self.bloques.append({"tipo": "img", "src": os.path.join(AQUI, a["src"]), "alt": a.get("alt", "")})
        elif tag == "br" and self.celda is None:
            self._vaciar()
        if tag == "th":
            self.estilo.add("b")

    def handle_endtag(self, tag):
        if tag in ("p", "li", "h3"):
            self._vaciar()
            self.encabezado = False
        elif tag in ("ul", "ol"):
            self._vaciar()
            self.lista = None
        elif tag in ("td", "th"):
            self.fila.append(self.celda)
            self.celda = None
            self.estilo.discard("b")
        elif tag == "tr":
            self.tabla.append(self.fila)
        elif tag == "table":
            self.bloques.append({"tipo": "tabla", "filas": self.tabla})
            self.tabla = None
        elif tag in ("strong", "b"):
            self.estilo.discard("b")
        elif tag in ("em", "i"):
            self.estilo.discard("i")
        elif tag in ("sub", "sup"):
            self.estilo.discard(tag)
        elif tag == "code":
            self.estilo.discard("m")

    def handle_data(self, data):
        if not data.strip() and not self.runs and self.celda is None:
            return
        run = {"t": re.sub(r"\s+", " ", data), **{k: True for k in self.estilo}}
        (self.celda if self.celda is not None else self.runs).append(run)

    def close(self):
        super().close()
        self._vaciar()
        return self.bloques


def bloques(html):
    p = Bloques()
    p.feed(html)
    return p.close()


def plano(html):
    return re.sub(r"<[^>]+>", "", html)


def main():
    salida = {"titulo": banco.TITULO, "pie": getattr(banco, "PIE", banco.TITULO), "portada": getattr(banco, "PORTADA_WORD", ""), "total": puntos_totales(), "minutos": LIMITE_MIN,
              "descripcion": bloques(banco.DESCRIPCION), "reactivos": []}
    for r in banco.REACTIVOS:
        d = {"tipo": r["type"]}
        if r["type"] == "header":
            d["bloques"] = bloques(r["text"])
        else:
            d.update(titulo=plano(r["title"]), puntos=r["points"], enunciado=bloques(r["text"]), fb=bloques(r["fb"]))
            if r["type"] in ("mc", "ma"):
                d["opciones"] = [bloques("<p>" + c + "</p>")[0]["runs"] for c in r["choices"]]
                d["correctas"] = [r["correct"]] if r["type"] == "mc" else r["correct"]
            elif r["type"] == "matching":
                d["pares"] = [[plano(a), plano(b)] for a, b in r["pairs"]]
                d["distractores"] = [plano(x) for x in r["distractors"]]
            elif r["type"] == "dropdowns":
                d["blancos"] = [[k, [plano(o) for o in ops], c] for k, (ops, c) in r["blanks"].items()]
            elif r["type"] == "numerical":
                d["respuesta"], d["tol"] = r["answer"], r["tol"]
        salida["reactivos"].append(d)
    json.dump(salida, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
