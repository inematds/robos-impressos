# Handoff — robos-impressos (14/11/2026 ~17:15, pausa para reiniciar a máquina)

## Objetivo
Rodada 2 (v1.1.2) dos robôs impressos: separar os 4 projetos, completar a energia, aproximar o design das imagens do Nei,
criar o 4º robô (cubo-rodas ≥ 30 cm), tornar as peças imprimíveis sem suporte e com reforços, refazer o banner e o guia.
As 10 ordens do Nei estão em `longrun/2026-11-14-rodada2-separar-energia-design/goal.md`, junto com o critério de pronto.

## O que NÃO fazer
- Não usar API externa de 3D/imagem (só Hunyuan3D local na GPU, Codex pela assinatura).
- Não postar de novo no INEMA.ROBOT. Não mexer no Vercel. Portal só se o título/descrição mudar (hoje diz "três robôs ~33 cm": vai mudar).
- Não publicar `referencia/` (origem das imagens não informada).

## Feito (em commit, local; o último push foi a v1.0.2)
- v1.0.2 publicada: 3 robôs, guia PT/EN/ES, portal, INEMA.ROBOT msg 2953.
- Rodada 2: régua de semelhança `cad/comparar.py` (antes: capivara 0,777; cubo 0,755); teste 10/11 de imprimibilidade;
  helper `ressalto_nervurado`; `cad/imagem3d.py` (Hunyuan3D-2 local) com malhas em `referencia/malhas/` (teto: capivara 0,927, dino 0,897);
  conversor `cad/pele_malha.py` + `cad/peles/capivara.npz` (commit 6816d13). Pausa salva em 4134fba.

## Pela metade
- **E1** (cubo: energia step-down 5 V/3 A + UBEC 6 V/3 A + carregador 18650 na base; depois `cubo_rodas.py` novo): começar do zero, nada salvo.
- **E3a** capivara: conversor e pele prontos; falta aplicar a pele em `cad/modelos/capivara.py` → furos discretos/olhos com câmera/energia → imprimibilidade.

## Próxima ação
Sessão nova nesta pasta, Fable 5.2 high: ler `state.md` (seção PAUSA) e relançar E1 e E3a em paralelo (donos de arquivo na tabela do state).
Depois: E3b dino → consolidação (`gerar todos` + `verificar todos`) → E4 números "depois" → E5a–d (estrutura `projetos/`, renders/banner, docs/listas, guia + revisor) → push + tag v1.1.2 → portal → `avisa-v3.sh`.

## Contexto extra
- Lista de compras do cubo já mandada ao Nei no v3 (msg 4711); ele já tem o Arduino.
- Fase 2 (voz, câmera, sensores, localização em casa) está nas pendências do wifi; a mecânica só reserva espaço.

## Comandos (estrutura nova, depois da reorganização em `comum/` + `projetos/`; valem sobre os `cad/…` citados acima)
```
.venv/bin/python comum/cad/gerar.py <id|todos>                # id: dino, capivara, cubo, cubo_rodas
.venv/bin/python comum/cad/verificar.py <id|todos>            # 11 testes
.venv/bin/python comum/cad/comparar.py <id> --sem-gravar      # régua de semelhança (precisa de referencia/)
.venv/bin/python comum/cad/tabelas.py --docs                  # projetos/TABELAS.md + tabelas de PLANO.md e README*.md (sem --docs mexe também no guia)
comum/cad/renders.sh <id>                                     # imagens em projetos/<robô>/imagens/
# documentos de UM robô (<robô> = pasta: dino, capivara, cubo, cubo-rodas); fontes em guia/src/robos/<robô>.{dados,pt}.json
.venv/bin/python guia/src/pagina_robo.py docs <robô> pt       # blocos GERADO dos .md em português
.venv/bin/python guia/src/pagina_robo.py traduzir <robô>      # EN/ES pelo inema-traduz (só o que mudou)
.venv/bin/python guia/src/pagina_robo.py docs <robô>          # *.en.md e *.es.md
.venv/bin/python guia/src/pagina_robo.py esquema <robô>       # ligacao.<lg>.svg (cubo: desenho no próprio gerador; bichos: esquema_bicho.py; cubo-rodas: esquema_cubo_rodas.py)
.venv/bin/python guia/src/pagina_robo.py zip <robô>           # projetos/<robô>/<robô>-stl.zip
.venv/bin/python guia/src/pagina_robo.py conferir <robô>      # sem página no guia, confere só docs + zip
.venv/bin/python guia/src/pagina_robo.py pagina <robô>        # guia/<robô>/ + en + es (etapa do guia)
.venv/bin/python guia/src/traduzir_readme.py                  # README.en.md e README.es.md; depois tabelas.py --docs
```
