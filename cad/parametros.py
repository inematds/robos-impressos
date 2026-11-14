"""Arquivo ÚNICO de medidas dos robôs impressos (mm, g). Mude aqui e rode cad/gerar.py + cad/verificar.py.

Eixos: X = esquerda/direita (simetria em X=0), +Y = frente, Z = cima, chão em Z=0. Eixo das rodas em Y=0.

Seções:  IMPRESSORA · FOLGAS · COMPONENTES (com a fonte de cada medida) · BASE (esqueleto comum dos
         bichos que rodam) · PESCOCO (pan + tilt comum) · modelos: DINO, CAPIVARA, CUBO.

Sobre as fontes: "P" = desenho/datasheet do fabricante; "T" = loja ou terceiro; "NC" = não confirmado em
fonte lida (valor usual de mercado: MEÇA a sua peça com paquímetro antes de imprimir; os bolsos têm
folga e, onde dá, rasgo). Lista completa das URLs em PLANO.md › Fontes das medidas.
"""
from types import SimpleNamespace as NS

# ------------------------------------------------------------------ IMPRESSORA
IMPRESSORA = NS(
    nome="Bambu Lab A1",
    volume=(256.0, 256.0, 256.0),      # P (ficha técnica A1)
    bico=0.4,
    camada=0.2,
    # estimativa de tempo (não há fatiador nesta máquina): volume de plástico / vazão média efetiva
    vazao_media_mm3_s=6.0,             # suposição conservadora p/ PLA/PETG a 0,2 mm (pico declarado 28 mm³/s é em ABS)
    preenchimento=0.15,                # peças maciças (chassi, garfo): 15 % de miolo
    casca_solida_mm=1.6,               # 2 paredes + topo/fundo ~ casca sólida de 1,6 mm nas peças maciças
    dens_pla=1.24, dens_petg=1.27, dens_tpu=1.21,   # g/cm³ (valores usuais de fabricante de filamento)
)

# ------------------------------------------------------------------ FOLGAS (FDM)
FOLGA = NS(
    encaixe=0.25,        # entre duas peças impressas que encostam/encaixam (pedido: 0,2–0,3)
    deslizante=0.4,      # partes que giram uma na outra
    componente=0.4,      # por lado, em volta de componente comprado (clones variam)
    casca=0.5,           # entre cascas vizinhas (perna x torso, cauda x torso)
    junta_esfera=2.0,    # folga da junta esférica cabeça x gola
    m3_passante=3.4,     # furo passante p/ parafuso M3
    m25_piloto=2.2,      # furo piloto p/ M2,5 auto-atarraxante no plástico (Raspberry Pi)
    m2_piloto=1.7,       # furo piloto p/ parafusinho dos servos pequenos
    m3_piloto=2.7,       # furo piloto p/ M3 auto-atarraxante
    inserto_d=4.0,       # furo p/ inserto M3 a quente (Ruthex RX-M3x5,7: furo 4,0)  T
    inserto_prof=6.5,    # profundidade do furo do inserto (inserto de 5,7 + sobra)
    porca_m3_faces=5.5,  # DIN 934: 5,5 entre faces, 2,4 de espessura                T
    porca_m3_esp=2.4,
    bolso_porca=5.9,     # bolso da porca com folga
    cabeca_m3_d=6.2,     # rebaixo p/ cabeça de M3 (cilíndrica/abaulada Ø5,5–6)
    parede=2.4,          # parede nominal das cascas (o verificador mede ≥ 2,0 real)
    parede_min=2.0,
    pino_d=4.0,          # pino-guia impresso entre as metades do torso
)

# ------------------------------------------------------------------ IMPRESSÃO SEM SUPORTE (teste 10 do verificador)
# Limites de cad/comum/imprimibilidade.py. São regras de projeto para FDM com bico 0,4 e camada 0,2 (PLA/PETG com a
# ventilação de peça ligada); NÃO saíram de impressão nossa (nada foi impresso na fase 1): ao imprimir, ajuste aqui.
# Regra do veredito: a peça PRECISA de suporte se  área sem apoio > max(area_max_mm2, area_max_pct % da área total)
# ou se algum ponto nasce no ar. É "max" de propósito: em peça pequena vale o piso absoluto (0,2 % de uma pupila
# seria menos que um fragmento); em casca grande vale o percentual (ruído da malha orgânica perto de 45°).
IMPRESSAO_LIMITES = NS(
    angulo_max=45.0,       # graus a partir da VERTICAL (parede = 0°, teto = 90°). A 45°, cada camada de 0,2 avança
                           # 0,2 mm: menos da metade do filete de 0,42 fica no ar. É o "balanços ≤ 45°" da ordem 9
    tol_angulo=1.0,        # graus de folga p/ arredondamento do STL (float32): chanfro de 45° exatos não é acusado
    z_mesa=0.3,            # face para baixo com |z| < 0,3 mm (1ª camada de 0,2 + folga) está NA MESA, não é balanço
    ponte_max=20.0,        # mm de vão de ponte PLANA apoiada nas duas pontas (teto da faixa 15–20 da ordem 9; em
                           # PETG, que escorre mais, mire 15)
    furo_max=6.0,          # mm de vão de teto curvo ou rasgo apoiado dos dois lados. O trecho do teto de um furo
                           # redondo que passa de 45° mede 0,71 x Ø: libera furo horizontal até ~Ø8 (M3 passante 3,4,
                           # inserto 4,0, rebaixo de cabeça 6,2). Furo maior: desenhar em gota
    balanco_curto=1.0,     # mm de aba horizontal tolerada sem nada embaixo ≈ 2 filetes (o 2º ainda gruda no 1º)
    fragmento_mm2=4.0,     # região isolada menor que isto (≈ 2 x 2 mm, 5 filetes) não conta: o filete atravessa
    area_max_mm2=30.0,     # tolerância ABSOLUTA por peça ≈ um teto de 5,5 x 5,5 mm (um furo no limite): é o tamanho
                           # de defeito que não muda encaixe nem aparência; absorve o erro do próprio método
    area_max_pct=0.2,      # tolerância RELATIVA, % da área total da peça (casca de 850 cm² → 170 mm² somados, uns 5
                           # defeitos do tamanho acima espalhados). Critério de projeto, não medição: aperte se sobrar
    inicio_no_ar_mm=0.6,   # ponta de paredes íngremes que nasce no ar só conta se pendurar ≥ 3 camadas
)

# ------------------------------------------------------------------ COMPONENTES COMPRADOS
# Cada medida com a fonte. As URLs por extenso estão em PLANO.md.
UNO = NS(
    nome="Arduino Uno R3",
    placa=(68.6, 53.4),                # T (Wevolver/Pololu); o datasheet A000066 não cota o contorno
    esp=1.6,
    # furos Ø3,2 em mils no datasheet oficial A000066 §5.4 (P). Origem: canto superior esquerdo
    # visto de cima, USB à esquerda; aqui já em mm com y medido a partir da borda de CIMA.
    furos=((15.24, 2.54), (66.04, 17.78), (66.04, 45.72), (13.97, 50.80)),   # o x do 4º furo (13,97) é lido pela escala
    furo_d=3.2,
    altura_pilha=30.0,                 # NC: Uno + Sensor Shield empilhado; reservado 30 mm
    massa=25.0,                        # T (25–28 g)
)
PI = NS(
    nome="Raspberry Pi 4 B / 5",
    altura_baixa=10.0, bloco_usb=22.0,   # envelope: 10 mm acima da placa (header GPIO 8,5 P) e blocos USB/Ethernet de 16 mm nos 22 mm de trás
    placa=(85.0, 56.0),                # P (desenho mecânico oficial Pi 4 e Pi 5)
    esp=1.5,
    furos=((3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)),   # P: 3,5 da borda, 58 x 49
    furo_d=2.7,                        # P
    altura_pilha=16.5,                 # P: blocos USB do Pi 4 a 16,0 acima da placa (+ folga)
    massa=47.0,                        # T (45–50 g)
)
SG90 = NS(
    nome="SG90",
    corpo=(22.7, 12.2),                # P Tower Pro (B, D)
    base_ate_aba=17.0,                 # P (F); datasheet de terceiro dá 16
    aba_esp=2.5,                       # NC
    comp_abas=32.3,                    # P (E)
    furos_aba=27.8, furo_aba_d=2.0,    # NC
    topo_caixa=27.0,                   # P (C): base até o topo do ressalto das engrenagens
    altura_total=31.0,                 # P 30,3 / T 31 (com o eixo)
    eixo_da_ponta=5.9,                 # NC: eixo a ~5,9 da extremidade do corpo
    massa=9.0,                         # P
)
MG90S = NS(
    nome="MG90S",
    corpo=(22.8, 12.4),                # P Tower Pro (B, D)
    base_ate_aba=18.5,                 # P (F)
    aba_esp=2.5,                       # NC
    comp_abas=32.5,                    # P 32,1 / T 32,5
    furos_aba=27.8, furo_aba_d=2.0,    # NC
    topo_caixa=28.4,                   # P (C)
    altura_total=32.5,                 # P (A); Components101 dá 35,5 com horn
    eixo_da_ponta=5.9,                 # NC
    massa=13.4,                        # P
)
# bolso que aceita SG90 OU MG90S (os dois cabem; usa o maior de cada medida)
MICRO = NS(
    nome="micro servo (SG90 ou MG90S)",
    janela=(23.6, 12.9),               # corpo 22,8 x 12,4 + folga
    corpo=(22.8, 12.4),
    base_ate_aba=18.5, aba_esp=2.5, comp_abas=32.5, furos_aba=27.8,
    aba_ate_ponta=14.0,                # face de baixo da aba até a ponta do eixo (MG90S: 32,5 − 18,5)
    eixo_da_ponta=5.9,
    horn=(19.5, 7.2, 4.4, 1.6),        # NC: horn de 1 braço: comprimento do centro à ponta, Ø do cubo, largura na ponta, espessura
    massa=13.4,
)
MG996R = NS(
    nome="MG996R",
    corpo=(40.9, 20.0),                # P Tower Pro (B, D)
    janela=(41.9, 21.0),
    base_ate_aba=26.8,                 # P (F)
    aba_esp=2.5,                       # NC
    comp_abas=54.0,                    # P (E)
    furos_aba=(49.5, 10.0), furo_aba_d=4.5,   # NC: 4 furos, 49,5 no comprimento x 10 na largura → rasgos
    topo_caixa=37.0,                   # P (C)
    aba_ate_topo_horn=21.0,            # T: desenho do datasheet 47,6 − 26,6 (altura total com horn); o site dá 42,7 sem horn
    eixo_da_ponta=10.0,                # NC: eixo a ~10 da extremidade do corpo
    horn_d=21.0, horn_esp=2.6,         # NC: horn redondo
    massa=55.0,                        # P
    alternativo="DS3218 270° (corpo 40 x 20 x 40,5, 60 g — T; abas e estriado NC)",
)
TT = NS(
    nome="motor TT amarelo 1:48",
    caixa=(37.0, 22.44, 18.6),         # T desenho Adafruit 3777: comprimento da caixa, largura, espessura
    comp_total=70.0,                   # T: do fundo do motor à ponta da orelha
    eixo_da_frente=11.5,               # T: eixo a ~11,5 da face da frente da caixa (SunFounder cota 11,0)
    orelha_alem=5.5,                   # T: a orelha passa ~5,5 da face da frente (furo a 14,0 do eixo)
    eixo_saliente=9.3,                 # T: 8,7 e 9,3 para fora da caixa, um de cada lado
    eixo_d=5.4, eixo_chato=3.7,        # T
    furos_tras=22.55,                  # T: 2 furos Ø3 a 22,55 atrás do eixo
    furos_tras_dist=17.6,              # T/NC: o desenho cota 17,60 entre furos; pela escala pode ser 12,3 → rasgo
    furo_orelha=14.0,                  # T: furo Ø3 da orelha, 14,0 à frente do eixo
    lata_d=22.4,                       # T (22,4 a 19)
    massa=30.6,                        # T
)
RODA = NS(nome="roda 65 mm p/ motor TT", d=65.0, larg=27.0, folga_caixa=3.5, massa=40.0)  # T: larg 26–27, massa 36–50; folga_caixa NC
BATERIA = NS(
    nome="suporte 2x18650 lado a lado",
    cx=(78.0, 41.0, 22.0),             # T: 74,5–80 x 40–41 x 17,7–22 (usa o maior)
    massa_suporte=18.0, massa_celula=47.0,   # T
)
L298N = NS(nome="driver L298N", placa=(43.0, 43.0), altura=27.0, furos=37.0, furo_d=3.0, massa=30.0)  # T 43x43x27; furos 37 NC
CHAVE = NS(nome="chave gangorra KCD11", recorte=(13.5, 9.0), corpo=(15.0, 10.5), prof=17.2, painel=1.6)  # T (recorte do KCD117S); painel NC
ESFERA = NS(nome="esfera de apoio 16 mm (aço ou bolinha de gude medida)", d=16.0, massa=17.0)          # NC: bolinha de gude varia 14–25
TELA35 = NS(
    nome='tela TFT 3,5" p/ Raspberry Pi (MPI3501, encaixa no GPIO)',
    placa=(85.42, 55.60),              # P manual lcdwiki MPI3501
    ativa=(73.44, 48.96),              # P
    esp_conjunto=7.0,                  # NC: placa + painel
    acima_do_pi=24.5,                  # NC: distância da face de cima do Pi até o vidro (a tela passa por cima dos blocos USB de 16 mm)
    massa=51.0,                        # P
)

# ------------------------------------------------------------------ COMPONENTES DA FASE 2 (só espaço e furos)
FALANTE = NS(nome="alto-falante 40 mm 3 W", d=40.0, prof=20.0, massa=25.0)                      # NC (nominal de mercado)
CAMERA = NS(nome="Raspberry Pi Camera Module 3", placa=(25.0, 24.0), furos=(21.0, 12.5), lente_d=7.5, lente_alt=11.5, flat=16.0)  # placa 25x24 (pedido); furos e lente NC
UNIVERSAL = NS(passo=20.0)   # "ponto universal": par de furos M3 a 20 mm p/ suportes de sensor da fase 2 (ToF, IMU, queda, microfone)
LIDAR = NS(nome="LiDAR LD06/LD19", d=38.0, alt=35.0)                                             # ~38 mm (pedido); NC
JACK = NS(nome="conector de carga P4 de painel", furo_d=8.2)                                     # NC

# ------------------------------------------------------------------ COMPONENTES DE ENERGIA (rodada 2, etapa E1)
# Envelope = caixa `cx` (comprimento, largura, altura). Em cad/comum/componentes.py: C.modulo(P.<NOME>) devolve a
# caixa centrada em XY com a base em z=0 e o comprimento em X. Fixação recomendada: berço de 4 cantoneiras + abraçadeira
# de nylon (cad/comum/geo.py › berco_modulo): NÃO depende de furo de placa (os furos destes módulos são NC ou não
# existem). Contas de tensão: pack 2S = 8,4 V cheio, 7,4 V nominal, ~6,0 V vazio; pack 3S = 12,6 / 11,1 / ~9,0 V.
STEPDOWN5V = NS(
    nome="step-down 5 V do Raspberry Pi (LM2596 no pack 2S; XL4015 no pack 3S)",
    cx=(54.0, 24.0, 16.0),             # T: o MAIOR dos dois (XL4015 com dissipador, 54 x 24 x 16, 15 g): o berço aceita qualquer um
                                       #    https://www.usinainfo.com.br/regulador-de-tensao/regulador-de-tensao-xl4015-step-down-saida-125-a-32v-dc-5a-8768.html
    massa=15.0,                        # T (mesma página); o LM2596 pesa 10 g
    lm2596=(43.0, 21.0, 14.0),         # T: 43 x 21 x 14, 10 g, entrada 4,5–40 V, 3 A máx.  https://curtocircuito.com.br/conversor-dc-dc-step-down-lm2596.html
    # Qual usar (decide a TENSÃO MÍNIMA de entrada, não a corrente):
    #  pack 2S → LM2596: entra a partir de 4,5 V (T); queda da chave 1,16 V típ. / 1,4 V máx. a 3 A (P, datasheet TI
    #            https://www.ti.com/lit/ds/symlink/lm2596.pdf) → os 5 V se mantêm até o pack cair a ~6,5 V (3,25 V por
    #            célula; calculado). Abaixo disso a saída acompanha a bateria e o Pi acusa subtensão: é o "fim de carga".
    #            O XL4015 NÃO serve no 2S: a loja dá entrada 8–35 V (T, URL acima) e o pack 2S passa quase todo o tempo abaixo de 8 V.
    #            O Mini560 (5 V fixo, 5 A) pede ≥ 7 V (T, kunkune.co.uk): perderia a metade de baixo da carga do 2S.
    #  pack 3S → XL4015 (5 A, recomendada 4,5 A; entrada 8–35 V): sobra tensão em toda a descarga (9,0–12,6 V).
    #  Os 3 A do LM2596 bastam? O Pi 4 pede fonte de 3 A porque reserva 1,2 A para as USB; aqui a câmera é CSI e a tela
    #  vai no GPIO/HDMI: consumo esperado ≤ 2 A (estimativa, NC). Pi 5 com 3 A funciona, mas limita as USB a 0,6 A.
    v_min_2s=6.5, v_min_3s=8.0,
    furos="NC (em geral 2 furos Ø3 em cantos opostos): por isso a fixação é berço + abraçadeira",
)
UBEC6V = NS(
    nome="UBEC 6 V 3 A dos servos (Hobbywing UBEC 3A 2-6S ou equivalente)",
    cx=(43.0, 17.0, 7.0),              # P: 43 x 17 x 7 mm, 11 g  https://www.hobbywing.com/en/products/ubec-3a-2-6s99.html
    massa=11.0,                        # P (a página não diz se inclui os fios)
    # P: saída 5 V ou 6 V a 3 A CONTÍNUOS (jumper), entrada 5,5–26 V (2–6S), ripple < 50 mVp-p. Pico: a página não dá (NC).
    # 2 x MG996R: travamento 1,4 A cada e 0,17 A girando sem carga (P, https://www.towerpro.com.tw/product/mg996r/ ; a
    # página não diz a tensão) → 2,8 A com os dois travados, dentro dos 3 A. Cópias do datasheet citam 2,5 A a 6 V
    # (NC): seriam 5 A com os DOIS travados ao mesmo tempo, acima do UBEC → o firmware não deixa travar (pan e tilt
    # param antes do batente) e vai um capacitor de 1000 µF no barramento dos servos. Uso típico (pan + tilt da cabeça,
    # carga leve): < 1 A (estimativa, NC). No pack 2S a saída de 6 V só se mantém com ~7 V de entrada (queda do
    # regulador NC ~1 V); abaixo disso ela acompanha a bateria (5–6 V), o que o MG996R aceita (4,8–6,6 V, P).
    i_continua=3.0, i_trav_2servos=(2.8, 5.0),
    furos="não tem: berço + abraçadeira (ou fita dupla-face)",
)
CARREGADOR2S = NS(
    nome="carregador USB-C 2S/3S com balanceamento (LX-USC-V2)",
    cx=(32.0, 18.0, 5.0),              # T: 32 x 18 x 5 mm, 3 g, 8,4 V (2S, como vem) ou 12,6 V (3S), 1,5 A ajustável, USB-C
                                       #    https://www.usinainfo.com.br/fonte-de-alimentacao/carregador-de-baterias-18650-litio-2s3s-com-balanceamento-usb-c-lx-usc-v2-8996.html
    massa=3.0,                         # T
    usb_c=(9.2, 3.4),                  # NC: boca do conector USB-C (8,94 x 3,26 da norma + folga); fica numa das pontas do comprimento
    # Decisão: módulo carregador USB-C COM balanceamento + placa de proteção (BMS2S abaixo). Por quê:
    #  - carrega com qualquer fonte USB-C de celular sem abrir o robô (o conector aparece só por trás/por baixo);
    #  - o suporte 2x18650 leva células soltas, quase sempre SEM proteção: quem corta a descarga funda e o curto é o BMS;
    #  - balancear exige o fio do ponto do meio do suporte (soldar um fio na mola/lâmina que une as duas células);
    #  - carregador externo (tirar as células pela porta) continua possível, mas não como rotina: abre o robô toda carga.
    #  Alternativa sem balanceamento: DDTCCRUB-2S-2A (CN3302, 38 x 18 x 6, 5 g, carga 1,1 A; T usinainfo 8763): cabe no mesmo berço alongado.
    furos="não tem: berço + abraçadeira, com a boca USB-C encostada numa janela da parede",
)
BMS2S = NS(
    nome="placa de proteção BMS 2S 10 A (modelo 10A2S)",
    cx=(24.0, 11.0, 3.0),              # T: ~24 x 11 x 3 mm, 1,3 g; corta a 2,82–2,98 V por célula, sobrecarga 4,26–4,31 V, curto
                                       #    https://www.usinainfo.com.br/controladores-de-carga/controlador-de-carga-placa-de-protecao-de-carga-bms-para-bateria-18650-2s-10a-84v-5446.html
    massa=1.3,                         # T
    furos="não tem: bolso raso + fita dupla-face (vai soldada nos fios da bateria)",
)

# ------------------------------------------------------------------ BASE (esqueleto comum dos bichos que rodam)
BASE = NS(
    piso_z=(9.0, 13.0),                # o piso fica 9 mm acima do chão
    piso_x=46.0, piso_y=(-76.0, 14.0),
    parede_x0=29.0, parede_esp=5.0,    # paredes do rack: X de 29 a 34; entre elas (58): bateria + bandejas
    parede_y=(-78.0, 14.0),
    eixo_roda_z=RODA.d / 2,            # 32,5
    asa_x=(40.0, 76.0), asa_y=(37.0, 46.0), faixa_x=(40.0, 53.0),
    lobo_motor_z=62.0,                 # as paredes só avançam até Y=+14 na altura do motor (abaixo deste Z)
    lanca_x=15.0, lanca_y_fim=-144.0, pa_x=27.0, pa_y=(-116.0, -100.0),
    esfera_y=-130.0,
    deck_z=137.0,                      # topo do deck = face de baixo da aba do servo de pan
    deck_esp=4.0,
    pescoco_y=-38.0,                   # eixo do pan (16 mm atrás do previsto no 1º desenho: põe o CG atrás das rodas)
    deck_y1=2.0,                       # borda da frente do deck
    ombro=(-16.5, 142.0),                # (y, z) do eixo dos servos dos braços (janelas nas paredes)
    orelha_ombro_z=157.0,
    trilho_z=(37.0, 86.0),             # fundo dos dois trilhos (níveis A e B) nas paredes
    trilho_alt=3.6, trilho_prof=2.0, trilho_y_fim=-9.2,
    bandeja=(61.4, 85.5, 3.0),         # largura, comprimento, espessura da bandeja deslizante
    bandeja_y0=-95.0,
    espacador=5.0,                     # altura dos pilares das placas eletrônicas
    trava_y=-68.0,                     # parafuso que trava cada bandeja (pela parede direita)
    travessa_y=(-9.0, -6.0), travessa_z=(36.0, 133.0), travessa_recorte=(12.0, 106.0),   # acima de z=106 a travessa abre |x|<12 (corpo do servo de pan)
    driver_z=57.5,                     # centro do L298N na travessa da frente
    baia_bateria=(58.0, 114.0, 23.0),  # largura x comprimento x altura livres no piso
    bateria_y=-36.0,                   # centro do suporte 2x18650 na baia
    chave_y=-108.0, jack_y=-90.0,
    costura_y=-38.0,                   # plano que divide torso-frente / torso-costas (passa pelo eixo do pescoço)
    encoder_extra=12.0,                # reserva acima do motor TT p/ o disco/placa do encoder (fase 2)
    # furos M3 no piso para prender as cascas (x, y); espelhados em X quando x != 0
    furos_torso_costas=((22.0, -84.0),),   # 2 orelhas (espelhadas), fora do caminho da chave e da esfera
    pa_frente_y=(-90.0, -78.0),
    # postes do chassi (|x|, z, y da ponta) que recebem 2 parafusos do torso-frente (ficam sob o painel da frente)
    postes_frente=((30.0, 104.0, 18.0),),
    furos_torso_frente=((0.0, 10.0),),
    furos_perna=((68.0, 41.5), (68.0, -41.5)),
    furos_cauda=((20.0, -108.0),),
)

# ------------------------------------------------------------------ PESCOCO (pan + tilt comum aos bichos)
PESCOCO = NS(
    garfo_base_esp=4.0, garfo_base_r=24.0,
    garfo_x=27.0, garfo_esp=4.0,       # faces internas dos montantes em X=±27 (entre eles: servo de tilt MG996R em pé)
    tilt_acima_da_base=23.0,           # eixo do tilt acima do topo da base do garfo
    gola_r=58.0,                       # raio da esfera do topo do torso: a cabeça gira e inclina em volta dela (sem pescoço à mostra)
    gola_abertura_r=32.0,              # abertura no topo da esfera por onde sobe a coluna
    coluna_r=12.0, coluna_chato=3.5,   # coluna em "D": os cabos sobem pela frente chata, junto ao eixo
    mesa_z=58.5,                       # face de baixo da mesa da cabeça, acima do centro da junta
    mesa_esp=4.0,
    cabeca_z=10.0,                     # plano de baixo da cabeça, acima do centro da junta
    pan=(-60.0, 60.0), tilt=(-15.0, 20.0), boca=(0.0, 18.0),   # graus; tilt positivo = cabeça para cima
)
# centro da junta do pescoço (interseção pan x tilt)
PESCOCO.centro = (0.0, BASE.pescoco_y,
                  BASE.deck_z + MG996R.aba_ate_topo_horn + PESCOCO.garfo_base_esp + PESCOCO.tilt_acima_da_base)

# ------------------------------------------------------------------ DINO (modelo 1)
# Blobs = (centro, raios). Tudo em mm, robô montado, chão em Z=0, eixo das rodas em Y=0.
DINO = NS(
    passo=1.25,                        # passo da grade da pele
    torso=[((0, -38, 44), (72, 68, 54)),          # pelve
           ((0, -46, 118), (64, 66, 72)),         # costas / peito
           ((0, -16, 74), (66, 58, 66)),          # barriga  (o topo é a esfera da gola, somada em bicho.pele_torso)
           ((44, 0, 40), (24, 58, 42)), ((-44, 0, 40), (24, 58, 42))],   # quadris (cobrem os motores e as faixas do piso)
    cabeca=[((0, -30, 256), (78, 72, 60)),        # crânio
            ((0, 34, 240), (58, 48, 40)),         # focinho
            ((36, 0, 296), (27, 27, 24)), ((-36, 0, 296), (27, 27, 24)),   # sobrancelhas
            ((0, -30, 210), (62, 60, 18))],       # base
    perna=[((71, 0, 32), (31, 56, 46)), ((60, 0, 32), (26, 56, 46)),   # roda (2 blobs = lateral mais chata)
           ((66, -14, 76), (30, 42, 40)),         # coxa
           ((72, 26, 22), (30, 44, 24))],         # pé
    cauda=[((0, -112, 34), (46, 42, 38)), ((0, -146, 26), (30, 32, 28)),
           ((0, -170, 27), (19, 24, 18)), ((0, -186, 31), (10, 12, 10))],
    olho=NS(c=(36.0, 12.0, 293.0), r=24.0, dir=(0.22, 0.93, 0.28), iris_r=14.0, pupila_r=8.0),
    boca=dict(y_eixo=28.0, z_eixo=220.0, y_corte=22.0, z0=234.0, y_ref=50.0, incl=-0.06, raio_sorriso=140.0, folga=1.2),
    barriga=NS(c=(0.0, 88.0), r=(40.0, 44.0)),    # janela elíptica (x, z) da barriga creme
    braco=NS(mao=(56.0, 26.0, 128.0), r_ombro=(11.0, 14.0, 13.0), r_mao=(11.0, 13.0, 11.0), lim=(-15.0, 40.0)),   # até 70° com a cabeça reta (o verificador testa o pior caso: cabeça virada e baixa)
    n_pecas=38,                        # contagem esperada de peças impressas (conferida pelo verificador)
)

# ------------------------------------------------------------------ CAPIVARA (modelo 2)
# Rodada 2: a casca vem da malha de image-to-3D (cad/peles/capivara.npz, 300 mm de altura, convertida por
# cad/pele_malha.py) e o esqueleto é o "baixo e largo" de cad/comum/base_baixa.py (junta do pescoço em Z=150, e não
# 185 como no esqueleto alto do dino). Valores marcados "pele" estão no referencial da pele (centro da caixa da malha
# em Y=0); no robô somam `dy`, porque o eixo das rodas é sempre Y=0.
CAPIVARA = NS(
    pele="capivara.npz",
    dy=25.0,                           # a pele fica 25 mm à frente do eixo das rodas: rodas sob as ancas (y da pele = -25)
    pescoco=(12.0, 150.0),             # (y na pele, z) do centro da junta pan x tilt = estrangulamento da malha
    soquete_r=66.0,                    # esfera oca da cabeça em volta da junta
    folga_junta=2.0,                   # a gola (esfera do corpo) fica com soquete_r - folga = 64 mm de raio
    cabeca_z=2.0,                      # plano de baixo da cabeça, acima do centro da junta
    z_fundo=5.0,                       # borda de baixo da bacia (é a face que vai na mesa)
    z_gola=124.0,                      # corte horizontal entre a bacia (corpo) e a gola-bandana
    gola_elev=45.0,                    # a esfera da gola sobe até 45° de elevação (acima disso não imprime sem suporte)
    anca=[((52.0, -25.0, 32.0), (45.0, 56.0, 50.0))],   # blob (pele) que engorda a anca só onde a roda pede
    porta=NS(x=38.0, y_max=-30.0),     # porta traseira: faixa |x| < 38 da bacia, atrás de y (pele) = -30, altura inteira
    # boca (pele): eixo da mandíbula, plano de corte de trás, altura da boca em y_ref, inclinação, raio do sorriso
    boca=dict(y_eixo=83.0, z_eixo=175.0, y_corte=77.0, z0=177.0, y_ref=118.0, incl=-0.08, raio_sorriso=150.0, folga=1.2),
    olho=NS(x=50.0, z=232.0, r=21.0, afunda=0.5, iris_r=15.0, pupila_r=10.0),   # centro = ponto da pele recuado r x afunda
    aro=NS(r_fora=20.0, r_dentro=14.0),           # aro ciano na lateral da anca, no eixo da roda
    # esqueleto baixo (cad/comum/base_baixa.py). y em "pele"; z e x no robô
    esq=NS(
        piso_z=(9.0, 13.0), piso_x=53.0, piso_nivel=-3.2,   # piso = seção da pele em z=9 (3,2 mm para dentro), |x| <= 53
        parede_x0=29.0, parede_esp=5.0,    # paredes do rack/torre: X de 29 a 34 (58 livres entre elas)
        parede_y=(-78.0, 25.5),            # pele: fundo do rack ... frente da torre do pan (até onde o piso existe: a bacia desce por cima)
        torre_x1=38.0,                     # face interna da parede DIREITA da torre: o servo de pan vai deitado de lado (corpo para +X)
        rack_z=78.0,                       # topo das paredes na parte do rack (a torre sobe até o deck)
        travessa_y=(-6.0, -3.0), travessa_z0=30.0,   # pele: parede transversal entre rack e torre (L298N na face da frente)
        deck_z=102.0, deck_esp=4.0,        # topo do deck = face de baixo da aba do servo de pan
        driver_z=44.0,                     # centro do L298N (sob o servo de pan)
        bateria_y=-45.5,                   # pele: centro do suporte 2x18650 (no piso, entre as paredes; sai por trás)
        trilho_z=(37.0, 66.0),             # fundo dos trilhos: nível de baixo = Pi, nível de cima = Uno + shield
        trilho_alt=3.6, trilho_prof=2.0,
        bandeja_larg=61.4, bandeja_esp=3.0, espacador=5.0,
        pi_y=(-97.0, -8.0), pi_placa_y=-10.0,     # pele: bandeja do Pi (fundo, frente) e borda da frente da placa
        uno_y=(-80.0, -7.0), uno_placa_y=-76.0,   # pele: bandeja do Uno e borda de trás da placa (USB para trás)
        esferas=((60.0, 29.0),),           # (|x|, y pele) das 2 esferas de apoio da frente, sob as patas
        orelhas=((46.0, -62.0, -1),),      # (|x|, y pele, sentido em Y) das 2 orelhas M3 de trás da bacia, no piso (na frente ela prende nas esferas)
        poste_porta=(24.0, 34.0, -78.0, -70.0, 32.0, 24.0),   # x0, x1, y0, y1 (pele), z do topo, z do parafuso da porta
        encoder_extra=12.0,
    ),
    n_pecas=21,
)

# ------------------------------------------------------------------ CUBO (modelo 3: robô quadrado de mesa)
# Não roda. Base baixa e larga com o servo de pan + engrenagens 2:1 (servo comum de 180° gira o pescoço ±170°), Arduino,
# bateria 2S e os módulos de energia; pescoço estreito (tubo oco Ø28); cabeça-cubo com tela de 3,5" + Raspberry Pi e o
# tilt por DENTRO (garfo interno). Geometria comum com o cubo que roda: cad/comum/quadrado.py.
def _cabeca_cubo(larg, y, z, zs, zcam, pilar_x, pilar_dz, lat_e_z, raio=20.0):
    """Parâmetros da cabeça-cubo no referencial do cruzamento pan x tilt (X lados, +Y rosto, Z cima)."""
    return NS(
        larg=larg, y=y, z=z,               # largura; (costas, frente); (fundo, topo) em relação ao eixo do tilt
        raio=raio, parede=2.8,             # raio das 4 arestas compridas (verticais na impressão); parede do copo
        chanfro_tras=4.0, raio_frente=1.4,  # aresta de trás em chanfro de 45° (encosta na mesa); borda da frente arredondada
        painel_esp=3.0, painel_recuo=1.0,  # painel escuro do rosto, 1 mm para dentro da borda (fresta de sombra)
        zs=zs, zcam=zcam,                  # centro da tela e da câmera (acima da tela, atrás do painel)
        pilar_x=pilar_x, pilar_dz=pilar_dz,   # 4 pilares do painel (por fora da tela), presos por trás da travessa
        espacador=5.0, travessa_esp=3.0, vao_tela_pi=6.0, lateral_esp=5.0, lat_e_z=lat_e_z,
        horn_x=11.0,                       # face do braço direito do garfo (horn do servo de tilt)
        braco_x=30.0, braco_esp=5.0, braco_esp_e=7.0,   # braço esquerdo em x=-30 (pino M3 + inserto)
        garfo_y=24.0, bloco_y=24.0, garfo_z=(-30.5, -12.0),   # garfo interno: fundo (assenta no tubo) e topo do bloco
        tubo_d=28.0, furo_cabos=9.0, tirante_r=8.5, tirante_ang=(0.0, 120.0, 240.0),   # 3 tirantes M3 no tubo
        mic_x=24.0, tilt=(-25.0, 30.0),
    )


CUBO = NS(
    base=(158.0, 146.0, 60.5),         # largura (x), profundidade (y), altura da base (antes 150 x 144 x 70: mais baixa e larga)
    base_r=20.0, parede=3.0, tampa_esp=4.0, chanfro=3.0,   # chanfro de 45° embaixo (base) e em cima (tampa)
    eixo_y=-6.0,                       # eixo do pescoço (pan): a cabeça fica centrada sobre a base
    ang_servo=45.0, ang_corpo=-90.0,   # o servo de pan fica a 45° do eixo (frente-direita), corpo apontando para trás
    modulo=1.5, dentes=(22, 44),       # pescoço 22 dentes, servo 44 dentes → o pescoço gira 2x o servo
    eng_z=(48.2, 56.2), eng_folga=0.25,
    flange=(20.0, 1.5),                # raio e altura da flange do tubo (depois vira cone de 45° até o Ø do tubo)
    folga_pescoco=22.0,                # vão entre a tampa e o fundo da cabeça (a cabeça inclinada desce 20 mm na frente)
    cab=_cabeca_cubo(larg=136.0, y=(-45.0, 57.0), z=(-36.8, 81.2), zs=20.0, zcam=61.3, pilar_x=59.5, pilar_dz=22.0, lat_e_z=(-9.0, 52.0)),
    pan=(-170.0, 170.0),
    uno_xy=(-59.0, 14.0),              # canto do Uno (USB para a esquerda)
    bateria_xy=(-35.0, -28.5),         # sai pela porta de trás
    porta_x=(-58.0, -12.0),
    stepdown_xy=(62.0, -7.0), ubec_xy=(16.0, -33.5), carregador_x=48.0, bms_xy=(-4.0, -40.0),
    falante_xz=(13.0, 34.0),           # alto-falante (fase 2) na parede de TRÁS, grade de fendas verticais
    chave_xz=(48.0, 30.0),             # chave na parede de trás, acima do carregador USB-C
    n_pecas=15,
)
CUBO.tilt = CUBO.cab.tilt
# altura do eixo do tilt: tampa + vão do pescoço + distância do eixo ao fundo da cabeça
CUBO.tilt_z = CUBO.base[2] + CUBO.folga_pescoco - CUBO.cab.z[0]

CORES = {
    "verde": (0.36, 0.72, 0.16), "creme": (0.96, 0.89, 0.62), "azul": (0.20, 0.55, 0.86),
    "branco": (0.97, 0.97, 0.97), "preto": (0.03, 0.03, 0.04), "cinza": (0.42, 0.44, 0.47),
    "laranja": (0.93, 0.52, 0.13), "marrom": (0.36, 0.19, 0.10), "verde-bandana": (0.30, 0.66, 0.16),
    "ciano": (0.25, 0.85, 0.95), "rosa": (0.92, 0.48, 0.52), "grafite": (0.22, 0.23, 0.25),
    "prata": (0.78, 0.79, 0.80), "amarelo": (0.98, 0.80, 0.08),
}
