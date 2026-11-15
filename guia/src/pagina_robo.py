#!/usr/bin/env python3
"""Página própria de UM robô no guia (PT/EN/ES) + docs do robô nos 3 idiomas + esquema de ligação (SVG) + zip.
Não toca nas outras páginas do guia (a entrada /guia/ é de montar.py; a evolução, de evolucao.py).

Fontes:
  projetos/<robô>/montagem.json · mesas.json · verificacao.json  números das peças (comum/cad/gerar.py e verificar.py)
  guia/src/robos/<robo>.dados.json     compras, parafusos, notas dos passos, rótulos das peças, LIGAÇÕES (fonte única do
                                       esquema, da tabela da página e do LIGACAO.md), glossário e riscos
  guia/src/robos/_comum.pt.json        rótulos iguais em todas as páginas de robô
  guia/src/robos/<robo>.pt.json        textos da página deste robô (e os rótulos do esquema, chaves sv_*)
  guia/src/robo.html                   estrutura única da página (os textos entram por [[chave]])
  projetos/<robo>/*.md                 docs em português; os blocos <!-- GERADO:x --> são preenchidos aqui. Os arquivos
                                       <nome>.en.md e <nome>.es.md são GERADOS (prosa pelo inema-traduz, tabelas daqui)

Robôs: cubo, dino, capivara, cubo-rodas (dicionário ROBOS). O esquema dos bichos é guia/src/esquema_bicho.py e o do cubo
que roda, guia/src/esquema_cubo_rodas.py (os dois desenham com guia/src/esquema_base.py).

Uso (sempre com o venv do repo; troque `cubo` pelo robô):
  .venv/bin/python guia/src/pagina_robo.py docs cubo [pt en es]   blocos GERADO dos .md + versões .en.md/.es.md
  .venv/bin/python guia/src/pagina_robo.py traduzir cubo [en es]  EN e ES pelo inema-traduz (só o que falta ou mudou)
  .venv/bin/python guia/src/pagina_robo.py esquema cubo [pt en es] ligacao.<lg>.svg (docs e guia/<robô>/assets/)
  .venv/bin/python guia/src/pagina_robo.py pagina cubo [pt en es] guia/cubo/, guia/en/cubo/, guia/es/cubo/
  .venv/bin/python guia/src/pagina_robo.py zip cubo               projetos/cubo/cubo-stl.zip
  .venv/bin/python guia/src/pagina_robo.py imagens cubo           cópias dos renders e dos mapas de balanços em guia/cubo/assets/
  .venv/bin/python guia/src/pagina_robo.py conferir cubo          links, tags, vírgula decimal no inglês, notas internas, zip
Ordem depois de mudar texto em português: docs pt → traduzir → docs → esquema → pagina → zip → conferir.
A página também mostra o mapa de balanços (projetos/<robô>/imagens/balancos/indice.json) e os números de semelhança
(comparacao/semelhanca.json). O guia inteiro (entrada, 4 robôs, evolução) de uma vez: .venv/bin/python guia/src/tudo.py
"""
import hashlib
import html
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GUIA = AQUI.parent
RAIZ = GUIA.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / "comum"))     # pacote `cad`: só o registro id → pasta (caminhos.py não importa numpy)
from cad.caminhos import MODELOS  # noqa: E402
import montar            # noqa: E402  (cabeça/CSS/rodapé do template do guia)
import semelhanca as SEM  # noqa: E402  (IoU de comparacao/semelhanca.json, mesma conta do alvo das tabelas)
import traduzir as TR    # noqa: E402  (pedido ao inema-traduz e conferência de tags)

REPO = "https://github.com/inematds/robos-impressos"
SITE = "https://inematds.github.io/robos-impressos/guia/"
RAW = REPO + "/raw/main/"
BLOB = REPO + "/blob/main/"
TREE = REPO + "/tree/main/"
ML = "https://lista.mercadolivre.com.br/"
# tutorial público de solda, em português (conferido em 15/11/2026: a página abre e ensina o básico, com fotos)
SOLDA_URL = "https://blog.fazedores.com/como-soldar-aprenda-a-fazer-uma-solda-perfeita/"
# tempo de montagem: ESTIMATIVA por contagem (nada foi montado ainda). Minutos por item e folga (mín, máx) sobre a soma.
MONT_MIN = {"bancada": 7, "passo": 6, "fio": 3, "inserto": 2}
MONT_FOLGA = (0.8, 1.5)
GLO_LINK = ("UBEC", "BMS", "2S", "3S")       # termos do glossário que ganham "o que é isso?" na 1ª vez que aparecem em #comprar
# página → robô. A chave é o nome da página (guia/<nome>/) e da pasta projetos/<nome>/; `id` é o id do modelo no código.
# `pecas` (stl, mesas, montagem.json) e `docs` são a MESMA pasta do robô, tirada do registro único comum/cad/caminhos.py.
# `esquema` = módulo de guia/src/ com svg(X, R) (esquema de ligação do robô); None = o desenho do cubo, que mora neste arquivo.
def _robo(id, emoji, esquema=None):
    p = f"projetos/{MODELOS[id]}"
    return dict(id=id, pecas=p, docs=p, emoji=emoji, esquema=esquema)


ROBOS = {"cubo": _robo("cubo", "🤖"), "dino": _robo("dino", "🦖", "esquema_bicho"), "capivara": _robo("capivara", "🦫", "esquema_bicho"),
         "cubo-rodas": _robo("cubo_rodas", "🤖", "esquema_cubo_rodas")}
CUPOM = "comum/pecas/stl/comum-teste-encaixe.stl"               # peça comum citada à mão nos docs
IDIOMAS = ("pt", "en", "es")
# mapa de balanços: a regra que comum/cad/mapas_balancos.py usou para escolher as peças (o texto para o leitor é a chave
# bal_regra; se a regra mudar, o assert do Robo avisa) e a cor de cada item da legenda (as do render)
BAL_REGRA = "peça com suporte declarado, ou >= 50 g, ou ponto de carga (garfo, berco, tubo-pescoco, chassi)"
BAL_COR = {"vermelho": "#e0262c", "amarelo": "#f4c20d", "azul": "#3d74d9", "cinza": "#c9c9ce"}
DOCS_LG = ("LISTA-DE-COMPRAS", "IMPRIMIR", "LIGACAO")            # docs que ganham versão .en.md e .es.md
LEIA = {"pt": "LEIA-ME.md", "en": "README.en.md", "es": "LEEME.es.md"}   # o guia de impressão dentro do zip
BANDEIRA = {"pt": "🇧🇷 Português", "en": "🇺🇸 English", "es": "🇪🇸 Español"}
# termos das páginas de robô que o pedido geral de guia/src/traduzir.py não cobre
GLOSSARIO = ('- "horn" (a peça que encaixa no eixo do servo) fica "horn": "servo horn" / "horn del servo"; nunca "arm" nem "brazo". '
             '"garfo" = fork / horquilla. "braço do garfo" = fork arm / brazo de la horquilla. "bancada" = workbench / mesa de trabajo. '
             '"copo da cabeça" = head shell / carcasa de la cabeza. "tirante" = tie rod / tirante. "cupom de teste" = test coupon / cupón de prueba. '
             '"chicote" (de fios) = wiring harness / mazo de cables. "borne" = screw terminal / borne. "ilha" (de solda) = solder pad / pad de soldadura. '
             '"preparo" = prep step / preparativo. "placa de proteção" = protection board / placa de protección. "ponto do meio" = middle point / punto medio. '
             '"termo-retrátil" = heat-shrink tubing / tubo termorretráctil. "esquema de ligação" = wiring diagram / esquema de conexión. '
             '"não testado na bancada" = not bench-tested / no probado en el banco de trabajo. '
             '"robô quadrado de mesa" = square desktop robot / robot cuadrado de mesa; "robô de mesa" = desktop robot / robot de mesa (nunca "tabletop"). '
             'Faixa de preço "R$ 10 a R$ 20" = "R$ 10 to R$ 20" / "R$ 10 a R$ 20". '
             '"barra de emenda" (a barra de bornes tipo sindal) = terminal block / barra de conexión, sempre com esse nome; "borne 1" = terminal 1 / borne 1.\n'
             '- Não traduza: Sensor Shield, UBEC, BMS, LM2596, GPIO, Dupont, SEL, VCC, GND, COM, IIC, NC, Mercado Livre, Raspberry Pi Imager, Raspberry Pi OS, Arduino IDE, LCD-show, MPI3501.')
MD_REGRA = ('- Os valores com chave "d_" são trechos de Markdown: mantenha idênticos os marcadores (#, -, 1., **, >), o que estiver entre crases, '
            'os nomes de arquivo, os caminhos e as URLs dos links; traduza só o texto.')


def PONTO(s):
    """Vírgula decimal → ponto (só no inglês): 5,1 V → 5.1 V; M2,5 → M2.5. Lista "3,9, 4,0" continua lista."""
    return re.sub(r"(?<=\d),(?=\d)", ".", s)


def sha(s, n=12):
    return hashlib.sha1(s.encode()).hexdigest()[:n]


# ------------------------------------------------------------------ dados
def ler(p):
    return json.loads(Path(p).read_text())


def reparte(vals, casas=0):
    """Arredonda cada valor de modo que a soma exibida feche com o total arredondado (maiores restos)."""
    f = 10 ** casas
    alvo = round(sum(vals) * f)
    base = [int(v * f + 1e-9) for v in vals]
    resto = sorted(range(len(vals)), key=lambda i: vals[i] * f - base[i], reverse=True)
    for i in resto[:max(0, alvo - sum(base))]:
        base[i] += 1
    return [b / f for b in base]


class Robo:
    def __init__(self, nome):
        self.nome = nome
        self.cfg = ROBOS[nome]
        self.pasta = RAIZ / self.cfg["pecas"]
        self.docs = RAIZ / self.cfg["docs"]
        self.mj = ler(self.pasta / "montagem.json")
        self.mesas = ler(self.pasta / "mesas.json")["mesas_lista"]
        self.verif = ler(self.pasta / "verificacao.json")
        self.d = ler(AQUI / "robos" / f"{nome}.dados.json")
        self.pecas = {p["nome"]: p for p in self.mj["pecas"]}
        bal = self.pasta / "imagens" / "balancos" / "indice.json"          # mapas de balanços (comum/cad/mapas_balancos.py)
        self.bal = ler(bal) if bal.exists() else None
        if self.bal:
            assert self.bal["regra"] == BAL_REGRA, "a regra de escolha das peças do mapa de balanços mudou: reescreva bal_regra em _comum.pt.json e BAL_REGRA"
            assert set(self.bal["cores"]) == set(BAL_COR), "cores do mapa de balanços mudaram: atualize BAL_COR"
        passos = {o["passo"] for o in self.mj["ordem_montagem"]}
        sobra = set(self.d["passos_nota"]) - passos
        assert not sobra, f"passos_nota com passo que não existe mais no modelo: {sorted(sobra)}"
        assert len(self.d["ordem_impressao"]) == len(self.mesas), "ordem_impressao não cobre todas as mesas"
        assert sum(p["qtd"] for p in self.d["parafusos"] if "inserto" in p["rosca"]) == self.d["insertos"], "insertos: tabela de parafusos não bate"
        assert set(self.d["rotulos"]) == set(self.pecas), "rotulos: falta ou sobra peça"
        for x in self.d["passos_extra"]:
            assert x["antes"] in passos, f"passos_extra: passo '{x['antes']}' não existe no modelo"
        # gramas e horas EXIBIDOS por peça (a linha soma as cópias): as 3 tabelas saem daqui e fecham no mesmo total
        nomes = [p["nome"] for p in self.mj["pecas"]]
        self.g = dict(zip(nomes, reparte([p["massa_g"] * p["qtd"] for p in self.mj["pecas"]], 0)))
        self.h = dict(zip(nomes, reparte([p["tempo_h"] * p["qtd"] for p in self.mj["pecas"]], 1)))
        # as linhas de filamento da lista de compras são digitadas: têm de bater com as peças
        for bl in self.d["compras"]:
            for it in bl["itens"]:
                c = it.get("confere")
                if c:
                    cores = [(g, k) for k, (g, _) in self.por_cor() if k[0] == c["material"]]
                    assert round(sum(g for g, _ in cores)) == c["g"] and len(cores) == c["cores"], f'filamento {c["material"]}: a lista diz {c["g"]} g em {c["cores"]} cores, as peças dão {sum(g for g, _ in cores):.0f} g em {len(cores)}'

    def altura(self):
        """Altura do robô montado (mm): a que o modelo calcula (obs.altura_mm); senão a de <robô>.dados.json (envelope medido)."""
        return self.mj["obs"].get("altura_mm") or self.d["altura_mm"]

    def caminho(self, p):
        """Caminho no repo do arquivo de uma peça (o montagem.json guarda relativo à pasta do modelo)."""
        return str((self.pasta / p["arquivo"]).resolve().relative_to(RAIZ))

    def gramas(self):
        return sum(self.g.values())

    def horas(self):
        return round(sum(self.h.values()), 1)

    def n_pecas(self):
        return sum(p["qtd"] for p in self.mj["pecas"])

    def n_servos(self):
        return sum(1 for c in self.mj["componentes"] if c["nome"].startswith("servo-"))

    def horas_montagem(self):
        """(mín, máx) em horas, do preparo na bancada ao robô fechado. ESTIMATIVA por contagem (MONT_MIN por passo de
        bancada, passo de montagem, fio da tabela de ligações e inserto), com a folga MONT_FOLGA. Nada foi montado ainda."""
        minutos = (MONT_MIN["bancada"] * sum(len(p["passos"]) for p in self.d["preparos"])
                   + MONT_MIN["passo"] * (sum(1 for o in self.mj["ordem_montagem"] if not o.get("sai")) + len(self.d["passos_extra"]))
                   + MONT_MIN["fio"] * sum(len(g["fios"]) for g in self.d["ligacoes"])
                   + MONT_MIN["inserto"] * self.d["insertos"])
        return tuple(round(minutos * f / 60) for f in MONT_FOLGA)

    def por_cor(self):
        o = {}
        for p in self.mj["pecas"]:
            k = (p["material"], p["cor"])
            g, h = o.get(k, (0.0, 0.0))
            o[k] = (g + self.g[p["nome"]], round(h + self.h[p["nome"]], 1))
        return sorted(o.items())

    def da_mesa(self, m):
        """(gramas, horas, {peça: cópias}) de uma mesa, pelos mesmos números exibidos na tabela de peças."""
        itens = {}
        for x in m["itens"]:
            itens[x] = itens.get(x, 0) + 1
        g = sum(self.g[x] * q / self.pecas[x]["qtd"] for x, q in itens.items())
        h = sum(self.h[x] * q / self.pecas[x]["qtd"] for x, q in itens.items())
        return g, round(h, 1), itens

    def custo(self):
        """Faixas (mín, máx) em R$: 'pecas' = fase 1 sem filamento nem ferramentas; 'tem' = o que o dono talvez já tenha
        (dentro de 'pecas'); 'fil' = 1 rolo de cada material; 'ferr' = ferramentas não opcionais; 'zero' = pecas + fil + ferr."""
        o = {k: [0, 0] for k in ("pecas", "tem", "fil", "ferr")}
        for bl in self.d["compras"]:
            onde = "ferr" if bl.get("ferramenta") else "fil" if bl.get("filamento") else "pecas"
            for it in bl["itens"]:
                if it.get("opcional"):
                    continue
                for k in [onde] + (["tem"] if it.get("tem") else []):
                    o[k][0] += it["faixa"][0] * it["n"]
                    o[k][1] += it["faixa"][1] * it["n"]
        o["zero"] = [o["pecas"][i] + o["fil"][i] + o["ferr"][i] for i in (0, 1)]
        return o


# ------------------------------------------------------------------ textos (manual + automático) e tradução
def chave_auto(s):
    return "a_" + hashlib.sha1(s.encode()).hexdigest()[:10]


def frases_auto(R):
    """Tudo o que a página mostra e vem dos JSON em português: vira chave a_<hash> e passa pelo tradutor."""
    f = []
    for p in R.mj["pecas"]:
        f += [p["material"], p["cor"], p["suporte"], p.get("orientacao", ""), p.get("reforco", ""), p.get("obs", "")]
    for o in R.mj["ordem_montagem"]:
        f.append(o["passo"])
    f += list(R.d["passos_nota"].values()) + list(R.d["rotulos"].values()) + list(R.d["riscos"])
    for x in R.d["passos_extra"]:
        f += [x["passo"], x["vem"], x["nota"]]
    for bl in R.d["compras"]:
        f.append(bl["bloco"])
        for it in bl["itens"]:
            f += [it["item"], it["usa"], it["comprar"], it["para"], it["base"], it.get("conf", ""), it.get("nc", "")]
    for it in R.d["fase2"]:
        f += [it["item"], it["qtd"], it["onde"], it.get("conf", ""), it.get("nc", "")]
    for p in R.d["parafusos"]:
        f += [p["onde"], p["tipo"], p["rosca"]]
    for o in R.d["ordem_impressao"]:
        f.append(o["porque"])
    for g in R.d["ligacoes"]:
        f.append(g["grupo"])
        for w in g["fios"]:
            f += [w["de"], w["para"], w["cor"], w["fio"], w["nota"]]
    for g in R.d["glossario"]:
        f += [g["termo"], g["def"]]
    for pr in R.d["preparos"]:
        f += [pr["titulo"]] + pr["passos"]
    if R.bal:                                                       # mapa de balanços: tudo o que a página mostra do indice.json
        f += list(R.bal["vistas"]) + list(R.bal["cores"].values())
        for p in R.bal["pecas"]:
            f += [p["veredito"], p["suporte"], p["orientacao"]]
    return {chave_auto(s): s for s in dict.fromkeys(f) if s and not re.fullmatch(r"[\d\s+.,×x–-]*", s)}


def textos_pt(R):
    t = ler(AQUI / "robos" / "_comum.pt.json")
    t.update(ler(AQUI / "robos" / f"{R.nome}.pt.json"))
    t.update(frases_auto(R))
    return t


def partes_md(s):
    """Quebra um .md em [(tipo, texto)]: 'ger' = nome de um bloco GERADO, 'cod' = cerca de código, 'txt' = parágrafo
    (título, texto ou lista) que vai ao tradutor, 'sep' = linhas em branco."""
    o = []
    for i, tr in enumerate(re.split(r"(<!-- GERADO:[a-z0-9_]+ -->.*?<!-- /GERADO -->)", s, flags=re.S)):
        if i % 2:
            o.append(("ger", re.match(r"<!-- GERADO:([a-z0-9_]+)", tr).group(1)))
            continue
        for j, c in enumerate(re.split(r"(```.*?```)", tr, flags=re.S)):
            if j % 2:
                o.append(("cod", c))
                continue
            for par in re.split(r"(\n[ \t]*\n)", c):
                o.append(("txt" if par.strip() else "sep", par))
    return o


def docs_pt(R):
    """Parágrafos em português dos docs que têm versão EN/ES: chave d_<hash> → texto."""
    o = {}
    for nome in DOCS_LG:
        for tipo, x in partes_md((R.docs / f"{nome}.md").read_text()):
            if tipo == "txt":
                o["d_" + sha(x.strip(), 10)] = x.strip()
    return o


def arq_lg(R, lg, docs=False):
    return AQUI / "robos" / (f"{R.nome}.docs.{lg}.json" if docs else f"{R.nome}.{lg}.json")


def arq_cache(R, lg, docs=False):
    return AQUI / "robos" / (f".cache.{R.nome}.docs.{lg}.json" if docs else f".cache.{R.nome}.{lg}.json")


def _traduz(pt, dest, cache, lg, lote=36, extra=""):
    feito = ler(dest) if dest.exists() else {}
    marcas = ler(cache) if cache.exists() else {}
    pend = [k for k in pt if k not in feito or marcas.get(k) != sha(pt[k])]
    print(f"{lg}: {len(pend)} de {len(pt)} textos a traduzir ({dest.name})", flush=True)
    cod = lambda s: sorted(re.findall(r"`[^`]*`", s))
    url = lambda s: sorted(re.findall(r"\]\(([^)]+)\)", s))
    itens = lambda s: len(re.findall(r"^(?:\s*[-*] |\s*\d+\. |#+ )", s, flags=re.M))
    for i in range(0, len(pend), lote):
        chaves = pend[i:i + lote]
        bloco = {k: pt[k] for k in chaves}
        regras = GLOSSARIO + extra + ("\n" + MD_REGRA if any(k.startswith("d_") for k in bloco) else "")
        out = None
        for tentativa in range(3):
            r = subprocess.run(["inema-traduz"], input=TR.pedido(lg, bloco).replace("- Números, unidades", regras + "\n- Números, unidades", 1), capture_output=True, text=True, timeout=1500)
            mo = re.search(r"\{.*\}", r.stdout.strip(), re.S)
            try:
                out = json.loads(mo.group(0))
                assert set(out) == set(bloco), "chaves diferentes"
                ruins = [k for k in bloco if TR.tags(out[k]) != TR.tags(bloco[k])]
                assert not ruins, f"tags diferentes em {ruins}"
                marc = [k for k in bloco if sorted(re.findall(r"\[\[\w+\]\]", out[k])) != sorted(re.findall(r"\[\[\w+\]\]", bloco[k]))]
                assert not marc, f"marcadores [[ ]] diferentes em {marc}"
                cr = [k for k in bloco if cod(out[k]) != cod(bloco[k])]
                assert not cr, f"trecho entre crases diferente em {cr}"
                capi = [k for k in bloco if lg == "es" and re.search("capibara", out[k], re.I)]
                assert not capi, f'"capibara" no espanhol (o projeto usa "carpincho") em {capi}'
                md = [k for k in bloco if k.startswith("d_") and (url(out[k]) != url(bloco[k]) or itens(out[k]) != itens(bloco[k]))]
                assert not md, f"Markdown diferente (crases, links ou itens de lista) em {md}"
                break
            except Exception as e:
                print(f"  {lg} bloco {i}: tentativa {tentativa + 1} falhou ({e})", flush=True)
                out = None
        if out is None:
            raise SystemExit(f"Falhou: tradução {lg} bloco {i}")
        feito.update(out)
        for k in chaves:
            marcas[k] = sha(pt[k])
        dest.write_text(json.dumps({k: feito[k] for k in pt if k in feito}, ensure_ascii=False, indent=1) + "\n")
        cache.write_text(json.dumps({k: marcas[k] for k in pt if k in marcas}))
        print(f"  {lg}: {min(i + lote, len(pend))}/{len(pend)}", flush=True)
    # o que saiu do português sai também da tradução e do cache
    dest.write_text(json.dumps({k: feito[k] for k in pt if k in feito}, ensure_ascii=False, indent=1) + "\n")
    cache.write_text(json.dumps({k: marcas[k] for k in pt if k in marcas}))


def herdar(R, lg):
    """Texto com o MESMO português já traduzido na página de outro robô (mesma chave e mesmo hash) herda essa tradução:
    os rótulos comuns ficam iguais nas 4 páginas e só o texto novo vai ao tradutor."""
    pt, dest, cache = textos_pt(R), arq_lg(R, lg), arq_cache(R, lg)
    feito = ler(dest) if dest.exists() else {}
    marcas = ler(cache) if cache.exists() else {}
    falta = [k for k in pt if k not in feito or marcas.get(k) != sha(pt[k])]
    n = 0
    for outro in ROBOS:
        fo, co = AQUI / "robos" / f"{outro}.{lg}.json", AQUI / "robos" / f".cache.{outro}.{lg}.json"
        if outro == R.nome or not falta or not (fo.exists() and co.exists()):
            continue
        do, mo = ler(fo), ler(co)
        for k in list(falta):
            if k in do and mo.get(k) == sha(pt[k]):
                feito[k], marcas[k] = do[k], mo[k]
                falta.remove(k)
                n += 1
    if n:
        dest.write_text(json.dumps({k: feito[k] for k in pt if k in feito}, ensure_ascii=False, indent=1) + "\n")
        cache.write_text(json.dumps({k: marcas[k] for k in pt if k in marcas}))
        print(f"{lg}: {n} textos herdados de outro robô ({dest.name})", flush=True)


def traduzir(R, lg):
    herdar(R, lg)
    extra = ("\n- " + R.d["glossario_traducao"]) if R.d.get("glossario_traducao") else ""     # termos só deste robô
    _traduz(textos_pt(R), arq_lg(R, lg), arq_cache(R, lg), lg, extra=extra)
    _traduz(docs_pt(R), arq_lg(R, lg, True), arq_cache(R, lg, True), lg, extra=extra)


def _carrega(pt, dest, cache, lg):
    """Tradução pronta de um dicionário PT; para se faltar texto ou se o português mudou depois da tradução."""
    d = ler(dest) if dest.exists() else {}
    marcas = ler(cache) if cache.exists() else {}
    falta = [k for k in pt if k not in d or marcas.get(k) != sha(pt[k])]
    if falta:
        raise SystemExit(f"{lg}: {len(falta)} textos sem tradução ou com o português alterado em {dest.name} (rode 'traduzir'): {falta[:5]}")
    return {k: PONTO(v) for k, v in d.items()} if lg == "en" else d


class Tx:
    """Textos de um idioma. t(chave) = texto manual; a(frase em PT) = a mesma frase no idioma; n(x) = número."""

    def __init__(self, R, lg, pagina=False):
        self.lg = lg
        self.pagina = pagina              # True só na página do guia: os docs e o zip continuam com o rótulo comum
        self.pt = textos_pt(R)
        self.d = self.pt if lg == "pt" else _carrega(self.pt, arq_lg(R, lg), arq_cache(R, lg), lg)

    def t(self, k):
        if self.pagina and "pag_" + k in self.d:
            return self.d["pag_" + k]
        return self.d[k]

    def a(self, s):
        if not s or self.lg == "pt":
            return s
        return self.d.get(chave_auto(s), PONTO(s) if self.lg == "en" else s)

    def n(self, x, casas=0):
        s = f"{x:.{casas}f}"
        return s if self.lg == "en" else s.replace(".", ",")


# ------------------------------------------------------------------ tabelas (uma definição, saída em HTML ou Markdown)
def L(texto, url):
    return ("link", texto, url)


def B(texto):
    return ("b", texto)


def faixa(f):
    return f"R$ {f[0]}–{f[1]}"


def rotulo(R, X, nome):
    """Nome exibido de uma peça: rótulo traduzido + nome do arquivo entre parênteses. Na página, a peça chamada "mesa"
    (a mesa da cabeça dos bichos) leva a palavra "peça", para não ser lida como mesa de impressão."""
    marca = f', {X.t("th_peca").lower()}' if X.pagina and nome.startswith("mesa-") else ""
    return f'{X.a(R.d["rotulos"][nome])}{marca} ({nome})'


def tabelas(R, X):
    """Devolve {nome: (cabeçalho, linhas)}; célula = texto, L(texto, url), B(texto) ou lista de pedaços."""
    t, a, n = X.t, X.a, X.n
    T = {}
    conf = lambda it: (a(it["conf"]) if it.get("conf") else t("nao_conferido"))
    nc = lambda it: ([" " + t("nc_rotulo") + " " + a(it["nc"]).rstrip(". ") + "."] if it.get("nc") else [])
    gr = lambda v: "<1" if v == 0 else n(v, 0)
    # --- compras, um bloco por tabela: o nome do item é o link de busca
    for i, bl in enumerate(R.d["compras"]):
        linhas = []
        for it in bl["itens"]:
            nome = [L(a(it["item"]), ML + it["ml"])] + ([" (" + t("ja_tem") + ")"] if it.get("tem") else [])
            linhas.append([nome, a(it["usa"]) + " / " + a(it["comprar"]), [a(it["para"])] + nc(it), faixa(it["faixa"]) + " (" + a(it["base"]) + ")", conf(it)])
        T[f"compras{i}"] = ([t("th_item"), t("th_usa"), t("th_para"), t("th_preco"), t("th_conf")], linhas)
    T["fase2"] = ([t("th_item"), t("th_qtd"), t("th_onde"), t("th_preco"), t("th_conf")],
                  [[L(a(it["item"]), ML + it["ml"]), a(it["qtd"]), [a(it["onde"])] + nc(it), faixa(it["faixa"]), conf(it)] for it in R.d["fase2"]])
    # --- peças
    linhas = []
    for p in R.mj["pecas"]:
        arq = R.caminho(p)
        linhas.append([rotulo(R, X, p["nome"]), L(Path(arq).name, RAW + arq), str(p["qtd"]), a(p["material"]) + " " + a(p["cor"]),
                       " × ".join(n(v, 0 if abs(v - round(v)) < 0.05 else 1) for v in p["dim"]),
                       a(p.get("orientacao", "")) or t("deitada"), a(p["suporte"]), str(p.get("perimetros", 3)), f'{p.get("infill", 15)} %',
                       gr(R.g[p["nome"]]), n(R.h[p["nome"]], 1)])
    linhas.append([t("total"), "", str(R.n_pecas()), "", "", "", "", "", "", n(R.gramas(), 0), n(R.horas(), 1)])
    T["pecas"] = ([t("th_peca"), t("th_arquivo"), t("th_qtd"), t("th_material"), t("th_dim"), t("th_orient"), t("th_suporte"), t("th_perim"), t("th_infill"), t("th_g"), t("th_h")], linhas)
    T["reforcos"] = ([t("th_peca"), t("th_reforco"), t("th_obs")], [[rotulo(R, X, p["nome"]), a(p.get("reforco", "")) or "—", a(p.get("obs", ""))] for p in R.mj["pecas"]])
    # --- mesas, na ordem sugerida de impressão
    mesa = {m["mesa"]: m for m in R.mesas}
    linhas = []
    for k, o in enumerate(R.d["ordem_impressao"], 1):
        m = mesa[o["mesa"]]
        g, h, itens = R.da_mesa(m)
        arq = f'{R.cfg["pecas"]}/{m["arquivo"]}'
        linhas.append([str(k), L(Path(arq).name, RAW + arq), a(m["material"]) + " " + a(m["cor"]),
                       ", ".join((rotulo(R, X, x) if q == 1 else f"{q} × {rotulo(R, X, x)}") for x, q in itens.items()),
                       gr(g), n(h, 1), a(o["porque"])])
    linhas.append([t("total"), "", "", "", n(sum(R.da_mesa(m)[0] for m in R.mesas), 0), n(sum(R.da_mesa(m)[1] for m in R.mesas), 1), ""])
    T["mesas"] = ([t("th_ordem"), t("th_mesa"), t("th_material"), t("th_pecas"), t("th_g"), t("th_h"), t("th_porque")], linhas)
    T["filamento"] = ([t("th_material"), t("th_g"), t("th_h")],
                      [[a(m) + " " + a(c), gr(g), n(h, 1)] for (m, c), (g, h) in R.por_cor()] + [[t("total"), n(R.gramas(), 0), n(R.horas(), 1)]])
    T["parafusos"] = ([t("th_onde"), t("th_qtd"), t("th_parafuso"), t("th_rosca")], [[a(p["onde"]), str(p["qtd"]), a(p["tipo"]), a(p["rosca"])] for p in R.d["parafusos"]])
    mont, abre = [], []
    for o in R.mj["ordem_montagem"]:
        for x in R.d["passos_extra"]:
            if x["antes"] == o["passo"]:
                mont.append([str(len(mont) + 1), a(x["passo"]), a(x["vem"]), a(x["nota"])])
        if o.get("sai"):
            abre.append([str(len(abre) + 1), a(o["passo"]), a(R.d["passos_nota"].get(o["passo"], ""))])
        else:
            # na montagem a peça vem de fora: por cima desce, por trás entra
            e = max(range(3), key=lambda i: abs(o["dir"][i]))                 # eixo dominante (há passos um pouco inclinados)
            como = t({(2, 1): "vem_cima", (2, -1): "vem_baixo", (1, -1): "vem_tras", (1, 1): "vem_frente",
                      (0, 1): "vem_direita", (0, -1): "vem_esquerda"}[(e, 1 if o["dir"][e] > 0 else -1)])
            mont.append([str(len(mont) + 1), a(o["passo"]), como, a(R.d["passos_nota"].get(o["passo"], ""))])
    T["passos"] = ([t("th_num"), t("th_passo"), t("th_vem"), t("th_nota")], mont)
    T["abrir"] = ([t("th_num"), t("th_passo"), t("th_nota")], abre)
    for i, g in enumerate(R.d["ligacoes"]):
        T[f"lig{i}"] = ([t("th_de"), t("th_para_fio"), t("th_cor"), t("th_fio"), t("th_atencao")],
                        [[a(w["de"]), a(w["para"]), a(w["cor"]), a(w["fio"]), a(w["nota"])] for w in g["fios"]])
    return T


def H(s):
    """Texto dos dados → HTML: escapa e troca `trecho` por <code>trecho</code>."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s, quote=False))


def cel_html(c):
    if isinstance(c, tuple):
        if c[0] == "b":
            return f"<b>{html.escape(c[1], quote=False)}</b>"
        return f'<a href="{html.escape(c[2])}" target="_blank" rel="noopener">{html.escape(c[1], quote=False)}</a>'
    if isinstance(c, list):
        return "".join(cel_html(x) for x in c)
    return H(c)


def cel_md(c):
    if isinstance(c, tuple):
        return f"**{c[1]}**" if c[0] == "b" else f"[{c[1]}]({c[2]})"
    if isinstance(c, list):
        return "".join(cel_md(x) for x in c)
    return c.replace("|", "\\|")


def dobra(titulo_html, miolo, n, X, classe=""):
    """Bloco recolhível: aberto no HTML (sem JavaScript nada some); o script da página fecha abaixo de 720 px."""
    return (f'<details class="dobra{classe}" open><summary>{titulo_html} <small>({n} {X.t("itens" if classe else "linhas")})</small></summary>\n{miolo}\n</details>')


def tab_html(cab, linhas, total=False, junta=False, estreita=False):
    """Tabela que vira cartões no celular (cada linha um cartão, cada célula com o nome da coluna).
    junta=True funde a 1ª coluna (número) na 2ª; estreita=True fica tabela mesmo no celular (poucas colunas curtas)."""
    if junta:
        cab = cab[1:]
        linhas = [[[B(l[0] + "."), " ", l[1]] if l[0].isdigit() else [B(l[0])]] + list(l[2:]) for l in linhas]
    cls = "estreita" if estreita else "cartoes"
    o = [f'<div class="tabela-wrap {cls}"><table class="tabela {cls}">', "<thead><tr>" + "".join(f"<th>{cel_html(c)}</th>" for c in cab) + "</tr></thead>", "<tbody>"]
    for i, l in enumerate(linhas):
        forte = total and i == len(linhas) - 1
        tds = []
        for j, c in enumerate(l):
            miolo = cel_html(c)
            curta = j > 0 and len(re.sub(r"<[^>]+>", "", miolo)) <= 24      # célula curta: no cartão do celular fica na mesma linha das vizinhas
            rot = "" if j == 0 else f' data-l="{html.escape(cab[j])}"' + (' class="c"' if curta else "")
            tds.append(f"<td{rot}>{'<strong>' + miolo + '</strong>' if forte and miolo else miolo}</td>")
        o.append("<tr>" + "".join(tds) + "</tr>")
    o.append("</tbody></table></div>")
    return "\n".join(o)


def tab_md(cab, linhas, total=False):
    o = ["| " + " | ".join(cel_md(c) for c in cab) + " |", "|" + "---|" * len(cab)]
    for i, l in enumerate(linhas):
        forte = total and i == len(linhas) - 1
        o.append("| " + " | ".join((f"**{cel_md(c)}**" if forte and c else cel_md(c)) for c in l) + " |")
    return "\n".join(o)


COM_TOTAL = {"pecas", "filamento", "mesas"}
DOBRA = {"pecas", "reforcos", "parafusos", "fase2"}          # tabelas longas: recolhidas no celular
JUNTA = {"passos", "abrir", "mesas"}
ESTREITA = {"filamento"}


def saida_verif(R):
    o = [f"== verificação: {R.mj['modelo']}"]
    for k, x in R.verif["testes"].items():
        o.append(f"  [{'PASSOU' if x['ok'] else 'FALHOU'}] {k}: {x['texto']}")
    return "\n".join(o)


def doc_url(R, nome, lg):
    arq = f"{nome}.md" if lg == "pt" else f"{nome}.{lg}.md"
    return BLOB + f'{R.cfg["docs"]}/{arq}', arq


# ------------------------------------------------------------------ esquema de ligação (SVG, um por idioma)
COR = {"v": "#d62828", "p": "#22232b", "a": "#e3a500", "g": "#2a9d4b", "z": "#1d6fd6", "l": "#e07a1f", "c": "#8a8f9c"}


def esquema_svg(X):
    """Desenho único das ligações do robô quadrado de mesa. As posições são fixas aqui; todo texto vem das chaves sv_*
    (traduzidas). Os fios seguem a lista 'ligacoes' do <robô>.dados.json: mudou um, mude o outro."""
    t = X.t
    e = lambda s: html.escape(s, quote=False)
    o = []

    def txt(x, y, s, tam=12, anc="start", peso=400, cor="#1a1a22", extra=""):
        o.append(f'<text x="{x}" y="{y}" font-size="{tam}" text-anchor="{anc}" font-weight="{peso}" fill="{cor}"{extra}>{e(s)}</text>')

    def caixa(x, y, w, h, fundo="#f4f5f8", borda="#3b3d4a", raio=8, traco=""):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raio}" fill="{fundo}" stroke="{borda}" stroke-width="1.5"{traco}/>')

    def fio(pts, cor, esp=3.2):
        p = " ".join(f"{x},{y}" for x, y in pts)
        o.append(f'<polyline points="{p}" fill="none" stroke="#fff" stroke-width="{esp + 3.6}" stroke-linejoin="round"/>')
        o.append(f'<polyline points="{p}" fill="none" stroke="{COR[cor]}" stroke-width="{esp}" stroke-linejoin="round" stroke-linecap="round"/>')

    def no(x, y, cor):
        o.append(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{COR[cor]}" stroke="#fff" stroke-width="1"/>')

    # ---- fundo, título, zonas
    o.append('<rect x="0" y="0" width="760" height="1086" fill="#ffffff"/>')
    txt(20, 28, t("sv_titulo"), 17, peso=700)
    txt(20, 47, t("sv_aviso"), 12, cor="#a14a00", peso=600)
    tr = ' stroke-dasharray="6 5"'
    caixa(10, 58, 740, 690, fundo="none", borda="#9aa0ad", raio=12, traco=tr)
    txt(22, 75, t("sv_base"), 11, cor="#6b7080", peso=700, extra=' letter-spacing="1.5"')
    o.append('<rect x="10" y="756" width="740" height="30" rx="6" fill="#e9ecf2"/>')
    caixa(10, 794, 740, 150, fundo="none", borda="#9aa0ad", raio=12, traco=tr)
    txt(62, 811, t("sv_cabeca"), 11, cor="#6b7080", peso=700, extra=' letter-spacing="1.5"')
    # ---- fios (antes das caixas: as pontas ficam por baixo da borda)
    fio([(214, 106), (236, 106)], "v")
    fio([(314, 106), (340, 106)], "v")                                   # suporte + → fusível → B+
    fio([(214, 174), (340, 174)], "p")                                   # suporte − → B−
    fio([(214, 140), (340, 140)], "a")                                   # ponto do meio → BM
    fio([(326, 140), (326, 82), (548, 82), (548, 140), (570, 140)], "a")  # BM → carregador (meio)
    fio([(500, 174), (570, 174)], "p")                                   # P− → carregador −
    fio([(500, 106), (570, 106)], "v")                                   # P+ → carregador +
    fio([(555, 174), (555, 300), (160, 300), (160, 330)], "p")           # P− → GND geral → LM2596 IN−
    fio([(520, 300), (520, 330)], "p")                                   # GND → UBEC IN−
    fio([(505, 106), (505, 222)], "v")                                   # P+ → chave
    fio([(505, 252), (505, 280), (110, 280), (110, 330)], "v")           # chave → LM2596 IN+
    fio([(430, 280), (430, 330)], "v")                                   # → UBEC IN+
    fio([(160, 406), (160, 470)], "p")                                   # LM2596 OUT− → shield G
    fio([(160, 448), (48, 448), (48, 904), (110, 904)], "p")             # OUT− → pescoço → adaptador USB-C −
    fio([(110, 406), (110, 470)], "v")                                   # LM2596 OUT+ → pino 5 V do shield
    fio([(110, 430), (34, 430), (34, 876), (110, 876)], "v")             # OUT+ → pescoço → adaptador USB-C +
    fio([(430, 406), (430, 470)], "v")                                   # UBEC + → borne VCC
    fio([(520, 406), (520, 470)], "p")                                   # UBEC − → borne GND
    fio([(430, 440), (442, 440)], "v", 2.4)
    fio([(508, 440), (520, 440)], "p", 2.4)                              # capacitor nos 6 V
    fio([(630, 500), (660, 500)], "l", 4.4)                              # D9 → servo de pan
    fio([(630, 580), (700, 580), (700, 850)], "l", 4.4)                  # D10 → pescoço → servo de tilt
    fio([(200, 620), (200, 840)], "g")                                   # D0 (RX) ← pino 32 (TX)
    fio([(300, 620), (300, 642)], "z")
    fio([(300, 664), (300, 840)], "z")                                   # D1 (TX) → 1 kΩ → pino 33 (RX)
    fio([(300, 692), (326, 692)], "p", 2.4)
    fio([(388, 692), (400, 692)], "p", 2.4)                              # divisor: nó → 2 × 1 kΩ → GND
    fio([(400, 620), (400, 840)], "p")                                   # G ↔ pino 34 (GND)
    fio([(530, 877), (540, 877)], "c", 9)                                # tela encaixada no Pi
    for x, y, c in ((326, 140, "a"), (505, 106, "v"), (555, 174, "p"), (520, 300, "p"), (430, 280, "v"),
                    (430, 440, "v"), (520, 440, "p"), (400, 692, "p")):
        no(x, y, c)
    # ---- faixa do pescoço (texto por cima dos fios)
    txt(545, 776, t("sv_pescoco"), 11, anc="middle", cor="#3b3d4a", peso=700)
    # ---- caixas
    caixa(24, 92, 190, 96)
    txt(34, 110, t("sv_suporte"), 12, peso=700)
    for y, k in ((120, "sv_cel1"), (152, "sv_cel2")):
        caixa(34, y, 92, 26, fundo="#dfe6f3", borda="#6b7896", raio=12)
        txt(80, y + 17, t(k), 11, anc="middle")
    txt(206, 110, "+", 14, anc="end", peso=700, cor=COR["v"])
    txt(206, 144, t("sv_meio"), 11, anc="end", cor="#8a6500", peso=700)
    txt(206, 179, "−", 14, anc="end", peso=700)
    caixa(236, 94, 78, 24, fundo="#fff4d6", borda="#a17400", raio=5)
    txt(275, 110, t("sv_fusivel"), 11, anc="middle", peso=600)
    caixa(340, 92, 160, 96)
    for y, a, b in ((110, "B+", "P+"), (144, "BM/B1", ""), (179, "B−", "P−/C−")):
        txt(347, y, a, 11, peso=700)
        txt(493, y, b, 11, anc="end", peso=700)
    txt(440, 129, t("sv_bms"), 12, anc="middle", peso=700)
    txt(440, 158, t("sv_bms2"), 11, anc="middle", cor="#4c4f5c")
    caixa(570, 92, 176, 96)
    for y, a, c in ((110, "B+", COR["v"]), (144, "BM", "#8a6500"), (179, "B−", "#1a1a22")):
        txt(577, y, a, 11, peso=700, cor=c)
    txt(672, 136, t("sv_carregador"), 12, anc="middle", peso=700)
    txt(672, 152, t("sv_carregador2"), 10.5, anc="middle", cor="#4c4f5c")
    caixa(460, 222, 90, 30, fundo="#e8eaf0")
    txt(505, 242, t("sv_chave"), 12, anc="middle", peso=700)
    txt(300, 273, t("sv_bat"), 11, anc="middle", cor=COR["v"], peso=600)
    caixa(60, 330, 240, 76)
    txt(110, 347, "IN+", 11, anc="middle", peso=700)
    txt(160, 347, "IN−", 11, anc="middle", peso=700)
    txt(110, 399, "OUT+", 11, anc="middle", peso=700)
    txt(160, 399, "OUT−", 11, anc="middle", peso=700)
    txt(240, 366, t("sv_lm"), 13, anc="middle", peso=700)
    txt(240, 383, t("sv_lm2"), 10.5, anc="middle", cor="#a14a00", peso=600)
    caixa(400, 330, 240, 76)
    txt(430, 347, "IN+", 11, anc="middle", peso=700)
    txt(520, 347, "IN−", 11, anc="middle", peso=700)
    txt(430, 399, "+", 13, anc="middle", peso=700, cor=COR["v"])
    txt(520, 399, "−", 13, anc="middle", peso=700)
    txt(585, 366, t("sv_ubec"), 13, anc="middle", peso=700)
    txt(585, 383, t("sv_ubec2"), 10.5, anc="middle", cor="#a14a00", peso=600)
    txt(102, 416, t("sv_51"), 11, anc="end", cor=COR["v"], peso=600)
    txt(424, 462, t("sv_6"), 11, anc="end", cor=COR["v"], peso=600)
    caixa(442, 429, 66, 22, fundo="#e6f1ff", borda="#3565a8", raio=5)
    txt(475, 444, t("sv_cap"), 10.5, anc="middle", peso=600)
    txt(475, 423, t("sv_capn"), 10.5, anc="middle", cor="#3565a8", peso=600)
    caixa(60, 470, 570, 150, fundo="#eef6ee", borda="#2f6b3a")
    txt(110, 488, t("sv_5v"), 11, anc="middle", peso=700)
    txt(166, 488, "− (COM)", 11, anc="middle", peso=700)
    txt(430, 488, "VCC", 11, anc="middle", peso=700)
    txt(520, 488, "GND", 11, anc="middle", peso=700)
    txt(475, 504, t("sv_borne"), 10.5, anc="middle", cor="#3565a8", peso=600)
    txt(345, 540, t("sv_shield"), 15, anc="middle", peso=700)
    txt(345, 560, t("sv_shield2"), 12, anc="middle", cor="#a14a00", peso=600)
    txt(622, 504, "D9", 11, anc="end", peso=700)
    txt(622, 584, "D10", 11, anc="end", peso=700)
    txt(200, 611, "D0 (RX)", 11, anc="middle", peso=700)
    txt(300, 611, "D1 (TX)", 11, anc="middle", peso=700)
    txt(400, 611, "G", 11, anc="middle", peso=700)
    caixa(279, 642, 42, 22, fundo="#fff", borda="#3b3d4a", raio=3)
    txt(300, 657, t("sv_r1"), 10.5, anc="middle", peso=600)
    caixa(288, 682, 24, 20, fundo="#fff4d6", borda="#a17400", raio=4)
    txt(282, 696, t("sv_b3"), 10.5, anc="end", cor="#6b4e00", peso=600)
    caixa(326, 681, 62, 22, fundo="#fff", borda="#3b3d4a", raio=3)
    txt(357, 696, t("sv_r2"), 10.5, anc="middle", peso=600)
    caixa(98, 421, 76, 36, fundo="#fff4d6", borda="#a17400", raio=4)
    txt(182, 443, t("sv_emenda"), 10.5, cor="#6b4e00", peso=600)
    caixa(660, 478, 90, 44, fundo="#fdebd9", borda="#a8581a")
    txt(705, 504, t("sv_pan"), 11, anc="middle", peso=700)
    txt(692, 700, t("sv_ext"), 11, anc="end", cor="#a8581a", peso=600)
    caixa(110, 840, 420, 80, fundo="#e9f6ea", borda="#2f6b3a")
    txt(200, 857, "32 (TX)", 11, anc="middle", peso=700)
    txt(300, 857, "33 (RX)", 11, anc="middle", peso=700)
    txt(400, 857, "34 (GND)", 11, anc="middle", peso=700)
    txt(118, 880, "+", 14, peso=700, cor=COR["v"])
    txt(118, 909, "−", 14, peso=700)
    txt(134, 894, t("sv_usbc"), 11, cor="#4c4f5c")
    txt(450, 898, t("sv_pi"), 14, anc="middle", peso=700)
    caixa(540, 852, 96, 50, fundo="#e8eaf0")
    txt(588, 881, t("sv_tela"), 10.5, anc="middle", peso=700)
    txt(632, 936, t("sv_tela2"), 10.5, anc="end", cor="#4c4f5c")
    caixa(642, 850, 106, 44, fundo="#fdebd9", borda="#a8581a")
    txt(695, 876, t("sv_tilt"), 10.5, anc="middle", peso=700)
    # ---- legenda
    for k, (x, y, cores, chave) in enumerate(((20, 966, "v", "sv_leg1"), (265, 966, "p", "sv_leg2"), (510, 966, "a", "sv_leg3"),
                                              (20, 988, "gz", "sv_leg4"), (265, 988, "l", "sv_leg5"), (510, 988, "", "sv_leg6"))):
        if not cores:
            o.append(f'<circle cx="{x + 12}" cy="{y - 4}" r="4.6" fill="#22232b"/>')
        for i, c in enumerate(cores):
            w = 24 / len(cores)
            o.append(f'<line x1="{x + i * w}" y1="{y - 4}" x2="{x + (i + 1) * w}" y2="{y - 4}" stroke="{COR[c]}" stroke-width="4"/>')
        txt(x + 32, y, t(chave), 11.5)
    txt(20, 1012, t("sv_leg7"), 11.5, peso=600)
    txt(20, 1032, t("sv_leg8"), 11.5, peso=600)
    txt(20, 1052, t("sv_leg9") + " " + t("sv_leg10"), 11.5, peso=600) if len(t("sv_leg9") + t("sv_leg10")) < 118 else (txt(20, 1052, t("sv_leg9"), 11.5, peso=600), txt(20, 1072, t("sv_leg10"), 11.5, peso=600))
    corpo = "\n".join(o)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 1086" width="760" height="1086" '
            f'font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif" role="img"><title>{e(t("sv_titulo"))}</title>\n{corpo}\n</svg>\n')


def esquema(R, lg, no_guia=True):
    X = Tx(R, lg)
    svg = __import__(R.cfg["esquema"]).svg(X, R) if R.cfg.get("esquema") else esquema_svg(X)
    for d in [R.docs] + ([GUIA / R.nome / "assets"] if no_guia else []):
        d.mkdir(parents=True, exist_ok=True)
        (d / f"ligacao.{lg}.svg").write_text(svg)
    print(f'{R.cfg["docs"]}/ligacao.{lg}.svg', len(svg))


# ------------------------------------------------------------------ página
CSS = """
.fase{margin:-.5em 0 1.5em;padding:.7em .95em;border-left:3px solid var(--amb);background:var(--bg2);border-radius:0 10px 10px 0;font-size:.98rem;max-width:46ch}
.fatos{font-family:Sora;font-weight:600;font-size:.95rem;color:var(--amb);margin:-.7em 0 1.5em}
.aviso{border-color:var(--amb);margin-top:22px}
.aviso ul{margin:.6em 0 0 1.1em;padding:0;color:var(--mut);font-size:.92rem}
.aviso li{margin:.45em 0}
.aviso li strong{color:var(--txt)}
.glossario{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:22px 0 0}
.glossario div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;min-width:0}
.glossario dt{font-family:Sora;font-weight:700;color:var(--amb)}
.glossario dd{margin:.3em 0 0;color:var(--mut);font-size:.92rem}
.esquema{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px;margin:18px 0 0;max-width:820px}
.esquema img{display:block;width:100%;height:auto}
.sep4{font-family:Sora;font-size:1rem;margin:26px 0 0;color:var(--txt)}
.dobra{margin:26px 0 0}
.dobra summary{cursor:pointer;font-family:Sora;font-size:.9rem;color:var(--mut);padding:.5em 0;list-style-position:outside}
.dobra summary h3,.dobra summary h4{display:inline;font-family:Sora;color:var(--txt);margin:0 .3em 0 .2em}
.dobra summary h3{font-size:1.17rem}.dobra summary h4{font-size:1rem}
.dobra summary small{font-weight:400;color:var(--mut)}
.dobra .tabela-wrap{margin-top:8px}
.step ol{margin:.2em 0 .8em 1.25em;padding:0;color:var(--mut)}
.step ol li{margin:.45em 0}
.topo{position:fixed;right:14px;bottom:14px;width:40px;height:40px;border-radius:50%;background:var(--amb);color:#1a1206;opacity:.88;font:800 1.2rem/40px Sora,sans-serif;text-align:center;box-shadow:0 4px 14px rgba(0,0,0,.35);z-index:50}
.tabela.estreita{min-width:0}
.step .solda{margin:12px 0 16px}
.solda h4{font-family:Sora;font-size:1rem;margin:0;color:var(--txt)}
.solda .mini{margin-top:.8em}
.oq{font-size:.82em;white-space:nowrap;text-decoration:underline}
.testes{margin:.6em 0 0 1.1em;padding:0;color:var(--mut);font-size:.9rem}
.testes li{margin:.4em 0}.testes strong{color:var(--txt)}
.testes b.ok{color:var(--amb);font-weight:600;white-space:nowrap}.testes b.nao{color:#e0262c;white-space:nowrap}
.tabela td b{font-family:Sora}
.step p a,.nota a,.mini a{text-decoration:underline}
.bal{min-width:0}.bal img{margin-bottom:10px;background:#999}
.bal h4{font-family:Sora;font-size:1rem;margin:0}
.bal ul{margin:.5em 0 0 1.1em;padding:0;color:var(--mut);font-size:.88rem}.bal li{margin:.3em 0}
.legenda .cor{display:inline-block;width:.85em;height:.85em;border-radius:3px;margin:0 .35em 0 .9em;vertical-align:-1px;border:1px solid var(--line)}
@media(max-width:720px){
  .glossario{grid-template-columns:1fr}
  .tabela-wrap.cartoes{border:0;overflow:visible}
  .tabela.cartoes{min-width:0;display:block}
  .tabela.cartoes thead{display:none}
  .tabela.cartoes tbody{display:block}
  .tabela.cartoes tr{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 10px}
  .tabela.cartoes td{display:block;border:0;padding:4px 0;overflow-wrap:anywhere}
  .tabela.cartoes td.c{display:inline-block;margin-right:18px}
  .tabela.cartoes td:empty{display:none}
  .tabela.cartoes td[data-l]::before{content:attr(data-l) ": ";font-family:Sora;font-size:.7rem;font-weight:600;color:var(--mut);text-transform:uppercase;letter-spacing:.05em}
  .tabela.cartoes td:first-child{font-weight:600;font-size:1rem;padding-bottom:6px}
}
"""


def preparos_html(R, X):
    """Os preparos da bancada: mesma lista numerada do LIGACAO.md (R.d["preparos"]); a frase de abertura (prepN_p) e a
    nota do fim (prepN_b) são textos da página."""
    o = []
    assert R.d["preparos"][0]["titulo"].startswith("Solde"), "o quadro 'Nunca soldou?' entra no preparo 1, que tem de ser o da solda"
    solda = (f'<div class="card aviso solda"><h4>🔰 {X.t("solda_t")}</h4><ul>{X.t("solda_li")}</ul>'
             f'<p class="mini">{X.t("solda_link_p")} <a href="{SOLDA_URL}" target="_blank" rel="noopener">{X.t("solda_link_txt")}</a> {X.t("solda_fonte")}</p></div>')
    for n, pr in enumerate(R.d["preparos"], 1):
        intro, fim = X.d.get(f"prep{n}_p"), X.d.get(f"prep{n}_b")
        o.append(f'<div class="step" id="preparo{n}"><div class="b">{n}</div><div><h3>{H(X.a(pr["titulo"]))}</h3>'
                 + (f"<p>{intro}</p>" if intro else "") + (solda if n == 1 else "") + "<ol>" + "".join(f"<li>{H(X.a(x))}</li>" for x in pr["passos"]) + "</ol>"
                 + (f'<p class="mini">{fim}</p>' if fim else "") + "</div></div>")
    return "\n".join(o)


def balancos_html(R, X, A):
    """Mapa de balanços: legenda + um cartão por peça (imagem de 3 vistas, veredito e números do teste 10)."""
    if not R.bal:
        return ""
    t, a, n = X.t, X.a, X.n
    esc = lambda s: html.escape(s, quote=False)
    vistas = "; ".join(f"{i}) {esc(a(v))}" for i, v in enumerate(R.bal["vistas"], 1))
    cores = "".join(f'<span class="cor" style="background:{BAL_COR[k]}"></span>{esc(a(v))}' for k, v in R.bal["cores"].items())
    o = []
    for p in R.bal["pecas"]:
        nome = esc(rotulo(R, X, p["peca"]))
        img = f'{A}balancos/{p["imagem"]}'
        ponte = f'{n(p["maior_ponte_mm"], 1)} mm' if p["maior_ponte_mm"] >= 0.05 else "—"
        o.append(f'<div class="card bal"><a href="{img}" target="_blank" rel="noopener"><img class="shot" loading="lazy" src="{img}" alt="{html.escape(t("bal_alt"))} {html.escape(rotulo(R, X, p["peca"]))}"></a>'
                 f'<h4>{nome}</h4><p class="mini"><strong>{esc(a(p["veredito"]))}</strong></p><ul>'
                 f'<li>{esc(t("th_orient"))}: {H(a(p["orientacao"]))}</li>'
                 f'<li>{esc(t("th_suporte"))}: {H(a(p["suporte"]))}</li>'
                 f'<li>{esc(t("bal_area"))}: {n(p["sem_apoio_mm2"], 0)} mm² ({n(p["sem_apoio_pct"], 1)} % {esc(t("bal_da_peca"))}). {esc(t("bal_limite"))}: {n(p["limite_mm2"], 0)} mm²</li>'
                 f'<li>{esc(t("bal_ponte"))}: {ponte}</li></ul></div>')
    miolo = (f'<p class="mini">{esc(t("bal_vistas"))} {vistas}.</p>\n<p class="mini legenda">{esc(t("bal_cores"))}{cores}</p>\n'
             f'<div class="grid g2 balancos">\n' + "\n".join(o) + "\n</div>")
    return dobra(f'<h4>{esc(t("bal_dobra"))}</h4>', miolo, len(o), X, " titulo")


def tem_evolucao(R):
    """A página /guia/evolucao/ mostra este robô? (lista em guia/evolucao/assets/dados.json, de comum/cad/evolucao.py)"""
    f = GUIA / "evolucao" / "assets" / "dados.json"
    return f.exists() and R.cfg["id"] in ler(f)["bichos"]


def semelhanca_html(R, X):
    """Números de semelhança com o desenho de referência (só números: as imagens de referência ficam na página de evolução)."""
    t, n = X.t, X.n
    esc = lambda s: html.escape(s, quote=False)
    m = SEM.medida(R.cfg["id"])
    f = lambda v: "—" if v is None else n(v, 3)
    cols = ["antes", "depois"] + (["teto"] if m["teto"] is not None else [])
    cols = [c for c in cols if m[c] is not None]
    cab = [t("sem_th_vista")] + [t("sem_th_" + c) for c in cols]
    linhas = [[t("vista_" + v["vista"].replace("-", "_"))] + [f(v[c]) for c in cols] for v in m["vistas"]]
    total = len(linhas) > 1
    if total:
        linhas.append([t("sem_media")] + [f(m[c]) for c in cols])
    o = [tab_html(cab, linhas, total=total, estreita=True)]
    if m["novo"]:
        o.append(f'<p class="nota">{esc(t("sem_novo"))}</p>')
    else:
        como = t("sem_alvo_malha") if m["teto"] is not None else t("sem_alvo_fixo")
        o.append(f'<p class="nota">{esc(t("sem_alvo"))} <strong>{f(m["alvo"])}</strong> ({esc(como)}). <strong>{esc(t("sem_ok" if m["atingiu"] else "sem_nao"))}</strong>.'
                 + (f' {esc(t("sem_teto_p"))}' if m["teto"] is not None else "") + (f' {X.d["sem_extra"]}' if X.d.get("sem_extra") else "") + "</p>")
    if tem_evolucao(R):
        o.append(f'<p class="nota">{esc(t("sem_evo"))} <a href="../evolucao/#{R.cfg["id"]}">{esc(t("sem_evo_link"))}</a>.</p>')
    o.append(f'<p class="nota">{esc(t("sem_md"))} <a href="{BLOB}comparacao/semelhanca.md" target="_blank" rel="noopener">comparacao/semelhanca.md</a> {esc(t("sem_md_pt"))}</p>')
    return "\n".join(o)


def slug(s):
    import unicodedata
    return re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip("-")


def resumo_testes(R, X):
    """Uma linha por teste do verificador, no idioma da página (a saída do programa é sempre em português)."""
    testes = list(R.verif["testes"].items())
    assert f"vt_{len(testes)}" in X.d and f"vt_{len(testes) + 1}" not in X.d, "os resumos vt_N de _comum.pt.json não batem com o verificador"
    o = []
    for i, (k, x) in enumerate(testes, 1):
        assert k.split()[0] == str(i), f"teste fora de ordem: {k}"
        o.append(f'<li><strong>{i}. {X.t(f"vt_{i}")}:</strong> {X.t(f"vt_{i}_p")} <b class="{"ok" if x["ok"] else "nao"}">{"✓" if x["ok"] else "✗"} {X.t("ver_passou" if x["ok"] else "ver_falhou")}</b></li>')
    return "".join(o)


def liga_glossario(secao, R, X):
    """Na seção dada, a 1ª vez que aparece cada termo de GLO_LINK que está no glossário ganha um link "o que é isso?".
    Se o termo está dentro de um link (o nome do item, que abre a busca), o link do glossário vem logo depois dele."""
    termos = [g["termo"] for g in R.d["glossario"] if g["termo"] in GLO_LINK]
    partes = re.split(r"(<[^>]+>)", secao)
    for termo in termos:
        link = f' <a class="oq" href="#glo-{slug(termo)}">({X.t("oq")})</a>'
        dentro = 0
        for i, x in enumerate(partes):
            if x.startswith("<"):
                dentro += x.startswith("<a ") - x.startswith("</a")
                continue
            mo = re.search(r"(?<![\w-])" + re.escape(termo) + r"(?!\w)", x)
            if not mo:
                continue
            if dentro:                                            # dentro de um <a>: depois do </a> que o fecha
                j = next(k for k in range(i + 1, len(partes)) if partes[k].startswith("</a"))
                partes[j] += link
            else:
                partes[i] = x[:mo.end()] + link + x[mo.end():]
            break
    return "".join(partes)


def pagina(R, lg):
    X = Tx(R, lg, pagina=True)
    head, script = montar.cabeca_rodape()
    corpo = (AQUI / "robo.html").read_text()
    T = tabelas(R, X)
    esc = lambda s: html.escape(s, quote=False)
    sub = f"{R.nome}/" if lg == "pt" else f"{lg}/{R.nome}/"
    fundo = "../" if lg == "pt" else "../../"                      # da página até guia/
    A = "assets/" if lg == "pt" else f"../../{R.nome}/assets/"     # imagens do robô ficam em guia/<robô>/assets/
    lang = "".join(f'<a{" class=\"on\"" if k == lg else ""} href="{"./" if k == lg else fundo + ("" if k == "pt" else k + "/") + R.nome + "/"}">{k.upper()}</a>' for k in IDIOMAS)
    C = R.custo()
    rs = lambda k: f"R$ {C[k][0]}–{C[k][1]}"
    fixos = {"LANG": f'<span class="lang">{lang}</span>', "LG": lg, "LEIA": LEIA[lg], "A": A, "GA": fundo + "assets/", "G": "../", "RAW": RAW, "BLOB": BLOB, "TREE": TREE, "REPO": REPO,
             "EMOJI": R.cfg["emoji"], "ID": R.cfg["id"], "PECAS": R.cfg["pecas"], "DOCS": R.cfg["docs"], "ZIP": RAW + f'{R.cfg["docs"]}/{R.nome}-stl.zip',
             "N_ALTURA": X.n(R.altura() / 10, 0), "N_PECAS": str(R.n_pecas()), "N_DISTINTAS": str(len(R.mj["pecas"])), "N_MESAS": str(len(R.mesas)),
             "N_HORAS": X.n(R.horas(), 0), "N_GRAMAS": X.n(R.gramas(), 0), "N_INSERTOS": str(R.d["insertos"]), "N_TESTES": str(len(R.verif["testes"])),
             "CUSTO": rs("pecas"), "CUSTO_TEM": rs("tem"), "CUSTO_ZERO": rs("zero"), "CUSTO_FIL": rs("fil"), "CUSTO_FERR": rs("ferr"),
             "PRECO_DATA": R.d["preco_data"], "PRECO_FONTE": R.d["preco_fonte"],
             "SAIDA_VERIF": html.escape(saida_verif(R), quote=False), "VER_RESUMO": resumo_testes(R, X),
             "COMPRAS": "\n".join(dobra(f'<h3>{esc(X.a(bl["bloco"]))}</h3>', tab_html(*T[f"compras{i}"]), len(bl["itens"]), X, " titulo") for i, bl in enumerate(R.d["compras"])),
             "LIGACOES": "\n".join(dobra(f'<h4>{esc(X.a(g["grupo"]))}</h4>', tab_html(*T[f"lig{i}"]), len(g["fios"]), X, " titulo") for i, g in enumerate(R.d["ligacoes"])),
             "RISCOS": "".join(f"<li>{H(X.a(r))}</li>" for r in R.d["riscos"]),
             "PREPAROS": preparos_html(R, X), "N_PREPAROS": str(len(R.d["preparos"])),
             "BALANCOS": balancos_html(R, X, A), "SEMELHANCA": semelhanca_html(R, X),
             "GLOSSARIO": "".join(f'<div id="glo-{slug(g["termo"])}"><dt>{esc(X.a(g["termo"]))}</dt><dd>{esc(X.a(g["def"]))}</dd></div>' for g in R.d["glossario"])}
    for nome in DOCS_LG:
        k = "DOC_" + nome.split("-")[0]
        fixos[k], fixos[k + "_NOME"] = doc_url(R, nome, lg)
    for k, v in T.items():
        if not k.startswith(("compras", "lig")):
            h = tab_html(*v, total=k in COM_TOTAL, junta=k in JUNTA, estreita=k in ESTREITA)
            fixos["TAB_" + k.upper()] = dobra(esc(X.t("dobra_tabela")), h, len(v[1]) - (k in COM_TOTAL), X) if k in DOBRA else h
    faltam = set()

    def troca(mo):
        k = mo.group(1)
        if k in fixos:
            return fixos[k]
        if k not in X.d:
            faltam.add(k)
            return mo.group(0)
        return X.d[k]

    for _ in range(2):                          # 2 passadas: texto pode conter [[N_...]]
        corpo = re.sub(r"\[\[([A-Za-z0-9_]+)\]\]", troca, corpo)
    assert not faltam, f"{lg}: textos faltando {sorted(faltam)}"
    # glossário à mão: "o que é isso?" na 1ª vez que UBEC, BMS e 2S/3S aparecem no quadro de riscos ou na lista de compras
    i = corpo.index('<section id="comprar">')
    j = corpo.index("</section>", i)
    corpo = corpo[:i] + liga_glossario(corpo[i:j], R, X) + corpo[j:]
    if lg == "pt":      # "mesa" tem 3 sentidos no português (o móvel, a da impressora e a peça): a numerada é a de impressão
        fora_de_tag = r"(?![^<]*>)"
        corpo = re.sub(r"\b([Mm])esa (\d\d)\b" + fora_de_tag, r"\1esa de impressão \2", corpo)
        corpo = re.sub(r"\b(\d+) mesas\b" + fora_de_tag, r"\1 mesas de impressão", corpo)
    head = head.replace("{{PROJETO}} — {{TAGLINE}}", X.t("titulo")).replace("{{META_DESCRICAO}}", html.escape(X.t("meta"))).replace("{{SLUG}}", "robos-impressos")
    for k in ("en/", "es/", ""):                # hreflang desta página, não o da entrada do guia
        head = head.replace(f'/guia/{k}">', f'/guia/{k}{R.nome}/">')
    head = head.replace('<html lang="pt-BR">', {"pt": '<html lang="pt-BR">', "en": '<html lang="en">', "es": '<html lang="es">'}[lg])
    assert head.count("</style>") >= 1, "template sem </style>"
    i = head.rindex("</style>")
    head = head[:i] + CSS + head[i:]
    script = script.replace("{{SLUG}}", "robos-impressos")
    pag = head + "\n\n" + corpo + "\n" + script
    assert "{{" not in pag.replace("${{", ""), "placeholder do template sobrando"
    destino = GUIA / sub / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pag)
    print(destino.relative_to(RAIZ), len(pag))
    return destino


INTERNAS = (r"\bNei\b", r"\brodada\b", r"lista antiga", r"\bE[1-6][a-d]?\b(?! ?=)", r"orquestrador")


def conferir(R):
    """Sem servidor: todo src/href relativo existe em disco; mesmas tags nos 3 idiomas; nada de [[ ]] sobrando; inglês sem
    vírgula decimal; nenhuma nota interna em texto público; docs EN/ES e zip no lugar."""
    ok = True

    def falha(msg):
        nonlocal ok
        ok = False
        print("  " + msg)

    conta = {}
    tem_pagina = all((GUIA / (f"{R.nome}/index.html" if lg == "pt" else f"{lg}/{R.nome}/index.html")).exists() for lg in IDIOMAS)
    if not tem_pagina:
        print("  (página do guia ainda não gerada para este robô: conferindo só os docs e o zip)")
    for lg in (IDIOMAS if tem_pagina else ()):
        f = GUIA / (f"{R.nome}/index.html" if lg == "pt" else f"{lg}/{R.nome}/index.html")
        h = f.read_text()
        for u in re.findall(r'(?:src|href)="([^"#]+)(?:#[^"]*)?"', h):
            if re.match(r"(https?:|mailto:|data:)", u):
                continue
            alvo = (f.parent / u)
            alvo = alvo / "index.html" if u.endswith("/") else alvo
            if not alvo.exists():
                falha(f"{lg}: link quebrado {u}")
        for u in sorted(set(re.findall(re.escape(RAW) + r'([^"]+)', h)) | set(re.findall(re.escape(BLOB) + r'([^"#]+)', h))):
            if not (RAIZ / u).exists():
                falha(f"{lg}: arquivo do link do GitHub não existe no repo: {u}")
        for ancora in set(re.findall(r'href="#([^"]+)"', h)):
            if f'id="{ancora}"' not in h:
                falha(f"{lg}: âncora #{ancora} sem destino")
        if "[[" in h or "{{" in h.replace("${{", ""):
            falha(f"{lg}: [[ ]] ou {{{{ }}}} sobrando")
        conta[lg] = {tg: len(re.findall(f"<{tg}[ >]", h)) for tg in ("section", "div", "tr", "td", "li", "img", "a", "h2", "h3", "h4", "dt")}
        assert f'/guia/{"" if lg == "pt" else lg + "/"}{R.nome}/"' in h, "hreflang da própria página"
        visivel = re.sub(r"<pre.*?</pre>|<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h[h.index("<body"):], flags=re.S)
        if lg == "en":
            for m in sorted(set(re.findall(r"\S*\d,\d\S*", visivel))):
                falha(f"en: vírgula decimal ou milhar em '{m}'")
        for pad in INTERNAS:
            for m in sorted(set(re.findall(pad, visivel))):
                falha(f"{lg}: nota interna na página: '{m}'")
    for lg in (("en", "es") if tem_pagina else ()):
        if conta[lg] != conta["pt"]:
            falha(f"{lg}: contagem de tags diferente do PT: {conta[lg]} x {conta['pt']}")
    # docs: versões por idioma, blocos preenchidos, sem nota interna
    for nome in DOCS_LG:
        for lg in IDIOMAS:
            f = R.docs / doc_url(R, nome, lg)[1]
            if not f.exists():
                falha(f"falta {f.relative_to(RAIZ)}")
                continue
            s = f.read_text()
            if re.search(r"<!-- GERADO:[a-z0-9_]+ -->\n<!-- /GERADO -->", s):
                falha(f"{f.name}: bloco GERADO vazio")
            for pad in INTERNAS:
                for m in sorted(set(re.findall(pad, s))):
                    falha(f"{f.name}: nota interna '{m}'")
            if lg == "en":
                sem_url = re.sub(r"\]\([^)]*\)|`[^`]*`", " ", s)
                for m in sorted(set(re.findall(r"\S*\d,\d\S*", sem_url))):
                    falha(f"{f.name}: vírgula decimal em '{m}'")
            for u in re.findall(r"\]\((?!https?:)([^)#]+)\)", s):
                if not (f.parent / u).exists():
                    falha(f"{f.name}: link relativo quebrado {u}")
    z = R.docs / f"{R.nome}-stl.zip"
    nomes = set(zipfile.ZipFile(z).namelist())
    for n in list(LEIA.values()) + [f"stl/{Path(R.caminho(p)).name}" for p in R.mj["pecas"]] + [str(f.relative_to(R.docs)) for f in sorted((R.docs / "firmware").rglob("*.ino"))]:
        if f"{R.nome}/{n}" not in nomes:
            falha(f"zip sem {n}")
    for n in sorted(nomes):                                  # todo link relativo de um .md do zip existe no zip
        if n.endswith(".md"):
            for u in re.findall(r"\]\((?!https?:)([^)#]+)\)", zipfile.ZipFile(z).read(n).decode()):
                if f"{R.nome}/{u}" not in nomes:
                    falha(f"zip/{n}: link relativo quebrado {u}")
    for lg in IDIOMAS:
        arq = doc_url(R, "IMPRIMIR", lg)[1]
        corpo = zipfile.ZipFile(z).read(f"{R.nome}/{arq}").decode() if f"{R.nome}/{arq}" in nomes else ""
        if not corpo or f'{R.cfg["pecas"]}/stl/' in re.sub(r"https?://[^\s)]+", "", corpo.split("\n\n", 3)[-1]):
            falha(f"zip/{arq}: falta ou ainda manda abrir {R.cfg['pecas']}/stl/")
    print("conferir:", "OK" if ok else "FALHOU", conta.get("pt", "(sem página)"))
    return ok


# ------------------------------------------------------------------ docs do robô (blocos gerados, versões EN/ES) e zip
def blocos(R, X):
    T = tabelas(R, X)
    t, a = X.t, X.a
    C = R.custo()
    rs = lambda k: f"R$ {C[k][0]}–{C[k][1]}"
    Bk = {k: tab_md(*v, total=k in COM_TOTAL) for k, v in T.items() if not k.startswith(("compras", "lig"))}
    Bk["compras"] = "\n\n".join(f'### {a(bl["bloco"])}\n\n' + tab_md(*T[f"compras{i}"]) for i, bl in enumerate(R.d["compras"]))
    Bk["ligacoes"] = "\n\n".join(f'### {a(g["grupo"])}\n\n' + tab_md(*T[f"lig{i}"]) for i, g in enumerate(R.d["ligacoes"]))
    Bk["glossario"] = "\n".join(f'- **{a(g["termo"])}:** {a(g["def"])}' for g in R.d["glossario"])
    Bk["riscos"] = "\n".join(f"- {a(r)}" for r in R.d["riscos"])
    for n, pr in enumerate(R.d["preparos"], 1):
        Bk[f"prep{n}"] = "\n".join(f"{i}. {a(x)}" for i, x in enumerate(pr["passos"], 1))
    Bk["custo"] = (f"- {t('doc_custo_1')} **{rs('pecas')}**.\n- {t('doc_custo_2')} **{rs('zero')}**.\n- {t('doc_custo_3')} {rs('fil')}.\n"
                   f"- {t('doc_custo_4')} {rs('tem')}.\n- {t('doc_custo_5')} {rs('ferr')}.")
    Bk["verificacao"] = "```\n" + saida_verif(R) + "\n```"
    Bk["numeros"] = (f"- Altura montado: {X.n(R.altura(), 1)} mm.\n- Peças impressas: {R.n_pecas()} ({len(R.mj['pecas'])} arquivos diferentes), em {len(R.mesas)} mesas.\n"
                     f"- Filamento: {X.n(R.gramas(), 0)} g. Tempo de impressão: {X.n(R.horas(), 1)} h. As duas contas são estimativas por volume, sem fatiador.\n"
                     f"- Insertos M3 a quente: {R.d['insertos']}.")
    return Bk


def idiomas_md(R, nome):
    return " · ".join(f"[{BANDEIRA[lg]}]({doc_url(R, nome, lg)[1]})" for lg in IDIOMAS)


def preenche(s, Bk, arq):
    usados = []

    def troca(mo):
        usados.append(mo.group(1))
        assert mo.group(1) in Bk, f"{arq}: bloco GERADO desconhecido '{mo.group(1)}'"
        return f"<!-- GERADO:{mo.group(1)} -->\n{Bk[mo.group(1)]}\n<!-- /GERADO -->"

    return re.sub(r"<!-- GERADO:([a-z0-9_]+) -->.*?<!-- /GERADO -->", troca, s, flags=re.S), usados


def doc_lg(R, nome, lg, Bk, trad):
    """Versão EN/ES de um doc: prosa traduzida parágrafo a parágrafo, blocos GERADO refeitos no idioma, links trocados."""
    o = []
    for tipo, x in partes_md((R.docs / f"{nome}.md").read_text()):
        if tipo == "ger":
            o.append(f"<!-- GERADO:{x} -->\n{Bk[x]}\n<!-- /GERADO -->")
        elif tipo == "txt":
            p = trad["d_" + sha(x.strip(), 10)]
            p = re.sub(r"\b(" + "|".join(DOCS_LG) + r")\.md\b", rf"\1.{lg}.md", p)
            p = p.replace(f"/guia/{R.nome}/", f"/guia/{lg}/{R.nome}/").replace("ligacao.pt.svg", f"ligacao.{lg}.svg")
            o.append(x.replace(x.strip(), p))
        else:
            o.append(x)
    return "".join(o)


def docs(R, lgs=IDIOMAS):
    if "pt" in lgs:
        Bk = blocos(R, Tx(R, "pt"))
        for f in sorted(R.docs.glob("*.md")):
            if re.search(r"\.(en|es)\.md$", f.name):
                continue
            s = f.read_text()
            n, usados = preenche(s, dict(Bk, idiomas=idiomas_md(R, f.stem)), f.name)
            if n != s:
                f.write_text(n)
            print(f.relative_to(RAIZ), "blocos:", ", ".join(usados) or "nenhum")
    for lg in lgs:
        if lg == "pt":
            continue
        Bk = blocos(R, Tx(R, lg))
        trad = _carrega(docs_pt(R), arq_lg(R, lg, True), arq_cache(R, lg, True), lg)
        for nome in DOCS_LG:
            f = R.docs / f"{nome}.{lg}.md"
            f.write_text(doc_lg(R, nome, lg, dict(Bk, idiomas=idiomas_md(R, nome)), trad))
            print(f.relative_to(RAIZ))


def leia_zip(R, lg):
    """LEIA-ME curto do zip: o que tem em cada pasta e a ordem dos guias (que têm o mesmo nome dos do repositório)."""
    X = Tx(R, lg)
    nome = lambda n: doc_url(R, n, lg)[1]
    site = SITE + ("" if lg == "pt" else lg + "/") + R.nome + "/"
    return (f"{X.t('zip_1')}\n\n{X.t('zip_2')}\n\n{X.t('zip_3')}\n\n"
            f"1. [{nome('IMPRIMIR')}]({nome('IMPRIMIR')}): {X.t('zip_g1')}\n2. [{nome('LISTA-DE-COMPRAS')}]({nome('LISTA-DE-COMPRAS')}): {X.t('zip_g2')}\n"
            f"3. [{nome('LIGACAO')}]({nome('LIGACAO')}): {X.t('zip_g3')}\n\n{X.t('zip_4')} {site}\n")


def imprimir_zip(R, lg):
    """O guia de impressão como ele vale DENTRO do zip: mesmos textos do IMPRIMIR, com os caminhos do zip."""
    X = Tx(R, lg)
    s = (R.docs / doc_url(R, "IMPRIMIR", lg)[1]).read_text()
    s = re.sub(r"<!-- GERADO:idiomas -->.*?<!-- /GERADO -->\n*", "", s, flags=re.S)
    pecas = R.cfg["pecas"]
    cupom = CUPOM
    urls = []                                                               # links do GitHub ficam como estão

    def guarda(mo):
        urls.append(mo.group(0))
        return f"\0{len(urls) - 1}\0"

    s = re.sub(r"https?://[^\s)]+", guarda, s)
    s = s.replace(cupom, "stl/comum-teste-encaixe.stl").replace(f"{pecas}/stl/", "stl/").replace(f"{pecas}/mesas/", "mesas/")
    s = re.sub(r"\0(\d+)\0", lambda mo: urls[int(mo.group(1))], s)
    i = s.index("\n", s.index("# ")) + 1                                    # logo depois do título
    return s[:i] + f"\n{X.t('zip_5')} `{pecas}/stl/`, `{pecas}/mesas/`, `{cupom}`.\n" + s[i:]


def zipar(R):
    """Zip estável (ordem e datas fixas): STL de cada peça + 3MF de cada mesa + sketch + guias nos 3 idiomas."""
    dest = R.docs / f"{R.nome}-stl.zip"
    itens = []
    for p in R.mj["pecas"]:
        arq = RAIZ / R.caminho(p)
        itens.append((f"stl/{arq.name}", arq.read_bytes()))
    for m in R.mesas:
        arq = R.pasta / m["arquivo"]
        itens.append((f"mesas/{arq.name}", arq.read_bytes()))
    for f in sorted((R.docs / "firmware").rglob("*.ino")):
        itens.append((str(f.relative_to(R.docs)), f.read_bytes()))
    for lg in IDIOMAS:
        itens.append((LEIA[lg], leia_zip(R, lg).encode()))
        itens.append((doc_url(R, "IMPRIMIR", lg)[1], imprimir_zip(R, lg).encode()))
        for nome in ("LISTA-DE-COMPRAS", "LIGACAO"):
            f = R.docs / doc_url(R, nome, lg)[1]
            itens.append((f.name, f.read_bytes()))
        itens.append((f"ligacao.{lg}.svg", (R.docs / f"ligacao.{lg}.svg").read_bytes()))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for nome, dados in sorted(itens):
            zi = zipfile.ZipInfo(f"{R.nome}/{nome}", date_time=(2026, 11, 14, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, dados)
    dest.write_bytes(buf.getvalue())
    print(dest.relative_to(RAIZ), f"{dest.stat().st_size / 1e6:.2f} MB", len(itens), "arquivos")


def imagens(R):
    """Cópias dos renders DESTE robô em guia/<robô>/assets/ (1200 px de largura). Não mexe em guia/assets/."""
    from PIL import Image
    dest = GUIA / R.nome / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in sorted((R.pasta / "imagens").glob(f"{R.cfg['id']}-*.jpg")):
        im = Image.open(f).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(dest / f.name, quality=84, optimize=True)
        print(f.name, im.size)
    if R.bal:                                                       # mapas de balanços das peças do indice.json
        (dest / "balancos").mkdir(exist_ok=True)
        usados = {p["imagem"] for p in R.bal["pecas"]}
        for f in sorted((dest / "balancos").glob("*.jpg")):
            if f.name not in usados:
                f.unlink()                                          # peça que saiu do mapa
        for nome in sorted(usados):
            im = Image.open(R.pasta / "imagens" / "balancos" / nome).convert("RGB")
            if im.width > 1200:
                im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            im.save(dest / "balancos" / nome, quality=84, optimize=True)
        print(f"balancos: {len(usados)} mapas")


if __name__ == "__main__":
    cmd, nome = sys.argv[1], sys.argv[2]
    R = Robo(nome)
    lgs = sys.argv[3:]
    if cmd == "docs":
        docs(R, lgs or IDIOMAS)
    elif cmd == "zip":
        zipar(R)
    elif cmd == "imagens":
        imagens(R)
    elif cmd == "traduzir":
        for lg in (lgs or ["en", "es"]):
            traduzir(R, lg)
    elif cmd == "esquema":
        for lg in (lgs or IDIOMAS):
            esquema(R, lg, (GUIA / R.nome / "index.html").exists())
    elif cmd == "pagina":
        for lg in (lgs or IDIOMAS):
            esquema(R, lg)
            pagina(R, lg)
    elif cmd == "conferir":
        sys.exit(0 if conferir(R) else 1)
    else:
        sys.exit(__doc__)
