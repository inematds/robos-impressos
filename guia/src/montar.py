#!/usr/bin/env python3
"""Monta a ENTRADA do guia (/guia/, /guia/en/, /guia/es/) a partir de corpo.html (estrutura única) + textos.<idioma>.json.
A estrutura é a mesma por construção; só os textos mudam. Todo número (peças, horas, custo, limites de movimento, testes,
semelhança) sai dos arquivos de cada robô na hora de montar: nada é digitado e não é preciso rodar comum/cad/tabelas.py.

Fontes: projetos/<robô>/montagem.json · mesas.json · verificacao.json e guia/src/robos/<robô>.dados.json (pela classe Robo de
pagina_robo.py, a mesma das páginas de cada robô), comparacao/semelhanca.json (guia/src/semelhanca.py) e
guia/evolucao/assets/dados.json (banner antigo × novo e, por robô, desenho de referência · antes · depois).

Este módulo também dá às outras páginas do guia a cabeça, o CSS e o rodapé do template (cabeca_rodape) e a versão (VERSAO).

Uso: .venv/bin/python guia/src/montar.py [pt en es]      (EN e ES: antes, .venv/bin/python guia/src/traduzir.py)
"""
import html
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GUIA = AQUI.parent
RAIZ = GUIA.parent
TEMPLATE = Path.home() / ".claude/skills/projetos-landing-guia/assets/template.html"
VERSAO = "v1.1.2"                       # versão do projeto mostrada no guia (a mesma do README e da tag)
MODELOS = ["dino", "capivara", "cubo", "cubo-rodas"]          # páginas (= pastas em projetos/), na ordem dos cartões
PREF = {"dino": "dino", "capivara": "capi", "cubo": "cubo", "cubo-rodas": "rodas"}   # prefixo das chaves de texto e dos marcadores
RODAM = {"dino", "capivara", "cubo-rodas"}
CSS_EXTRA = """
  .techhead{background:var(--bg2);border-top:3px solid var(--amb);padding:58px 0 8px}
  .techhead h2{font-family:Sora;margin:.3em 0 0}
  .techzone{background:var(--bg2)}
  .nota{font-size:.88rem;color:var(--mut);margin-top:14px;max-width:80ch}
  .mini{font-size:.82rem;color:var(--mut);margin:.4em 0 0}
  .shot{display:block;width:100%;border-radius:12px;border:1px solid var(--line);margin:0 0 14px;background:#e9e9ee}
  .g2{grid-template-columns:repeat(2,1fr)} .g4{grid-template-columns:repeat(4,1fr)}
  .numero{text-align:center} .numero b{display:block;font-family:Sora;font-size:2.1rem;color:var(--amb);line-height:1.15} .numero span{display:block;font-size:.9rem;color:var(--mut);margin-top:6px}
  .arraste{display:none;font-size:.8rem;color:var(--mut);margin:18px 0 -14px}
  .sep4{font-family:Sora;margin:22px 0 10px}
  #pecas,#compras,section{scroll-margin-top:76px} .hero figcaption.mini{padding:8px 12px 10px}
  .glossario{margin:18px 0 0;display:grid;grid-template-columns:max-content 1fr;gap:8px 18px} .glossario dt{font-weight:700;color:var(--amb)} .glossario dd{margin:0}
  .tabela-wrap{overflow-x:auto;margin:22px 0 6px;border:1px solid var(--line);border-radius:12px}
  .tabela{border-collapse:collapse;width:100%;font-size:.9rem;min-width:560px}
  .tabela th,.tabela td{padding:8px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
  .tabela th{font-family:Sora;font-size:.82rem;color:var(--mut);background:var(--bg2)}
  .tabela tr:last-child td{border-bottom:0}
  .barras{margin-top:22px} .barra{display:grid;grid-template-columns:150px 1fr 60px;gap:10px;align-items:center;margin:8px 0;font-size:.92rem}
  .barra i{display:block;height:16px;border-radius:8px;background:var(--amb)}
  .lista{margin:.4em 0 0 1.2em;padding:0} .lista li{margin:.3em 0}
  .sep3{font-family:Sora;margin:34px 0 0}
  pre.saida{white-space:pre-wrap;font-size:.8rem;line-height:1.5}
  .card ul{margin:.5em 0 0 1.1em;padding:0} .card li{margin:.35em 0}
  @media(max-width:1180px){nav .links .sec{display:none}}
  @media(max-width:860px){.g2,.g4{grid-template-columns:1fr}.barra{grid-template-columns:110px 1fr 50px}.arraste{display:block}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.74rem}figcaption.mini{padding:8px 4px 0}.glossario{grid-template-columns:1fr;gap:2px 0}.glossario dd{margin:0 0 10px}}
"""
# só da entrada (entra depois do CSS das páginas de robô, de onde vêm .dobra, .topo e o glossário em cartões)
CSS_ENTRADA = """
.robos .card{display:flex;flex-direction:column}
.robos .card h3{font-size:1.05rem}
.robos .fatos{font-family:Sora;font-weight:600;font-size:.84rem;color:var(--txt);margin:.9em 0 0}
.robos .fatos+.fatos{margin-top:.35em}
.robos .selo{display:inline-block;align-self:flex-start;font:600 .76rem Sora,sans-serif;color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:.3em .8em;margin:.1em 0 .7em}
.robos .selo.facil{color:#1a1206;background:var(--amb);border-color:var(--amb)}
.robos .card .mini{margin-top:.6em}
.robos .custo{font-size:.84rem;color:var(--amb);margin:.4em 0 0;font-family:Sora;font-weight:600}
.robos .card .ir{margin-top:auto;padding-top:14px}
.robos .card .btn{display:block;text-align:center;font-size:.88rem}
@media(min-width:861px) and (max-width:1100px){.robos{grid-template-columns:repeat(2,1fr)}}
.evo-robo{max-width:900px;margin:22px 0 0}
.evo-robo h4{font-family:Sora;font-size:1.02rem;margin:0 0 10px}
.evo-robo h4 small{font-weight:600;color:var(--amb);margin-left:.5em;white-space:nowrap}
.zips{display:flex;flex-wrap:wrap;gap:10px;margin:.4em 0 1em}
.zips .btn{font-size:.88rem}.zips small{font-weight:400;opacity:.8}
.barra{grid-template-columns:200px 1fr 60px}
.tabela td.ok{color:var(--amb);font-weight:600;white-space:nowrap}
.tabela td a{text-decoration:underline}
.nota a{text-decoration:underline}
details.dobra summary{color:var(--amb)}
nav .brand,nav .links a.sec{white-space:nowrap}
@media(max-width:1240px){nav .links .sec{display:none}}
@media(max-width:860px){.barra{grid-template-columns:118px 1fr 50px}}
"""


# trio = desenho de referência · antes · depois; bn = banner antigo × novo (entrada e página de evolução)
CSS_TRIO = """
.trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.bn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:22px}
.trio figure,.bn figure{margin:0;min-width:0}
.trio img,.bn img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:#e9e9ee}
.trio figcaption,.bn figcaption{font-size:.86rem;color:var(--mut);margin-top:6px;text-align:center}
.trio figcaption b,.bn figcaption b{font-family:Sora;color:var(--txt)}
.bn figcaption{text-align:left;font-size:.9rem;line-height:1.5}
@media(max-width:860px){.bn{grid-template-columns:1fr}}
@media(max-width:560px){.trio{gap:6px}.trio img{border-radius:8px}.trio figcaption{font-size:.76rem;line-height:1.35}}
"""


def figuras(figs, classe="trio"):
    """Figuras lado a lado; cada uma (src, alt, legenda em HTML). A imagem abre em tamanho grande."""
    return (f'<div class="{classe}">' + "".join(
        f'<figure><a href="{src}" target="_blank" rel="noopener"><img loading="lazy" src="{src}" alt="{html.escape(alt)}"></a><figcaption>{cap}</figcaption></figure>'
        for src, alt, cap in figs) + "</div>")


def cabeca_rodape():
    t = TEMPLATE.read_text().split("\n")
    i_body = next(i for i, l in enumerate(t) if l.strip() == "<body>")
    i_script = next(i for i, l in enumerate(t) if l.strip().startswith("<script>"))
    head = "\n".join(t[:i_body + 1])
    script = "\n".join(t[i_script:])
    head = head.replace("</style>", CSS_EXTRA + "</style>", 1)
    head = re.sub(r"<!-- TEMPLATE.*?-->\n?", "", head, flags=re.S)
    return head, script


def tab(cab, linhas):
    """Tabela simples (rola de lado no celular). As células já vêm em HTML; a que começa por <td traz a própria classe."""
    o = ['<div class="tabela-wrap"><table class="tabela">', "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cab) + "</tr></thead>", "<tbody>"]
    for l in linhas:
        o.append("<tr>" + "".join((c if c.startswith("<td") else f"<td>{c}</td>") for c in l) + "</tr>")
    o.append("</tbody></table></div>")
    return "\n".join(o)


def graus(lim, n):
    """Faixa de uma junta: ±60° quando simétrica; −15° … +20°; 0 … 18°."""
    a, b = lim
    if a == -b:
        return f"±{n(b)}°"
    sinal = lambda v: ("−" if v < 0 else "+" if v > 0 else "") + n(abs(v))
    return f"{sinal(a)}° … {sinal(b)}°" if a < 0 else f"{n(a)} … {n(b)}°"


def montar(lg):
    import pagina_robo as P          # aqui dentro: pagina_robo importa este módulo (cabeça e CSS do template)
    import traduzir as TR
    tx = json.loads((AQUI / "textos.pt.json").read_text())
    if lg != "pt":                   # para se faltar tradução ou se o português mudou depois dela; no inglês, vírgula decimal → ponto
        tx = P._carrega(tx, AQUI / f"textos.{lg}.json", TR.cache_de(lg), lg)
    t = tx.__getitem__
    esc = lambda s: html.escape(s, quote=False)
    n = lambda x, casas=0: (f"{x:.{casas}f}" if lg == "en" else f"{x:.{casas}f}".replace(".", ","))
    R = {m: P.Robo(m) for m in MODELOS}
    nome = {m: t(PREF[m] + "_nome") for m in MODELOS}
    rs = lambda f: f"{f[0]}–{f[1]}"
    A = "assets/" if lg == "pt" else "../assets/"
    head, script = cabeca_rodape()
    corpo = (AQUI / "corpo.html").read_text()

    # --- os testes têm de estar todos passando: a página afirma isso
    for m in MODELOS:
        ruins = [k for k, x in R[m].verif["testes"].items() if not x["ok"]]
        assert not ruins, f"{m}: teste falhando ({ruins}); a entrada do guia diz que os quatro passam em todos"
    testes = list(R[MODELOS[0]].verif["testes"])
    n_testes = len(testes)
    assert [k.split()[0] for k in testes] == [str(i) for i in range(1, n_testes + 1)], "testes fora de ordem"
    for m in MODELOS:
        assert list(R[m].verif["testes"]) == testes, f"{m}: lista de testes diferente da dos outros robôs"
    assert f"tst_{n_testes}" in tx and f"tst_{n_testes + 1}" not in tx, "textos dos testes (tst_N) não batem com o verificador"

    fixos = {"A": A, "SUF": "" if lg == "pt" else f"-{lg}", "VERSAO": VERSAO, "N_TESTES": str(n_testes)}
    fixos["LANG"] = {"pt": '<span class="lang"><a class="on" href="./">PT</a><a href="en/">EN</a><a href="es/">ES</a></span>',
                     "en": '<span class="lang"><a href="../">PT</a><a class="on" href="./">EN</a><a href="../es/">ES</a></span>',
                     "es": '<span class="lang"><a href="../">PT</a><a href="../en/">EN</a><a class="on" href="./">ES</a></span>'}[lg]

    # --- números por robô (os mesmos da página de cada um)
    por = {}
    for m in MODELOS:
        r, C = R[m], R[m].custo()
        com = [p["nome"] for p in r.mj["pecas"] if p["suporte"].startswith("sim")]
        mont = r.horas_montagem()                    # ESTIMATIVA por contagem de passos (pagina_robo.MONT_MIN): nada foi montado ainda
        por[m] = dict(ALTURA=n(r.altura() / 10), PECAS=str(r.n_pecas()), MESAS=str(len(r.mesas)), HORAS=n(r.horas()), GRAMAS=n(r.gramas()),
                      CUSTO="R$ " + rs(C["pecas"]), DIF=str(len(r.mj["pecas"])), SEM=str(len(r.mj["pecas"]) - len(com)), COM=str(len(com)),
                      SERVOS=str(r.n_servos()), MONT=f"{mont[0]}–{mont[1]}")
        # o Raspberry Pi pode ficar para depois? só onde a lista de compras do robô diz isso (hoje: os dois bichos)
        pi = [it for bl in r.d["compras"] for it in bl["itens"] if it["item"].startswith("Raspberry Pi") and "adiar esta compra" in it["para"]]
        if pi:
            por[m]["PI"] = n(100 * sum(pi[0]["faixa"]) / sum(C["pecas"]))
        for k, v in por[m].items():
            fixos[f"{PREF[m].upper()}_{k}"] = v

    # --- cartões dos robôs: selo de nível (com peças e servos), horas de impressão e de montagem, custo
    #     "o mais simples" = o de menos peças e menos servos, sem rodas; se isso mudar, os selos <robô>_nivel têm de ser reescritos
    facil = min(MODELOS, key=lambda m: R[m].n_pecas())
    assert facil == "cubo" and facil not in RODAM and R[facil].n_servos() == min(R[m].n_servos() for m in MODELOS), "mudou o robô mais simples: reescreva os selos *_nivel"
    assert all(m in RODAM or m == facil for m in MODELOS), "robô sem rodas que não é o mais simples: falta o selo dele"
    cart = []
    for m in MODELOS:
        p = PREF[m]
        sub = lambda s: re.sub(r"\[\[R_([A-Z]+)\]\]", lambda mo: por[m][mo.group(1)], s)
        cart.append(f'    <div class="card"><a href="{m}/"><img class="shot" src="{A}{R[m].cfg["id"]}-montado.jpg" alt="{html.escape(t(p + "_alt"))}"></a>'
                    f'<h3>{R[m].cfg["emoji"]} {esc(nome[m])}</h3><p class="selo{" facil" if m == facil else ""}">{esc(sub(t(p + "_nivel")))}</p><p>{t(p + "_txt")}</p>'
                    f'<p class="fatos">{esc(sub(t("card_fatos")))}</p><p class="fatos">{esc(sub(t("card_tempo")))}</p><p class="custo">{esc(sub(t("card_custo")))}</p>'
                    + (f'<p class="mini">{esc(sub(t("card_pi")))}</p>' if "PI" in por[m] else "") +
                    f'<p class="ir"><a class="btn" href="{m}/">{esc(t(p + "_link"))}</a></p></div>')
    fixos["CARTOES"] = "\n".join(cart)
    lk = lambda m, anc, txt: f'<a href="{m}/{anc}">{esc(txt)}</a>'
    fixos["LINKS_ROBOS"] = ", ".join(lk(m, "", nome[m]) for m in MODELOS)
    fixos["LINKS_FASE2"] = ", ".join(lk(m, "#fase2", nome[m]) for m in MODELOS)

    # --- tabelas
    fixos["TAB_RESUMO"] = tab([t(k) for k in ("rs_robo", "rs_nivel", "rs_altura", "rs_pecas", "rs_servos", "rs_mesas", "rs_g", "rs_h", "rs_mont", "rs_custo", "rs_zero")],
                              [[lk(m, "", nome[m]), esc(t("nivel_facil" if m == facil else "nivel_avancado")), por[m]["ALTURA"], por[m]["PECAS"], por[m]["SERVOS"],
                                por[m]["MESAS"], por[m]["GRAMAS"], por[m]["HORAS"], por[m]["MONT"],
                                rs(R[m].custo()["pecas"]), rs(R[m].custo()["zero"])] for m in MODELOS])
    for k, v in P.MONT_MIN.items():
        fixos["M_" + k.upper()] = str(v)
    fixos["M_FOLGA_MENOS"], fixos["M_FOLGA_MAIS"] = n(round((1 - P.MONT_FOLGA[0]) * 100)), n(round((P.MONT_FOLGA[1] - 1) * 100))
    j = {m: R[m].mj["juntas"] for m in MODELOS}
    fixos["TAB_MOV"] = tab([t("mv_h0")] + [esc(nome[m]) for m in MODELOS],
                           [[t("mv_1")] + [graus(j[m]["pan"]["lim"], n) for m in MODELOS],
                            [t("mv_2")] + [graus(j[m]["cabeca"]["lim"], n) for m in MODELOS],
                            [t("mv_3")] + [graus(j[m]["mandibula"]["lim"], n) if "mandibula" in j[m] else t("mv_tela") for m in MODELOS],
                            [t("mv_4")] + [graus(j[m]["braco_d"]["lim"], n) if "braco_d" in j[m] else (t("mv_parado") if "mandibula" in j[m] else "—") for m in MODELOS],
                            [t("mv_5")] + [t("mv_roda" if m in RODAM else "mv_mesa") for m in MODELOS]])
    fixos["TAB_TESTES"] = tab([t("th_teste"), t("th_prova")] + [esc(nome[m]) for m in MODELOS],
                              [[f"{i}. {esc(t(f'tst_{i}'))}", t(f"tst_{i}_p")] + [f'<td class="ok">✓ {esc(t("passou"))}</td>' for m in MODELOS] for i in range(1, n_testes + 1)])
    S = {m: P.SEM.medida(R[m].cfg["id"]) for m in MODELOS}
    f3 = lambda v: "—" if v is None else n(v, 3)
    fixos["TAB_SEM"] = tab([t(k) for k in ("sem_th_robo", "sem_th_antes", "sem_th_depois", "sem_th_teto", "sem_th_alvo", "sem_th_res")],
                           [[lk(m, "#semelhanca", nome[m]), f3(S[m]["antes"]), f3(S[m]["depois"]), f3(S[m]["teto"]), f3(S[m]["alvo"]),
                             esc(t("sem_novo") if S[m]["novo"] else t("sem_ok" if S[m]["atingiu"] else "sem_nao"))] for m in MODELOS])
    fixos["TAB_PECAS"] = tab([t("rs_robo"), t("rs_pecas"), t("pc_dif"), t("rs_mesas"), t("pc_sem"), t("pc_com"), t("pc_ver")],
                             [[esc(nome[m]), por[m]["PECAS"], por[m]["DIF"], por[m]["MESAS"], por[m]["SEM"], por[m]["COM"],
                               lk(m, "#imprimir", t("pc_link1")) + " · " + lk(m, "#balancos", t("pc_link2"))] for m in MODELOS])
    fixos["TAB_COMPRAS"] = tab([t("rs_robo"), t("rs_custo"), t("rs_zero"), t("cp_fil"), t("pc_ver")],
                               [[esc(nome[m]), rs(R[m].custo()["pecas"]), rs(R[m].custo()["zero"]), rs(R[m].custo()["fil"]),
                                 lk(m, "#comprar", t("cp_link")) + " · " + lk(m, "#energia", t("cp_lig"))] for m in MODELOS])
    zips = []
    for m in MODELOS:
        mb = (R[m].docs / f"{m}-stl.zip").stat().st_size / 1e6
        zips.append(f'<a class="btn ghost" href="{P.RAW}{R[m].cfg["docs"]}/{m}-stl.zip">{R[m].cfg["emoji"]} {esc(nome[m])} <small>({n(mb, 1 if mb < 9.5 else 0)} MB)</small></a>')
    fixos["ZIPS"] = "".join(zips)

    # --- números gerais
    paredes = [v["min"] for m in MODELOS for v in R[m].mj.get("parede_medida", {}).values()]
    horas = {m: R[m].horas() for m in MODELOS}
    fixos["N_PECAS"] = str(sum(R[m].n_pecas() for m in MODELOS))
    fixos["N_PAREDE"] = n(min(paredes), 2)
    fixos["N_MAIOR"] = n(max(max(p["dim"]) for m in MODELOS for p in R[m].mj["pecas"]))
    fixos["BARRAS"] = "\n    ".join(f'<div class="barra"><span>{esc(nome[m])}</span><i style="width:{horas[m] / max(horas.values()) * 100:.0f}%"></i><b>~{n(horas[m])} h</b></div>' for m in MODELOS)
    fixos["SAIDA_VERIF"] = html.escape("\n".join(P.saida_verif(R[m]) for m in MODELOS), quote=False)

    # --- evolução do desenho: banner antigo × novo e, por robô, desenho de referência · antes · depois
    #     (imagens em guia/evolucao/assets/, gravadas por comum/cad/evolucao.py; o banner novo é o de guia/assets/)
    ev = json.loads((GUIA / "evolucao" / "assets" / "dados.json").read_text())
    E = "evolucao/assets/" if lg == "pt" else "../evolucao/assets/"
    fixos["EVO_BANNER"] = figuras([(E + ev["banner"]["antes"][lg], t("evo_bn_alt_antes"), f'<b>{esc(t("evo_bn_antes"))}</b>: {esc(t("evo_bn_antes_p"))}'),
                                   (A + ev["banner"]["depois"][lg], t("evo_bn_alt_depois"), f'<b>{esc(t("evo_bn_depois")).replace("[[VERSAO]]", VERSAO)}</b>: {esc(t("evo_bn_depois_p"))}')], "bn")
    do_id = {R[m].cfg["id"]: m for m in MODELOS}
    blocos = []
    for id, b in ev["bichos"].items():
        m = do_id[id]
        v = next(x for x in b["vistas"] if x["vista"] == b["vista_da_entrada"])
        figs = [(E + v["imagem_" + k], f'{t("evo_alt_" + k)} {nome[m]}', esc(t("evo_" + k)).replace("[[VERSAO]]", VERSAO)) for k in ("ref", "antes", "depois")]
        blocos.append(f'  <div class="evo-robo"><h4>{R[m].cfg["emoji"]} {esc(nome[m])} <small>IoU {f3(S[m]["antes"])} → {f3(S[m]["depois"])}</small></h4>{figuras(figs)}</div>')
    fixos["EVO_TRIOS"] = "\n".join(blocos)
    # o robô de mesa é o único com "antes" que ficou abaixo do alvo: a frase e o porquê (o da página dele) dependem disso
    assert [m for m in MODELOS if S[m]["atingiu"] is False] == ["cubo"], "mudou quem atinge o alvo: reescreva evo_cubo em textos.pt.json"
    for k in ("antes", "depois", "alvo"):
        fixos[f"SEM_CUBO_{k.upper()}"] = f3(S["cubo"][k])
    fixos["CUBO_PORQUE"] = P.Tx(R["cubo"], lg).d["sem_extra"]

    faltam = set()

    def troca(mo):
        k = mo.group(1)
        if k in fixos:
            return fixos[k]
        if k not in tx:
            faltam.add(k)
            return mo.group(0)
        return tx[k]

    for _ in range(2):                              # 2 passadas: os textos trazem marcadores de número
        corpo = re.sub(r"\[\[([A-Za-z0-9_]+)\]\]", troca, corpo)
    assert not faltam, f"{lg}: textos faltando {sorted(faltam)}"
    assert "[[" not in corpo, f"{lg}: marcador sobrando"
    head = (head.replace("{{PROJETO}} — {{TAGLINE}}", tx["titulo"]).replace("{{META_DESCRICAO}}", html.escape(tx["meta"])).replace("{{SLUG}}", "robos-impressos"))
    head = head.replace('<html lang="pt-BR">', {"pt": '<html lang="pt-BR">', "en": '<html lang="en">', "es": '<html lang="es">'}[lg])
    i = head.rindex("</style>")
    head = head[:i] + P.CSS + CSS_TRIO + CSS_ENTRADA + head[i:]
    script = script.replace("{{SLUG}}", "robos-impressos")
    pagina = head + "\n\n" + corpo + "\n" + script
    assert "{{" not in pagina.replace("${{", ""), "placeholder do template sobrando"
    destino = GUIA / ("index.html" if lg == "pt" else f"{lg}/index.html")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pagina)
    print(destino.relative_to(RAIZ), len(pagina))


if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    for lg in (sys.argv[1:] or ("pt", "en", "es")):
        montar(lg)
