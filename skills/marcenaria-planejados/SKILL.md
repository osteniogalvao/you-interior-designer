---
name: marcenaria-planejados
description: Projeta móveis planejados em MDF para um cômodo (estantes, mesas, gaveteiros, armários) em Python local, com modelo 3D paramétrico, vistas 2D e plano de corte de chapas com fita de borda e CSV para Cortecloud. Use para marcenaria, móveis sob medida, lista de corte ou plano de corte de MDF. Also for custom MDF/plywood cabinetry, 3D furniture models and sheet cut lists.
---

# Marcenaria planejada: do levantamento ao plano de corte

Fluxo completo para projetar móveis sob medida em MDF, painel por painel:

**levantamento → modelo paramétrico → 3D + vistas 2D → ciclo de ajustes → plano de corte**

Para as regras técnicas (folgas, fórmulas de portas e gavetas, furação, ferragens, plano de corte e porta mimetizada), use junto a skill `marcenaria-tecnica`.

Tudo roda em Python local. Os scripts estão em `scripts/`, na mesma pasta deste SKILL.md. Copie-os para a pasta do projeto do usuário em vez de editar os originais. Responda no idioma do usuário. Medidas internas sempre em **milímetros**; para o usuário, use metros com vírgula (0,70) se ele escreve assim.

## 0. Preparar o ambiente

Use um venv: o pip do sistema costuma ser bloqueado pela PEP 668.

```bash
python3 -m venv .venv && .venv/bin/pip install -r <pasta-da-skill>/scripts/requirements.txt
```

- O `trimesh` precisa do `scipy` para exportar.
- O visualizador 3D carrega o three.js 0.160.0 do jsdelivr, então precisa de internet.
- Se o usuário já tem um projeto em andamento, procure antes um `PROMPT_CONTINUACAO.md` ou uma nota do projeto e leia tudo antes de agir.

## 1. Levantamento

Monte uma tabela com a coluna **Origem** (medido / assumido / estimado). Nunca trate um valor estimado como medido.

- **Cômodo:** paredes, pé-direito, recuos e polígono do piso em mm, a partir de um canto.
- **Aberturas e instalações:** janela (início, largura, peitoril, altura) e porta (posição, folha, lado da dobradiça). Também tomadas, interruptores, ar-condicionado, sanca ou LED do forro e rodapé existente.
- **Programa:** quem usa, que móveis quer e quais equipamentos precisam caber, com medidas (piano, instrumentos, monitor, roteador, impressora).
- **Material:** pergunte a cor e o fornecedor. Um padrão comum:
  - MDF 18 nas faces aparentes;
  - MDF 15 branco nas caixas de gaveta;
  - MDF 6 nos fundos;
  - fita de borda de 0,4 × 22 mm.

Fotos ajudam a localizar pontos fixos, mas peça confirmação das medidas críticas.

**Eixos do modelo:**
- X corre ao longo da parede de referência, a partir de um canto.
- Y é a profundidade, para dentro do cômodo.
- Z é a altura a partir do piso.

Fixe isso no topo do script e use em todo o projeto.

## 2. Modelo paramétrico (fonte única)

Crie `modelo_<comodo>.py` a partir de `exemplo/exemplo_estante.py`:

```python
from marcenaria import Projeto
p = Projeto("Quarto - estante", poligono=[(0,0),(3000,0),(3000,3200),(0,3200)], pe_direito=2600)
p.box("Lateral esquerda", "Estante", x, y, z, dx, dy, dz, mat="mdf18", fita="frente", obs="")
p.exportar("saida", "estante")
```

- **Parâmetros:** um bloco de PARÂMETROS (mm) no topo, com todas as medidas. Comente a origem e a data de cada pedido de mudança. Nada de número mágico no meio do código.
- **Painéis:** cada painel é uma caixa alinhada aos eixos. Desconte as espessuras de verdade: as laterais "comem" 2 × 18 do vão, e o fundo de 6 encaixa em rasgo.
- **Materiais:** os padrões são `mdf18`, `mdf15`, `fundo`, `vidro` e `ref`. Os dois últimos não entram no corte; use `ref` para objetos de referência, como piano, monitor e LED.
  - Para trocar nome, cor ou regra de veio, passe `materiais=` ao `Projeto`. Cada material tem os campos `nome`, `cor`, `espessura`, `corte` e `gira`.
  - MDF com veio (madeirado) usa `gira=False`.
- **Fita:** o campo `fita` é texto livre, como "frente", "frente + lado", "frente + 2 lados" ou "4 lados". O plano de corte interpreta esse texto.
- **Opções de layout:** compare variantes com um argumento de linha de comando (`modelo.py A|B|C`) e um sufixo nos arquivos.

`exportar` gera:
- `<base>.json`: ambiente, materiais e peças com comprimento, largura, espessura, posição e fita;
- `<base>_3d.glb`, `.obj` e `.stl`, que abrem no SketchUp ou no Blender;
- `<base>_3d.html`: visualizador three.js com câmeras, grupos liga/desliga e medidas ao passar o mouse.

## 3. Vistas 2D

```bash
.venv/bin/python <skill>/scripts/vistas_2d.py saida/estante.json [--grupo Estante] [--rev B]
```

Gera uma folha A3 em PDF e PNG com planta, elevação frontal, elevação lateral e cotas gerais. Para folhas de execução, com cotas de cada nicho, escala fixa e carimbo, escreva um `desenho_<movel>.py` próprio partindo deste. Ele deve ler o JSON, nunca duplicar parâmetros. **Toda alteração num desenho sobe a letra da revisão.**

## 4. Ciclo de ajuste

Normalmente o usuário manda prints do 3D apontando o que mudar. A cada pedido:

1. **Interprete.** Leia a medida no ponto indicado. Se houver dúvida real sobre qual móvel ou peça é, diga a suposição que adotou. Cantos e móveis parecidos se confundem com facilidade.
2. **Altere.** Mude só o parâmetro no modelo.
3. **Regenere.** Rode todas as variantes, as vistas 2D e, se já existir, o plano de corte.
4. **Confira.** Abra o 3D num servidor local (`python3 -m http.server 8765 --bind 127.0.0.1`) e use `?v=N` na URL para furar o cache. Salve um `preview_*.png`.
5. **Responda.** Informe as medidas finais, as revisões novas e o preview. Uma resposta curta basta.

**Sinalize problemas de projeto, mas respeite quando o usuário mantiver a decisão:**
- **Ergonomia:** tampo de 0,73 a 0,75. Abaixo de bandejas e gavetas, sobre menos de 0,60 livre para as pernas.
- **Vãos:** prateleira de MDF 18 com livros enverga acima de ~0,55–0,65 m apoiada só nas pontas (~0,90 m se parafusada no fundo). Use reforço, testeira, 25 mm ou divisória; calcule com `marcenaria-tecnica`.
- **Circulação:** confira o giro da porta e a folga até o móvel.
- **Conflitos:** tomadas, interruptores, sanca ou cortineiro e o peitoril da janela.
- **Equipamentos:** confira se cabem com folga, como violão em pé ou um piano com a profundidade da bandeja.

## 5. Plano de corte

```bash
.venv/bin/python <skill>/scripts/plano_corte.py saida/estante.json --chapa 2750x1850 --kerf 4 --refilo 10
```

**Regras:**
- Encaixa as peças com `rectpack`, separado por material e espessura, testando vários algoritmos.
- Materiais com `gira=False` nunca giram, por causa do veio. `--girar-tudo` libera isso, mas só com autorização.
- Peça maior que a chapa útil é dividida e gera um aviso. Planeje a emenda atrás de uma divisória.
- Fita: `FITA_MAPA` e um interpretador de palavras-chave convertem o texto em bordas C1/C2 (comprimento) e L1/L2 (largura). Texto não reconhecido gera aviso; acrescente-o ao mapa. O total de fita sai com 10% de sobra.

**Saídas:**
- `_plano_corte.pdf`: resumo, lista de peças e diagrama de cada chapa, com a fita em vermelho;
- `_lista_corte.csv`;
- `_cortecloud.csv`, com separador `;` e UTF-8 com BOM.

Confira as colunas do CSV com o modelo de importação da sua conta no Cortecloud antes do primeiro uso.

**Antes do plano definitivo:**
- Confirme a variante e os itens opcionais.
- Se a última chapa sair quase vazia, tente eliminá-la ajustando medidas ou o encaixe, ou indique as peças para retalho.
- Confira se nenhum material de referência entrou no corte.

## 6. Registro e continuidade

- **Decisões:** mantenha uma lista no formato `AAAA-MM-DD - decisão (folhas/revisões)` num arquivo `DECISOES.md` do projeto ou no sistema de notas do usuário, se ele tiver um.
- **Pausas longas:** ao fim de uma rodada, escreva um `PROMPT_CONTINUACAO.md` com o cômodo, o estado aprovado de cada móvel, os parâmetros principais, os arquivos, o próximo passo e os pontos em aberto. Empacote a pasta num zip sem o `.venv`.

## Arquivos desta skill

| Arquivo | Função |
|---|---|
| `scripts/marcenaria.py` | Classe `Projeto`: `box()`, materiais e exportação para JSON, GLB/OBJ/STL e HTML 3D |
| `scripts/viewer_template.html` | Visualizador three.js; o JSON é injetado em `/*__DADOS__*/null` |
| `scripts/vistas_2d.py` | Folha A3 com planta e elevações a partir do JSON |
| `scripts/plano_corte.py` | Plano de corte: PDF, lista e CSV para o Cortecloud |
| `scripts/requirements.txt` | Dependências Python |
| `exemplo/exemplo_estante.py` | Exemplo completo: estante e escrivaninha com gaveta |
