# -*- coding: utf-8 -*-
"""Genera las figuras con datos simulados del examen (carpeta figuras/).

Uso: python3 figuras_examen.py
Los datos son ilustrativos (semilla fija), construidos para que cada figura muestre un hallazgo claro.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "figuras")
os.makedirs(SALIDA, exist_ok=True)

TINTA, GRIS, REJILLA = "#1B2B34", "#6C757D", "#E3E7EA"
VERDE, CORAL, AZUL, AMBAR = "#2A9D8F", "#E76F51", "#264653", "#D4A017"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GRIS, "axes.labelcolor": TINTA,
    "xtick.color": TINTA, "ytick.color": TINTA, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 12, "axes.titlecolor": TINTA,
})


def guardar(fig, nombre):
    fig.savefig(os.path.join(SALIDA, nombre), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def rejilla(ax, eje="y"):
    ax.grid(axis=eje, color=REJILLA, linewidth=0.8)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- E1-1
def lactasa_por_genotipo():
    rng = np.random.default_rng(11)
    datos = {
        "C/C": rng.normal(8, 2.5, 12).clip(2),
        "C/T": rng.normal(36, 6, 12),
        "T/T": np.append(rng.normal(41, 6, 11), 9.5),  # un T/T con actividad baja
    }
    colores = [CORAL, AMBAR, VERDE]
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    for i, ((g, v), c) in enumerate(zip(datos.items(), colores)):
        x = i + rng.uniform(-0.12, 0.12, len(v))
        ax.scatter(x, v, s=38, color=c, edgecolor="white", linewidth=0.6, zorder=3)
        ax.hlines(np.median(v), i - 0.25, i + 0.25, color=TINTA, linewidth=2, zorder=4)
    ax.annotate("Persona 36", xy=(2 + 0.0, 9.5), xytext=(2.32, 16), fontsize=9.5, color=TINTA,
                arrowprops=dict(arrowstyle="-", color=GRIS, lw=0.8))
    ax.axhline(15, color=GRIS, linestyle="--", linewidth=1)
    ax.text(-0.45, 16, "Límite de actividad baja", fontsize=9.5, color=GRIS)
    ax.set_xticks(range(3), [f"{g}\n(n = 12)" for g in datos])
    ax.set_xlim(-0.5, 2.7)
    ax.set_ylim(0, 60)
    ax.set_ylabel("Actividad de lactasa\n(U/g de proteína)")
    ax.set_xlabel("Genotipo MCM6 −13910")
    ax.set_title("Actividad de lactasa en biopsias de adultos (datos simulados)")
    ax.text(2.7, 57, "— mediana", fontsize=9.5, color=TINTA, ha="right")
    rejilla(ax)
    guardar(fig, "e1-1_lactasa.png")


# ---------------------------------------------------------------- E1-3
def gel_y_amilasa():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw={"width_ratios": [1, 1.25]})
    # Panel A: gel de PCR de punto final (fondo oscuro, bandas claras)
    carriles = ["M", "P1", "P2", "P3", "P4"]
    alto, ancho = 300, 250
    img = np.zeros((alto, ancho))
    yy = np.arange(alto)[:, None]

    def banda(cx, y, intensidad, grosor=3.0):
        xs = np.arange(ancho)[None, :]
        perfil_x = 1 / (1 + np.exp(-(xs - (cx - 17)) * 1.2)) * (1 - 1 / (1 + np.exp(-(xs - (cx + 17)) * 1.2)))
        return intensidad * np.exp(-((yy - y) ** 2) / (2 * grosor ** 2)) * perfil_x

    pos = [30 + 47 * i for i in range(5)]
    escalera = {1000: 40, 700: 80, 500: 115, 400: 140, 300: 170, 200: 210, 100: 260}
    for y in escalera.values():
        img += banda(pos[0], y, 0.55, 2.4)
    for p in pos[1:]:
        img += banda(p, 182, 1.0, 3.4)  # mismo tamaño e intensidad en las cuatro personas
    img += np.random.default_rng(3).normal(0, 0.03, img.shape)
    ax1.imshow(img.clip(0, 1), cmap="gray", aspect="auto", vmin=0, vmax=1)
    ax1.set_xticks(pos, carriles)
    ax1.set_yticks([escalera[k] for k in (1000, 500, 300, 100)], ["1000", "500", "300", "100"])
    ax1.set_ylabel("Tamaño (pb)")
    ax1.tick_params(length=0)
    for s in ax1.spines.values():
        s.set_visible(False)
    ax1.set_title("A. PCR de punto final de AMY1")
    # Panel B: copias contadas por otro método frente a amilasa en saliva
    rng = np.random.default_rng(5)
    copias = np.repeat([2, 4, 6, 8, 10, 12, 14], 4)
    actividad = 18 + 9.5 * copias + rng.normal(0, 12, copias.size)
    ax2.scatter(copias + rng.uniform(-0.25, 0.25, copias.size), actividad, s=34, color=VERDE, edgecolor="white", linewidth=0.6, zorder=3)
    for persona, (c, a) in {"P1": (2, 38), "P2": (6, 70), "P3": (10, 112), "P4": (14, 150)}.items():
        ax2.scatter([c], [a], s=70, facecolor="none", edgecolor=AZUL, linewidth=1.6, zorder=4)
        ax2.text(c + 0.35, a - 9, persona, fontsize=9.5, color=AZUL, fontweight="bold")
    ax2.set_xlabel("Copias del gen AMY1 por persona")
    ax2.set_ylabel("Actividad de amilasa en saliva (U/mL)")
    ax2.set_xticks([2, 4, 6, 8, 10, 12, 14])
    ax2.set_title("B. Copias del gen y actividad")
    rejilla(ax2)
    fig.suptitle("Datos simulados", x=0.99, ha="right", fontsize=9.5, color=GRIS)
    fig.tight_layout()
    guardar(fig, "e1-3_amy1.png")


# ---------------------------------------------------------------- E1-4
def yogur_betaglucano():
    rng = np.random.default_rng(21)
    cambios = np.concatenate([rng.normal(-14, 3, 7), rng.normal(-4, 2.5, 7), rng.normal(1.5, 2, 6)])
    cambios = np.sort(cambios)
    colores = [VERDE if c <= -10 else (GRIS if c <= 0 else CORAL) for c in cambios]
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.bar(range(1, 21), cambios, color=colores, width=0.72, zorder=3)
    media = cambios.mean()
    ax.axhline(media, color=AZUL, linestyle="--", linewidth=1.4, zorder=4)
    ax.text(20.6, media - 0.2, f"Promedio\n{media:.1f} %", fontsize=9.5, color=AZUL, va="center")
    ax.axhline(0, color=TINTA, linewidth=0.8)
    ax.set_xticks(range(1, 21))
    ax.tick_params(axis="x", labelsize=8.5)
    ax.set_xlim(0.3, 23.2)
    ax.set_xlabel("Participante (ordenados de mayor a menor reducción)")
    ax.set_ylabel("Cambio en LDL (%)")
    ax.set_title("Yogur con 3 g/día de β-glucano de avena, 4 semanas (datos simulados)")
    rejilla(ax)
    guardar(fig, "e1-4_betaglucano.png")
    return media


# ---------------------------------------------------------------- E1-9
def acetaldehido_aldh2():
    t = np.linspace(0, 180, 200)

    def curva(pico, t_pico=30, k=0.022):
        return pico * (t / t_pico) * np.exp(1 - t / t_pico) ** 1 * np.exp(-k * np.clip(t - t_pico, 0, None) * 0)

    def bateman(pico, ka=0.09, ke=0.025):
        c = np.exp(-ke * t) - np.exp(-ka * t)
        return pico * c / c.max()

    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    for nombre, pico, color in (("ALDH2 *1/*1", 3, VERDE), ("ALDH2 *1/*2", 19, AMBAR), ("ALDH2 *2/*2", 46, CORAL)):
        y = bateman(pico)
        ax.plot(t, y, color=color, linewidth=2.4, label=nombre)
        ax.text(t[y.argmax()] + 4, pico + 1.2, f"{pico} µM", fontsize=9.5, color=color, fontweight="bold")
    ax.set_xlabel("Minutos después de una bebida estándar")
    ax.set_ylabel("Acetaldehído en sangre (µM)")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 52)
    ax.set_xticks(range(0, 181, 30))
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("Acetaldehído en sangre según genotipo ALDH2 (datos simulados)")
    rejilla(ax)
    guardar(fig, "e1-9_aldh2.png")
    del curva


# ---------------------------------------------------------------- E1-10
def cafeina_cyp1a2():
    t = np.linspace(0, 12, 300)  # horas desde las 16:00

    def perfil(t12, ka=3.0, pico=6.0):
        ke = np.log(2) / t12
        c = (np.exp(-ke * t) - np.exp(-ka * t))
        return pico * c / c.max()

    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    for nombre, t12, color in (("A/A (rápido)", 2.5, VERDE), ("C/C (lento)", 5.0, CORAL)):
        ax.plot(t, perfil(t12), color=color, linewidth=2.4, label=nombre)
    ax.axhline(3, color=GRIS, linestyle=":", linewidth=1)
    ax.text(11.9, 3.15, "mitad del máximo", fontsize=9, color=GRIS, ha="right")
    ax.axvline(7, color=AZUL, linestyle="--", linewidth=1.2)
    ax.text(6.88, 0.35, "23:00 · hora de dormir", fontsize=9.5, color=AZUL, ha="right")
    horas = list(range(0, 13, 2))
    ax.set_xticks(horas, [f"{(16 + h) % 24:02d}:00" for h in horas])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)
    ax.set_xlabel("Hora (café de 200 mg a las 16:00)")
    ax.set_ylabel("Cafeína en plasma (mg/L)")
    ax.legend(frameon=False, title="CYP1A2 rs762551", loc="upper right")
    ax.set_title("Cafeína en plasma según genotipo CYP1A2 (datos simulados)")
    rejilla(ax)
    guardar(fig, "e1-10_cafeina.png")
    return {n: perfil(t12)[np.searchsorted(t, 7)] for n, t12 in (("A/A", 2.5), ("C/C", 5.0))}


if __name__ == "__main__":
    lactasa_por_genotipo()
    gel_y_amilasa()
    print("promedio beta-glucano:", round(yogur_betaglucano(), 1))
    acetaldehido_aldh2()
    print("cafeína a las 23:00:", {k: round(v, 2) for k, v in cafeina_cyp1a2().items()})
