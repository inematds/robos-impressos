# Objetivo da rodada 2 (pedido do Nei em 14/11/2026, via coordenador)

1. **Separar cada robô** em `projetos/<robô>/` (README, PLANO, LISTA-DE-COMPRAS com qtd, preço estimado e link
   `https://lista.mercadolivre.com.br/<termos>`, stl/, mesas 3MF, imagens, verificação) e o comum em `comum/`.
   Guia: página de entrada com os robôs + página própria de cada um, PT/EN/ES, sem quebrar /guia/, /guia/en/, /guia/es/.
2. **Energia**: no cubo faltavam step-down 5 V 3 A (Pi), UBEC 6 V 3 A (2 MG996R) e carregador de 18650: pôr na lista,
   modelar os volumes na base com fixação e provar no verificador. Mesma auditoria nos bichos (Pi 5 V/3 A, servos 6 V).
3. **Design mais perto das referências** (`referencia/*.png`): tentar image-to-3D LOCAL na GPU; se não der malha
   utilizável, esculpir melhor. Medir: mesmas 4 vistas, lado a lado, IoU de silhueta antes × depois.
4. **4º robô `cubo-rodas`**: cubo que roda, ≥ 30 cm, tela maior, pan amplo (engrenagens 2:1 + tubo oco) + tilt, tração
   diferencial com encoder, CG provado (parado, cabeça nos extremos, frenagem/aceleração estimadas), fase 2 preparada,
   LiDAR avaliado, lista de compras própria.
5. Renderizar tudo de novo (inclusive banner do guia), versão **v1.1.2**, commit + push, guia trilíngue, revisor independente.
   Portal só se título/descrição mudar. NÃO postar no INEMA.ROBOT.

## Critério de pronto (comando → saída esperada) — revisto em 14/11 depois das ordens 6–10
- `.venv/bin/python cad/verificar.py todos` (ou o caminho novo depois da reorganização) → 4 linhas `=> <modelo>: TUDO PASSOU`
  para `dino`, `capivara`, `cubo`, `cubo_rodas`; 10 testes `[PASSOU]` por modelo (9 antigos + imprimibilidade), nenhum
  `[FALHOU]`; exit 0. O limite do teste 10 é o que a E6 justificou, sem afrouxar.
- Declarativo: toda peça estrutural com `perimetros` ≥ 4 e `reforco`/`orientacao` preenchidos; toda peça com `suporte` declarado.
- Semelhança: tabela IoU antes × depois por robô e por vista gravada (`comparacao/semelhanca.*`) + imagens lado a lado
  em `referencia/comparacao/`. Regra de parada definida ANTES de ver o "depois": alvo = pelo menos metade da distância
  entre o "antes" e o teto da malha crua da E2 (ou +0,10 de IoU médio se não houver malha), no máximo 6 iterações de
  forma por bicho; 3 iterações seguidas sem ganho ≥ 0,01 → parar e relatar.
- Frente e 3/4 dos renders: nenhum furo técnico nem parafuso visível (conferido a olho nas imagens finais, por robô).
- Olhos: pupila como peça separada com bolso de câmera/sensor; decisão (a/b/c) escrita no PLANO de cada robô.
- Energia: step-down do Pi, regulador dos servos, driver, bateria e carregador como `Comp` nos 4 modelos, na lista de compras.
- Estrutura: `projetos/{dino,capivara,cubo,cubo-rodas}/` com README, PLANO, LISTA-DE-COMPRAS (links `lista.mercadolivre.com.br`),
  stl, mesas, imagens, verificação; `comum/`.
- Guia: URLs antigas (`/guia/`, `/guia/en/`, `/guia/es/`) → 200 depois do push; página de cada um dos 4 robôs → 200 nos 3
  idiomas; banner feito dos renders reais (contagem de membros conferida); mapa de balanços no guia.
- `git status --short` vazio; tag `v1.1.2` no remoto; revisor independente registrado em `revisor-nota.py`.
- `avisa-v3.sh` enviado; "msg N" no relatório final.

## Ordens acrescentadas pelo Nei durante a rodada (valem para dino, capivara e, onde couber, cubo e cubo-rodas)
6. **Furos discretos.** Nos renders de frente e de 3/4, nenhum furo técnico chama atenção. Microfones nas narinas,
   orelhas, atrás da bandana (capivara) ou dos espinhos (dino). Alto-falante pela boca, por baixo ou por trás, com a
   grade em forma de faixas da barriga, sem fendas evidentes. Sensores de distância no lugar de detalhes que já existem
   (dedos/garras, manchas, anel ciano da capivara). Parafusos só por baixo ou por trás, nunca na frente nem no rosto.
7. **Sensores nos OLHOS.** Avaliar e escolher, justificando no PLANO de cada robô: (a) 2 câmeras, uma em cada pupila
   (estéreo / campo largo; Pi 5 tem 2 CSI, Pi 4 só 1); (b) câmera num olho e ToF no outro; (c) câmera grande-angular
   num olho e outro sensor escondido. A pupila é peça separada, escura (semitransparente ou vazada no centro), com o
   bolso da câmera atrás e o cabo flat passando pela cabeça até o pescoço. Atualizar fase 2 e lista de compras.
8. **Banner do guia (correção do Nei).** O banner de IA estava errado (dino com 6 membros, capivara "desabada", cubo com
   pernas). Caminho: montar o banner a partir dos RENDERS novos dos modelos reais, compondo os 4 robôs numa cena no
   Blender (mesa de madeira, luz quente, fundo desfocado, como nas referências), nos 3 idiomas. Se usar o Codex
   image_gen para acabamento, passar os renders como referência e CONFERIR a contagem de membros de cada robô (dino: 2
   pernas com pés de 3 dedos creme, 2 bracinhos, cauda; capivara: pera compacta, patas de trás grossas na frente,
   mãozinhas na barriga, cabeça larga encostada, bandana verde; cubo sem pernas; cubo-rodas com a base de rodas).
   Vale também para a capa do INEMA.ROBOT e as imagens do portal, se forem trocadas.
9. **Imprimibilidade e reforços (ordem do Nei para TODAS as peças dos 4 robôs).** "Pensar como vai ser construída por
   causa do suporte, ou seja, das áreas sem apoio, e deve ter reforços. Planeja bem isso."
   - Sem suporte sempre que der: balanços ≤ 45° (≤ 50° com justificativa), pontes ≤ 15–20 mm, furo horizontal em gota
     ou com ponte sacrificial, chanfro de 45° (não filete) nas bordas viradas para baixo, casca dividida de modo que
     cada parte tenha face plana na mesa; se o corte da casca gerar área sem apoio, mudar a linha de corte antes de
     aceitar suporte.
   - Suporte inevitável: só onde não aparece, em árvore, documentado por peça (onde, tipo, interface); nunca no rosto
     nem em encaixe.
   - Reforços: nervuras internas na casca; ressalto com 2–3 nervuras em volta de cada inserto/parafuso (parede ≥ 2× o
     diâmetro do inserto); filete na base de pinos e abas; 4–5 perímetros nas peças estruturais. Pontos críticos: garfo
     e berço do pan/tilt, fixação dos MG996R, suportes dos motores, eixo/cubo das rodas, asas do piso, tubo do pescoço,
     engrenagens. Camadas nunca no sentido da carga em peças sob flexão/tração (garfo, tubo, abas).
   - Verificador: teste novo "imprimibilidade" por peça (área de faces viradas para baixo com ângulo > 45° fora da mesa,
     em mm² e %; pontes longas; lista das que precisam de suporte); falha se peça declarada SEM suporte passar do limite
     (limite definido e justificado); teste negativo (girar uma peça e ver o teste acusar).
   - Tabela por peça em cada robô: orientação, suporte (sim/não, onde, tipo), perímetros, infill, material, motivo dos
     reforços. Render do "mapa de balanços" (faces sem apoio em vermelho) das peças principais, no guia.
10. **Aviso no bot v3 no fim.** Com push feito e verificador passando: `~/projetos/wifi/scripts/avisa-v3.sh "<mensagem>"`
    com resumo curto dos 4 robôs, semelhança antes × depois, resultado do teste de imprimibilidade, links do guia
    (PT/EN/ES) e do repo, e pendências. Guardar o "msg N" devolvido para o relatório final. Se parar no meio por falha,
    avisar do mesmo jeito ("Falhou: … — motivo").

## Ordens 11 e 12 (Nei, 14/11 noite)
11. **Cubo primeiro, para imprimir.** "Assim que tiver tudo pronto do cubo e postar no portal me avisa para verificar; também
    quero a lista de material para criar ele e os STL para mim imprimir." Cubo = robô quadrado de mesa (`cubo`).
    Pronto = `projetos/cubo/LISTA-DE-COMPRAS.md` (itens dos `Comp` + decisões da E1, links ML, NC marcado) + STL/3MF na
    orientação de impressão com link direto + página `/guia/cubo/` (+ en, es) → 200 + revisor independente + push +
    portal com texto que bate com o que está no ar + `avisa-v3.sh` próprio (msg N guardado). Sem tag (a v1.1.2 é no fim).
12. **Página de referência da evolução da capivara e do dino** (didática): imagens antes (v1.0.2) × depois nas mesmas
    4 vistas + tabela de IoU por vista (antes, depois, teto da malha, alvo) + como ler o IoU. Fica em `/guia/evolucao/`
    (PT/EN/ES), feita na E5d depois da E3b. Imagens da referência do Nei só se ele autorizar (pergunta feita em 14/11).
13. **(Nei, 15/11 madrugada)** "Faltou a imagem original antes. E faça dos 3: capi, dino e box. Também coloque a imagem de banner junto, antes, nesta seção Evolução do desenho — Os bichos ficaram mais parecidos com o desenho."
    Pronto = na seção "Evolução do desenho" da ENTRADA (`/guia/` + en + es) e na página `/guia/evolucao/`: para capivara, dino E cubo, a imagem ORIGINAL de referência do Nei + render antes (v1.0.2) + render depois, lado a lado; tabela de IoU com o cubo também (antes 0,755 → depois); + o banner antigo (v1.0.2, feito por IA, com o dino errado) ao lado do banner novo (modelos reais), com legenda honesta. Nei autorizou as referências (decisions.md), inclusive a do cubo (`referencia/robo-quadrado.png`).
