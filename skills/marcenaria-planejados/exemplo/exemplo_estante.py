#!/usr/bin/env python3
"""Exemplo: estante de livros + escrivaninha com gaveta, num quarto de 3,00 x 3,20.

Rode a partir da pasta da skill:
  python exemplo/exemplo_estante.py
  python scripts/vistas_2d.py exemplo/saida/estante.json
  python scripts/plano_corte.py exemplo/saida/estante.json
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "scripts"))
from marcenaria import Projeto  # noqa: E402

# ============================ PARÂMETROS (mm) ================================
QUARTO_L, QUARTO_P, PE_DIREITO = 3000, 3200, 2600
E, E_FUNDO = 18, 6

EST_X0 = 0                  # estante encostada no canto (parede Y = 0)
EST_L, EST_P, EST_A = 1200, 300, 2100
EST_DIV = 1                 # divisórias verticais internas
PRATELEIRAS = (350, 700, 1050, 1400, 1750)   # alturas das faces superiores
RODAPE_H, RODAPE_RECUO = 80, 40

MESA_X0 = 1400              # escrivaninha ao lado da estante
MESA_L, MESA_P, MESA_A = 1200, 600, 750
GAV_L, GAV_FRENTE_H, FOLGA = 400, 150, 3
# ============================================================================

p = Projeto("Exemplo - estante e escrivaninha",
            poligono=[(0, 0), (QUARTO_L, 0), (QUARTO_L, QUARTO_P), (0, QUARTO_P)],
            pe_direito=PE_DIREITO)

# ------------------------------- ESTANTE -------------------------------------
g = "Estante"
p.box("Lateral esquerda", g, EST_X0, 0, 0, E, EST_P, EST_A, fita="frente")
p.box("Lateral direita", g, EST_X0 + EST_L - E, 0, 0, E, EST_P, EST_A, fita="frente")
vao = EST_L - 2 * E
p.box("Base", g, EST_X0 + E, 0, RODAPE_H, vao, EST_P, E, fita="frente")
p.box("Rodapé", g, EST_X0 + E, EST_P - RODAPE_RECUO - E, 0, vao, E, RODAPE_H)
p.box("Topo", g, EST_X0 + E, 0, EST_A - E, vao, EST_P, E, fita="frente")
p.box("Fundo", g, EST_X0 + E, 0, RODAPE_H, vao, E_FUNDO, EST_A - RODAPE_H - E, mat="fundo",
      obs="encaixado em rasgo de 6 mm nas laterais")
larg_mod = (vao - EST_DIV * E) / (EST_DIV + 1)
for k in range(EST_DIV):
    x = EST_X0 + E + (k + 1) * larg_mod + k * E
    p.box(f"Divisória {k+1}", g, x, E_FUNDO, RODAPE_H + E, E, EST_P - E_FUNDO, EST_A - RODAPE_H - 2 * E, fita="frente")
for k in range(EST_DIV + 1):
    x = EST_X0 + E + k * (larg_mod + E)
    for z in PRATELEIRAS:
        p.box(f"Prateleira m{k+1} z{z}", g, x, E_FUNDO, z - E, larg_mod, EST_P - E_FUNDO, E, fita="frente")

# ----------------------------- ESCRIVANINHA ----------------------------------
g = "Escrivaninha"
p.box("Tampo", g, MESA_X0, 0, MESA_A - E, MESA_L, MESA_P, E, fita="frente + 2 lados")
p.box("Lateral esquerda", g, MESA_X0, 0, 0, E, MESA_P, MESA_A - E, fita="frente")
p.box("Lateral direita", g, MESA_X0 + MESA_L - E, 0, 0, E, MESA_P, MESA_A - E, fita="frente")
p.box("Travessa traseira", g, MESA_X0 + E, 0, MESA_A - E - 100, MESA_L - 2 * E, E, 100)
# gaveta sob o tampo, junto à lateral direita
gx = MESA_X0 + MESA_L - E - GAV_L
p.box("Divisória da gaveta", g, gx - E, E, MESA_A - E - GAV_FRENTE_H - 20, E, MESA_P - E, GAV_FRENTE_H + 20, fita="frente")
p.box("Frente da gaveta", g, gx + FOLGA, MESA_P - E, MESA_A - E - GAV_FRENTE_H, GAV_L - 2 * FOLGA, E, GAV_FRENTE_H - FOLGA,
      fita="4 lados")
cx_l, cx_p, cx_h = GAV_L - 26, MESA_P - E - 40, GAV_FRENTE_H - 40     # 13 mm de corrediça de cada lado
cx0, cz0 = gx + 13, MESA_A - E - GAV_FRENTE_H + 10
p.box("Gaveta - lateral esq.", g, cx0, 20, cz0, 15, cx_p, cx_h, mat="mdf15")
p.box("Gaveta - lateral dir.", g, cx0 + cx_l - 15, 20, cz0, 15, cx_p, cx_h, mat="mdf15")
p.box("Gaveta - traseira", g, cx0 + 15, 20, cz0, cx_l - 30, 15, cx_h, mat="mdf15")
p.box("Gaveta - contrafrente", g, cx0 + 15, 20 + cx_p - 15, cz0, cx_l - 30, 15, cx_h, mat="mdf15")
p.box("Gaveta - fundo", g, cx0, 20, cz0 - 6, cx_l, cx_p, 6, mat="fundo")

p.exportar(os.path.join(AQUI, "saida"), "estante")
