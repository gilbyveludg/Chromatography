// Genera el Word del preexamen: primero el examen (sin respuestas) y al final la clave completa.
// Uso: node generar_word.js banco.json salida.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, LevelFormat, BorderStyle, Footer, PageNumber, PageBreak,
} = require("docx");

const [, , entrada, salida] = process.argv;
const banco = JSON.parse(fs.readFileSync(entrada, "utf8"));

const ANCHO = 9360; // 6.5" útiles en carta con márgenes de 1"
const VERDE = "1F6B3A", GRIS = "5A6470", AZUL = "1F4E79", FONDO_OK = "E6F2EA";
const LETRAS = "ABCDEFGHIJ";

const run = (r, extra = {}) => new TextRun({
  text: r.t, bold: r.b || extra.bold, italics: r.i, subScript: r.sub, superScript: r.sup,
  font: r.m ? "Consolas" : undefined, color: extra.color, size: extra.size,
});
const runs = (rs, extra) => rs.map((r) => run(r, extra));
const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 100 }, ...opts });
const texto = (t, extra = {}) => new TextRun({ text: t, ...extra });
const salto = () => new Paragraph({ children: [new PageBreak()] });

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
      out.push(p([], { spacing: { after: 60 } }));
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

// Orden fijo de la columna B: invertida y rotada, para que no quede alineada con la columna A.
function ordenColumnaB(r) {
  const n = r.pares.length + r.distractores.length;
  return Array.from({ length: n }, (_, i) => (2 * n - 1 - i + 3) % n);
}

const tituloReactivo = (r, extra = "") => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  keepNext: true,
  children: [texto(r.titulo), texto(`   ${r.puntos} pts${extra}`, { color: GRIS, bold: false, size: 20 })],
});

// ---------------------------------------------------------------- examen
function pregunta(r) {
  const out = [tituloReactivo(r), ...bloques(r.enunciado)];
  if (r.tipo === "mc" || r.tipo === "ma") {
    if (r.tipo === "ma") out.push(p([texto("Marca todas las correctas.", { italics: true, color: GRIS, size: 20 })]));
    r.opciones.forEach((op, i) => out.push(new Paragraph({
      indent: { left: 360, hanging: 360 }, spacing: { after: 60 },
      children: [texto(`${LETRAS[i]})  `, { bold: true }), ...runs(op)],
    })));
  } else if (r.tipo === "matching") {
    const der = [...r.pares.map((x) => x[1]), ...r.distractores];
    const orden = ordenColumnaB(r);
    const filas = [["Columna A", "Columna B (una opción sobra)"]];
    for (let i = 0; i < der.length; i++) filas.push([r.pares[i] ? `${i + 1}. ${r.pares[i][0]}` : "", `${LETRAS[i]}) ${der[orden[i]]}`]);
    out.push(tabla(filas, [3600, 5760]));
  } else if (r.tipo === "dropdowns") {
    out.push(p([texto("Opciones para cada espacio:", { italics: true, color: GRIS, size: 20 })]));
    for (const [k, ops] of r.blancos) {
      out.push(p([texto(`[${k}]  `, { bold: true }), texto(ops.join("   ·   "), { size: 20 })], { indent: { left: 360 }, spacing: { after: 40 } }));
    }
  } else if (r.tipo === "numerical") {
    out.push(p([texto("Resultado: ______________", { bold: true })]));
  } else if (r.tipo === "essay") {
    for (let i = 0; i < 10; i++) out.push(p([], { border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "C8CDD3", space: 8 } }, spacing: { after: 160 } }));
  }
  out.push(p([], { spacing: { after: 160 } }));
  return out;
}

// ----------------------------------------------------------------- clave
function respuesta(r) {
  const verde = { bold: true, color: VERDE };
  switch (r.tipo) {
    case "mc":
    case "ma":
      return [texto("Respuesta: ", verde), texto(r.correctas.map((i) => LETRAS[i]).join(", "), verde)];
    case "numerical":
      return [texto("Respuesta: ", verde), texto(`${r.respuesta}`, verde), texto(`   (Canvas acepta ± ${r.tol})`, { color: GRIS })];
    case "matching": {
      const orden = ordenColumnaB(r);
      return [texto("Respuesta: ", verde), texto(r.pares.map((_, i) => `${i + 1}–${LETRAS[orden.indexOf(i)]}`).join(", "), verde)];
    }
    case "dropdowns":
      return [texto("Respuesta: ", verde), texto(r.blancos.map(([k, ops, c]) => `[${k}] ${ops[c]}`).join("; "), verde)];
    default:
      return [texto("Calificación con la rúbrica (respuesta modelo abajo).", verde)];
  }
}

function clave(r) {
  return [
    tituloReactivo(r),
    new Paragraph({
      children: respuesta(r),
      shading: { type: ShadingType.CLEAR, fill: FONDO_OK, color: "auto" },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: VERDE, space: 6 } },
      spacing: { after: 80 }, indent: { left: 120, right: 120 },
    }),
    ...bloques(r.fb, { size: 21 }),
  ];
}

// ------------------------------------------------------------ documento
const reactivos = banco.reactivos;
const esBloque = (r) => r.tipo === "header" && /^Bloque/.test((r.bloques[0]?.runs || []).map((x) => x.t).join(""));
const nombreBloque = (r) => r.bloques[0].runs.map((x) => x.t).join("");

const cuerpo = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [texto(banco.titulo)] }),
  p([texto(`${banco.total} puntos · ${banco.minutos} minutos`, { color: GRIS })]),
  p([texto("Nombre: ____________________________________   Código: ______________   Fecha: ____________")], { spacing: { after: 200 } }),
  ...bloques(banco.descripcion),
];

let primero = true;
for (const r of reactivos) {
  if (r.tipo === "header") {
    const bloque = esBloque(r);
    if (bloque && !primero) cuerpo.push(salto());
    if (bloque) primero = false;
    for (const b of r.bloques) {
      if (b.h) cuerpo.push(new Paragraph({ heading: bloque ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2, children: runs(b.runs) }));
      else cuerpo.push(...bloques([b]));
    }
  } else {
    cuerpo.push(...pregunta(r));
  }
}

cuerpo.push(salto());
cuerpo.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [texto("Clave de respuestas y rúbrica")] }));
cuerpo.push(p([texto("Para el docente. Cada reactivo incluye la justificación de la respuesta correcta y por qué fallan las alternativas. "
  + "Las letras siguen el orden de este documento; en Canvas las opciones se barajan.", { italics: true, color: GRIS })]));
for (const r of reactivos) {
  if (esBloque(r)) cuerpo.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [texto(nombreBloque(r))] }));
  else if (r.tipo !== "header") cuerpo.push(...clave(r));
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 40, bold: true, color: AZUL }, paragraph: { spacing: { after: 120 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: AZUL }, paragraph: { spacing: { before: 120, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: AZUL }, paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 1 } },
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
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [texto("Preexamen · Del Genoma Crudo a la Clínica · ", { color: GRIS, size: 18 }), new TextRun({ children: [PageNumber.CURRENT], color: GRIS, size: 18 })] })] }),
    },
    children: cuerpo,
  }],
});

Packer.toBuffer(doc).then((buf) => fs.writeFileSync(salida, buf));
