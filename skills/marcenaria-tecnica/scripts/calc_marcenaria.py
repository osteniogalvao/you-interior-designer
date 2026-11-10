#!/usr/bin/env python3
"""Calculadoras de marcenaria (sem dependências externas).

Subcomandos:
  portas      medidas de portas de abrir, nº e posição das dobradiças, furo do caneco
  gaveta      caixa de gaveta para corrediça telescópica ou oculta
  ripado      módulo de ripas e largura da porta mimetizada para a junta cair num vão
  prateleira  flecha estimada de prateleira (vão livre) e vão máximo recomendado
  sistema32   posições dos furos de 5 mm numa lateral (linha de 32 mm)

Exemplos:
  python calc_marcenaria.py portas --largura 800 --altura 2000 --n 2 --tipo sobreposta
  python calc_marcenaria.py gaveta --vao 564 --profundidade 520 --corredica telescopica --altura-lateral 120
  python calc_marcenaria.py ripado --ripa 40 --vao 15 --porta 800 --altura 2400
  python calc_marcenaria.py prateleira --vao 900 --espessura 18 --profundidade 300 --carga livros
  python calc_marcenaria.py sistema32 --altura 2000 --espessura-base 18

Todas as medidas em mm. Os padrões seguem a prática brasileira de móveis planejados
em MDF. Sempre confira no catálogo da ferragem escolhida (Blum, Hettich, Salice,
Häfele, FGV, Hafele, Telescópica nacional) antes de liberar a furação.
"""
import argparse
import math

DENS_MDF = 0.75  # g/cm³ ~ 750 kg/m³ (MDF 15-18 mm típico 700-780)


def peso_painel_kg(l, a, esp, dens=DENS_MDF):
    return l * a * esp * dens / 1e6


# ------------------------------------------------------------------ portas
def n_dobradicas(altura, peso):
    """Regra prática (tabelas Blum/Salice): por altura e peso, o que for maior."""
    por_altura = 2 if altura <= 900 else 3 if altura <= 1600 else 4 if altura <= 2000 else 5
    por_peso = 2 if peso <= 7 else 3 if peso <= 13 else 4 if peso <= 17 else 5 if peso <= 22 else 6
    return max(por_altura, por_peso)


def posicoes_dobradicas(altura, n, borda=100):
    if n == 1:
        return [altura / 2]
    passo = (altura - 2 * borda) / (n - 1)
    return [round(borda + i * passo, 1) for i in range(n)]


def cmd_portas(a):
    n = a.n
    if a.tipo == "sobreposta":
        # vão = medida EXTERNA do corpo; folga nas bordas externas e entre portas
        larg = (a.largura - 2 * a.folga_borda - (n - 1) * a.folga) / n
        alt = a.altura - 2 * a.folga_borda
        nota = "Medidas a partir da largura/altura EXTERNA do corpo (sobreposição total)."
    else:
        larg = (a.largura - 2 * a.folga - (n - 1) * a.folga) / n
        alt = a.altura - 2 * a.folga
        nota = "Medidas a partir do vão INTERNO (porta embutida / dobradiça supercurva)."
    peso = peso_painel_kg(larg, alt, a.espessura) + a.peso_extra
    nd = n_dobradicas(alt, peso)
    pos = posicoes_dobradicas(alt, nd, a.borda_dobradica)
    centro_caneco = a.c + 17.5
    print(f"Portas: {n} x {larg:.1f} (L) x {alt:.1f} (A) x {a.espessura} mm  [{a.tipo}]")
    print(f"  {nota}")
    print(f"  Peso estimado por porta: {peso:.1f} kg (MDF {DENS_MDF*1000:.0f} kg/m³"
          + (f" + {a.peso_extra} kg de extras" if a.peso_extra else "") + ")")
    print(f"  Dobradiças por porta: {nd}  (regra altura/peso; confira no catálogo)")
    print(f"  Centros a partir do topo da porta (mm): {', '.join(str(p) for p in pos)}")
    print(f"  Caneco Ø35: distância C = {a.c} mm da borda -> centro a {centro_caneco:.1f} mm da borda;"
          f" profundidade 11-13 mm")
    print(f"  Furos de fixação do caneco (se cavilhado): Ø8, a ±22,5 mm do eixo e 9,5 mm para dentro do centro")
    print(f"  Calço/base na lateral: linha a 37 mm da borda frontal, furos a 32 mm (sistema 32)")
    if larg > 600:
        print("  ATENÇÃO: porta de abrir acima de 600 mm de largura: verifique peso, empenamento e giro.")
    if alt > 2000:
        print("  ATENÇÃO: porta acima de 2,00 m: preveja desempenador (perfil de aço/alumínio embutido).")


# ------------------------------------------------------------------ gaveta
NOMINAIS = [250, 300, 350, 400, 450, 500, 550, 600, 650, 700]


def cmd_gaveta(a):
    folga_fundo = 10 if a.corredica == "telescopica" else 3
    nominal = a.nominal or max([x for x in NOMINAIS if x <= a.profundidade - folga_fundo] or [0])
    if not nominal:
        raise SystemExit("Profundidade interna pequena demais para as corrediças padrão.")
    esp_lat = a.espessura_lateral
    if a.corredica == "telescopica":
        larg_ext = a.vao - 2 * a.folga_corredica
        comp = nominal
        print(f"Gaveta com corrediça telescópica {nominal} mm (folga {a.folga_corredica} mm por lado)")
        print(f"  Caixa: largura externa {larg_ext:.1f} x comprimento {comp} x altura {a.altura_lateral}")
        print(f"  Laterais: 2 x {comp} x {a.altura_lateral} x {esp_lat}")
        print(f"  Frente/traseira internas: 2 x {larg_ext - 2*esp_lat:.1f} x {a.altura_lateral} x {esp_lat}"
              " (laterais passantes)")
        print(f"  Fundo: {larg_ext - 2*esp_lat + 2*a.rasgo:.1f} x {comp - 2*esp_lat + 2*a.rasgo:.1f} x 6"
              f" em rasgo de {a.rasgo} mm a 10 mm da base")
        print("  Corrediça: centro na altura da lateral; 1º furo a 37 mm da frente do corpo (lateral do móvel)")
    else:
        larg_int = a.vao - 42  # padrão Tandem/Movento p/ laterais 16 mm
        comp = nominal - 10
        print(f"Gaveta com corrediça oculta (tipo Tandem/Movento) {nominal} mm, laterais {esp_lat} mm")
        print(f"  Largura INTERNA da gaveta = vão - 42 = {larg_int:.1f} mm (válido p/ laterais 16 mm;"
              " outras espessuras: consulte o catálogo)")
        print(f"  Comprimento da gaveta = nominal - 10 = {comp} mm")
        print(f"  Fundo (16 mm recomendado) recuado 13 mm da base das laterais; traseira com recorte p/ ferragem")
        print("  Profundidade interna mínima do corpo: nominal + 3 mm (ver catálogo)")
    if a.frente:
        print(f"  Frente sobreposta: {a.frente}")


# ------------------------------------------------------------------ ripado
def cmd_ripado(a):
    mod = a.ripa + a.vao
    print(f"Ripado: ripa {a.ripa} + vão {a.vao} = módulo {mod} mm")
    if a.folga > a.vao:
        print(f"  ATENÇÃO: folga da porta ({a.folga}) maior que o vão entre ripas ({a.vao}): a junta vai aparecer.")
    # porta deve ter n módulos inteiros: a borda da folha cai no meio de um vão
    alvo = a.porta
    n0 = alvo / mod
    print(f"  Porta-alvo {alvo} mm = {n0:.2f} módulos. Opções com módulo inteiro (junta dentro do vão):")
    for n in sorted({math.floor(n0), math.ceil(n0), math.ceil(n0) + 1}):
        if n <= 0:
            continue
        larg = n * mod
        print(f"    {n} módulos -> folha {larg - a.folga:.0f} mm (eixo a eixo dos vãos {larg} mm,"
              f" folga {a.folga} mm dentro do vão), ripas na folha: {n}")
    if a.largura_total:
        n_tot = a.largura_total / mod
        sobra = a.largura_total - math.floor(n_tot) * mod
        print(f"  Parede {a.largura_total} mm = {n_tot:.2f} módulos; sobra {sobra:.0f} mm"
              " -> distribua metade em cada ponta ou ajuste o vão.")
    if a.altura:
        print(f"  Altura da folha: {a.altura} - folga superior {a.folga} - folga inferior {a.folga_piso}"
              f" = {a.altura - a.folga - a.folga_piso} mm (ripas podem descer até ~5 mm do piso)")
    print("  Regras: nunca corte uma ripa ao meio na junta; a folha leva ripas inteiras;"
          " a junta vertical fica no fundo de um vão (pintado/escuro).")


# ------------------------------------------------------------------ prateleira
CARGAS = {"livros": 1.2, "objetos": 0.5, "pesado": 2.0}  # kN/m² aprox. (livros ~ 35 kg/m p/ 300 mm)


def cmd_prateleira(a):
    E = a.modulo  # MPa (N/mm²)
    b = a.profundidade
    h = a.espessura
    I = b * h ** 3 / 12  # mm^4
    w = CARGAS.get(a.carga, 1.2) * 1e-3 * b  # N/mm  (kN/m² * mm = N/mm² * mm)
    L = a.vao
    apoio = 5 / 384 if a.apoio == "simples" else 1 / 384
    f = apoio * w * L ** 4 / (E * I) * a.fluencia
    limite = L / 300 if a.criterio == "L/300" else 1.7 * L / 1000
    print(f"Prateleira {L} x {b} x {h} mm, carga '{a.carga}' (~{w*1000/9.81:.0f} kg/m), apoio {a.apoio}")
    print(f"  Flecha estimada (com fluência x{a.fluencia}): {f:.1f} mm  | limite visual: {limite:.1f} mm")
    print("  " + ("OK" if f <= limite else "EXCESSIVA: reduza o vão, engrosse (25 mm ou dupla 36), "
                  "fixe atrás num sarrafo/fundo parafusado ou cole uma testeira/perfil sob a frente."))
    # vão máximo
    k = 1 / 300 if a.criterio == "L/300" else 1.7 / 1000   # flecha admissível = k * L
    Lm = (k * E * I / (apoio * w * a.fluencia)) ** (1 / 3)
    print(f"  Vão máximo estimado para este caso: {Lm:.0f} mm")


# ------------------------------------------------------------------ sistema 32
def cmd_sistema32(a):
    z0 = a.espessura_base + a.primeiro
    furos = []
    z = z0
    while z <= a.altura - a.espessura_topo - a.primeiro + 0.01:
        furos.append(round(z, 1))
        z += 32
    print(f"Lateral h={a.altura}: base {a.espessura_base}, topo {a.espessura_topo}.")
    print(f"  Linha frontal a {a.recuo_frontal} mm da frente; linha traseira a {a.recuo_traseiro} mm do fundo"
          " (ou múltiplo de 32 a partir da frontal).")
    print(f"  Furos Ø5 x 13 mm, {len(furos)} por linha, alturas (mm a partir da base da lateral):")
    print("  " + ", ".join(str(f) for f in furos))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    q = s.add_parser("portas")
    q.add_argument("--largura", type=float, required=True, help="largura externa (sobreposta) ou do vão (embutida)")
    q.add_argument("--altura", type=float, required=True)
    q.add_argument("--n", type=int, default=1)
    q.add_argument("--tipo", choices=["sobreposta", "embutida"], default="sobreposta")
    q.add_argument("--folga", type=float, default=3, help="folga entre portas / perímetro (embutida)")
    q.add_argument("--folga-borda", type=float, default=1.5, help="recuo na borda externa (sobreposta)")
    q.add_argument("--espessura", type=float, default=18)
    q.add_argument("--peso-extra", type=float, default=0, help="espelho, vidro, ripas coladas (kg)")
    q.add_argument("--c", type=float, default=4, help="distância C do caneco à borda (3-6)")
    q.add_argument("--borda-dobradica", type=float, default=100, help="centro da 1ª dobradiça ao topo/base")
    q.set_defaults(f=cmd_portas)

    q = s.add_parser("gaveta")
    q.add_argument("--vao", type=float, required=True, help="vão interno entre laterais do móvel")
    q.add_argument("--profundidade", type=float, required=True, help="profundidade interna livre")
    q.add_argument("--corredica", choices=["telescopica", "oculta"], default="telescopica")
    q.add_argument("--nominal", type=int, default=0)
    q.add_argument("--folga-corredica", type=float, default=12.7, help="por lado (telescópica 12,5-13)")
    q.add_argument("--altura-lateral", type=float, default=120)
    q.add_argument("--espessura-lateral", type=float, default=15)
    q.add_argument("--rasgo", type=float, default=7)
    q.add_argument("--frente", default="")
    q.set_defaults(f=cmd_gaveta)

    q = s.add_parser("ripado")
    q.add_argument("--ripa", type=float, required=True)
    q.add_argument("--vao", type=float, required=True)
    q.add_argument("--porta", type=float, required=True, help="largura de passagem desejada")
    q.add_argument("--folga", type=float, default=3)
    q.add_argument("--folga-piso", type=float, default=8)
    q.add_argument("--altura", type=float, default=0)
    q.add_argument("--largura-total", type=float, default=0)
    q.set_defaults(f=cmd_ripado)

    q = s.add_parser("prateleira")
    q.add_argument("--vao", type=float, required=True)
    q.add_argument("--espessura", type=float, default=18)
    q.add_argument("--profundidade", type=float, default=300)
    q.add_argument("--carga", choices=list(CARGAS), default="livros")
    q.add_argument("--apoio", choices=["simples", "engastado"], default="simples")
    q.add_argument("--modulo", type=float, default=2800, help="módulo de elasticidade MDF (MPa)")
    q.add_argument("--fluencia", type=float, default=1.0, help="fator de longo prazo (1,5-2 p/ carga permanente pesada)")
    q.add_argument("--criterio", choices=["L/300", "visual"], default="visual")
    q.set_defaults(f=cmd_prateleira)

    q = s.add_parser("sistema32")
    q.add_argument("--altura", type=float, required=True)
    q.add_argument("--espessura-base", type=float, default=18)
    q.add_argument("--espessura-topo", type=float, default=18)
    q.add_argument("--primeiro", type=float, default=32, help="1º furo acima da face da base")
    q.add_argument("--recuo-frontal", type=float, default=37)
    q.add_argument("--recuo-traseiro", type=float, default=37)
    q.set_defaults(f=cmd_sistema32)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
