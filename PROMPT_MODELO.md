# Prompt modelo: projeto de marcenaria

Copie o bloco abaixo como primeira mensagem para o agente (Claude Code, Claude.ai ou outro) com a skill `marcenaria-planejados` instalada. Preencha o que estiver entre colchetes e apague as linhas que não se aplicam. Se não souber alguma medida, escreva "não sei". O agente vai marcar como estimada e pedir para confirmar depois.

---

```markdown
Use a skill marcenaria-planejados para projetar os móveis planejados em MDF deste cômodo. Responda em português, de forma direta.

## 1. O cômodo
- Cômodo: [ex.: quarto de hóspedes / escritório / quarto do bebê]
- Medidas das paredes, em metros, no sentido horário a partir da porta:
  - Parede 1 (da porta): [0,00]
  - Parede 2: [0,00]
  - Parede 3: [0,00]
  - Parede 4: [0,00]
  - Recuos, pilares ou vigas: [descrever, ou "nenhum"]
- Pé-direito: [0,00] (forro de gesso? [sim/não])
- Porta: na parede [n], a [0,00] do canto [esquerdo/direito]. Largura da folha [0,80]. Abre para [dentro/fora] e para o lado [esquerdo/direito].
- Janela: na parede [n], começa a [0,00] do canto. Largura [0,00], peitoril [0,00], altura [0,00].
- Tomadas e interruptores: [parede, distância do canto e altura de cada um]
- Outros pontos fixos: [ar-condicionado, sanca de LED, cortineiro, rodapé, quadro de luz...]
- Fotos: [anexe as fotos de cada parede]

## 2. O que eu quero
- Quem usa e como: [ex.: home office para 1 pessoa, 8 h por dia, 2 monitores]
- Móveis e onde ficam:
  1. [ex.: mesa de 2,00 x 0,70 na parede 2, com gaveteiro de 3 gavetas]
  2. [ex.: estante do piso ao teto na parede 4, profundidade 0,30]
  3. [ex.: armário com portas embaixo da janela]
- Equipamentos e objetos que precisam caber, com medidas: [ex.: impressora 0,45 x 0,35 x 0,25; violão; 200 livros; caixas de arquivo]
- Referências de estilo: [anexe imagens ou descreva: prateleiras em tijolinho, portas com puxador cava, nichos abertos...]
- O que não pode: [ex.: nada sob a janela; manter 0,90 livre para circulação]

## 3. Material e fabricação
- MDF das faces aparentes: [espessura 18] na cor [nome da cor e do fabricante]. Tem veio? [sim/não]
- Caixas de gaveta: [MDF 15 branco]
- Fundos: [MDF 6 na cor do móvel / branco]
- Fita de borda: [0,4 x 22 mm]
- Chapa do fornecedor: [2750 x 1850] mm. Espessura da serra (kerf): [4] mm.
- Ferragens preferidas: [corrediça telescópica, dobradiça com amortecedor, puxador...]
- Quem vai cortar: [Cortecloud / marceneiro / loja de chapas]

## 4. Como quero trabalhar
- Primeiro, a tabela de medidas marcando o que é medido e o que é estimado, e as dúvidas.
- Depois, o modelo 3D e as vistas 2D. Eu reviso mandando prints do 3D com o que mudar.
- Por último, o plano de corte em PDF, a lista de peças com fita de borda e o CSV para importar no [Cortecloud].
- Se quiser comparar layouts, gere opções A, B e C.
- Aponte problemas de ergonomia, folgas, vãos longos e conflitos com tomadas ou janela. A decisão final é minha.
- Salve tudo na pasta [nome da pasta do projeto]. Ao fim de cada rodada, mantenha um DECISOES.md e um PROMPT_CONTINUACAO.md atualizados.

Comece preparando o ambiente e me mostrando a tabela de medidas com as dúvidas.
```
