#!/usr/bin/env python3
"""Folha 2D automática (A3) a partir do JSON gerado por marcenaria.py.

Uso:
  python vistas_2d.py projeto.json                 # todos os grupos
  python vistas_2d.py projeto.json --grupo Estante # só um grupo (pode repetir --grupo)
  python vistas_2d.py projeto.json --rev B

Gera {base}_vistas.pdf e {base}_vistas.png com três projeções ortogonais e cotas gerais:
  - Planta (X x Y, vista de cima) com o polígono do cômodo
  - Elevação frontal (X x Z, olhando de Y+ para a parede Y = 0)
  - Elevação lateral (Y x Z, olhando de X+ para a parede X = 0)

Painéis são desenhados como retângulos de arestas finas; profundidade é ignorada
(é uma projeção, não um corte). Para folhas de execução detalhadas, escreva um
script próprio do cômodo usando esta como base.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle


def cota(ax, a, b, pos, horizontal=True, txt=None, fs=7):
    """Linha de cota simples entre a e b, na coordenada pos."""
    txt = txt or f"{abs(b - a):.0f}"
    if horizontal:
        ax.annotate("", (a, pos), (b, pos), arrowprops=dict(arrowstyle="<->", lw=0.6))
        ax.text((a + b) / 2, pos, txt, ha="center", va="bottom", fontsize=fs)
    else:
        ax.annotate("", (pos, a), (pos, b), arrowprops=dict(arrowstyle="<->", lw=0.6))
        ax.text(pos, (a + b) / 2, txt, ha="right", va="center", rotation=90, fontsize=fs)


def projetar(ax, pecas, eixo_h, eixo_v, cores, titulo):
    xs, ys = [], []
    # desenha primeiro o que está mais "atrás" para a frente sobrepor
    for p in pecas:
        h0, dh = p[eixo_h], p["d" + eixo_h]
        v0, dv = p[eixo_v], p["d" + eixo_v]
        ax.add_patch(Rectangle((h0, v0), dh, dv, fc=cores.get(p["mat_key"], "#ddd"), ec="#222", lw=0.4, alpha=0.55))
        xs += [h0, h0 + dh]
        ys += [v0, v0 + dv]
    if xs:
        h0, h1, v0, v1 = min(xs), max(xs), min(ys), max(ys)
        m = max(h1 - h0, v1 - v0) * 0.06
        cota(ax, h0, h1, v0 - m, True)
        cota(ax, v0, v1, h0 - m, False)
        ax.set_xlim(h0 - 2.2 * m, h1 + m)
        ax.set_ylim(v0 - 2.2 * m, v1 + m)
    ax.set_aspect("equal")
    ax.set_title(titulo, fontsize=10, loc="left")
    ax.axis("off")


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        raise SystemExit(__doc__)
    caminho = args[0]
    grupos = [args[k + 1] for k, a in enumerate(args) if a == "--grupo"]
    rev = next((args[k + 1] for k, a in enumerate(args) if a == "--rev"), "A")
    dados = json.load(open(caminho, encoding="utf-8"))
    amb = dados.get("ambiente", {})
    pecas = [p for p in dados["pecas"] if not grupos or p["grupo"] in grupos]
    cores = {k: m.get("cor", "#ddd") for k, m in dados.get("materiais", {}).items()}
    base = os.path.splitext(caminho)[0]

    fig = plt.figure(figsize=(16.54, 11.69))   # A3 paisagem
    ax_pl = fig.add_axes([0.03, 0.10, 0.42, 0.80])
    ax_fr = fig.add_axes([0.50, 0.42, 0.47, 0.50])
    ax_la = fig.add_axes([0.50, 0.08, 0.47, 0.32])

    poly = amb.get("poligono") or []
    if len(poly) >= 3:
        ax_pl.add_patch(Polygon(poly, closed=True, fc="none", ec="#555", lw=1.6))
    projetar(ax_pl, pecas, "x", "y", cores, "Planta (vista de cima) - X x Y")
    if len(poly) >= 3:
        pxs, pys = [q[0] for q in poly], [q[1] for q in poly]
        m = max(max(pxs) - min(pxs), max(pys) - min(pys)) * 0.06
        ax_pl.set_xlim(min(pxs) - 2.2 * m, max(pxs) + m)
        ax_pl.set_ylim(min(pys) - 2.2 * m, max(pys) + m)
        ax_pl.invert_yaxis()   # Y cresce para dentro do cômodo (para baixo no papel)
    projetar(ax_fr, pecas, "x", "z", cores, "Elevação frontal - X x Z")
    projetar(ax_la, pecas, "y", "z", cores, "Elevação lateral - Y x Z")
    pd = amb.get("pe_direito")
    if pd:
        for ax in (ax_fr, ax_la):
            ax.axhline(pd, color="#999", lw=0.6, ls="--")

    titulo = amb.get("titulo", os.path.basename(base)) + (f" - {', '.join(grupos)}" if grupos else "")
    fig.text(0.03, 0.95, titulo, fontsize=16, weight="bold")
    fig.text(0.03, 0.04, f"Medidas em mm · {len(pecas)} painéis · projeções sem escala fixa · rev. {rev}",
             fontsize=9)
    fig.savefig(f"{base}_vistas.pdf")
    fig.savefig(f"{base}_vistas.png", dpi=110)
    print(f"gerado: {base}_vistas.pdf e .png ({len(pecas)} painéis)")


if __name__ == "__main__":
    main()
