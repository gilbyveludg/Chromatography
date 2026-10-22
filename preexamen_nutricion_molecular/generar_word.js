// Genera el Word del preexamen con respuestas a partir del JSON de exportar_json.py.
// Uso: node generar_word.js banco.json salida.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, LevelFormat, BorderStyle, Footer, PageNumber, PageBreak,
} = require("docx");

const [, , entrada, salida] = process.argv;
const banco = JSON.parse(fs.readFileSync(entrada, "utf8"));

const ANCHO = 9360; // 6.5" útiles en carta con márgenes de 1"
const VERDE = "1F6B3A", GRIS = "5A6470", AZUL = "1F4E79", FONDO_OK = "E6F2EA", FONDO_FB = "F3F5F8";
const LETRAS = "ABCDEFGHIJ";

const run = (r, extra = {}) => new TextRun({
  text: r.t, bold: r.b || extra.bold, italics: r.i, subScript: r.sub, superScript: r.sup,
  color: extra.color, size: extra.size,
});
const runs = (rs, extra) => rs.map((r) => run(r, extra));
const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 100 }, ...opts });
const texto = (t, extra = {}) => new TextRun({ text: t, ...extra });

function tabla(filas, anchos) {
  const n = filas[0].length;
  const cols = anchos || Array(n).fill(Math.floor(ANCHO / n));
  const borde = { style: BorderStyle.SINGLE, size: 4, color: "B8BEC6" };
  return new Table({
    width: { size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: cols,
    rows: filas.map((fila, i) => new TableRow({
      tableHeader: i === 0,
      children: fila.map((celda, j) => new TableCell({
        width: { size: cols[j], type: WidthType.DXA },
        borders: { top: borde, bottom: borde, left: borde, right: borde },
        shading: i === 0 ? { type: ShadingType.CLEAR, fill: "E9ECEF", color: "auto" } : undefined,
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [p(Array.isArray(celda) ? runs(celda, { size: 20 }) : [texto(celda, { size: 20, bold: i === 0 })], { spacing: { after: 0 } })],
      })),
    })),
  });
}

function bloques(lista, extra = {}) {
  const out = [];
  for (const b of lista) {
    if (b.tipo === "tabla") {
      out.push(tabla(b.filas));
      out.push(p([]));
    } else if (b.h) {
      out.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(b.runs) }));
    } else if (b.lista) {
      out.push(new Paragraph({ numbering: { reference: b.lista === "num" ? "numeros" : "vinetas", level: 0 }, children: runs(b.runs, extra), spacing: { after: 60 } }));
    } else {
      out.push(p(runs(b.runs, extra)));
    }
  }
  return out;
}

// Recuadro sombreado (respuesta o explicación): párrafos con fondo y borde izquierdo.
function recuadro(parrafos, fondo, color) {
  return parrafos.map((par) => new Paragraph({
    children: par,
    shading: { type: ShadingType.CLEAR, fill: fondo, color: "auto" },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color, space: 6 } },
    spacing: { after: 0 },
    indent: { left: 120, right: 120 },
  }));
}

// Orden fijo de la columna B: invertida y rotada, para que no quede alineada con la columna A.
function ordenColumnaB(r) {
  const n = r.pares.length + r.distractores.length;
  return Array.from({ length: n }, (_, i) => (2 * n - 1 - i + 3) % n);
}

function respuesta(r) {
  const etiqueta = texto("Respuesta: ", { bold: true, color: VERDE });
  switch (r.tipo) {
    case "mc":
    case "ma":
      return [[etiqueta, texto(r.correctas.map((i) => LETRAS[i]).join(", "), { bold: true, color: VERDE })]];
    case "numerical":
      return [[etiqueta, texto(`${r.respuesta}`, { bold: true, color: VERDE }), texto(`  (Canvas acepta ± ${r.tol})`, { color: GRIS })]];
    case "matching": {
      const orden = ordenColumnaB(r);
      const clave = r.pares.map((_, i) => `${i + 1}–${LETRAS[orden.indexOf(i)]}`).join(", ");
      return [[etiqueta, texto(clave, { bold: true, color: VERDE })], ...r.pares.map(([a, b]) => [texto(`${a} → `, { bold: true }), texto(b)])];
    }
    case "dropdowns":
      return [[etiqueta], ...r.blancos.map(([k, ops, c]) => [texto(`[${k}] `, { bold: true }), texto(ops[c])])];
    default:
      return [[texto("Calificación manual con la rúbrica de abajo.", { bold: true, color: VERDE })]];
  }
}

function reactivo(r) {
  const out = [new Paragraph({
    heading: HeadingLevel.HEADING_3,
    keepNext: true,
    children: [texto(r.titulo), texto(`   ${r.puntos} pts`, { color: GRIS, bold: false, size: 20 })],
  })];
  out.push(...bloques(r.enunciado));

  if (r.tipo === "mc" || r.tipo === "ma") {
    r.opciones.forEach((op, i) => {
      const ok = r.correctas.includes(i);
      out.push(new Paragraph({
        indent: { left: 360, hanging: 360 },
        spacing: { after: 60 },
        children: [texto(`${LETRAS[i]})  `, { bold: true, color: ok ? VERDE : undefined }), ...runs(op, ok ? { color: VERDE, bold: true } : {})],
      }));
    });
  } else if (r.tipo === "matching") {
    const der = [...r.pares.map((x) => x[1]), ...r.distractores];
    const filas = [["Columna A", "Columna B (en desorden; una sobra)"]];
    const orden = ordenColumnaB(r);
    for (let i = 0; i < der.length; i++) filas.push([r.pares[i] ? `${i + 1}. ${r.pares[i][0]}` : "", `${LETRAS[i]}) ${der[orden[i]]}`]);
    out.push(tabla(filas, [4680, 4680]));
    out.push(p([]));
  } else if (r.tipo === "dropdowns") {
    for (const [k, ops] of r.blancos) out.push(p([texto(`[${k}]  `, { bold: true }), texto(ops.join("  ·  "), { color: GRIS })], { indent: { left: 360 }, spacing: { after: 40 } }));
  }

  out.push(p([], { spacing: { after: 60 } }));
  out.push(...recuadro(respuesta(r), FONDO_OK, VERDE));
  const fb = r.fb.map((b) => (b.tipo === "p" ? runs(b.runs, { size: 20 }) : null)).filter(Boolean);
  out.push(...recuadro(fb, FONDO_FB, AZUL));
  out.push(p([], { spacing: { after: 200 } }));
  return out;
}

const cuerpo = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [texto(banco.titulo)] }),
  p([texto(`Versión docente con respuestas · ${banco.total} puntos · ${banco.minutos} minutos`, { color: GRIS })]),
  p([texto("Las letras de las opciones siguen el orden del banco. En Canvas las opciones se barajan, así que el alumno las ve en otro orden.", { italics: true, color: GRIS, size: 20 })]),
  ...bloques(banco.descripcion),
];

let primeraSeccion = true;
for (const r of banco.reactivos) {
  if (r.tipo === "header") {
    const esSeccion = r.bloques[0] && r.bloques[0].h && /^Secci/.test(r.bloques[0].runs.map((x) => x.t).join(""));
    if (esSeccion && !primeraSeccion) cuerpo.push(new Paragraph({ children: [new PageBreak()] }));
    if (esSeccion) primeraSeccion = false;
    for (const b of r.bloques) {
      if (b.h) cuerpo.push(new Paragraph({ heading: esSeccion ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2, children: runs(b.runs) }));
      else cuerpo.push(...bloques([b]));
    }
  } else {
    cuerpo.push(...reactivo(r));
  }
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 40, bold: true, color: AZUL }, paragraph: { spacing: { after: 120 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: AZUL }, paragraph: { spacing: { before: 120, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: AZUL }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, color: "222222" }, paragraph: { spacing: { before: 240, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numeros", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [texto("Preexamen Nutrición Molecular · versión docente · ", { color: GRIS, size: 18 }), new TextRun({ children: [PageNumber.CURRENT], color: GRIS, size: 18 })] })] }),
    },
    children: cuerpo,
  }],
});

Packer.toBuffer(doc).then((buf) => fs.writeFileSync(salida, buf));
