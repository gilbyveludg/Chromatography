# Decisiones cromatográficas con evidencia

Actividad guiada (90 min) con simulador de cromatografía (HPLC y GC). Los equipos predicen, comprueban con el simulador y diagnostican cromatogramas. Al terminar se genera el **reporte en PDF** para subir a Classroom.

## Publicar en Netlify

Es un sitio estático, sin compilación:

- **Arrastrar y soltar:** en Netlify → *Add new site → Deploy manually*, arrastren la carpeta completa (con `index.html` y `vendor/`).
- **Desde GitHub:** *Import an existing project*, elijan este repositorio; `netlify.toml` ya indica publicar la raíz.

Deben subirse `index.html` **y** la carpeta `vendor/`: ahí están el generador de PDF y las fuentes. No dependen de CDN externos, así que el PDF funciona aunque la red escolar bloquee esos dominios.

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | La actividad completa (HTML, CSS y JS en un solo archivo). |
| `vendor/pdfmake-0.2.20.min.js` | [pdfmake](https://github.com/bpampuch/pdfmake) 0.2.20 (MIT), genera el PDF en el navegador. Se carga solo al llegar al reporte. |
| `vendor/report-fonts.js` | Subconjunto de las fuentes DejaVu Sans / Serif (licencia libre Bitstream Vera/DejaVu) con griego, flechas, ≥, √, ✓ ✗. |
| `netlify.toml` | Configuración de publicación y caché. |

## Cómo funciona el reporte

- El PDF se arma con texto real (seleccionable y ligero, ~150–250 KB), tamaño Carta, con encabezado, número de página, datos del equipo, puntajes, cada paso con su hora de envío y las imágenes de los tres cromatogramas de diagnóstico.
- Botones: **Descargar PDF**, **Abrir PDF en otra pestaña** y, en celulares, **Compartir PDF** (directo a Classroom o Drive). Alternativas: imprimir la página, copiar como texto o descargar el respaldo `.json`.
- El avance se guarda en el navegador (`localStorage`). El menú **Opciones** permite descargar/cargar un respaldo y reiniciar la actividad (útil en computadoras compartidas). Cargar un respaldo queda registrado en el reporte.
