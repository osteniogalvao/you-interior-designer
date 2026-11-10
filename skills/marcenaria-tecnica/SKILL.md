---
name: marcenaria-tecnica
description: Regras técnicas de marcenaria em MDF para projetar e revisar móveis planejados - folgas e medidas de portas e gavetas, furação (sistema 32, minifix, cavilha, dobradiça de caneco, corrediças), plano de corte (veio, refilo, kerf, fita de borda) e painel ripado ou liso com porta mimetizada (porta oculta). Use ao dimensionar peças, gerar furação ou lista de corte, ou revisar um projeto de marcenaria. Also for cabinet hardware drilling, cut lists and hidden doors in wall panels.
---

# Marcenaria técnica: medidas, furação, plano de corte e porta mimetizada

Manual de regras para transformar um desenho de móvel em peças cortáveis e furáveis. Complementa a skill `marcenaria-planejados`, que faz o modelo 3D, as vistas e o plano de corte: use esta para **decidir as medidas de cada peça, as folgas, a furação e as ferragens**, e para revisar o projeto antes de mandar cortar.

Princípios:
- Medidas em **mm**. Ao falar com o usuário, use o formato dele (0,70 m).
- Os números abaixo são o padrão da prática brasileira e dos catálogos (Blum, Hettich, Salice, Häfele, FGV). **Ferragem manda**: antes de liberar furação, confira a ficha da peça escolhida e diga isso ao usuário.
- Marque cada medida como medida / assumida / estimada. Nunca corte a partir de uma medida estimada.
- Calculadoras em `scripts/calc_marcenaria.py` (só Python padrão): `portas`, `gaveta`, `ripado`, `prateleira`, `sistema32`. Rode `python3 scripts/calc_marcenaria.py <cmd> -h`.

## 1. Materiais

| Item | Padrão |
|---|---|
| Chapa MDF | 2750 × 1850 (Guararapes, Arauco, Berneck) ou 2750 × 1840 (Duratex/Eucatex e "multimarcas"). Confirme com o fornecedor. Veio corre no comprimento (2750). |
| Espessuras | 6 (fundos), 15 (corpo interno, caixas de gaveta), 18 (corpo aparente, portas, prateleiras), 25 (prateleira longa, tampo). Tampo engrossado = 2 × 18 colado (36) com testeira. |
| Revestimento | BP/melamínico 2 faces nas peças visíveis dos dois lados; 1 face só em fundo (selar a face crua). Área úmida: MDF RU (verde). |
| Fita de borda | PVC 0,45 × 22 (para 18 e 15) ou 0,45 × 19 (15). Fita 1 mm ou 2 mm em bordas de impacto (frente de prateleira, tampo, porta de cozinha). |
| Densidade | ~750 kg/m³ → MDF 18 pesa ~13,5 kg/m². Use para peso de porta e carga em ferragem. |

## 2. Construção da caixa (corpo)

- **Esquema de montagem** tem que estar decidido antes da lista de corte, porque muda as medidas:
  - *Laterais passantes* (padrão em armário alto e aéreo): base e tampo entram entre as laterais. Base/tampo = largura externa − 2 × espessura.
  - *Base e tampo passantes* (comum em balcão e em móvel com tampo aparente): laterais = altura − 2 × espessura.
  - Divisória interna: altura interna; prateleira fixa: vão − 0 (encaixe justo) ou − 1 mm.
- **Fundo**:
  - *Encaixado em rasgo* (melhor acabamento, trava o esquadro): rasgo 6–7 mm de largura × 8–10 mm de profundidade, a 10–20 mm da borda traseira. Fundo = vão interno + 2 × (profundidade do rasgo − 1).
  - *Sobreposto parafusado/grampeado* atrás: fundo = medida externa − 2 a 4 mm. Mais rápido, porém aparece de lado.
  - Recuo de 15–20 mm atrás do fundo quando o móvel encosta em parede torta ou precisa passar fiação.
- **Base/rodapé**: rodapé recuado 50–70 mm, altura 80–150 mm. Pés reguláveis na cozinha. Em piso flutuante/vinílico, nunca fixe o móvel ao piso.
- **Profundidades usuais**: aéreo 300–350; balcão de cozinha 550–600 (corpo) + porta; armário de roupa 550–600 (porta de abrir), 600–650 (porta de correr); estante de livros 250–300; mesa 600–700.
- **Prateleiras (flecha)**: para livros em MDF 18 com 300 de profundidade, vão livre até ~0,55–0,65 m apoiada só nas pontas; até ~0,90 m se parafusada no fundo/sarrafo (engastada). Acima disso: 25 mm, 36 mm (dupla), testeira de 40–60 mm sob a frente, ou divisória. Use `calc_marcenaria.py prateleira` para o caso real.
- **Tamponamento**: lateral aparente de móvel que encosta em outro ganha tampão de 18 (lateral dupla) ou acabamento 2 faces.
- Peças que ficam em contato com parede torta (tampo, laterais de canto) levam **sobra de 10–20 mm para recorte em obra** (rodatampo, "ajuste na obra").

## 3. Portas e frentes

### 3.1 Folgas
- Entre portas/frentes vizinhas: **3 mm** (2–4). Na borda externa da caixa (sobreposta total): 1,5–2 mm de cada lado.
- Porta embutida (dentro do vão): 2–3 mm em todo o perímetro.
- Gavetas sobrepostas: 3 mm entre frentes. Frente de gaveta inferior a 2–3 mm acima do rodapé.

### 3.2 Fórmulas (n portas)
- **Sobreposta total** sobre corpo de largura externa L e altura externa A: largura = (L − 2 × 1,5 − (n − 1) × 3) / n; altura = A − 3.
- **Embutida** num vão interno Lv × Av: largura = (Lv − (n + 1) × 3) / n; altura = Av − 6.
- **Porta de abrir**: largura ideal até 500–600 mm. Acima de 600, peso e giro complicam; acima de 2000 de altura, preveja **desempenador** (perfil de aço/alumínio embutido em rasgo) para não empenar.
- Calcule com `calc_marcenaria.py portas`.

### 3.3 Dobradiça de caneco (Ø35)
- Caneco **Ø35 × 11–13 mm** de profundidade (porta de 16–25 mm).
- **Distância C** (borda da porta até a borda do caneco): 3–6 mm, padrão 4–5. O centro do caneco fica a C + 17,5 da borda (≈ 21,5–22,5).
- Furos de fixação do caneco (versão cavilhada/prensada): 2 × Ø8 a 45 mm entre si, deslocados 9,5 mm do centro do caneco para dentro da porta. Versão de parafuso: 2 parafusos 3,5 × 16 pelas abas.
- **Calço (base)** na lateral do corpo: furos na linha de **37 mm** da borda frontal, espaçados **32 mm** (sistema 32), parafusos 3,5 × 16 ou bucha Ø5.
- **Tipo pela sobreposição** (o braço muda, o caneco não):
  - **Reta**: sobreposição total, a porta cobre toda a espessura da lateral (~16–18 mm).
  - **Curva**: sobreposição parcial (~8–9 mm), duas portas dividem a mesma divisória.
  - **Supercurva**: porta embutida no vão.
  - Especiais: 165°/170° (porta que precisa abrir totalmente, gaveteiro interno), 0 mm/"dobradiça para porta mimetizada no painel", canto 45°, para porta de alumínio/vidro, para porta grossa (até 35–40 mm com caneco de 40).
- **Quantidade por porta** (o que for maior):
  - Por altura: até 900 mm → 2; até 1600 → 3; até 2000 → 4; até 2400 → 5.
  - Por peso, em porta de ~600 mm de largura: até 7 kg → 2; 13 kg → 3; 17 kg → 4; 22 kg → 5 (tabela Salice série 300).
  - Porta com espelho, vidro ou ripas coladas: some o peso.
- Posição: primeira e última a **80–120 mm** do topo e da base; as demais distribuídas sem cair na altura de uma prateleira fixa.
- Amortecedor: dobradiça com amortecimento embutido (clip-on soft-close) ou pistão separado. **Push-open** (fecho toque) exige dobradiça SEM mola/amortecimento.
- Regulagem 3D típica: lateral −1,5 a +4,5 mm, altura ±2 mm, profundidade ~+3 mm. Use para alinhar folgas, não para corrigir erro de furação.

### 3.4 Puxadores
- Cava usinada (perfil J ou fresada no topo da porta), perfil de alumínio, puxador externo (furação na distância do modelo, ex. 96, 128, 160, 192, 256, 320 mm — múltiplos de 32) ou push-open.
- Porta mimetizada: cava escondida no topo/lateral, ripa como pega, ou push.

## 4. Gavetas e corrediças

- **Telescópica (rolamento)**: precisa de **12,5–13 mm de folga por lado** (total ~25–26). Caixa da gaveta: largura externa = vão interno − 25,4 (confira a ficha). Comprimento nominal ≤ profundidade interna − 10. Fixação na lateral do móvel na linha de 37 mm.
- **Oculta (Tandem, Movento, nacionais tipo "invisível")**: monta sob o fundo da gaveta. Padrão Blum para laterais de 16 mm: **largura interna da gaveta = vão − 42**; comprimento da gaveta = nominal − 10; fundo recuado 13 mm da base das laterais; traseira recortada para o gancho. Use a ficha do fabricante, os valores variam com a espessura da lateral.
- **Metálica (Legrabox, Tandembox, Antaro)**: medidas pelo configurador do fabricante.
- **Caixa de gaveta clássica**: laterais e traseira MDF 15 branco, fundo 6 em rasgo a 10 mm da base; laterais passantes, frente interna + frente decorativa (18) sobreposta, fixada por dentro com 4 parafusos.
- **Alturas úteis**: frentes 120–200 (talheres, roupas), 250–300 (panelas). Altura da lateral = altura da frente − ~30–50.
- Push para gaveta = ferragem específica (Tip-On ou similar) e corrediça sem amortecedor.
- Calcule com `calc_marcenaria.py gaveta`.

## 5. Furação e ligações

### 5.1 Sistema 32
- Grade de furos **Ø5 × 13 mm**, **espaçados 32 mm**, em duas linhas verticais nas laterais: frontal a **37 mm** da borda frontal e traseira a 37 mm do fundo (ou a um múltiplo de 32 da frontal).
- A grade serve para tudo: suporte de prateleira, calço de dobradiça, corrediça, minifix. Mantém o projeto modular e permite furar em furadeira múltipla.
- Primeiro furo ~32 mm acima da face da base (ou alinhado ao eixo de uma peça fixa). Use `calc_marcenaria.py sistema32`.
- Suporte de prateleira: pino Ø5 (metálico, com trava, ou "invisível" que entra num furo no topo da prateleira).

### 5.2 Minifix (excêntrico/tambor)
- **Tambor Ø15 × 12,5–13,5 mm** na face da peça horizontal (base, tampo, prateleira fixa), com centro a **34 mm** da borda (24 mm em peças finas; confira se o modelo é "34" ou "24").
- **Furo de passagem Ø8** no topo dessa peça, no eixo da espessura (9 mm na de 18), de comprimento até o tambor.
- **Haste/pino** na face da lateral: rosca em furo Ø5 (parafuso direto) ou bucha Ø8 (haste com bucha), na linha que coincide com o eixo do topo.
- Quantidade: 2 por junta até 600 mm de profundidade, 3 acima. Sempre combine com 1–2 **cavilhas** por junta para alinhar e resistir ao cisalhamento.
- Distância mínima da borda (frente/fundo): 32–50 mm.

### 5.3 Cavilha
- **Ø8 × 30** (padrão para 15–18). Profundidade: 12–13 mm na face (no máximo 2/3 da espessura, nunca furar através) e 18–20 mm no topo. Broca com limitador; cola PVA na cavilha.
- Ø6 × 30 para 15 mm finos; Ø10 para peças estruturais grossas.
- Gabarito de cavilhar ou furadeira de bancada garante o alinhamento entre face e topo.

### 5.4 Parafusos
- Parafuso de topo em MDF: **4,0 × 40–50** (chapa 18) ou confirmat **7 × 50** (furo Ø5 no topo + Ø7 na face com escareador). Furo-piloto sempre, ~85% do diâmetro do núcleo; nunca a menos de 25 mm do canto sem piloto (racha o MDF).
- Parafuso de face para ferragem: 3,5 × 16 (chapa 18) ou 3,5 × 12 (chapa 15).
- MDF segura mal parafuso no topo e quase nada após retirar e recolocar: em ligação que monta e desmonta, use minifix ou bucha.

### 5.5 Fixação na parede
- Aéreos: trilho/cantoneira de suspensão ou suspensor regulável (Camar etc.) + bucha 8 ou 10 em alvenaria. Drywall exige reforço (madeira/OSB ou perfil) previsto **antes** de fechar a placa.
- Estantes altas: sempre travar no topo na parede (anti-tombamento).

## 6. Plano de corte

### 6.1 Antes de otimizar
1. Lista de peças com: código, nome, material/cor/espessura, comprimento × largura **acabados**, quantidade, fita por aresta (C1, C2, L1, L2), sentido do veio, observação (rasgo, usinagem, furação).
2. **Convenção**: comprimento = dimensão no sentido do veio. Em MDF liso/unicolor, pode girar; em madeirado, **não gira** (ou só com OK do usuário).
3. **Fita**: com fita 0,45 a medida de corte = medida final (desprezível). Com fita 1 ou 2 mm, desconte a espessura da fita por aresta fitada, ou confirme se o serviço de corte (Cortecloud, Leo Madeiras etc.) já desconta automaticamente.
4. Peça maior que a chapa útil: divida com a emenda escondida atrás de uma divisória ou numa junta proposital.

### 6.2 Parâmetros
- **Refilo**: 10 mm em cada borda da chapa (bordas de fábrica são lascadas/fora de esquadro).
- **Kerf** (espessura da serra): 3–4,4 mm; use 4 se não souber.
- **Corte guilhotinado** (seccionadora e esquadrejadeira cortam de ponta a ponta): prefira algoritmos guilhotina; maxrects rende mais, mas pode gerar cortes impossíveis numa esquadrejadeira.
- Agrupe por material + espessura + cor. Considere 1 chapa como mínimo de compra por cor.
- Fita: some as arestas fitadas e acrescente 10% (perda em pontas e emendas).

### 6.3 Veio e aparência
- Portas e frentes em madeirado: veio **vertical** nas portas, **horizontal** em frentes de gaveta (ou contínuo vertical em gaveteiro "de veio corrido" — peça a decisão ao usuário).
- **Veio contínuo** (frentes de gaveta empilhadas, porta mimetizada no painel): corte as peças da mesma chapa, em sequência, e marque na lista "sequência de veio" com a ordem. No otimizador, agrupe essas peças como um bloco único antes de dividir.
- Peças visíveis lado a lado do mesmo lote de chapa (tonalidade varia por lote).

### 6.4 Conferência
- Última chapa quase vazia: ajuste medidas, troque espessura de peças internas, ou use retalho.
- Rendimento razoável: 75–90% por chapa.
- Etiquete cada peça com código e posição (o Cortecloud gera etiquetas).
- Antes de mandar: confira se nenhuma peça de referência (vidro, eletro, objeto) entrou no corte e se todas as medidas são acabadas.

## 7. Painel com porta mimetizada (porta oculta)

Porta de passagem (ou de armário) que some num painel de parede, ripado ou liso, sem batente aparente nem maçaneta à vista.

### 7.1 Decisões de partida
1. **Sentido de abertura**: o mais limpo é a porta **abrir para dentro do cômodo de trás** (empurrando, do lado do painel). Se abrir para o lado do painel, a ripa/face da folha colide com o painel vizinho e o painel precisa de recortes no lado da dobradiça.
2. **Tipo de giro**:
   - **Dobradiça invisível 3D** (Tectus/Simonswerk e similares nacionais, fresadas no topo da folha e no batente): melhor acabamento, giro 180°, regulagem ±3 mm. Ex.: TE 340 3D suporta 80 kg com 2 peças por folha (1 × 2 m); use 3 em folha alta ou pesada.
   - **Pivô** (pivô de piso + pivô superior, eixo deslocado 100–150 mm da borda): aguenta folhas grandes e pesadas (ripado maciço, até o teto), mas abre para os dois lados do eixo e invade o vão.
   - **Dobradiça de caneco de 0 mm/165°**: só para porta de armário mimetizada no painel (TV, rack), não para porta de passagem.
3. **Altura**: idealmente **até o teto** (sem bandeira) ou com o topo alinhado a uma junta horizontal do painel. Porta mais baixa que o painel deixa uma "bandeira" que precisa da mesma modulação.
4. **Fecho**: fechadura magnética silenciosa embutida (sem maçaneta, com cilindro ou rolete), fecho toque (push) para folhas leves, ou trinco rolete + cava. Puxar a porta exige uma pega: cava no topo/lateral, ripa como pega ou um puxador cava discreto do lado de trás.

### 7.2 Estrutura
- **Folha**: miolo estável (porta sólida/semissólida de 35–40 mm, ou MDF 30–36 com desempenador). Ripas e acabamento colados e parafusados por trás. Mesmo revestimento nas duas faces (balanceamento) para não empenar.
- **Batente**: batente invisível de alumínio (kit "porta invisível/rente à parede", ex. Eclisse Syntesis para drywall ou alvenaria) ou batente de madeira embutido, alinhado no **plano final do painel**. O painel, a folha e o batente precisam terminar no mesmo plano: calcule a espessura total (estrutura + base + ripa) antes de chumbar o batente.
- **Painel da parede**: base de MDF 15/18 sobre estrutura de sarrafos (30–40 mm) ou trilhos, nivelada e no prumo; ripas coladas e pregadas (pino sem cabeça) por trás, ou em perfil clicado.
- Peso: some ripas (MDF ripado 18 × 40 a cada 55 mm ≈ 10–12 kg/m²; maciço mais) e dimensione as dobradiças.

### 7.3 Modulação das ripas (o que faz a porta "sumir")
- Defina o **módulo = ripa + vão** (ex.: 40 + 15 = 55 mm). A largura do painel e a da porta são múltiplos inteiros do módulo.
- A **junta da porta cai sempre no meio de um vão** entre ripas: a borda da folha não aparece porque o vão já é escuro/profundo. Nunca corte uma ripa ao meio para a porta.
- A folga da porta (3 mm) precisa ser **menor que o vão** entre ripas. Pinte o fundo do vão de preto fosco ou da cor mais escura do conjunto.
- A largura de passagem resultante raramente é 800 exatos: escolha o múltiplo do módulo mais próximo (ex.: 15 × 55 = 825 → folha 822). Use `calc_marcenaria.py ripado`.
- Comece a modulação **pela porta** e distribua a sobra nas pontas do painel (meio módulo de cada lado) ou nos cantos, nunca ao lado da porta.

### 7.4 Painel liso (laca, laminado, MDF madeirado)
- Crie **juntas falsas** (frisos de 3–5 mm) repetindo a modulação do painel; a junta real da porta é só mais uma delas.
- Madeirado: veio vertical **contínuo** entre painel e porta (mesma chapa, sequência marcada no plano de corte); evite folha mais larga que a chapa.
- Laca: pinte porta e painel juntos, na mesma demão.

### 7.5 Folgas e giro
- Perímetro: **3 mm** (2–4) laterais e topo. Base: 5–10 mm acima do piso acabado (8 mm padrão; ripas podem descer até ~5 mm do piso).
- **Lado da fechadura**: a aresta da folha descreve um arco maior que a largura (√(L² + e²)). Faça um **chanfro de 3–5°** na borda da folha e do batente desse lado, ou aumente a folga, e confirme o giro numa planta 1:1 com o raio.
- **Lado da dobradiça**: com dobradiça invisível, a folga mínima é a da ficha (normalmente 3–4 mm); ripas na borda da folha do lado da dobradiça não podem passar do plano da folha.
- Rodapé: interrompa o rodapé na porta ou use rodapé embutido no próprio painel (o mesmo na folha). Soleira rente.
- Acústica/luz: escova ou perfil de vedação no batente; feltro atrás das ripas.

### 7.6 Checklist da porta mimetizada
- [ ] Sentido de abertura e lado da dobradiça definidos
- [ ] Plano final calculado (estrutura + base + ripa) e batente alinhado a ele
- [ ] Módulo das ripas com junta da porta no vão; sobra distribuída nas pontas
- [ ] Peso da folha somado e dobradiças dimensionadas (quantidade e modelo)
- [ ] Chanfro/folga do lado da fechadura conferido no giro
- [ ] Fecho e pega definidos (magnético, push, cava)
- [ ] Folga do piso, rodapé e soleira resolvidos
- [ ] Interruptor, tomada e quadro elétrico fora da folha e do giro
- [ ] Veio/sequência marcada no plano de corte (se madeirado)

## 8. Revisão de projeto antes do corte

- Esquema de montagem (laterais ou base passantes) aplicado igual em todas as peças.
- Toda porta tem dobradiças em quantidade e posição corretas e não colide com prateleira, gaveta, puxador vizinho ou parede (porta junto à parede precisa de 30–50 mm de enchimento/tampão para abrir 90°+).
- Gavetas: folga de corrediça descontada; gavetas internas atrás de porta precisam de enchimento para passar pela dobradiça.
- Vãos de prateleira dentro do limite de flecha.
- Peças com recorte em obra marcadas com sobra.
- Tomadas, interruptores, ar-condicionado, sanca/LED e rodapé existentes respeitados; passa-cabos (Ø60) onde houver eletrônico.
- Lista de ferragens fechada: dobradiças (tipo e quantidade), corrediças (tipo e comprimento), minifix, cavilhas, suportes, puxadores, pés, trilhos, pistões, fechos.
- Plano de corte por material, com veio respeitado e fita somada.

## Arquivos desta skill

| Arquivo | Função |
|---|---|
| `scripts/calc_marcenaria.py` | Calculadoras: portas e dobradiças, gaveta e corrediça, módulo de ripado, flecha de prateleira, furos do sistema 32 |
