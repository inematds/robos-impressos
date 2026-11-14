Você vai executar a etapa "CUBO PRIMEIRO" (ordem 11 do goal.md) no projeto `~/projetos/robos-impressos`. Português do Brasil.
O dono (Nei) quer IMPRIMIR e MONTAR o robô quadrado de mesa (`cubo`) já: "assim que tiver tudo pronto do cubo e postar no
portal me avisa para verificar; também quero a lista de material para criar ele, e os STL para mim imprimir".

Leia antes, em `longrun/2026-11-14-rodada2-separar-energia-design/`: `CONTEXTO.md`, `goal.md` (ordens 1, 6, 9, 11),
`canal.md` (blocos da E1 e da E6), `decisions.md`, `E5-brief.md` (estrutura final de pastas e regras de lista/guia),
`pesquisa-energia.md`. Depois `cad/modelos/cubo.py`, `cad/comum/quadrado.py`, seções CUBO e componentes de `cad/parametros.py`,
`pecas/cubo/montagem.json`, `PLANO.md`, `guia/src/` (como o guia é montado hoje), `~/.claude/skills/projetos-landing-guia/SKILL.md`
e `~/projetos/inema-design/DESIGN.md` (+ `regras/chamada.md`).

Em paralelo: a etapa E3a/E3b trabalha na capivara e no dino (`cad/comum/{base,bicho,base_baixa,casca}.py`, `cad/modelos/{capivara,dino}.py`,
`pecas/{capivara,dino}/`, `comparacao/`). NÃO toque nesses arquivos, NÃO rode `gerar.py todos`/`verificar.py todos`, NÃO rode
`guia/src/montar.py` (reconstruiria o guia inteiro com bichos pela metade). `git add` só dos seus caminhos, nunca `-A`.
Não edite `cad/modelos/cubo.py` sem motivo forte (a E1 fechou); se achar bug, corrija pequeno e diga.

## Passos
1. **STL frescos e na orientação de impressão.** `.venv/bin/python cad/gerar.py cubo` e `verificar.py cubo` (11 PASSOU; grave a
   saída). `git status` de `pecas/cubo/` tem que ficar limpo ou o diff ser só o regerado. Abra 2–3 STL (ex.: base, cabeca-corpo,
   cabeca-face) com trimesh e confirme que estão DEITADOS na orientação de impressão (face declarada em Z=0). Se os STL estiverem
   na posição de montagem, diga isso e aponte o Nei para os 3MF/mesas (que estão na orientação certa), ou exporte uma pasta de
   STL orientados. Ele precisa abrir no Bambu Studio e imprimir sem girar nada.
2. **Pasta `projetos/cubo/`** (local final da E5; NÃO mova `pecas/cubo/` nem `cad/`, só crie os arquivos novos):
   - `LISTA-DE-COMPRAS.md`: a partir dos `Comp` do modelo + decisões da E1 (não da lista antiga do v3). Item, quantidade, para
     que serve, preço ESTIMADO em faixa R$ com data (consulta pública; se não der, "estimativa não conferida"), link
     `https://lista.mercadolivre.com.br/<termos-com-hifen>`. Tem que ter: Pi, Uno (+ shield se usar), 2 MG996R, tela, LM2596
     (step-down 5 V do Pi, 2S), UBEC 6 V 3 A, carregador USB-C com balanceamento + BMS 2S (e o 3º fio no ponto do meio),
     2×18650 + suporte, chave, fios/conectores, insertos, parafusos (inclusive M3x45, M3x50, M5x16), abraçadeiras 3,6 mm,
     chave Allen 2,5 mm longa, filamento (gramas por cor do montagem.json). Fase 2 em bloco separado (câmera, mic, alto-falante…).
     Medidas NC marcadas. Nota: o Nei já tem o Arduino.
   - `IMPRIMIR.md`: tabela por peça (arquivo, qtd, cor/material, orientação, suporte, perímetros, infill, tempo, gramas),
     ordem sugerida, e: **imprima primeiro o `teste-encaixe`** (nada foi impresso ainda; confere folga e insertos).
     Links diretos para os arquivos no GitHub (`https://github.com/inematds/robos-impressos/raw/main/...`).
   - `README.md` curto (o que é, montagem passo a passo a partir de `ordem`, abertura para manutenção, verificação).
   - `cubo-stl.zip` com os STL (e 3MF das mesas) prontos para baixar de uma vez (link direto no README/guia).
3. **Renders do cubo** (só do cubo): montado, explodido e 4 vistas, por `~/projetos/wifi/scripts/fila-vaga render robos -- cad/renders.sh cubo`
   (ou o equivalente que só renderiza o cubo). Confira a olho: frente e 3/4 sem parafuso nem furo técnico à vista. Coloque
   cópias em `guia/cubo/assets/` (o lugar das imagens de `imagens/` não muda).
4. **Página `/guia/cubo/`** (+ `/guia/en/cubo/`, `/guia/es/cubo/`): página própria do cubo, no padrão visual do guia atual
   (mesmo CSS/estrutura, leia `guia/index.html`), chamada D20 (dor/desejo, "você"), renders, peças e mesas, lista de
   compras com links, como imprimir (teste-encaixe primeiro), montagem, energia, fase 2, downloads (zip + STL), verificação.
   Gere pelo mecanismo do `guia/src/` se der para gerar SÓ esta página sem tocar nas outras; senão um script pequeno novo
   (`guia/src/pagina_robo.py`) que a E5d vai reaproveitar. Tradução EN/ES só com `inema-traduz`. hreflang + troca de idioma.
   Na página atual `/guia/` (e en/es), acrescente só um link/botão visível "Cubo: página nova com lista e STL" na seção do
   cubo, sem regenerar o resto. Regra do guia: tudo dentro do repo, sem servidor rodando no fim.
5. **Commit local** (autor inematds; rodapé `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`) + linha em `state.md`.
   NÃO faça push, portal nem aviso: o orquestrador chama o revisor independente e publica.

## Relatório final (curto)
Saída real do `verificar.py cubo`; se os STL estão na orientação de impressão (como conferiu); caminhos de `projetos/cubo/*`
e das páginas; total de filamento e tempo; custo estimado total da lista (faixa); o que ficou NC/pendente; hash do commit.
