Você vai executar a ETAPA E3b (o DINO) de uma rodada longa no projeto `~/projetos/robos-impressos` (robôs impressos em 3D, peças geradas por código em Python). Trabalhe e escreva em português do Brasil. Quedas de sessão já mataram agentes desta rodada: COMMIT LOCAL A CADA PACOTE VERIFICADO e uma linha em `state.md` a cada commit.

Seu pedido completo está em `~/projetos/robos-impressos/longrun/2026-11-14-rodada2-separar-energia-design/E3-brief.md`: leia-o INTEIRO (os blocos finais "COMO EXECUTAR", "Medidas tiradas das máscaras" e "ATUALIZAÇÃO 17:00" valem mais do que o começo) e siga a ordem de leitura dele (`CONTEXTO.md` com os dois ACRÉSCIMOS, `goal.md`, `plan.md`, `canal.md`, `decisions.md`, `imprimibilidade-antes.md`, depois o código e as imagens).

A capivara JÁ FOI FEITA na etapa E3a com a mesma receita. Antes de começar, leia em `canal.md` e `state.md` tudo o que a E3a deixou: como converter a malha em pele (`cad/pele_malha.py`, `PeleGrade`, `cad/peles/`), como ficaram as funções genéricas de `base.py`/`bicho.py` com parâmetros por bicho, a decisão dos olhos (repita a mesma no dino, salvo motivo escrito), os módulos de energia (`STEPDOWN5V`, `UBEC6V`, `CARREGADOR2S`, feitos pela E1) e a política de imprimibilidade das cascas. Reaproveite; não reinvente.

O bicho desta etapa é o **dino** (`cad/modelos/dino.py`, id `dino`), malha `referencia/malhas/dino-hy2mv-fl-s2.glb` (Y para cima, +Z frente). Alvo da régua: IoU médio ≥ 0,856 (antes 0,814; teto da malha 0,897) e semelhança clara a olho nas 4 vistas. Requisitos do dino que não mudam: 2 pernas com pés de 3 dedos creme, 2 bracinhos, cauda (pode encurtar ou sair em peça à parte para caber em 256 mm), crista, boca sorridente, cabeça grande e redonda.

Pacotes (iguais aos da capivara): 1 esqueleto + forma (pele da malha) → régua → verificador → commit; 2 furos discretos + pupila com sensor + energia → commit; 3 imprimibilidade e reforços, testes 10 e 11 passando sem afrouxar limite → commit.
A capivara e os dois cubos NÃO podem quebrar: antes de cada commit rode `.venv/bin/python cad/gerar.py capivara && .venv/bin/python cad/verificar.py capivara` (11 testes) além do dino. No fechamento rode `gerar.py todos` e `verificar.py todos`.
Não edite `cad/modelos/cubo.py`, `cad/modelos/cubo_rodas.py`, nem as seções CUBO/CUBO_RODAS. `git add` só dos seus arquivos. Não renderize imagens finais nem mexa em docs/guia. Sem push.

Se o contexto apertar, feche o pacote em que está (commit + `state.md` + o que falta em `canal.md`) e relate.

Relatório final (curto): IoU antes × depois por vista; caminhos das imagens lado a lado; o que mudou no esqueleto; olhos; furos disfarçados; energia; altura/largura/massa; saída REAL do `verificar.py todos` (linhas `=>` dos 4 e as 11 do dino); hashes; pendências sem enfeite.

## Regra nova do Nei (14/11): nenhum modelo local novo sem aprovação
Não rode Hunyuan3D, rembg nem qualquer modelo local (nem `pip install` de torch/diffusers): a malha `referencia/malhas/dino-hy2mv-fl-s2.glb` e as máscaras já existem. Se achar que precisa gerar malha nova, PARE e relate.
Em paralelo roda a etapa "cubo primeiro" (só `projetos/cubo/`, `guia/cubo/`, `pecas/cubo/`): não mexa nisso.
