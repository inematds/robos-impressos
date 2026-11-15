# CONTEXTO da rodada 2 (leia inteiro antes de mexer) — robos-impressos

Repo: `~/projetos/robos-impressos` (remoto `inematds/robos-impressos`, branch main, publicado; guia em
https://inematds.github.io/robos-impressos/guia/ + /en/ + /es/). Estado de partida: tag `v1.0.2` + commit `ab51a39`.
Fase 1 = SÓ mecânica e encaixe. Nada foi impresso. Tudo em português do Brasil.

## Comandos (sempre com o venv do repo)
```
cd ~/projetos/robos-impressos
.venv/bin/python cad/gerar.py <modelo|todos>      # STL/3MF/montagem.json/mesas  (dino, capivara, cubo)
.venv/bin/python cad/verificar.py <modelo|todos>  # 9 testes; sai 1 se falhar; grava pecas/<m>/verificacao.json
.venv/bin/python cad/depurar.py <modelo>          # volume/corpos/caixa de cada peça, sem exportar
.venv/bin/python cad/onde.py <modelo> [pose]      # ONDE cada par se sobrepõe (caixa em mm)
cad/vistas.sh <modelo> <saida.png> 600x600 40 --sem-componentes   # 4 vistas rápidas (Blender Cycles CPU, ~15 s)
cad/renders.sh <modelo>                           # renders finais em imagens/ (usa fila-vaga render)
.venv/bin/python cad/tabelas.py                   # injeta tabelas nos docs (marcadores <!-- TABELA:... -->)
```
Build de um bicho ≈ 25–40 s; do cubo < 1 s. Verificar ≈ 1 min por bicho.

## Arquitetura do CAD (trimesh + manifold3d; eixos: X lados, +Y frente, Z cima, chão Z=0, eixo das rodas Y=0)
- `cad/parametros.py`: TODAS as medidas. Componentes com a fonte ao lado: P (fabricante), T (loja/terceiro), NC (não
  confirmado: valor usual, marcar). Seções: IMPRESSORA, FOLGA, componentes, BASE (esqueleto dos bichos), PESCOCO, DINO,
  CAPIVARA, CUBO, CORES. Cada modelo tem `n_pecas` (contagem esperada, teste 1).
- `cad/comum/geo.py`: sólidos exatos (caixa, cil, esfera, prisma(pts, eixo, a, b), secao, casco, engrenagem,
  ret_arredondado), `Pele` (campo de blobs → marching cubes → Manifold; `.solido()`, `.deslocado(±mm)` com distância
  REAL, `.ponto_na_pele(origem, direção)`), `maior_corpo`, `arrastar` (varredura), `limpar`, `desbeliscar`, `medir_parede`.
- `cad/comum/componentes.py`: envelopes dos componentes comprados (sistema local documentado em cada função) + `M(R,t)`.
- `cad/comum/modelo.py`: `Peca` (nome, solido na posição de MONTAGEM, material, cor, grupo cinemático, `imprimir` =
  rotação montagem→mesa, suporte, comum, copias, explode, macica, liso), `Comp`, `Junta`, `Modelo` (pecas, comps, juntas,
  apoios, poses, obs, encaixes, ordem).
- `cad/comum/base.py`: esqueleto comum dos bichos (chassi = piso + rack de bandejas + deck; bandejas Uno/Pi; garfo e
  berço do pescoço pan+tilt com MG996R; peças pequenas; `comps_base`; `ordem_bicho` = ordem de montagem E de abertura).
- `cad/comum/bicho.py`: casca dos bichos (torso frente/costas com gola esférica R=58 no topo, pernas, traseiro, cabeça
  = crânio + mandíbula, olho, crista, painel, unha/domo, `mecanica_cabeca`, `frente_com_painel`).
- `cad/modelos/{dino,capivara,cubo}.py`: `construir() -> Modelo`.
- `cad/gerar.py`, `cad/verificar.py`, `cad/tabelas.py`, `cad/render_blender.py`, `cad/renders.sh`, `cad/vistas.sh`.
- Saída hoje: `pecas/<modelo>/{stl,3mf,mesas,componentes}/`, `pecas/comum/`, `imagens/`. (A reorganização em
  `projetos/<robô>/` + `comum/` é a ÚLTIMA etapa da rodada: até lá, não mude caminhos de saída.)

## Os 9 testes do verificador (todos têm que passar em todos os modelos)
1 contagem (= `n_pecas`) · 2 malha (STL fechado, 1 corpo) · 3 mesa (≤ 256³ na orientação de impressão) · 4 parede
(cascas ≥ 2,0 mm; `obs["parede_medida"]`) · 5 interferência (volume booleano > 1 mm³ entre quaisquer peças/componentes,
em TODAS as poses) · 6 teste negativo · 7 peça solta · 8 equilíbrio (CG dentro dos apoios, margem ≥ 10 mm, todas as
poses) · 9 caminho (cada passo de `Modelo.ordem`: a peça vem de fora na direção `dir`, contra o que já está montado;
passos com `sai=True` testam a ABERTURA para manutenção).
Sobreposição proposital (eixo no cubo da roda, horn no rebaixo) entra em `Modelo.encaixes` com o motivo.

## Armadilhas já pagas (não repita)
- `prisma()` exige polígono simples; orientação é corrigida sozinha. Peça VAZIA aborta o `gerar`.
- Corte que pode deixar ilha → `maior_corpo()` logo depois. Arestas beliscadas são tratadas no `gerar` (`desbeliscar`).
- Orelha de parafuso não pode ter material embaixo do furo do inserto. Orelha que cai no poço da roda fica solta.
- Varredura de obstáculo: visto da peça, o obstáculo anda no sentido OPOSTO ao movimento dela.
- Posição final sem interferência NÃO basta: declare o passo em `ordem` e deixe o teste 9 provar que entra e que sai.
- Componente novo = medida com fonte em `parametros.py` + envelope em `componentes.py` + `Comp` no modelo (massa!).
- Classe CSS `.num` já existe no template do guia. No guia, número digitado à mão envelhece: use `cad/tabelas.py`.
- Blender daqui não tem denoiser (já tratado). Render pesado: `~/projetos/wifi/scripts/fila-vaga render <quem> -- cmd`;
  GPU: `~/projetos/wifi/scripts/fila-vaga gpu <quem> -- cmd` (leia `~/projetos/wifi/scripts/README-vagas.md`).

## Regras do Nei que valem aqui
- NENHUMA API externa/paga (Magnific, fal, Replicate, Tripo, OpenRouter…). Codex e Claude só pela assinatura. Baixar
  pesos abertos (Hugging Face) para rodar LOCAL é permitido. Tradução EN/ES só por `inema-traduz`.
- NÃO postar no Telegram, NÃO mexer no portal, NÃO consultar o Vercel. Push e tag: só a etapa final (E5) faz.
- Commits locais ao fim de cada pacote: autor `inematds <inematds@gmail.com>` (já configurado no repo), mensagem
  terminando com `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`. Sem `git push`.
- Não inventar número: medida de componente com fonte (URL) ou marcada NC; tempo/filamento/preço = estimativa.
- Falha real corrigida → linha no topo da tabela de `FALHAS.md` do repo. Barreira de ambiente → linha em
  `~/projetos/wifi/LIMITES.md`. Fato útil para as outras etapas → acrescente em `canal.md` desta pasta (só acrescentar).
- Arquivos temporários: `~/projetos/robos-impressos/.preview/` (ignorado pelo git). Não deixe servidor rodando.
- `referencia/` (imagens do Nei) está fora do git de propósito: não publique.
- Relatório final de cada etapa: curto, com caminhos absolutos, números reais e o que ficou pendente, sem enfeite.

## ACRÉSCIMO (ordem 9 do goal.md): imprimibilidade e reforços — vale para TODA peça que você criar ou alterar
- Projete para imprimir SEM suporte: face plana na mesa, balanços ≤ 45°, pontes ≤ 15–20 mm, furo horizontal em gota,
  chanfro de 45° nas bordas viradas para baixo, linha de corte da casca escolhida para isso. Suporte só quando
  inevitável, em árvore, fora do rosto e dos encaixes, declarado em `Peca.suporte` ("não" ou "sim (onde, tipo)").
- Reforce: nervuras na casca, ressalto com 2–3 nervuras em cada inserto/parafuso (parede ≥ 2× Ø do inserto), filete na
  base de pinos/abas, camadas ao longo da carga em garfo/tubo/abas. Declare por peça perímetros, infill e o motivo do
  reforço (campos novos em `Peca`: veja `cad/comum/modelo.py`; se ainda não existirem, a etapa E6 está criando).
- O verificador ganha o teste 10 "imprimibilidade" (etapa E6, módulo `cad/comum/imprimibilidade.py`): peça declarada sem
  suporte com área sem apoio acima do limite FALHA. Rode-o nos seus modelos antes de fechar a etapa.

## ACRÉSCIMO 2: política para o INTERIOR das cascas ocas (decidido pelo orquestrador em 14/11)
Meia casca impressa sobre a face da costura é uma cúpula: o teto da cavidade é face virada para baixo muito além de 45°.
Regra, nesta ordem de preferência:
1. Escolha a linha de corte/orientação que dê parede subindo a ≤ 45° (ex.: imprimir a casca "de pé" sobre a borda de
   baixo, como um vaso, em vez de deitada sobre a costura; dividir a cabeça em anéis/calotas).
2. Teto da cavidade em ogiva: engrosse o ápice por dentro (cone/telhado a 45°) para a cavidade fechar em ponta. O
   interior não aparece: pode ter material a mais, desde que não bata no esqueleto (teste 5).
3. Só se 1 e 2 não derem: suporte em árvore DENTRO da casca (não aparece), declarado em `Peca.suporte` como
   "sim (interior da casca, árvore)". Nunca suporte em face externa visível do rosto nem em encaixe.
Não se resolve afrouxando o limite do teste 10.
O teste 10 não mede reforço: ressalto de inserto sai do helper único `ressalto_nervurado` de `cad/comum/geo.py` (a E1
está criando; veja `canal.md`), e peça estrutural tem `perimetros` ≥ 4 e `reforco`/`orientacao` preenchidos.
Nota do orquestrador sobre o aprendizado da E6 ("tigela com a boca para cima zera o teto"): vale para o INTERIOR; por
fora, a tigela de boca para cima apoia num ponto e a parede externa nasce quase horizontal (reprova do mesmo jeito, e
em face VISÍVEL). O que resolve os dois lados é imprimir a casca "em pé" como um vaso (corte horizontal, anéis cujas
paredes sobem perto da vertical), com a base plana na mesa, fechando o topo em ogiva ou em peça separada (calota/tampa).
O verificador agora tem 11 testes (10 imprimibilidade, 11 negativo da imprimibilidade).

## ACRÉSCIMO 3 (E5a, 15/11): ESTRUTURA NOVA — vale sobre os caminhos e comandos escritos acima
O repo foi reorganizado. Onde este arquivo (e o canal, os briefs e o FALHAS.md) diz o caminho da esquerda, leia o da direita:

| antes | agora |
|---|---|
| `cad/…` (scripts, `parametros.py`, `comum/`, `peles/`) | `comum/cad/…` |
| `cad/modelos/<id>.py` | `projetos/<robô>/modelo.py` |
| `pecas/<id>/{stl,3mf,mesas,componentes}/`, `montagem.json`, `montagem.glb`, `mesas.json`, `verificacao.json` | `projetos/<robô>/…` (mesmos nomes) |
| `pecas/comum/{stl,3mf}/` (garfo-pescoco, berco-tilt, capa-esfera, teste-encaixe) | `comum/pecas/{stl,3mf}/` |
| `pecas/comum/…` chassi, bandeja-pi, bandeja-uno, pino-guia, bucha-eixo (órfãos) | `comum/legado/{stl,3mf}/` |
| `imagens/<id>-*.jpg` | `projetos/<robô>/imagens/<id>-*.jpg` |
| `pecas/TABELAS.md`, `pecas/verificacao-saida.txt` | `projetos/TABELAS.md`, `projetos/verificacao-saida.txt` (+ um por robô) |
| `pecas/LEIAME.md` | `comum/README.md` |

`<robô>` = pasta: `dino`, `capivara`, `cubo`, `cubo-rodas`. O id no código, em `parametros.py` e no nome dos STL continua
`cubo_rodas`. Registro ÚNICO id → pasta: `comum/cad/caminhos.py` (`MODELOS`, `pasta(id)`, `construir(id)`, `rel_comum`).
O pacote Python continua `cad` (`from cad import parametros`, `from cad.comum.geo import …`): a raiz de import é `comum/`.
```
.venv/bin/python comum/cad/gerar.py <id|todos>
.venv/bin/python comum/cad/verificar.py <id|todos>
.venv/bin/python comum/cad/depurar.py <id>            .venv/bin/python comum/cad/onde.py <id> [pose]
.venv/bin/python comum/cad/comum/imprimibilidade.py <id> [peça]
.venv/bin/python comum/cad/comparar.py <id> --sem-gravar        # sem a opção, regrava comparacao/ e referencia/comparacao/
.venv/bin/python comum/cad/tabelas.py
comum/cad/vistas.sh <id> <saida.png> 600x600 40 --sem-componentes
comum/cad/renders.sh <id>                              # saída em projetos/<robô>/imagens/
.venv/bin/python guia/src/pagina_robo.py docs|pagina|zip|conferir <robô>
```
