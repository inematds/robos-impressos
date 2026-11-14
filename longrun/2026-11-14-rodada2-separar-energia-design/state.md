# Estado

- 14/11 07:1x: rodada aberta. E1 e E2 lançadas em paralelo.
- 14/11: brief da E3 escrito em E3-brief.md (lançar quando E1 e E2 terminarem). E5 (estrutura+docs+guia+publicar) ainda sem brief.
- 14/11: ordem 8 (banner a partir dos renders reais, cena Blender) registrada em goal.md; é trabalho da E5.
- 14/11: ordem 9 (imprimibilidade + reforços + teste 10) registrada; E6 (teste 10) lançada; E1 avisada por mensagem; E3-brief atualizado.
- 14/11: ordem 10 (avisa-v3 no fim, guardar msg N) registrada.

## Agentes vivos (atualizado 14/11 ~10:00) — o orquestrador NÃO edita cad/ enquanto rodam
| Etapa | O que faz | Arquivos de que é dona | Situação |
|---|---|---|---|
| E1 | cubo (energia + redesenho) e cubo_rodas (novo) | `cad/modelos/cubo.py`, `cubo_rodas.py`, seções CUBO/CUBO_RODAS e componentes NOVOS em `parametros.py`/`componentes.py`, `MODELOS` em gerar/verificar/tabelas, helper `ressalto_nervurado` em `geo.py` | rodando; recebeu ordem 9 por mensagem |
| E2 | régua `cad/comparar.py` + números "antes" + image-to-3D local | só arquivos novos; `.venv-i23d`, `referencia/malhas`, `referencia/comparacao`, `comparacao/` | rodando |
| E6 | `cad/comum/imprimibilidade.py`, teste 10, campos novos em `Peca`, diagnóstico `imprimibilidade-antes.md` | arquivo novo + edições mínimas em `modelo.py`, `gerar.py`, `verificar.py`, bloco `IMPRESSAO_LIMITES` em `parametros.py` | rodando |
Arquivos compartilhados sem dono único: `gerar.py`, `verificar.py`, `parametros.py`. Commits e saídas dos agentes são PROVISÓRIOS.
**Quando os três terminarem:** eu rodo `gerar.py todos` + `verificar.py todos`, confiro que o limite do teste 10 não foi afrouxado, e faço o commit de consolidação. Só então lanço a E3 (um bicho por vez: capivara primeiro).

## Próximas etapas (ainda não lançadas)
- E3a capivara → E3b dino (brief em `E3-brief.md`; sequência: esqueleto+forma → furos/olhos/energia → imprimibilidade; commit + verificador a cada pacote).
- E4 números "depois" (régua) dos 4.
- E5 dividida em 4: (a) reorganização `projetos/` + `comum/` com o verificador de portão; (b) renders, cena do banner no Blender, mapas de balanços; (c) docs e listas de compras por robô; (d) guia (entrada + 4 páginas × 3 idiomas), tradução, revisor.
- Eu mesmo: push, tag v1.1.2, conferência das URLs, portal (só se título/descrição disser "três robôs"), `avisa-v3.sh`, relatório.
- 14/11: PORTAL precisa de ajuste no fim: Portal.tsx:119 e translated-courses id 10225 dizem "Três corpos… ~33 cm" (vira quatro robôs; altura nova). Título de courses.ts cita "dino, capivara ou cubo" (avaliar).
- 14/11: conselheiro consultado; E1 avisada (teste 10 só nos cubos; helper ressalto_nervurado); E3-brief com sequência em 3 pacotes e regra de parada.
