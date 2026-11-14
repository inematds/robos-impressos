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
