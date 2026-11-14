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
# Mesmo esqueleto do dino (chassi, bandejas, garfo, berço): só a casca muda.
CAPIVARA = NS(
    passo=1.25,
    junta=3.0,                         # folga da cabeça em volta da esfera (maior: a faixa da bandana fica por baixo)
    torso=[((0, -39, 46), (78, 68, 58)),          # pelve (pera)
           ((0, -46, 116), (64, 66, 72)),         # costas / peito
           ((0, -14, 74), (68, 62, 66)),          # barriga
           ((44, 0, 40), (24, 58, 42)), ((-44, 0, 40), (24, 58, 42)),     # quadris (cobrem os motores e as faixas do piso)
           ((52, 14, 106), (12, 15, 26)), ((-52, 14, 106), (12, 15, 26))],  # braços (parados, fazem parte da casca)
    cabeca=[((0, -28, 254), (80, 76, 60)),        # crânio
            ((0, 38, 244), (48, 44, 36)),         # focinho
            ((0, -30, 210), (62, 60, 18))],       # base
    perna=[((71, 0, 34), (31, 58, 48)), ((60, 0, 34), (26, 58, 48))],     # coxa (cobre a roda)
    pata=((72, 46, 15), (22, 26, 15)),            # pata traseira marrom (peça separada, colada)
    rabo=[((0, -110, 24), (42, 26, 28)), ((0, -130, 22), (40, 34, 30))],
    olho=NS(c=(42.0, 12.0, 272.0), r=21.0, dir=(0.14, 0.97, 0.20), iris_r=15.0, pupila_r=10.0),
    boca=dict(y_eixo=28.0, z_eixo=223.0, y_corte=22.0, z0=234.0, y_ref=50.0, incl=-0.05, raio_sorriso=150.0, folga=1.2),
    barriga=NS(c=(0.0, 88.0), r=(40.0, 44.0)),    # painel da frente (mesma cor do corpo): tampa + grade do alto-falante
    focinho=NS(c=(0.0, 258.0), r=(40.0, 21.0), y0=36.0),   # painel marrom do focinho (janela elíptica x, z; só para y > y0)
    aro=NS(r_fora=20.0, r_dentro=14.0),           # aro ciano na lateral da coxa (janela para o cubo da roda / LED)
    n_pecas=39,
)

# ------------------------------------------------------------------ CUBO (modelo 3: robô quadrado de mesa)
# Não roda: base fixa com o servo de pan + engrenagens 2:1 (servo comum de 180° gira o pescoço ±170°),
# garfo, e cabeça-cubo com tela de 3,5" + Raspberry Pi; tilt por servo padrão dentro da cabeça.
CUBO = NS(
    base=(150.0, 144.0, 70.0),         # largura (x), profundidade (y), altura da base
    base_y=(-78.0, 66.0),              # a base vai de y=-78 (porta traseira) a y=+66
    base_r=12.0, parede=3.0, tampa_esp=4.0,
    eixo_y=14.0,                       # eixo do pescoço (pan)
    servo_y=-35.5,                     # eixo do servo de pan (distância = m*(z1+z2)/2)
    modulo=1.5, dentes=(22, 44),       # pescoço 22 dentes, servo 44 dentes → o pescoço gira 2x o servo
    eng_z=(48.2, 56.2), eng_folga=0.25,
    tubo=(28.0, 14.0),                 # Ø externo e Ø do furo do tubo do pescoço (os cabos sobem por dentro)
    garfo_y=24.0, garfo_braco=(61.5, 5.0),   # largura do garfo em y; face interna dos braços em |x| e espessura
    cabeca=(112.0, 92.0, 100.0), cabeca_r=14.0, cabeca_parede=2.4,
    tela_dz=-6.0,                      # centro da tela abaixo do centro da cabeça
    tilt=(-25.0, 30.0), pan=(-170.0, 170.0),
    uno_xy=(7.0, -15.0),              # canto do Uno na base (USB para trás)
    bateria_xy=(-40.5, -1.0),
    falante_xz=(-38.0, 30.0),
    n_pecas=14,
)
# altura do eixo do tilt: topo do garfo-base + meia diagonal da cabeça + folga
CUBO.garfo_z = (CUBO.base[2] + 0.3, CUBO.base[2] + 10.3)
CUBO.tilt_z = CUBO.garfo_z[1] + ((CUBO.cabeca[1] / 2) ** 2 + (CUBO.cabeca[2] / 2) ** 2) ** 0.5 + 2.3

CORES = {
    "verde": (0.36, 0.72, 0.16), "creme": (0.96, 0.89, 0.62), "azul": (0.20, 0.55, 0.86),
    "branco": (0.97, 0.97, 0.97), "preto": (0.03, 0.03, 0.04), "cinza": (0.42, 0.44, 0.47),
    "laranja": (0.93, 0.52, 0.13), "marrom": (0.36, 0.19, 0.10), "verde-bandana": (0.30, 0.66, 0.16),
    "ciano": (0.25, 0.85, 0.95), "rosa": (0.92, 0.48, 0.52), "grafite": (0.22, 0.23, 0.25),
    "prata": (0.78, 0.79, 0.80), "amarelo": (0.98, 0.80, 0.08),
}
