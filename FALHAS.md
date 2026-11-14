# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-14 | Mandíbula com o eixo baixo demais: o servo da boca não cabia na largura do focinho e batia no fundo | subir o eixo (z 204 → 220) e afastar a mandíbula da esfera do pescoço pelo recuo ao abrir | prompt |
| 2026-11-14 | Pescoço com esfera pequena (33 mm): o garfo batia na gola e sobrava "pescoço" à mostra | esfera de 58 mm = o próprio topo do torso; servo de tilt padrão em pé | prompt |
| 2026-11-14 | STL soldado virava não-variedade por arestas "beliscadas"; a 1ª correção (fios finos) criou mais arestas ruins | cápsula que funde OU abre a aresta, ficando com a variante que reduz a contagem (`geo.desbeliscar`) | prompt |
| 2026-11-14 | Centro de gravidade a 15 mm do eixo das rodas (tombava com 9°) | recuar corpo e pescoço 16 mm em relação às rodas (margem 26 mm) | prompt |
| 2026-11-14 | Orelhas de parafuso do torso caíam dentro do poço da roda: ficavam soltas e batiam na roda | 2 postes do chassi sob o painel da barriga + 1 orelha na frente | prompt |
| 2026-11-14 | Rampa "autoportante" das orelhas das pernas tampava o furo do inserto (vazio fechado dentro da peça) | tirar a rampa; suporte só sob as orelhas | prompt |
| 2026-11-14 | `prisma()` devolvia sólido vazio com polígono em sentido horário: 5 peças saíam VAZIAS sem erro | calcular a área com sinal e inverter os pontos; `gerar.py` aborta em peça vazia | prompt |
| 2026-11-14 | Render estourado de branco e Blender sem OpenImageDenoise | energia das luzes ÷ 12; denoise só se o build tiver; mais amostras | infra + prompt |
