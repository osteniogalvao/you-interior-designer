#!/usr/bin/env python3
"""Plano de corte de chapas de MDF a partir da lista de peças gerada por marcenaria.py.

Uso:
  python plano_corte.py projeto.json
  python plano_corte.py projeto.json --chapa 2750x1850 --kerf 4 --refilo 10 --girar-tudo

Gera, ao lado do JSON:
  {base}_plano_corte.pdf   resumo + lista de peças + diagrama de cada chapa
  {base}_lista_corte.csv   uma linha por peça, com fita de borda e chapa
  {base}_cortecloud.csv    peças agrupadas, pronto para importar no Cortecloud

Regras:
- Peças agrupadas por material (chave mat_key) e encaixadas com rectpack.
- Materiais com "corte": false no JSON (vidro, referências) ficam fora.
- Materiais com "gira": false (MDF com veio) nunca giram, salvo --girar-tudo.
- Peça maior que a chapa útil é dividida, com aviso.
- O campo "fita" é texto livre; FITA_MAPA (e um interpretador de palavras-chave)
  converte em bordas C1/C2 (no comprimento) e L1/L2 (na largura).
"""
import csv, json, math, os, sys
from collections import OrderedDict, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
import rectpack

# ---------------- parâmetros ----------------
CHAPA_C, CHAPA_L = 2750, 1850   # comprimento (sentido do veio) x largura
REFILO = 10                     # refilo em cada borda da chapa (mm)
KERF = 4                        # espessura da serra (mm)
FITA_PERDA = 0.10               # 10% de perda/sobra de fita
FITA_DESC = "Fita 0,4 x 22 mm"

GRUPOS_MAT = OrderedDict()      # preenchido a partir de "materiais" do JSON: mat_key -> (rótulo, pode girar)
CORES = {}

# fita: arestas no comprimento (C1, C2) e na largura (L1, L2)
FITA_MAPA = {
    "":                       (0, 0, 0, 0),
    "frente":                 (1, 0, 0, 0),
    "frente + lado":          (1, 0, 1, 0),
    "frente + lado direito":  (1, 0, 1, 0),
    "frente + lado esquerdo": (1, 0, 1, 0),
    "frente + base":          (1, 0, 1, 0),
    "frente + 2 lados":       (1, 0, 1, 1),
    "4 lados":                (1, 1, 1, 1),
    "face inferior aparente": (1, 0, 0, 0),
    "frente + trás":          (1, 1, 0, 0),
    "2 comprimentos":         (1, 1, 0, 0),
}


def interpretar_fita(txt):
    """Traduz o texto livre de fita em (C1, C2, L1, L2). Retorna (bordas, reconhecido)."""
    t = (txt or "").strip().lower()
    if t in FITA_MAPA:
        return FITA_MAPA[t], True
    if "4 lados" in t or "todas" in t or "contorno" in t:
        return (1, 1, 1, 1), True
    c1 = 1 if ("frente" in t or "comprimento" in t) else 0
    c2 = 1 if ("trás" in t or "tras" in t or "2 comprimentos" in t) else 0
    l1 = l2 = 0
    if "2 lados" in t or "dois lados" in t or "ambos os lados" in t:
        l1 = l2 = 1
    elif "lado" in t or "topo" in t or "base" in t:
        l1 = 1
    ok = bool(c1 or c2 or l1 or l2)
    return ((c1, c2, l1, l2) if ok else (1, 0, 0, 0)), ok

ALGOS = [rectpack.GuillotineBssfSas, rectpack.GuillotineBssfLas, rectpack.GuillotineBafSas,
         rectpack.GuillotineBlsfSas, rectpack.GuillotineBafMinas, rectpack.MaxRectsBssf,
         rectpack.MaxRectsBaf, rectpack.SkylineMwf]
ORDENS = [rectpack.SORT_AREA, rectpack.SORT_LSIDE, rectpack.SORT_SSIDE, rectpack.SORT_PERI]


def carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    for mk, m in dados.get("materiais", {}).items():
        if m.get("corte", True):
            GRUPOS_MAT[mk] = (m.get("nome", mk), bool(m.get("gira", True)))
            CORES[mk] = m.get("cor", "#cccccc")
    return dados


def preparar(dados, girar_tudo):
    """Separa as peças de corte por material e divide as que não cabem na chapa."""
    util_c, util_l = CHAPA_C - 2 * REFILO, CHAPA_L - 2 * REFILO
    pecas, avisos = [], []
    for p in dados["pecas"]:
        mk = p["mat_key"]
        if mk not in GRUPOS_MAT:
            continue   # vidro, referências e outros materiais fora do corte
        fita = (p.get("fita") or "").strip()
        (c1, c2, l1, l2), ok = interpretar_fita(fita)
        if fita and not ok:
            avisos.append(f"Fita '{fita}' da peça {p['id']} não reconhecida - considerada só a frente")
        C, L = int(round(p["comprimento"])), int(round(p["largura"]))
        gira = True if girar_tudo else GRUPOS_MAT[mk][1]
        cabe = (C <= util_c and L <= util_l) or (gira and C <= util_l and L <= util_c)
        partes = 1
        if not cabe:
            # divide no sentido da medida que estoura
            if C > util_c:
                partes = math.ceil(C / util_c)
                Cs, Ls = math.ceil(C / partes), L
            else:
                partes = math.ceil(L / util_l)
                Cs, Ls = C, math.ceil(L / partes)
            avisos.append(f"Peça {p['id']} ({p['nome']}, {C} x {L}) não cabe na chapa: "
                          f"dividida em {partes} partes de {Cs} x {Ls}. Emenda atrás de uma divisória.")
            C, L = Cs, Ls
        for k in range(partes):
            nome = p["nome"] + (f" (parte {k+1}/{partes})" if partes > 1 else "")
            pecas.append(dict(id=p["id"], parte=k + 1, partes=partes, grupo=p["grupo"], nome=nome,
                              C=C, L=L, esp=p["espessura"], mk=mk, gira=gira, fita=fita,
                              c1=c1, c2=c2, l1=l1, l2=l2, obs=p.get("obs", "") or ""))
    return pecas, avisos


def encaixar(lista):
    """Testa vários algoritmos e ordenações; fica com o que usa menos chapas e
    concentra mais sobra na última chapa."""
    util_c, util_l = CHAPA_C - 2 * REFILO + KERF, CHAPA_L - 2 * REFILO + KERF
    gira = lista[0]["gira"]
    melhor = None
    for algo in ALGOS:
        for ordem in ORDENS:
            pk = rectpack.newPacker(mode=rectpack.PackingMode.Offline, bin_algo=rectpack.PackingBin.BFF,
                                    pack_algo=algo, sort_algo=ordem, rotation=gira)
            for i, p in enumerate(lista):
                pk.add_rect(p["C"] + KERF, p["L"] + KERF, rid=i)
            pk.add_bin(util_c, util_l, count=float("inf"))
            pk.pack()
            rects = pk.rect_list()
            if len(rects) != len(lista):
                continue
            nb = len(pk)
            areas = [sum(r.width * r.height for r in b) for b in pk]
            chave = (nb, min(areas))
            if melhor is None or chave < melhor[0]:
                melhor = (chave, rects, nb)
    if melhor is None:
        raise SystemExit("Não foi possível encaixar as peças")
    _, rects, nb = melhor
    chapas = [[] for _ in range(nb)]
    for b, x, y, w, h, rid in rects:
        p = lista[rid]
        girada = (w - KERF) != p["C"] or (p["C"] == p["L"] and False)
        if p["C"] != p["L"]:
            girada = (w - KERF) == p["L"] and (h - KERF) == p["C"]
        chapas[b].append(dict(p=p, x=x + REFILO, y=y + REFILO, w=w - KERF, h=h - KERF, girada=girada))
    return chapas


def fita_mm(p):
    return (p["c1"] + p["c2"]) * p["C"] + (p["l1"] + p["l2"]) * p["L"]


def cor_peca(mk):
    """Versão clara da cor do material, para o texto ficar legível."""
    h = CORES.get(mk, "#cccccc").lstrip("#")
    r, g, b = (int(h[k:k + 2], 16) for k in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * 0.55) for v in (r, g, b))


def desenhar_chapa(pdf, titulo, chapa, n, total, etiqueta):
    fig = plt.figure(figsize=(16.54, 11.69))  # A3 paisagem
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.80])
    ax.add_patch(Rectangle((0, 0), CHAPA_C, CHAPA_L, fc="#f6f6f6", ec="black", lw=1.2))
    ax.add_patch(Rectangle((REFILO, REFILO), CHAPA_C - 2 * REFILO, CHAPA_L - 2 * REFILO,
                           fc="none", ec="#999", lw=0.6, ls="--"))
    area = 0
    for r in chapa:
        p = r["p"]
        area += r["w"] * r["h"]
        ax.add_patch(Rectangle((r["x"], r["y"]), r["w"], r["h"], fc=cor_peca(p["mk"]), ec="black", lw=0.8))
        # fita: traço grosso nas arestas com fita
        lw = 2.2
        C_horiz = not r["girada"]
        ed = []
        if C_horiz:
            if p["c1"]: ed.append(((r["x"], r["y"]), (r["x"] + r["w"], r["y"])))
            if p["c2"]: ed.append(((r["x"], r["y"] + r["h"]), (r["x"] + r["w"], r["y"] + r["h"])))
            if p["l1"]: ed.append(((r["x"], r["y"]), (r["x"], r["y"] + r["h"])))
            if p["l2"]: ed.append(((r["x"] + r["w"], r["y"]), (r["x"] + r["w"], r["y"] + r["h"])))
        else:
            if p["c1"]: ed.append(((r["x"], r["y"]), (r["x"], r["y"] + r["h"])))
            if p["c2"]: ed.append(((r["x"] + r["w"], r["y"]), (r["x"] + r["w"], r["y"] + r["h"])))
            if p["l1"]: ed.append(((r["x"], r["y"]), (r["x"] + r["w"], r["y"])))
            if p["l2"]: ed.append(((r["x"], r["y"] + r["h"]), (r["x"] + r["w"], r["y"] + r["h"])))
        for (a, b) in ed:
            ax.plot([a[0], b[0]], [a[1], b[1]], color="#b03a2e", lw=lw, solid_capstyle="butt")
        cx, cy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
        menor = min(r["w"], r["h"])
        fs = 7 if menor > 120 else 5.5
        rot = 90 if (r["h"] > r["w"] * 1.6 and r["w"] < 260) else 0
        txt = f"#{etiqueta[id(p)]}  {p['C']} x {p['L']}"
        if menor > 150:
            nome = p["nome"] if len(p["nome"]) <= 34 else p["nome"][:32] + "…"
            txt += f"\n{nome}"
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=fs, rotation=rot)
    ax.set_xlim(-40, CHAPA_C + 40)
    ax.set_ylim(-40, CHAPA_L + 40)
    ax.set_aspect("equal")
    ax.axis("off")
    aprov = area / ((CHAPA_C) * (CHAPA_L)) * 100
    fig.text(0.04, 0.95, f"{titulo} - chapa {n}/{total}", fontsize=15, weight="bold")
    fig.text(0.04, 0.925, f"Chapa {CHAPA_C} x {CHAPA_L} mm · refilo {REFILO} · kerf {KERF} · "
             f"aproveitamento {aprov:.0f}% · {len(chapa)} peças · veio no sentido dos {CHAPA_C} mm "
             f"(horizontal no desenho)", fontsize=10)
    fig.text(0.04, 0.06, "Traço vermelho = aresta com fita de borda 0,4 x 22 mm. "
             "Número # = etiqueta da peça na lista de corte.", fontsize=9, color="#b03a2e")
    pdf.savefig(fig)
    plt.close(fig)
    return aprov


def paginas_tabela(pdf, titulo, cab, linhas, larguras, por_pagina=42):
    for ini in range(0, len(linhas), por_pagina):
        fig = plt.figure(figsize=(16.54, 11.69))
        fig.text(0.04, 0.95, titulo + (f" (cont.)" if ini else ""), fontsize=15, weight="bold")
        ax = fig.add_axes([0.04, 0.04, 0.92, 0.88])
        ax.axis("off")
        t = ax.table(cellText=linhas[ini:ini + por_pagina], colLabels=cab, colWidths=larguras,
                     loc="upper left", cellLoc="left")
        t.auto_set_font_size(False)
        t.set_fontsize(7.5)
        t.scale(1, 1.25)
        for (r, c), cell in t.get_celld().items():
            if r == 0:
                cell.set_facecolor("#ddd")
                cell.set_text_props(weight="bold")
        pdf.savefig(fig)
        plt.close(fig)


def main():
    global CHAPA_C, CHAPA_L, KERF, REFILO
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        raise SystemExit(__doc__)
    caminho = args[0]
    girar_tudo = "--girar-tudo" in args
    for k, a in enumerate(args):
        if a == "--chapa":
            CHAPA_C, CHAPA_L = (int(v) for v in args[k + 1].lower().split("x"))
        elif a == "--kerf":
            KERF = int(args[k + 1])
        elif a == "--refilo":
            REFILO = int(args[k + 1])
    dados = carregar(caminho)
    base = os.path.splitext(caminho)[0]
    pecas, avisos = preparar(dados, girar_tudo)
    if not pecas:
        raise SystemExit("Nenhuma peça de corte no JSON")

    # etiquetas sequenciais na ordem do JSON
    etiqueta = {id(p): i + 1 for i, p in enumerate(pecas)}

    resultado = OrderedDict()
    for mk, (rotulo, _) in GRUPOS_MAT.items():
        lista = [p for p in pecas if p["mk"] == mk]
        if lista:
            resultado[mk] = encaixar(lista)

    # chapa de cada peça
    chapa_de = {}
    n_global = 0
    for mk, chapas in resultado.items():
        for j, ch in enumerate(chapas):
            n_global += 1
            for r in ch:
                chapa_de[id(r["p"])] = (n_global, r["girada"])

    titulo = f"{dados.get('ambiente', {}).get('titulo', os.path.basename(base))} - plano de corte"
    total_fita = sum(fita_mm(p) for p in pecas) / 1000
    fita_por_mat = defaultdict(float)
    for p in pecas:
        fita_por_mat[p["mk"]] += fita_mm(p) / 1000

    # ---------- CSV lista completa ----------
    with open(f"{base}_lista_corte.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Etiqueta", "ID modelo", "Grupo", "Peça", "Comprimento (veio)", "Largura", "Espessura",
                    "Material", "Fita C1", "Fita C2", "Fita L1", "Fita L2", "Fita (m)", "Chapa", "Girada", "Obs"])
        for p in pecas:
            ch, gir = chapa_de[id(p)]
            w.writerow([etiqueta[id(p)], p["id"], p["grupo"], p["nome"], p["C"], p["L"], p["esp"],
                        GRUPOS_MAT[p["mk"]][0], p["c1"], p["c2"], p["l1"], p["l2"],
                        f"{fita_mm(p)/1000:.2f}".replace(".", ","), ch, "sim" if gir else "não", p["obs"]])

    # ---------- CSV Cortecloud (agrupado) ----------
    grupos = OrderedDict()
    for p in pecas:
        k = (p["mk"], p["C"], p["L"], p["c1"], p["c2"], p["l1"], p["l2"], p["nome"].split(" z")[0])
        grupos.setdefault(k, []).append(p)
    with open(f"{base}_cortecloud.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Quantidade", "Comprimento", "Largura", "Descricao", "Material", "Espessura",
                    "Veio", "Fita C1", "Fita C2", "Fita L1", "Fita L2", "Fita"])
        for k, ps in grupos.items():
            p = ps[0]
            w.writerow([len(ps), p["C"], p["L"], f"{p['grupo']} - {k[7]}", GRUPOS_MAT[p['mk']][0], p["esp"],
                        "não" if p["gira"] else "sim", p["c1"], p["c2"], p["l1"], p["l2"],
                        FITA_DESC if (p["c1"] or p["c2"] or p["l1"] or p["l2"]) else ""])

    # ---------- PDF ----------
    with PdfPages(f"{base}_plano_corte.pdf") as pdf:
        fig = plt.figure(figsize=(16.54, 11.69))
        fig.text(0.04, 0.93, titulo, fontsize=20, weight="bold")
        y = 0.86
        linhas = [f"Chapa {CHAPA_C} x {CHAPA_L} mm · refilo {REFILO} mm · kerf {KERF} mm · "
                  f"{FITA_DESC}",
                  ("Todas as peças PODEM girar (veio liberado)" if girar_tudo else
                   "Materiais com veio NÃO giram: " + (", ".join(r for r, g in GRUPOS_MAT.values() if not g) or "nenhum")),
                  "Fora do plano: materiais marcados sem corte (vidro, referências).", ""]
        for mk, chapas in resultado.items():
            n = len([p for p in pecas if p["mk"] == mk])
            linhas.append(f"{GRUPOS_MAT[mk][0]}: {len(chapas)} chapa(s), {n} peças, "
                          f"fita {fita_por_mat[mk]:.1f} m")
        linhas += ["", f"Total de chapas: {sum(len(c) for c in resultado.values())}",
                   f"Fita de borda: {total_fita:.1f} m líquidos · {total_fita*(1+FITA_PERDA):.1f} m com "
                   f"{FITA_PERDA*100:.0f}% de sobra", ""]
        if avisos:
            linhas.append("Avisos:")
            linhas += ["  • " + a for a in avisos]
        for l in linhas:
            fig.text(0.05, y, l, fontsize=12)
            y -= 0.035
        pdf.savefig(fig)
        plt.close(fig)

        cab = ["#", "ID", "Grupo", "Peça", "Comp.", "Larg.", "Esp.", "Mat.", "Fita C1 C2 L1 L2", "Fita m", "Chapa"]
        rows = []
        for p in pecas:
            nome = p["nome"] if len(p["nome"]) <= 58 else p["nome"][:56] + "…"
            rows.append([etiqueta[id(p)], p["id"], p["grupo"], nome, p["C"], p["L"], p["esp"], p["mk"],
                         f"{p['c1']}  {p['c2']}  {p['l1']}  {p['l2']}", f"{fita_mm(p)/1000:.2f}",
                         chapa_de[id(p)][0]])
        paginas_tabela(pdf, f"{titulo} - lista de peças", cab, rows,
                       [0.03, 0.03, 0.15, 0.36, 0.05, 0.05, 0.04, 0.07, 0.11, 0.05, 0.05])

        n_global = 0
        total = sum(len(c) for c in resultado.values())
        resumo_aprov = []
        for mk, chapas in resultado.items():
            for ch in chapas:
                n_global += 1
                a = desenhar_chapa(pdf, f"{titulo} · {GRUPOS_MAT[mk][0]}", ch, n_global, total, etiqueta)
                resumo_aprov.append((n_global, mk, a))

    print(f"{len(pecas)} peças de corte -> {base}_plano_corte.pdf, {base}_lista_corte.csv, {base}_cortecloud.csv")
    for mk, chapas in resultado.items():
        print(f"  {GRUPOS_MAT[mk][0]}: {len(chapas)} chapa(s)")
    for n, mk, a in resumo_aprov:
        print(f"  chapa {n} ({mk}): {a:.0f}%")
    print(f"  fita: {total_fita:.1f} m (+{FITA_PERDA*100:.0f}% = {total_fita*(1+FITA_PERDA):.1f} m)")
    for a in avisos:
        print("  AVISO:", a)


if __name__ == "__main__":
    main()
