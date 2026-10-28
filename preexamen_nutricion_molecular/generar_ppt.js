// Genera la presentación de revisión del preexamen: por cada reactivo, una diapositiva con la pregunta
// y otra con la respuesta explicada. Lee el JSON de exportar_json.py.
// Uso: node generar_ppt.js banco.json salida.pptx [ruta_apply_theme.js]
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheck, FaTimes, FaFlask, FaDna, FaUserMd, FaLaptopCode, FaLightbulb } = require("react-icons/fa");

const [, , entrada, salida, rutaTema] = process.argv;
const banco = JSON.parse(fs.readFileSync(entrada, "utf8"));

const THEME = {
  name: "Genoma a la Clinica",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2B34", lt1: "FFFFFF", dk2: "0B3C49", lt2: "EEF4F3",
    accent1: "2A9D8F", accent2: "E76F51", accent3: "E9C46A", accent4: "264653", accent5: "8AB17D", accent6: "6C757D",
    hlink: "2A9D8F", folHlink: "264653",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = banco.titulo;
pres.author = "Nutrición Molecular";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333, X0 = 0.6, ANCHO = W - 2 * X0, Y_FIN = 6.75;
const LETRAS = "ABCDEFGHIJ";

// ------------------------------------------------------------------ iconos
async function icono(Comp, color, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: px }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ----------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 2.2, w: 11.5, h: 1.8, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, valign: "bottom" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: X0, y: 4.2, w: 11.5, h: 1.4, fontSize: 20, color: C.background2, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "DIVISOR",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 1.6, w: 8.4, h: 1.6, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "bottom" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: X0, y: 3.4, w: 8.0, h: 3.0, fontSize: 18, color: C.background2, valign: "top" }, text: "" } },
  ],
});
const pie = (color) => ({ text: { text: "Preexamen · Del Genoma Crudo a la Clínica", options: { x: X0, y: 7.0, w: 8, h: 0.3, fontSize: 10, color, margin: 0 } } });
pres.defineSlideMaster({
  title: "PREGUNTA",
  background: { color: C.background1 },
  objects: [
    pie(C.accent6),
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.55, w: 10.6, h: 0.75, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});
pres.defineSlideMaster({
  title: "RESPUESTA",
  background: { color: C.background2 },
  objects: [
    pie(C.accent6),
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.55, w: 10.6, h: 0.75, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

// ------------------------------------------------------- texto y medición
const plano = (runs) => runs.map((r) => r.t).join("");
const opcRun = (r, extra = {}) => ({
  text: r.t,
  options: { bold: r.b || extra.bold, italic: r.i, subscript: r.sub, superscript: r.sup, fontFace: r.m ? "Courier New" : undefined, color: extra.color },
});

// Líneas aproximadas de un texto en una caja (Calibri: ~0.5 em por carácter en promedio).
function lineas(texto, anchoIn, pt) {
  const porLinea = Math.max(10, Math.floor((anchoIn * 72) / (pt * 0.46)));
  return texto.split("\n").reduce((n, t) => n + Math.max(1, Math.ceil(t.length / porLinea)), 0);
}
const altoTexto = (texto, anchoIn, pt, interlineado = 1.2) => (lineas(texto, anchoIn, pt) * pt * interlineado) / 72 + 0.07;

// Tabla de bloques del banco a addTable, devuelve alto aproximado.
function tablaFilas(filas, pt) {
  return filas.map((fila, i) => fila.map((celda) => ({
    text: celda.map((r) => opcRun(r, { bold: i === 0 })),
    options: { fontSize: pt, fill: { color: i === 0 ? THEME.colors.lt2 : THEME.colors.lt1 }, color: C.text1, margin: 0.05, valign: "middle" },
  })));
}
function altoTabla(filas, anchoIn, pt) {
  const colW = anchoIn / filas[0].length;
  return filas.reduce((h, fila) => h + Math.max(...fila.map((c) => (lineas(plano(c), colW - 0.15, pt) * pt * 1.2) / 72)) + 0.17, 0);
}

// Coloca bloques (párrafos, listas, tablas) en columna; dibujar=false solo mide.
// Los elementos de lista consecutivos van en una sola caja para que el espaciado sea uniforme.
function bloques(slide, lista, x, y, w, pt, dibujar, extra = {}) {
  for (let k = 0; k < lista.length; k++) {
    const b = lista[k];
    if (b.tipo === "tabla") {
      const colW = Math.min(2.4, w / b.filas[0].length);
      const tw = colW * b.filas[0].length;
      if (dibujar) slide.addTable(tablaFilas(b.filas, pt - 1), { x, y, w: tw, colW: Array(b.filas[0].length).fill(colW), border: { type: "solid", pt: 0.75, color: "B8C4C2" }, objectName: "tabla" });
      y += altoTabla(b.filas, tw, pt - 1) + 0.15;
    } else if (b.lista) {
      // Viñeta dibujada como círculo: pptxgenjs repite las propiedades de párrafo en cada run
      // y pierde la viñeta cuando el elemento tiene subíndices o negritas.
      const t = plano(b.runs);
      const h = altoTexto(t, w - 0.3, pt);
      if (dibujar) {
        const d = Math.max(0.06, pt / 200);
        slide.addShape(pres.ShapeType.ellipse, { x: x + 0.06, y: y + (pt * 0.62) / 72 - d / 2 + 0.03, w: d, h: d, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: "vineta" });
        slide.addText(b.runs.map((r) => opcRun(r, extra)), { x: x + 0.28, y, w: w - 0.28, h, fontSize: pt, color: extra.color || C.text1, valign: "top", margin: 0.02, isTextBox: true, objectName: "elemento" });
      }
      y += h + 0.06;
    } else {
      const t = plano(b.runs);
      if (!t.trim()) continue;
      const h = altoTexto(t, w, pt);
      if (dibujar) {
        slide.addText(b.runs.map((r) => opcRun(r, extra)), { x, y, w, h, fontSize: pt, color: extra.color || C.text1, valign: "top", margin: 0.02, isTextBox: true, objectName: "texto" });
      }
      y += h + 0.08;
    }
  }
  return y;
}

// Prueba tamaños de letra de mayor a menor hasta que el contenido quepa.
function ajustar(construir, tamaños = [20, 19, 18, 17, 16, 15, 14, 13, 12]) {
  for (const pt of tamaños) if (construir(null, pt, false) <= Y_FIN) return pt;
  return tamaños[tamaños.length - 1];
}

// ----------------------------------------------------------- etiquetas
function etiqueta(slide, texto, color, fondo, x = X0, y = 0.22, w = 3.2) {
  slide.addText(texto, { x, y, w, h: 0.3, fontSize: 11, bold: true, color, fill: { color: fondo }, rectRadius: 0.08, shape: pres.ShapeType.roundRect, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "etiqueta" });
}
function circuloLetra(slide, letra, x, y, fondo, color, d = 0.42) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: fondo }, line: { color: fondo }, objectName: "circulo" });
  slide.addText(letra, { x, y, w: d, h: d, fontSize: 16, bold: true, color, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "letra" });
}

// ------------------------------------------------------- diapositiva pregunta
function pregunta(r, bloque, seccion) {
  const tipoTexto = { mc: "Opción múltiple", ma: "Selección múltiple: marca todas las correctas", numerical: "Cálculo", matching: "Relaciona columnas", dropdowns: "Completa cada espacio", essay: "Respuesta extendida" }[r.tipo];
  const construir = (slide, pt, dibujar) => {
    let y = 1.5;
    if (r.tipo === "matching" && r.enunciado.some((b) => b.tipo === "tabla")) {
      const wi = 7.2, wd = ANCHO - wi - 0.4;
      const yi = bloques(slide, r.enunciado, X0, y, wi, pt, dibujar);
      const der = [...r.pares.map((x) => x[1]), ...r.distractores];
      const n = der.length, orden = Array.from({ length: n }, (_, i) => (2 * n - 1 - i + 3) % n);
      let yd = y;
      const fila = (txt, negrita) => {
        const h = altoTexto(txt, wd, pt - 1);
        if (dibujar) slide.addText(txt, { x: X0 + wi + 0.4, y: yd, w: wd, h, fontSize: pt - 1, bold: negrita, color: negrita ? C.text2 : C.text1, valign: "top", margin: 0.02, isTextBox: true, objectName: "columna" });
        yd += h + 0.02;
      };
      fila("Columna A", true);
      r.pares.forEach(([a], i) => fila(`${i + 1}. ${a}`));
      yd += 0.15;
      fila("Columna B (una opción sobra)", true);
      der.forEach((_, i) => fila(`${LETRAS[i]}) ${der[orden[i]]}`));
      return Math.max(yi, yd);
    }
    // Opción múltiple con tabla en el enunciado: enunciado a la izquierda, opciones a la derecha.
    const conTabla = (r.tipo === "mc" || r.tipo === "ma") && r.enunciado.some((b) => b.tipo === "tabla");
    const wEnun = conTabla ? 5.6 : ANCHO;
    const xOpc = conTabla ? X0 + wEnun + 0.4 : X0, wOpc = conTabla ? ANCHO - wEnun - 0.4 : ANCHO;
    const yEnun = bloques(slide, r.enunciado, X0, y, wEnun, pt, dibujar);
    y = conTabla ? y : yEnun;
    if (r.tipo === "mc" || r.tipo === "ma") {
      y += conTabla ? 0 : 0.08;
      const optPt = pt - 1;
      r.opciones.forEach((op, i) => {
        const h = Math.max(0.46, altoTexto(plano(op), wOpc - 0.65, optPt));
        if (dibujar) {
          circuloLetra(slide, LETRAS[i], xOpc, y + 0.02, C.accent1, C.background1);
          slide.addText(op.map((x) => opcRun(x)), { x: xOpc + 0.6, y, w: wOpc - 0.6, h, fontSize: optPt, color: C.text1, valign: "middle", margin: 0.02, isTextBox: true, objectName: "opcion" });
        }
        y += h + 0.1;
      });
      y = Math.max(y, yEnun);
    } else if (r.tipo === "matching") {
      const der = [...r.pares.map((x) => x[1]), ...r.distractores];
      const n = der.length, orden = Array.from({ length: n }, (_, i) => (2 * n - 1 - i + 3) % n);
      const filas = [["Columna A", "Columna B (una opción sobra)"].map((t) => [{ t, b: true }])];
      for (let i = 0; i < n; i++) filas.push([[{ t: r.pares[i] ? `${i + 1}. ${r.pares[i][0]}` : "" }], [{ t: `${LETRAS[i]}) ${der[orden[i]]}` }]]);
      y = bloques(slide, [{ tipo: "tabla", filas }], X0, y + 0.05, ANCHO, pt, dibujar);
    } else if (r.tipo === "dropdowns") {
      for (const [k, ops] of r.blancos) {
        const t = `[${k}]  ${ops.join("   ·   ")}`;
        const h = altoTexto(t, ANCHO, pt - 2);
        if (dibujar) slide.addText([{ text: `[${k}]  `, options: { bold: true, color: C.accent4 } }, { text: ops.join("   ·   ") }], { x: X0, y, w: ANCHO, h, fontSize: pt - 2, color: C.text1, margin: 0.02, isTextBox: true, objectName: "opciones" });
        y += h + 0.04;
      }
    }
    return y;
  };
  const pt = ajustar(construir);
  const slide = pres.addSlide({ masterName: "PREGUNTA", sectionTitle: seccion });
  slide.addText(r.titulo, { placeholder: "title" });
  etiqueta(slide, `${bloque} · ${r.puntos} pts`, C.background1, C.text2);
  etiqueta(slide, tipoTexto, C.text2, C.background2, X0 + 3.35, 0.22, 4.6);
  construir(slide, pt, true);
  slide.addNotes("Pregunta a la clase. Da tiempo para responder (o votar a mano alzada) antes de pasar a la respuesta.");
}

// ------------------------------------------------------- diapositiva respuesta
const ICONOS = {};

function cajaRespuesta(slide, r, y, dibujar) {
  // Recuadro superior con la respuesta correcta; devuelve el nuevo y.
  const pt = 16;
  let lineasResp = [];
  if (r.tipo === "mc" || r.tipo === "ma") lineasResp = r.correctas.map((i) => [{ t: `${LETRAS[i]})  `, b: true }, ...r.opciones[i]]);
  else if (r.tipo === "numerical") {
    const dec = r.tol < 0.1 ? 2 : r.tol < 1 ? 1 : 0;
    lineasResp = [[{ t: r.respuesta.toFixed(dec), b: true }]];
  }
  else if (r.tipo === "matching") {
    const n = r.pares.length + r.distractores.length, orden = Array.from({ length: n }, (_, i) => (2 * n - 1 - i + 3) % n);
    lineasResp = r.pares.map(([a, b], i) => [{ t: `${i + 1}–${LETRAS[orden.indexOf(i)]}  `, b: true }, { t: `${a} → ${b}` }]);
  } else if (r.tipo === "dropdowns") lineasResp = r.blancos.map(([k, ops, c]) => [{ t: `[${k}]  `, b: true }, { t: ops[c] }]);
  if (!lineasResp.length) return y;

  const grande = r.tipo === "numerical";
  const anchoTexto = ANCHO - 1.0;
  const ptR = pt - (lineasResp.length > 4 ? 2 : 0);
  const alto = grande ? 0.95 : Math.max(0.75, lineasResp.reduce((h, l) => h + (lineas(plano(l), anchoTexto, ptR) * ptR * 1.2) / 72, 0) + 0.3);
  if (dibujar) {
    slide.addShape(pres.ShapeType.roundRect, { x: X0, y, w: ANCHO, h: alto, fill: { color: C.background1 }, line: { color: C.accent1, width: 1.5 }, rectRadius: 0.12, objectName: "caja respuesta" });
    slide.addShape(pres.ShapeType.ellipse, { x: X0 + 0.22, y: y + Math.min(0.2, alto / 2 - 0.25), w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "circulo check" });
    slide.addImage({ data: ICONOS.check, x: X0 + 0.34, y: y + Math.min(0.2, alto / 2 - 0.25) + 0.12, w: 0.26, h: 0.26, altText: "Respuesta correcta" });
    const runs = [];
    lineasResp.forEach((l, i) => l.forEach((x, j) => {
      const o = opcRun(x, { color: C.text1 });
      if (j === l.length - 1 && i < lineasResp.length - 1) o.options.breakLine = true;
      runs.push(o);
    }));
    if (grande && r.tol) runs.push({ text: `   (se acepta ± ${r.tol})`, options: { fontSize: 14, color: C.accent6 } });
    slide.addText(runs, { x: X0 + 0.9, y: y + 0.08, w: anchoTexto, h: alto - 0.16, fontSize: grande ? 36 : pt - (lineasResp.length > 4 ? 2 : 0), color: C.text1, valign: "middle", margin: 0.02, isTextBox: true, objectName: "respuesta" });
  }
  return y + alto + 0.25;
}

// Divide la retroalimentación en «por qué sí» y «por qué no las demás».
function partirFb(fb) {
  const i = fb.findIndex((b) => b.tipo === "p" && /^Por qué no las demás/.test(plano(b.runs)));
  if (i < 0) return [fb, []];
  return [fb.slice(0, i), fb.slice(i)];
}

function columna(slide, titulo, icon, color, lista, x, y, w, pt, dibujar) {
  if (dibujar) {
    slide.addShape(pres.ShapeType.ellipse, { x, y, w: 0.36, h: 0.36, fill: { color }, line: { color }, objectName: "circulo icono" });
    slide.addImage({ data: icon, x: x + 0.09, y: y + 0.09, w: 0.18, h: 0.18, altText: titulo });
    slide.addText(titulo, { x: x + 0.48, y, w: w - 0.48, h: 0.36, fontSize: 16, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: "subtitulo" });
  }
  return bloques(slide, lista, x, y + 0.5, w, pt, dibujar);
}

function respuesta(r, bloque, seccion) {
  if (r.tipo === "essay") return respuestaEnsayo(r, bloque, seccion);
  let [si, no] = partirFb(r.fb);
  no = no.filter((b) => !/^Por qué no las demás/.test(plano(b.runs)));
  const construir = (slide, pt, dibujar) => {
    let y = cajaRespuesta(slide, r, 1.5, dibujar);
    if (no.length) {
      const w = (ANCHO - 0.4) / 2;
      const y1 = columna(slide, "Por qué es correcta", ICONOS.check, C.accent1, si, X0, y, w, pt, dibujar);
      const y2 = columna(slide, "Por qué fallan las demás", ICONOS.x, C.accent2, no, X0 + w + 0.4, y, w, pt, dibujar);
      return Math.max(y1, y2);
    }
    return columna(slide, "Explicación", ICONOS.foco, C.accent4, si, X0, y, ANCHO, pt, dibujar);
  };
  const pt = ajustar(construir, [19, 18, 17, 16, 15, 14, 13, 12]);
  const slide = pres.addSlide({ masterName: "RESPUESTA", sectionTitle: seccion });
  slide.addText(r.titulo, { placeholder: "title" });
  etiqueta(slide, `${bloque} · Respuesta`, C.background1, C.accent1);
  construir(slide, pt, true);
  slide.addNotes(r.fb.map((b) => (b.tipo === "p" ? (b.lista ? "• " : "") + plano(b.runs) : "")).filter(Boolean).join("\n"));
}

// Respuesta modelo de los casos: se separa por incisos a), b)... y la rúbrica va en una tarjeta.
function respuestaEnsayo(r, bloque, seccion) {
  const textoModelo = r.fb.map((b) => plano(b.runs)).find((t) => t.startsWith("Respuesta modelo")) || "";
  const rubrica = r.fb.map((b) => plano(b.runs)).find((t) => t.startsWith("Rúbrica")) || "";
  const partes = textoModelo.replace(/^Respuesta modelo\.\s*/, "").split(/\s(?=[a-e]\)\s)/).map((t) => t.trim()).filter(Boolean);
  const comoBloques = (ps) => ps.map((t) => {
    const m = t.match(/^([a-e]\))\s*(.*)$/s);
    return { tipo: "p", runs: m ? [{ t: m[1] + " ", b: true }, { t: m[2] }] : [{ t }] };
  });
  // Reparte los incisos en dos diapositivas si no caben en una.
  const grupos = [];
  let actual = [];
  const pt = 15, w = (ANCHO - 0.4) / 2;
  const altoGrupo = (ps) => {
    const mitad = Math.ceil(ps.length / 2);
    return Math.max(bloques(null, comoBloques(ps.slice(0, mitad)), X0, 1.5, w, pt, false), bloques(null, comoBloques(ps.slice(mitad)), X0, 1.5, w, pt, false));
  };
  for (const p of partes) {
    if (actual.length && altoGrupo([...actual, p]) > Y_FIN - 0.9) { grupos.push(actual); actual = []; }
    actual.push(p);
  }
  if (actual.length) grupos.push(actual);

  grupos.forEach((g, k) => {
    const slide = pres.addSlide({ masterName: "RESPUESTA", sectionTitle: seccion });
    slide.addText(grupos.length > 1 ? `${r.titulo} (${k + 1}/${grupos.length})` : r.titulo, { placeholder: "title" });
    etiqueta(slide, `${bloque} · Respuesta modelo`, C.background1, C.accent1);
    const mitad = Math.ceil(g.length / 2);
    bloques(slide, comoBloques(g.slice(0, mitad)), X0, 1.5, w, pt, true);
    bloques(slide, comoBloques(g.slice(mitad)), X0 + w + 0.4, 1.5, w, pt, true);
    if (k === grupos.length - 1 && rubrica) {
      const h = altoTexto(rubrica, ANCHO - 0.4, 13) + 0.1;
      slide.addShape(pres.ShapeType.roundRect, { x: X0, y: Y_FIN - h + 0.05, w: ANCHO, h, fill: { color: C.background1 }, line: { color: C.accent3, width: 1.25 }, rectRadius: 0.1, objectName: "rubrica" });
      slide.addText([{ text: "Rúbrica  ", options: { bold: true, color: C.text2 } }, { text: rubrica.replace(/^Rúbrica[^:]*:\s*/, "") }], { x: X0 + 0.2, y: Y_FIN - h + 0.1, w: ANCHO - 0.4, h: h - 0.1, fontSize: 13, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "rubrica texto" });
    }
    slide.addNotes(textoModelo + "\n\n" + rubrica);
  });
}

// ------------------------------------------------------------- portada y cierre
const TEMAS = {
  "Bloque 1": "Ómicas y dogma central · SNP, indels y CNV · Respuesta interindividual · TAS2R38 · PKU frente a lactasa · MTHFR · FTO · ALDH2",
  "Bloque 2": "Percepción sensorial (TAS2R38, OR6A2, OR2M7) · CYP1A2 y café · ALDH2 · APOE × alcohol · FTO · Lactosa: hipolactasia, malabsorción e intolerancia",
  "Bloque 3": "Lectura de secuencias · Gel de Alu PV92 · Ciclo de PCR · Columnas de sílice y extracción · UCSC, BLAST, Primer-BLAST · GWAS Catalog",
  "Bloque 4": "DPPH con blanco · IC₅₀ · FRAP · Catalasa · SOD · Troubleshooting de laboratorio",
};
const ICONO_BLOQUE = { "Bloque 1": "dna", "Bloque 2": "medico", "Bloque 3": "lap", "Bloque 4": "matraz" };

function divisor(nombre, seccion, n) {
  const clave = nombre.match(/^Bloque \d/)[0];
  const [, titulo, peso] = nombre.match(/^Bloque \d · (.*) \((\d+ %)\)$/) || [null, nombre, ""];
  const slide = pres.addSlide({ masterName: "DIVISOR", sectionTitle: seccion });
  slide.addText(`${clave}\n${titulo}`, { placeholder: "title" });
  slide.addText(TEMAS[clave] || "", { placeholder: "body" });
  slide.addShape(pres.ShapeType.ellipse, { x: 9.55, y: 1.75, w: 2.9, h: 2.9, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "circulo bloque" });
  slide.addImage({ data: ICONOS[ICONO_BLOQUE[clave]], x: 10.35, y: 2.55, w: 1.3, h: 1.3, altText: titulo });
  slide.addText([{ text: peso, options: { fontSize: 40, bold: true, breakLine: true } }, { text: `${n} reactivos`, options: { fontSize: 16 } }],
    { x: 9.25, y: 4.85, w: 3.5, h: 1.2, color: C.background1, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: "peso" });
}

const IDEAS = [
  ["Genotipo ≠ destino", "Las variantes comunes cambian probabilidades; la dieta y el ambiente modulan su efecto."],
  ["Gen asignado ≠ gen efector", "−13910 está en MCM6 pero regula LCT: lee el mecanismo, no solo la etiqueta."],
  ["Asociación ≠ causalidad", "Un p de GWAS diminuto indica certeza estadística, no un efecto grande."],
  ["Resta siempre el blanco", "Los pigmentos absorben cerca de 517 nm y falsean la inhibición y la IC₅₀."],
  ["Menor IC₅₀ = más potencia", "Es una concentración: cuanto menos extracto se necesita, más activo es."],
  ["Más enzima ≠ más salud", "SOD alta con catalasa baja acumula H₂O₂; integra todos los ensayos."],
];

async function main() {
  ICONOS.check = await icono(FaCheck, "FFFFFF");
  ICONOS.x = await icono(FaTimes, "FFFFFF");
  ICONOS.foco = await icono(FaLightbulb, "FFFFFF");
  ICONOS.dna = await icono(FaDna, "FFFFFF");
  ICONOS.medico = await icono(FaUserMd, "FFFFFF");
  ICONOS.lap = await icono(FaLaptopCode, "FFFFFF");
  ICONOS.matraz = await icono(FaFlask, "FFFFFF");

  pres.addSection({ title: "Inicio" });
  const port = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Inicio" });
  port.addText("Revisión del preexamen\nDel Genoma Crudo a la Clínica", { placeholder: "title" });
  const nReact = banco.reactivos.filter((r) => r.tipo !== "header").length;
  port.addText(`Respuestas explicadas · ${nReact} reactivos · ${banco.total} puntos\nNutrición Molecular`, { placeholder: "body" });
  port.addShape(pres.ShapeType.ellipse, { x: 10.2, y: 0.8, w: 2.4, h: 2.4, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "circulo portada" });
  port.addImage({ data: ICONOS.dna, x: 10.85, y: 1.45, w: 1.1, h: 1.1, altText: "DNA" });
  port.addNotes("Dinámica sugerida: muestra cada pregunta, da 1–2 minutos para que respondan y después pasa a la diapositiva de respuesta.");

  let bloque = "", seccion = "Inicio";
  const reactivos = banco.reactivos;
  for (let i = 0; i < reactivos.length; i++) {
    const r = reactivos[i];
    if (r.tipo === "header") {
      const nombre = (r.bloques[0]?.runs || []).map((x) => x.t).join("");
      if (!/^Bloque/.test(nombre)) continue;
      bloque = nombre.match(/^Bloque \d/)[0];
      seccion = nombre.replace(/ \(\d+ %\)$/, "");
      pres.addSection({ title: seccion });
      let n = 0;
      for (let j = i + 1; j < reactivos.length && reactivos[j].tipo !== "header"; j++) n++;
      divisor(nombre, seccion, n);
      continue;
    }
    pregunta(r, bloque, seccion);
    respuesta(r, bloque, seccion);
  }

  pres.addSection({ title: "Cierre" });
  const fin = pres.addSlide({ masterName: "PREGUNTA", sectionTitle: "Cierre" });
  fin.addText("Seis ideas que más se repiten en el examen", { placeholder: "title" });
  const cw = (ANCHO - 0.8) / 3, ch = 2.35;
  IDEAS.forEach(([t, d], k) => {
    const x = X0 + (k % 3) * (cw + 0.4), y = 1.6 + Math.floor(k / 3) * (ch + 0.35);
    fin.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: ch, fill: { color: C.background2 }, line: { color: C.background2 }, rectRadius: 0.12, objectName: "tarjeta idea" });
    circuloLetra(fin, String(k + 1), x + 0.3, y + 0.3, C.accent1, C.background1, 0.5);
    fin.addText(t, { x: x + 0.3, y: y + 0.95, w: cw - 0.6, h: 0.45, fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: "idea titulo" });
    fin.addText(d, { x: x + 0.3, y: y + 1.4, w: cw - 0.6, h: 0.85, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: "idea texto" });
  });

  await pres.writeFile({ fileName: salida });
  if (rutaTema) await require(rutaTema).applyTheme(salida, THEME);
}

main();
