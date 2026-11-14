#!/usr/bin/env python3
"""Página própria de UM robô no guia (PT/EN/ES) + tabelas dos docs do robô + zip dos arquivos de impressão.
Não toca nas outras páginas do guia (quem monta a entrada /guia/ continua sendo montar.py).

Fontes:
  pecas/<id>/montagem.json · mesas.json · verificacao.json     números das peças (gerados por cad/gerar.py e verificar.py)
  guia/src/robos/<robo>.dados.json     lista de compras, parafusos, notas dos passos (o que o montagem.json não tem)
  guia/src/robos/_comum.pt.json        rótulos iguais em todas as páginas de robô
  guia/src/robos/<robo>.pt.json        textos da página deste robô
  guia/src/robo.html                   estrutura única da página (os textos entram por [[chave]])

Uso (sempre com o venv do repo):
  .venv/bin/python guia/src/pagina_robo.py docs cubo        preenche os blocos <!-- GERADO:x --> de projetos/cubo/*.md
  .venv/bin/python guia/src/pagina_robo.py zip cubo         projetos/cubo/cubo-stl.zip (STL + mesas 3MF + LEIA-ME)
  .venv/bin/python guia/src/pagina_robo.py traduzir cubo    EN e ES pelo inema-traduz (só o que falta ou mudou)
  .venv/bin/python guia/src/pagina_robo.py pagina cubo      guia/cubo/, guia/en/cubo/, guia/es/cubo/
  .venv/bin/python guia/src/pagina_robo.py entrada cubo     botão "página nova" no cartão do robô em /guia/ (+ en, es)
  .venv/bin/python guia/src/pagina_robo.py conferir cubo    links relativos, chaves e tags das 3 páginas
"""
import hashlib
import html
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
import montar            # noqa: E402  (cabeça/CSS/rodapé do template do guia)
import traduzir as TR    # noqa: E402  (pedido ao inema-traduz e conferência de tags)

REPO = "https://github.com/inematds/robos-impressos"
RAW = REPO + "/raw/main/"
BLOB = REPO + "/blob/main/"
TREE = REPO + "/tree/main/"
ML = "https://lista.mercadolivre.com.br/"
# robô → onde estão os arquivos. Quando a E5a mover pecas/<id>/ para projetos/<robô>/, muda só aqui.
ROBOS = {"cubo": dict(id="cubo", pecas="pecas/cubo", docs="projetos/cubo", emoji="🤖")}
IDIOMAS = ("pt", "en", "es")


# ------------------------------------------------------------------ dados
def ler(p):
    return json.loads(Path(p).read_text())


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
        passos = {o["passo"] for o in self.mj["ordem_montagem"]}
        sobra = set(self.d["passos_nota"]) - passos
        assert not sobra, f"passos_nota com passo que não existe mais no modelo: {sorted(sobra)}"
        assert len(self.d["ordem_impressao"]) == len(self.mesas), "ordem_impressao não cobre todas as mesas"
        assert sum(p["qtd"] for p in self.d["parafusos"] if "inserto" in p["rosca"]) == self.d["insertos"], "insertos: tabela de parafusos não bate"

    def caminho(self, p):
        """Caminho no repo do arquivo de uma peça (o montagem.json guarda relativo à pasta do modelo)."""
        return str((self.pasta / p["arquivo"]).resolve().relative_to(RAIZ))

    def gramas(self):
        return sum(p["massa_g"] * p["qtd"] for p in self.mj["pecas"])

    def horas(self):
        return sum(p["tempo_h"] * p["qtd"] for p in self.mj["pecas"])

    def n_pecas(self):
        return sum(p["qtd"] for p in self.mj["pecas"])

    def por_cor(self):
        o = {}
        for p in self.mj["pecas"]:
            k = (p["material"], p["cor"])
            g, h = o.get(k, (0.0, 0.0))
            o[k] = (g + p["massa_g"] * p["qtd"], h + p["tempo_h"] * p["qtd"])
        return sorted(o.items())

    def custo(self):
        """(mín, máx) da fase 1 sem ferramentas; (mín, máx) do que o dono já tem; (mín, máx) do filamento pelo peso."""
        a = b = ta = tb = 0
        for bl in self.d["compras"]:
            if bl.get("ferramenta"):
                continue
            for it in bl["itens"]:
                a += it["faixa"][0] * it["n"]
                b += it["faixa"][1] * it["n"]
                if it.get("tem"):
                    ta += it["faixa"][0] * it["n"]
                    tb += it["faixa"][1] * it["n"]
        kg = self.gramas() / 1000
        fa, fb = self.d["filamento_preco_kg"]
        return (a, b), (ta, tb), (round(fa * kg), round(fb * kg))


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
    f += list(R.d["passos_nota"].values())
    for bl in R.d["compras"]:
        f.append(bl["bloco"])
        for it in bl["itens"]:
            f += [it["item"], it["qtd"], it["para"], it["base"], it.get("conf", ""), it.get("nc", "")]
    for it in R.d["fase2"]:
        f += [it["item"], it["qtd"], it["onde"], it.get("conf", ""), it.get("nc", "")]
    for p in R.d["parafusos"]:
        f += [p["onde"], p["tipo"], p["rosca"]]
    for o in R.d["ordem_impressao"]:
        f.append(o["porque"])
    return {chave_auto(s): s for s in dict.fromkeys(f) if s and not re.fullmatch(r"[\d\s+.,×x–-]*", s)}


def textos_pt(R):
    t = ler(AQUI / "robos" / "_comum.pt.json")
    t.update(ler(AQUI / "robos" / f"{R.nome}.pt.json"))
    t.update(frases_auto(R))
    return t


def arq_lg(R, lg):
    return AQUI / "robos" / f"{R.nome}.{lg}.json"


def traduzir(R, lg, lote=40):
    pt = textos_pt(R)
    dest, cache = arq_lg(R, lg), AQUI / "robos" / f".cache.{R.nome}.{lg}.json"
    feito = ler(dest) if dest.exists() else {}
    marcas = ler(cache) if cache.exists() else {}
    h = lambda t: hashlib.sha1(t.encode()).hexdigest()[:12]
    pend = [k for k in pt if k not in feito or marcas.get(k) != h(pt[k])]
    print(f"{lg}: {len(pend)} de {len(pt)} textos a traduzir", flush=True)
    for i in range(0, len(pend), lote):
        chaves = pend[i:i + lote]
        bloco = {k: pt[k] for k in chaves}
        out = None
        for tentativa in range(3):
            r = subprocess.run(["inema-traduz"], input=TR.pedido(lg, bloco), capture_output=True, text=True, timeout=1500)
            mo = re.search(r"\{.*\}", r.stdout.strip(), re.S)
            try:
                out = json.loads(mo.group(0))
                assert set(out) == set(bloco), "chaves diferentes"
                ruins = [k for k in bloco if TR.tags(out[k]) != TR.tags(bloco[k])]
                assert not ruins, f"tags diferentes em {ruins}"
                marc = [k for k in bloco if sorted(re.findall(r"\[\[\w+\]\]", out[k])) != sorted(re.findall(r"\[\[\w+\]\]", bloco[k]))]
                assert not marc, f"marcadores [[ ]] diferentes em {marc}"
                break
            except Exception as e:
                print(f"  {lg} bloco {i}: tentativa {tentativa + 1} falhou ({e})", flush=True)
                out = None
        if out is None:
            raise SystemExit(f"Falhou: tradução {lg} bloco {i}")
        feito.update(out)
        for k in chaves:
            marcas[k] = h(pt[k])
        dest.write_text(json.dumps({k: feito[k] for k in pt if k in feito}, ensure_ascii=False, indent=1) + "\n")
        cache.write_text(json.dumps(marcas))
        print(f"  {lg}: {min(i + lote, len(pend))}/{len(pend)}", flush=True)


class Tx:
    """Textos de um idioma. t(chave) = texto manual; a(frase em PT) = a mesma frase no idioma."""

    def __init__(self, R, lg):
        self.lg = lg
        self.pt = textos_pt(R)
        self.d = self.pt if lg == "pt" else ler(arq_lg(R, lg))
        falta = [k for k in self.pt if k not in self.d]
        assert not falta, f"{lg}: {len(falta)} textos sem tradução (rode 'traduzir'): {falta[:5]}"

    def t(self, k):
        return self.d[k]

    def a(self, s):
        if not s or self.lg == "pt":
            return s
        return self.d.get(chave_auto(s), s)

    def n(self, x, casas=0):
        s = f"{x:.{casas}f}"
        return s if self.lg == "en" else s.replace(".", ",")


# ------------------------------------------------------------------ tabelas (uma definição, saída em HTML ou Markdown)
def L(texto, url):
    return ("link", texto, url)


def faixa(f):
    return f"R$ {f[0]}–{f[1]}"


def tabelas(R, X):
    """Devolve {nome: (cabeçalho, linhas)}; célula = texto ou L(texto, url) ou lista de pedaços."""
    t, a, n = X.t, X.a, X.n
    T = {}
    conf = lambda it: (a(it["conf"]) if it.get("conf") else t("nao_conferido"))
    # --- compras, um bloco por tabela
    for i, bl in enumerate(R.d["compras"]):
        linhas = []
        for it in bl["itens"]:
            nome = [a(it["item"])]
            if it.get("tem"):
                nome.append(" (" + t("ja_tem") + ")")
            para = [a(it["para"])]
            if it.get("nc"):
                para.append(" " + t("nc_rotulo") + " " + a(it["nc"]) + ".")
            linhas.append([nome, a(it["qtd"]), para, faixa(it["faixa"]) + " (" + a(it["base"]) + ")", conf(it), L(t("buscar"), ML + it["ml"])])
        T[f"compras{i}"] = ([t("th_item"), t("th_qtd"), t("th_para"), t("th_preco"), t("th_conf"), t("th_link")], linhas)
    T["fase2"] = ([t("th_item"), t("th_qtd"), t("th_onde"), t("th_preco"), t("th_conf"), t("th_link")],
                  [[a(it["item"]), a(it["qtd"]), [a(it["onde"])] + ([" " + t("nc_rotulo") + " " + a(it["nc"]) + "."] if it.get("nc") else []),
                    faixa(it["faixa"]), conf(it), L(t("buscar"), ML + it["ml"])] for it in R.d["fase2"]])
    # --- peças
    linhas = []
    for p in R.mj["pecas"]:
        arq = R.caminho(p)
        linhas.append([L(Path(arq).name, RAW + arq), str(p["qtd"]), a(p["material"]) + " " + a(p["cor"]), " × ".join(n(v, 0 if abs(v - round(v)) < 0.05 else 1) for v in p["dim"]),
                       a(p.get("orientacao", "")) or t("deitada"), a(p["suporte"]), str(p.get("perimetros", 3)), f'{p.get("infill", 15)} %',
                       n(p["massa_g"] * p["qtd"], 0), n(p["tempo_h"] * p["qtd"], 1)])
    linhas.append([t("total"), str(R.n_pecas()), "", "", "", "", "", "", n(R.gramas(), 0), n(R.horas(), 1)])
    T["pecas"] = ([t("th_arquivo"), t("th_qtd"), t("th_material"), t("th_dim"), t("th_orient"), t("th_suporte"), t("th_perim"), t("th_infill"), t("th_g"), t("th_h")], linhas)
    T["reforcos"] = ([t("th_peca"), t("th_reforco"), t("th_obs")], [[p["nome"], a(p.get("reforco", "")) or "—", a(p.get("obs", ""))] for p in R.mj["pecas"]])
    # --- mesas, na ordem sugerida de impressão
    mesa = {m["mesa"]: m for m in R.mesas}
    linhas = []
    for k, o in enumerate(R.d["ordem_impressao"], 1):
        m = mesa[o["mesa"]]
        g = sum(R.pecas[x]["massa_g"] for x in m["itens"])
        h = sum(R.pecas[x]["tempo_h"] for x in m["itens"])
        itens = {}
        for x in m["itens"]:
            itens[x] = itens.get(x, 0) + 1
        arq = f'{R.cfg["pecas"]}/{m["arquivo"]}'
        linhas.append([str(k), L(Path(arq).name, RAW + arq), a(m["material"]) + " " + a(m["cor"]), ", ".join(x if q == 1 else f"{q} × {x}" for x, q in itens.items()),
                       n(g, 0), n(h, 1), a(o["porque"])])
    T["mesas"] = ([t("th_ordem"), t("th_mesa"), t("th_material"), t("th_pecas"), t("th_g"), t("th_h"), t("th_porque")], linhas)
    T["filamento"] = ([t("th_material"), t("th_g"), t("th_h")],
                      [[a(m) + " " + a(c), n(g, 0), n(h, 1)] for (m, c), (g, h) in R.por_cor()] + [[t("total"), n(R.gramas(), 0), n(R.horas(), 1)]])
    T["parafusos"] = ([t("th_onde"), t("th_qtd"), t("th_parafuso"), t("th_rosca")], [[a(p["onde"]), str(p["qtd"]), a(p["tipo"]), a(p["rosca"])] for p in R.d["parafusos"]])
    mont, abre = [], []
    for o in R.mj["ordem_montagem"]:
        d = tuple(int(round(v)) for v in o["dir"])
        if o.get("sai"):
            abre.append([str(len(abre) + 1), a(o["passo"]), a(R.d["passos_nota"].get(o["passo"], ""))])
        else:
            # na montagem a peça vem de fora: por cima desce, por trás entra
            como = {(0, 0, 1): t("vem_cima"), (0, 0, -1): t("vem_baixo"), (0, -1, 0): t("vem_tras"), (0, 1, 0): t("vem_frente")}[d]
            mont.append([str(len(mont) + 1), a(o["passo"]), como, a(R.d["passos_nota"].get(o["passo"], ""))])
    T["passos"] = ([t("th_num"), t("th_passo"), t("th_vem"), t("th_nota")], mont)
    T["abrir"] = ([t("th_num"), t("th_passo"), t("th_nota")], abre)
    return T


def cel_html(c):
    if isinstance(c, tuple):
        return f'<a href="{html.escape(c[2])}" target="_blank" rel="noopener">{html.escape(c[1])}</a>'
    if isinstance(c, list):
        return "".join(cel_html(x) for x in c)
    return html.escape(c, quote=False)


def cel_md(c):
    if isinstance(c, tuple):
        return f"[{c[1]}]({c[2]})"
    if isinstance(c, list):
        return "".join(cel_md(x) for x in c)
    return c.replace("|", "\\|")


def tab_html(cab, linhas, total=False):
    o = ['<div class="tabela-wrap"><table class="tabela">', "<thead><tr>" + "".join(f"<th>{cel_html(c)}</th>" for c in cab) + "</tr></thead>", "<tbody>"]
    for i, l in enumerate(linhas):
        forte = total and i == len(linhas) - 1
        o.append("<tr>" + "".join(f"<td>{'<strong>' if forte and c else ''}{cel_html(c)}{'</strong>' if forte and c else ''}</td>" for c in l) + "</tr>")
    o.append("</tbody></table></div>")
    return "\n".join(o)


def tab_md(cab, linhas, total=False):
    o = ["| " + " | ".join(cel_md(c) for c in cab) + " |", "|" + "---|" * len(cab)]
    for i, l in enumerate(linhas):
        forte = total and i == len(linhas) - 1
        o.append("| " + " | ".join((f"**{cel_md(c)}**" if forte and c else cel_md(c)) for c in l) + " |")
    return "\n".join(o)


COM_TOTAL = {"pecas", "filamento"}


def saida_verif(R):
    o = [f"== verificação: {R.mj['modelo']}"]
    for k, x in R.verif["testes"].items():
        o.append(f"  [{'PASSOU' if x['ok'] else 'FALHOU'}] {k}: {x['texto']}")
    return "\n".join(o)


# ------------------------------------------------------------------ página
def pagina(R, lg):
    X = Tx(R, lg)
    head, script = montar.cabeca_rodape()
    corpo = (AQUI / "robo.html").read_text()
    T = tabelas(R, X)
    sub = f"{R.nome}/" if lg == "pt" else f"{lg}/{R.nome}/"
    fundo = "../" if lg == "pt" else "../../"                      # da página até guia/
    A = "assets/" if lg == "pt" else f"../../{R.nome}/assets/"     # imagens do robô ficam em guia/<robô>/assets/
    lang = "".join(f'<a{" class=\"on\"" if k == lg else ""} href="{"./" if k == lg else fundo + ("" if k == "pt" else k + "/") + R.nome + "/"}">{k.upper()}</a>' for k in IDIOMAS)
    (ca, cb), (ta, tb), (fa, fb) = R.custo()
    fixos = {"LANG": f'<span class="lang">{lang}</span>', "A": A, "GA": fundo + "assets/", "G": "../", "RAW": RAW, "BLOB": BLOB, "TREE": TREE, "REPO": REPO,
             "EMOJI": R.cfg["emoji"], "ID": R.cfg["id"], "PECAS": R.cfg["pecas"], "DOCS": R.cfg["docs"], "ZIP": RAW + f'{R.cfg["docs"]}/{R.nome}-stl.zip',
             "N_ALTURA": X.n(R.mj["obs"]["altura_mm"] / 10, 0), "N_PECAS": str(R.n_pecas()), "N_DISTINTAS": str(len(R.mj["pecas"])), "N_MESAS": str(len(R.mesas)),
             "N_HORAS": X.n(R.horas(), 0), "N_GRAMAS": X.n(R.gramas(), 0), "N_INSERTOS": str(R.d["insertos"]), "N_TESTES": str(len(R.verif["testes"])),
             "CUSTO": f"R$ {ca}–{cb}", "CUSTO_TEM": f"R$ {ta}–{tb}", "CUSTO_SEM": f"R$ {ca - ta}–{cb - tb}", "CUSTO_FIL": f"R$ {fa}–{fb}",
             "PRECO_DATA": R.d["preco_data"], "PRECO_FONTE": R.d["preco_fonte"],
             "SAIDA_VERIF": html.escape(saida_verif(R), quote=False),
             "COMPRAS": "\n".join(f'<h3 class="sep3">{html.escape(X.a(bl["bloco"]))}</h3>\n' + tab_html(*T[f"compras{i}"]) for i, bl in enumerate(R.d["compras"]))}
    for k, v in T.items():
        if not k.startswith("compras"):
            fixos["TAB_" + k.upper()] = tab_html(*v, total=k in COM_TOTAL)
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
    head = head.replace("{{PROJETO}} — {{TAGLINE}}", X.t("titulo")).replace("{{META_DESCRICAO}}", html.escape(X.t("meta"))).replace("{{SLUG}}", "robos-impressos")
    for k in ("en/", "es/", ""):                # hreflang desta página, não o da entrada do guia
        head = head.replace(f'/guia/{k}">', f'/guia/{k}{R.nome}/">')
    head = head.replace('<html lang="pt-BR">', {"pt": '<html lang="pt-BR">', "en": '<html lang="en">', "es": '<html lang="es">'}[lg])
    script = script.replace("{{SLUG}}", "robos-impressos")
    pag = head + "\n\n" + corpo + "\n" + script
    assert "{{" not in pag.replace("${{", ""), "placeholder do template sobrando"
    destino = GUIA / sub / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pag)
    print(destino.relative_to(RAIZ), len(pag))
    return destino


def conferir(R):
    """Sem servidor: todo src/href relativo existe em disco; mesmas tags nos 3 idiomas; nada de [[ ]] sobrando."""
    ok = True
    conta = {}
    for lg in IDIOMAS:
        f = GUIA / (f"{R.nome}/index.html" if lg == "pt" else f"{lg}/{R.nome}/index.html")
        h = f.read_text()
        for u in re.findall(r'(?:src|href)="([^"#]+)(?:#[^"]*)?"', h):
            if re.match(r"(https?:|mailto:|data:)", u):
                continue
            alvo = (f.parent / u)
            alvo = alvo / "index.html" if u.endswith("/") else alvo
            if not alvo.exists():
                ok = False
                print(f"  {lg}: link quebrado {u}")
        for u in sorted(set(re.findall(re.escape(RAW) + r'([^"]+)', h))):
            if not (RAIZ / u).exists():
                ok = False
                print(f"  {lg}: arquivo do link raw não existe no repo: {u}")
        if "[[" in h:
            ok = False
            print(f"  {lg}: [[ ]] sobrando")
        conta[lg] = {tg: len(re.findall(f"<{tg}[ >]", h)) for tg in ("section", "div", "tr", "td", "li", "img", "a", "h2", "h3")}
        assert f'/guia/{"" if lg == "pt" else lg + "/"}{R.nome}/"' in h, "hreflang da própria página"
    for lg in ("en", "es"):
        if conta[lg] != conta["pt"]:
            ok = False
            print(f"  {lg}: contagem de tags diferente do PT: {conta[lg]} x {conta['pt']}")
    print("conferir:", "OK" if ok else "FALHOU", conta["pt"])
    return ok


# ------------------------------------------------------------------ docs do robô (blocos gerados) e zip
def docs(R):
    X = Tx(R, "pt")
    T = tabelas(R, X)
    (ca, cb), (ta, tb), (fa, fb) = R.custo()
    B = {k: tab_md(*v, total=k in COM_TOTAL) for k, v in T.items() if not k.startswith("compras")}
    B["compras"] = "\n\n".join(f'### {bl["bloco"]}\n\n' + tab_md(*T[f"compras{i}"]) for i, bl in enumerate(R.d["compras"]))
    B["custo"] = (f"- Peças compradas da fase 1 (sem ferramentas e sem filamento): **R$ {ca}–{cb}**.\n"
                  f"- Tirando o que já está marcado como \"já tem\" (R$ {ta}–{tb}): **R$ {ca - ta}–{cb - tb}**.\n"
                  f"- Filamento, pelo peso ({X.n(R.gramas(), 0)} g a R$ {R.d['filamento_preco_kg'][0]}–{R.d['filamento_preco_kg'][1]} o quilo): R$ {fa}–{fb}.")
    B["verificacao"] = "```\n" + saida_verif(R) + "\n```"
    B["numeros"] = (f"- Altura montado: {X.n(R.mj['obs']['altura_mm'], 1)} mm.\n- Peças impressas: {R.n_pecas()} ({len(R.mj['pecas'])} arquivos diferentes), em {len(R.mesas)} mesas.\n"
                    f"- Filamento: {X.n(R.gramas(), 0)} g. Tempo de impressão: {X.n(R.horas(), 1)} h. As duas contas são estimativas por volume, sem fatiador.\n"
                    f"- Insertos M3 a quente: {R.d['insertos']}.")
    for f in sorted(R.docs.glob("*.md")):
        s = f.read_text()
        usados = []

        def troca(mo):
            usados.append(mo.group(1))
            assert mo.group(1) in B, f"{f.name}: bloco GERADO desconhecido '{mo.group(1)}'"
            return f"<!-- GERADO:{mo.group(1)} -->\n{B[mo.group(1)]}\n<!-- /GERADO -->"

        n = re.sub(r"<!-- GERADO:([a-z0-9_]+) -->.*?<!-- /GERADO -->", troca, s, flags=re.S)
        if n != s:
            f.write_text(n)
        print(f.relative_to(RAIZ), "blocos:", ", ".join(usados) or "nenhum")


def zipar(R):
    """Zip estável (ordem e datas fixas): STL de cada peça + 3MF de cada mesa + LEIA-ME."""
    dest = R.docs / f"{R.nome}-stl.zip"
    itens = []
    for p in R.mj["pecas"]:
        arq = RAIZ / R.caminho(p)
        itens.append((f"stl/{arq.name}", arq.read_bytes()))
    for m in R.mesas:
        arq = R.pasta / m["arquivo"]
        itens.append((f"mesas/{arq.name}", arq.read_bytes()))
    leia = (R.docs / "IMPRIMIR.md").read_text()
    itens.append(("LEIA-ME.md", ("Arquivos de impressão do robô quadrado de mesa (robos-impressos).\n"
                                 "stl/ = uma peça por arquivo, já deitada na posição de impressão. mesas/ = 3MF com as peças já arrumadas por cor.\n"
                                 "Comece pela mesa 06 (cupom de teste). Guia: https://inematds.github.io/robos-impressos/guia/cubo/\n\n" + leia).encode()))
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for nome, dados in sorted(itens):
            zi = zipfile.ZipInfo(f"{R.nome}/{nome}", date_time=(2026, 11, 14, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, dados)
    print(dest.relative_to(RAIZ), f"{dest.stat().st_size / 1e6:.2f} MB", len(itens), "arquivos")


def imagens(R):
    """Cópias dos renders DESTE robô em guia/<robô>/assets/ (1200 px de largura). Não mexe em guia/assets/."""
    from PIL import Image
    dest = GUIA / R.nome / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in sorted((RAIZ / "imagens").glob(f"{R.cfg['id']}-*.jpg")):
        im = Image.open(f).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(dest / f.name, quality=84, optimize=True)
        print(f.name, im.size)


def entrada(R):
    """Só acrescenta, no cartão do robô da página de entrada (/guia/, /guia/en/, /guia/es/), o botão para a página
    nova. Não regenera a entrada. O próximo montar.py apaga o botão: a E5d põe o link na estrutura (corpo.html)."""
    for lg in IDIOMAS:
        f = GUIA / ("index.html" if lg == "pt" else f"{lg}/index.html")
        h = re.sub(rf'<!-- link-robo:{R.nome} -->.*?<!-- /link-robo -->', "", f.read_text(), flags=re.S)
        botao = f'<!-- link-robo:{R.nome} --><p style="margin-top:12px"><a class="btn" href="{R.nome}/">{html.escape(Tx(R, lg).t("entrada_link"))}</a></p><!-- /link-robo -->'
        n, k = re.subn(rf'(<div class="card"><img class="shot" src="[^"]*{R.cfg["id"]}-montado\.jpg".*?</p>)(</div>)', lambda mo: mo.group(1) + botao + mo.group(2), h, count=1, flags=re.S)
        assert k == 1, f"{lg}: cartão do robô não encontrado na entrada"
        f.write_text(n)
        print(f.relative_to(RAIZ), "botão posto")


if __name__ == "__main__":
    cmd, nome = sys.argv[1], sys.argv[2]
    R = Robo(nome)
    if cmd == "docs":
        docs(R)
    elif cmd == "zip":
        zipar(R)
    elif cmd == "imagens":
        imagens(R)
    elif cmd == "traduzir":
        for lg in (sys.argv[3:] or ["en", "es"]):
            traduzir(R, lg)
    elif cmd == "pagina":
        for lg in (sys.argv[3:] or IDIOMAS):
            pagina(R, lg)
    elif cmd == "entrada":
        entrada(R)
    elif cmd == "conferir":
        sys.exit(0 if conferir(R) else 1)
    else:
        sys.exit(__doc__)
