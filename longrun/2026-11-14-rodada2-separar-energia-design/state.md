# Estado

- 14/11 07:1x: rodada aberta. E1 e E2 lançadas em paralelo.
- 14/11: brief da E3 escrito em E3-brief.md (lançar quando E1 e E2 terminarem). E5 (estrutura+docs+guia+publicar) ainda sem brief.
- 14/11: ordem 8 (banner a partir dos renders reais, cena Blender) registrada em goal.md; é trabalho da E5.
- 14/11: ordem 9 (imprimibilidade + reforços + teste 10) registrada; E6 (teste 10) lançada; E1 avisada por mensagem; E3-brief atualizado.
- 14/11: ordem 10 (avisa-v3 no fim, guardar msg N) registrada.

## Situação (atualizado 14/11 17:00, depois da queda das 10:20)
- FEITO e em commit: régua + "antes" (fe5b50f); teste 10/11 de imprimibilidade (48c9bb5); helper `ressalto_nervurado`, `imagem3d.py`, malhas medidas (fd85379; teto: capivara 0,927, dino 0,897).
- PERDIDO na queda: todo o trabalho do cubo/cubo_rodas (E1). Relançado às 17:0x.
- Regra nova: cada agente faz commit a cada pacote verificado e escreve uma linha aqui.

## Agentes lançados às 17:0x
| Etapa | O que faz | Dona de |
|---|---|---|
| E1 (refeita) | cubo (energia + redesenho + imprimibilidade) → commit → cubo_rodas → commit | `cad/modelos/cubo.py`, `cubo_rodas.py`, seções CUBO/CUBO_RODAS + componentes novos, `MODELOS` |
| E3a | capivara: esqueleto + casca da malha → furos/olhos/energia → imprimibilidade (3 pacotes, 3 commits) | `base.py`, `bicho.py`, `capivara.py`, seções BASE/PESCOCO/CAPIVARA, `cad/peles/` |
Depois: E3b dino (mesma receita), consolidação (`gerar todos` + `verificar todos` por mim), E4, E5a–d, publicar, avisa-v3.

## Próximas etapas (ainda não lançadas)
- E3a capivara → E3b dino (brief em `E3-brief.md`; sequência: esqueleto+forma → furos/olhos/energia → imprimibilidade; commit + verificador a cada pacote).
- E4 números "depois" (régua) dos 4.
- E5 dividida em 4: (a) reorganização `projetos/` + `comum/` com o verificador de portão; (b) renders, cena do banner no Blender, mapas de balanços; (c) docs e listas de compras por robô; (d) guia (entrada + 4 páginas × 3 idiomas), tradução, revisor.
- Eu mesmo: push, tag v1.1.2, conferência das URLs, portal (só se título/descrição disser "três robôs"), `avisa-v3.sh`, relatório.
- 14/11: PORTAL precisa de ajuste no fim: Portal.tsx:119 e translated-courses id 10225 dizem "Três corpos… ~33 cm" (vira quatro robôs; altura nova). Título de courses.ts cita "dino, capivara ou cubo" (avaliar).
- 14/11: conselheiro consultado; E1 avisada (teste 10 só nos cubos; helper ressalto_nervurado); E3-brief com sequência em 3 pacotes e regra de parada.
- 14/11 E3a: conversor da malha (cad/pele_malha.py), classe PeleGrade (geo.py) e pele processada cad/peles/capivara.npz (300 mm, simétrica, 2,3 MB) em commit; nenhum modelo alterado ainda.

## PAUSA 14/11 ~17:10 (Nei vai reiniciar a máquina)
- Orquestrador e agentes E1/E3a PARADOS de propósito. Último commit de trabalho: 6816d13 (pele da capivara).
- E1 (cubo energia + cubo_rodas) tinha relançado às 17:0x e não chegou a commitar: começar a E1 do zero.
- E3a capivara: pacote 1 parcial (conversor + pele em commit); falta aplicar a pele no modelo `capivara.py`.
- Para retomar: sessão nova em ~/projetos/robos-impressos, Fable 5.2 high, ler goal → state → plan → canal → decisions → E3-brief → E5-brief e seguir "Agentes lançados às 17:0x". Ordens do Nei estão em goal.md (1–10), inclusive avisa-v3 no fim.

## RETOMADA 14/11 (sessão nova, depois do reinício)
- Briefs originais da E1 e da E3a recuperados do histórico e gravados em `E1-brief.md` e `E3a-brief.md` (+ bloco RETOMADA); pesquisa de energia das 10:16 em `pesquisa-energia.md`.
- E1 e E3a relançadas em paralelo (Fable, esforço high). Donos de arquivo: os mesmos da tabela "Agentes lançados às 17:0x".
- 14/11 E1 pacote 1: componentes de energia (STEPDOWN5V, UBEC6V, CARREGADOR2S, BMS2S) em parametros.py + C.modulo + geo.berco_modulo; receita no canal.md.
- 14/11 E1 pacote 2: cubo redesenhado (tilt interno, copo sem ponte, energia 2S, furos discretos); 11 testes passando; IoU 0,755 → 0,797. cad/comum/quadrado.py é o código comum com o cubo_rodas.
- 14/11 E3a pacote 1a: capivara refeita sobre a pele da malha (bacia + porta traseira + gola + cabeça em vasos de corte horizontal) e esqueleto baixo novo (cad/comum/base_baixa.py, casca.py); verificador 1–9 passando (dino também), IoU médio 0,921 (antes 0,777, alvo 0,852); falta: peças coloridas, limpeza do pescoço, pacotes 2 e 3.
- 14/11 E1 pacote 3: 4º robô cubo_rodas (306,5 mm, 2 JGB37 + rodas 85 mm + bola atrás, pack 3S, tela 5", LiDAR no topo); 11 testes passando; registrado em gerar/verificar/tabelas. IoU depois: cubo 0,797; cubo_rodas 0,669 (referência do cubo de mesa).
- 14/11 E3a pacote 1 FECHADO: capivara com peças coloridas recortadas da malha (focinho, orelhas, mãos, rabo, avental da bandana, topete, aro ciano); verificador 1–9 passando; régua gravada como "depois": IoU médio 0,920 (frente 0,939 · 3/4 0,908 · lado 0,907 · costas 0,924; antes 0,777; teto 0,927; alvo 0,852). Pendências de forma: laço da bandana, patas marrons, olhos maiores (entra no pacote 2).
- 14/11 E1 correções pós-revisão: postes da frente do cubo_rodas saíram do canto (furavam a parede de fora), pino do tilt M5 + furos de acesso de chave, ordem de bancada; cubo e cubo_rodas com 11 testes passando de novo.
- 14/11 (retomada): E1 FECHADA (fb3b893, 72a5bf8, 4b2e52b, f28eb9c, 9fdf7cf). cubo 15 peças, 11/11; cubo_rodas 19 peças, 11/11, CG z=127, margem 37,6 mm na pior pose, frenagem máx 0,30 g. IoU cubo 0,755 → 0,797 (alvo +0,10 = 0,855 NÃO atingido; 0,827 exigiria tilt −15°: pendência para o relatório). 72a5bf8 levou linhas em andamento da E3a em parametros.py (sem dano; E3a segue dona da seção).
- 14/11 E3a pacote 2 FECHADO: olhos com sensor (câmera na pupila direita, ToF na esquerda; decisão (b) em decisions.md), mandíbula sem furo no rosto, microfones nas narinas, alto-falante na mesa da cabeça, ToF laterais no miolo dos aros, carregador USB-C dentro do rabo, step-down/UBEC/BMS/chave fixados no chassi; verificador 1–9 passando na capivara e no dino; IoU 0,920. Falta: pacote 3 (teste 10).
- 14/11 E3a pacote 3 FECHADO: capivara com os 11 testes passando (23 de 29 peças sem suporte; 6 com suporte declarado: crânio por dentro, corpo 1,0 %, porta, mandíbula, garfo e berço comuns); dino segue passando 1–9 e 11; régua final IoU 0,919–0,920; fatos, receita para o dino e pendências em canal.md.
- 14/11 noite: ordens 11 (cubo primeiro: lista, STL, página, portal, aviso) e 12 (página de evolução) gravadas em goal.md.
- 14/11 E3a FECHADA (revisão final): parede da gola medida (3,38 mm; casca esférica engrossada e esfera completa no campo), mandíbula aliviada contra a esfera do soquete em todos os ângulos (o mesmo alívio na zona varrida), código morto e docstrings corrigidos; capivara 11/11, IoU 0,921, 197 × 274 × 300 mm, 1714 g. Bloco "VALE ESTE" em canal.md.
