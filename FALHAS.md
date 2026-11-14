# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-14 | Promessa "tira as costas e as bandejas saem" era falsa: a calota de trás da esfera do pescoço fica dentro da cabeça e as orelhas das pernas raspavam | teste de ABERTURA no verificador (peça sai contra o resto); cabeça entra na ordem de abertura; folga de 1,2 mm no recorte das pernas; textos corrigidos | prompt |
| 2026-11-14 | Os "8 testes" passavam com montagem impossível: mesa da cabeça maior que a abertura do crânio, rodas antes do torso, costas presas pela chave e pela esfera de apoio | teste 9 (caminho de montagem por varredura); mesa recortada pela sombra do crânio e presa por 3 parafusos por baixo; orelhas das costas fora do eixo; rodas depois do torso | prompt |
| 2026-11-14 | Sinal da varredura invertido (recortei a saia do lado errado e o teste ainda passava por acaso) | visto da peça, o obstáculo anda no sentido oposto ao movimento dela; comentário no código | prompt |
| 2026-11-14 | Guia: cartões de número ilegíveis porque a classe `.num` já existia no template | renomear para `.numero`; conferir captura em 390 px antes do revisor | prompt |
| 2026-11-14 | `mesas.json`: a lista de mesas era sobrescrita pela chave `mesas` dos retângulos do render | lista em `mesas_lista` | prompt |
| 2026-11-14 | Banner: instrução ao gerador colocada em `--line` saiu desenhada na arte ("deixe margem acima do título…") e "guadrado" | gerar de novo só com o texto final; olhar a imagem antes de usar | prompt |
| 2026-11-14 | Mandíbula com o eixo baixo demais: o servo da boca não cabia na largura do focinho e batia no fundo | subir o eixo (z 204 → 220) e afastar a mandíbula da esfera do pescoço pelo recuo ao abrir | prompt |
| 2026-11-14 | Pescoço com esfera pequena (33 mm): o garfo batia na gola e sobrava "pescoço" à mostra | esfera de 58 mm = o próprio topo do torso; servo de tilt padrão em pé | prompt |
| 2026-11-14 | STL soldado virava não-variedade por arestas "beliscadas"; a 1ª correção (fios finos) criou mais arestas ruins | cápsula que funde OU abre a aresta, ficando com a variante que reduz a contagem (`geo.desbeliscar`) | prompt |
| 2026-11-14 | Centro de gravidade a 15 mm do eixo das rodas (tombava com 9°) | recuar corpo e pescoço 16 mm em relação às rodas (margem 26 mm) | prompt |
| 2026-11-14 | Orelhas de parafuso do torso caíam dentro do poço da roda: ficavam soltas e batiam na roda | 2 postes do chassi sob o painel da barriga + 1 orelha na frente | prompt |
| 2026-11-14 | Rampa "autoportante" das orelhas das pernas tampava o furo do inserto (vazio fechado dentro da peça) | tirar a rampa; suporte só sob as orelhas | prompt |
| 2026-11-14 | `prisma()` devolvia sólido vazio com polígono em sentido horário: 5 peças saíam VAZIAS sem erro | calcular a área com sinal e inverter os pontos; `gerar.py` aborta em peça vazia | prompt |
| 2026-11-14 | Render estourado de branco e Blender sem OpenImageDenoise | energia das luzes ÷ 12; denoise só se o build tiver; mais amostras | infra + prompt |
