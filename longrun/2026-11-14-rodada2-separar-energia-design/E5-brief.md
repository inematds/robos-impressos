# Etapa E5 — reorganizar, renderizar, documentar, guia (dividida em 4 agentes; o orquestrador publica)

Leia antes: `CONTEXTO.md`, `goal.md` (itens 1, 5, 8, 9 e o critério de pronto), `state.md`, `canal.md`, `decisions.md`.
Estado de partida: os 4 modelos (`dino`, `capivara`, `cubo`, `cubo_rodas`) passam nos 11 testes de `cad/verificar.py`.
Nenhum agente da E5 faz push, tag, post no Telegram nem mexe no portal. Commit local a cada pacote + linha em `state.md`.

## E5a — estrutura `projetos/` + `comum/` (portão: verificador passando nos 4, antes e depois)
Destino (decidido pelo orquestrador):
```
comum/
  README.md               o que é comum e como cada robô usa
  cad/                    TODO o código: parametros.py, comum/ (biblioteca), gerar.py, verificar.py, comparar.py,
                          tabelas.py, render_*.py, renders.sh, vistas.sh, depurar.py, onde.py, peles/, imagem3d.py
  pecas/{stl,3mf}/        peças comuns (chassi, bandejas, garfo, berço, teste-encaixe…), se continuarem comuns
projetos/
  dino/        README.md · PLANO.md · LISTA-DE-COMPRAS.md · modelo.py · stl/ · 3mf/ · mesas/ · componentes/ ·
  capivara/    imagens/ · montagem.json · montagem.glb · mesas.json · verificacao.json · verificacao-saida.txt
  cubo/
  cubo-rodas/  (pasta com hífen; id do modelo no código continua `cubo_rodas`)
README.md (+ .en/.es)     índice: os 4 robôs, o que é comum, "O processo, do início ao fim", versão
PLANO.md                  só decisões gerais + ponteiros para o PLANO de cada robô
comparacao/               tabela de semelhança (fica na raiz)
guia/                     guia (E5d)
```
- `modelo.py` de cada robô = o antigo `cad/modelos/<id>.py`; `gerar.py`/`verificar.py` carregam por caminho (importlib)
  a partir de um registro único `MODELOS = {id: pasta}` em UM lugar. Comandos novos:
  `.venv/bin/python comum/cad/gerar.py <id|todos>` e `.venv/bin/python comum/cad/verificar.py <id|todos>`.
- Use `git mv` (preserva histórico). Atualize TODOS os caminhos: scripts de render/vistas/tabelas/comparar, `guia/src/*.py`,
  `.gitignore`, `requirements.txt`, docs. Procure caminhos antigos com `grep -rn "pecas/\|cad/" --include=*.py --include=*.sh
  --include=*.md --include=*.html --include=*.json` e resolva cada um (o guia publicado tem links para pastas do GitHub).
- Portão: `gerar.py todos` + `verificar.py todos` passando nos 4 com os MESMOS números de antes (compare os
  `verificacao.json`); `comparar.py` rodando; clone limpo em `.preview/clone` + venv novo + `gerar`/`verificar` de um
  modelo pequeno (cubo) para provar que nada depende de arquivo fora do git.
- Grave em cada `projetos/<robô>/verificacao-saida.txt` a saída real do verificador daquele robô.

## E5b — renders finais, banner em cena no Blender, mapas de balanços
- Renders de cada robô em `projetos/<robô>/imagens/`: montado, explodido, esqueleto, mesas, 4 vistas (as MESMAS da
  referência), sempre por `~/projetos/wifi/scripts/fila-vaga render robos -- …`. Confira a olho (Read) cada imagem:
  frente e 3/4 sem furo técnico nem parafuso à vista.
- Mapa de balanços (faces sem apoio em vermelho) das peças principais de cada robô: `cad/render_balancos.py`.
- Lado a lado final (referência × render) e IoU "depois" dos 4 (`comparar.py --rotulo depois`); as imagens lado a lado
  ficam em `referencia/comparacao/` (fora do git).
- **Banner do guia a partir dos modelos reais** (ordem 8): cena no Blender com os 4 robôs sobre mesa de madeira, luz
  quente, fundo desfocado (profundidade de campo), cores/materiais dos modelos. Saídas no padrão do guia (banner "live"
  e banner "grade", PT/EN/ES; veja como `guia/assets/banner*.jpg` e `hero.png` são usados em `guia/src/`) e a capa
  `capa/capa.png`. Texto dos banners por composição (PIL/HTML), não por IA. Se usar o Codex `image_gen` só para
  acabamento, passe o render como referência e CONFIRA: dino com 2 pernas (pés de 3 dedos creme), 2 bracinhos e cauda;
  capivara em pera compacta, patas de trás grossas na frente, mãos na barriga, cabeça larga encostada, bandana verde;
  cubo sem pernas; cubo-rodas com a base de rodas. Na dúvida, fique com o render puro.

## E5c — documentação por robô e listas de compras
- `projetos/<robô>/README.md`, `PLANO.md` (decisões e porquês, peças impressas com a tabela nova: orientação, suporte
  sim/não/onde/tipo, perímetros, infill, material, motivo do reforço; passo a passo de montagem e de abertura; seção
  "Preparado para a fase 2" com a decisão dos OLHOS e onde ficou cada sensor/furo disfarçado; energia; pendências).
- `projetos/<robô>/LISTA-DE-COMPRAS.md`: só o que AQUELE robô usa: item, quantidade, para que serve, preço ESTIMADO
  (marcado como estimativa, faixa em R$, data da consulta) e link de busca `https://lista.mercadolivre.com.br/<termos-com-hífen>`.
  Energia completa em todos: bateria, carregador, step-down 5 V do Pi, regulador 6 V dos servos, driver dos motores,
  chave, fios. Itens de fase 2 (câmeras, ToF, mic, alto-falante, IMU, LiDAR) em bloco separado "fase 2 (opcional agora)".
  Preço: consulte páginas públicas de busca; se não der para consultar, escreva a faixa como estimativa e diga que não
  foi conferida. Nunca invente preço "exato".
- Tabelas geradas por `tabelas.py` (marcadores `<!-- TABELA:... -->`), não digitadas. README raiz PT/EN/ES com o índice
  dos 4, a seção "O processo, do início ao fim" (passos numerados, comando e quem faz) e a versão **v1.1.2**.
  Tradução EN/ES só por `inema-traduz` (veja `guia/src/traduzir_readme.py`).
- `comum/README.md`; `FALHAS.md`; `PLANO.md` raiz com a tabela de semelhança antes × depois e o resumo da imprimibilidade.

## E5d — guia (entrada + página de cada robô, PT/EN/ES) e revisor
- `/guia/`, `/guia/en/`, `/guia/es/` continuam existindo (viram a ENTRADA com os 4 robôs); cada robô ganha página
  própria: `/guia/<robô>/`, `/guia/en/<robô>/`, `/guia/es/<robô>/` (pastas `dino`, `capivara`, `cubo`, `cubo-rodas`).
  Âncoras antigas da página única não podem cair no vazio: mantenha as seções gerais na entrada ou redirecione.
- Conteúdo por robô: chamada (regra D20: abre pela dor/desejo de quem lê, em "você"), o que é, fotos (renders reais),
  comparação com a referência NÃO entra (a referência é privada) mas os números de semelhança sim, peças e mesas,
  mapa de balanços, lista de compras com os links, montagem, fase 2 (olhos com sensor), downloads, verificação.
- Mesma mecânica de hoje: estrutura única + textos por idioma (`guia/src/`), tabelas injetadas, tradução por
  `inema-traduz` com cache. Leia `~/.claude/skills/projetos-landing-guia/SKILL.md` e `~/projetos/inema-design/DESIGN.md`.
- Banners novos da E5b. hreflang e links de idioma em todas as páginas.
- Revisor independente conforme `~/.claude/runbooks/revisor-independente.md` é chamado pelo ORQUESTRADOR, não por você.

## Acréscimo (ordem 12): página `/guia/evolucao/` na E5d
Capivara e dino: renders próprios antes (worktree `.preview/v102` da tag v1.0.2, receita no canal) × depois, nas mesmas 4 vistas da régua; tabela de IoU por vista (antes, depois, teto da malha, alvo); explicação curta de como ler o IoU. NÃO publicar os lado a lado, máscaras ou renders da malha crua (contêm/derivam da referência do Nei), salvo autorização dele registrada em decisions.md. A página `/guia/cubo/` já existe (feita na etapa "cubo primeiro"): a E5d integra, não refaz.
- ATUALIZAÇÃO 14/11 noite: o Nei AUTORIZOU (decisions.md) usar na `/guia/evolucao/` as imagens de referência e os lado a lado referência × render (`referencia/comparacao/<bicho>-antes|depois.png`). Copie só as imagens usadas para `guia/evolucao/assets/` (redimensionadas, JPG); o resto de `referencia/` (malhas, máscaras, recortes) continua fora do git.
