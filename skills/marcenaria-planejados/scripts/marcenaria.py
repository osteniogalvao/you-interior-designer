# -*- coding: utf-8 -*-
"""
marcenaria.py - núcleo para modelar móveis planejados em MDF, painel por painel.

Unidades: MILÍMETROS. Eixos: X ao longo da parede de referência (0 = um canto),
Y = profundidade entrando no cômodo, Z = altura a partir do piso.

Uso típico (veja exemplo/exemplo_estante.py):

    from marcenaria import Projeto, MATERIAIS_PADRAO
    p = Projeto("Quarto - estante", poligono=[(0,0),(3000,0),(3000,3500),(0,3500)], pe_direito=2600)
    p.box("Lateral esquerda", "Estante", 0, 0, 0, 18, 300, 2200, fita="frente")
    p.exportar("saida", "estante")   # -> estante.json, .glb, .obj, .stl, _3d.html

Cada painel é uma caixa alinhada aos eixos. Comprimento/largura/espessura da peça
de corte são as 3 dimensões ordenadas (maior, média, menor).
"""
import json
import os

# chave -> nome, cor (3D), espessura (mm), corte (entra no plano de corte), gira (pode girar na chapa)
MATERIAIS_PADRAO = {
    "mdf18": dict(nome="MDF 18 (face aparente)", cor="#8f6a45", espessura=18, corte=True, gira=False),
    "mdf15": dict(nome="MDF 15 Branco (interno)", cor="#e9e6df", espessura=15, corte=True, gira=True),
    "fundo": dict(nome="MDF 6 (fundo)", cor="#a88a68", espessura=6, corte=True, gira=True),
    "vidro": dict(nome="Vidro temperado", cor="#bfe3ff", espessura=6, corte=False, gira=False),
    "ref":   dict(nome="Referência (não é peça)", cor="#3a3d42", espessura=0, corte=False, gira=False),
}

AQUI = os.path.dirname(os.path.abspath(__file__))


class Projeto:
    def __init__(self, titulo, poligono=None, pe_direito=2600, materiais=None, ambiente=None):
        self.titulo = titulo
        self.poligono = poligono or []
        self.pe_direito = pe_direito
        self.materiais = dict(materiais or MATERIAIS_PADRAO)
        self.ambiente = dict(ambiente or {})
        self.pecas = []

    def box(self, nome, grupo, x, y, z, dx, dy, dz, mat="mdf18", fita="", obs=""):
        """Adiciona um painel. dx, dy, dz = dimensões ao longo de X, Y, Z.

        fita: texto livre descrevendo as bordas com fita ("frente", "frente + lado", "4 lados"...).
        O plano de corte traduz esse texto em bordas C1/C2/L1/L2 (veja FITA_MAPA em plano_corte.py).
        """
        if mat not in self.materiais:
            raise ValueError(f"material desconhecido: {mat}")
        if min(dx, dy, dz) <= 0:
            raise ValueError(f"painel '{nome}' com dimensão nula ou negativa: {dx} x {dy} x {dz}")
        self.pecas.append(dict(nome=nome, grupo=grupo, x=x, y=y, z=z, dx=dx, dy=dy, dz=dz,
                               mat=mat, fita=fita, obs=obs))

    # ------------------------------------------------------------------ saída
    def lista(self):
        out = []
        for i, p in enumerate(self.pecas):
            dims = sorted([p["dx"], p["dy"], p["dz"]], reverse=True)
            m = self.materiais[p["mat"]]
            out.append(dict(id=i + 1, grupo=p["grupo"], nome=p["nome"],
                            comprimento=round(dims[0]), largura=round(dims[1]), espessura=round(dims[2]),
                            material=m["nome"], mat_key=p["mat"], fita=p["fita"], obs=p["obs"],
                            x=p["x"], y=p["y"], z=p["z"], dx=p["dx"], dy=p["dy"], dz=p["dz"], cor=m["cor"]))
        return out

    def dados(self):
        amb = dict(self.ambiente, titulo=self.titulo, poligono=self.poligono, pe_direito=self.pe_direito)
        return dict(ambiente=amb, materiais=self.materiais, pecas=self.lista())

    def exportar(self, pasta, base):
        """Gera {base}.json, {base}_3d.glb/.obj/.stl e {base}_3d.html (visualizador three.js)."""
        os.makedirs(pasta, exist_ok=True)
        dados = self.dados()
        with open(os.path.join(pasta, f"{base}.json"), "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=1)

        try:
            import trimesh
            scene, meshes = trimesh.Scene(), []
            for i, p in enumerate(self.pecas):
                m = trimesh.creation.box(extents=[p["dx"], p["dy"], p["dz"]])
                m.apply_translation([p["x"] + p["dx"] / 2, p["y"] + p["dy"] / 2, p["z"] + p["dz"] / 2])
                h = self.materiais[p["mat"]]["cor"].lstrip("#")
                m.visual = trimesh.visual.ColorVisuals(
                    m, face_colors=[int(h[k:k + 2], 16) for k in (0, 2, 4)] + [255])
                nome = f"{i+1:03d} {p['grupo']} - {p['nome']}"
                scene.add_geometry(m, node_name=nome, geom_name=nome)
                meshes.append(m)
            if meshes:
                scene.export(os.path.join(pasta, f"{base}_3d.glb"))
                scene.export(os.path.join(pasta, f"{base}_3d.obj"))
                trimesh.util.concatenate(meshes).export(os.path.join(pasta, f"{base}_3d.stl"))
        except ImportError:
            print("aviso: trimesh não instalado - GLB/OBJ/STL não gerados")

        tpl = open(os.path.join(AQUI, "viewer_template.html"), encoding="utf-8").read()
        html = tpl.replace("/*__DADOS__*/null", json.dumps(dados, ensure_ascii=False))
        html = html.replace("__TITULO__", self.titulo)
        with open(os.path.join(pasta, f"{base}_3d.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{len(self.pecas)} painéis -> {pasta}/{base}.json, {base}_3d.glb/.obj/.stl, {base}_3d.html")
        return dados
