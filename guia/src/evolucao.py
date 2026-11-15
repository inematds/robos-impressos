#!/usr/bin/env python3
"""Página /guia/evolucao/ (PT/EN/ES): a capivara, o dinossauro e o robô quadrado de mesa antes (v1.0.2) × depois, ao lado
do desenho de referência, e o banner antigo × novo.

Fontes:
  guia/evolucao/assets/dados.json   quais robôs, quais vistas, o nome de cada imagem e os banners (gravado por comum/cad/evolucao.py,
                                    junto com as imagens; as de referência têm autorização registrada em decisions.md)
  comparacao/semelhanca.json        os números (guia/src/semelhanca.py: mesma conta do alvo das tabelas, sem arredondar)
  projetos/<robô>/montagem.json     altura da junta do pescoço e abertura da boca citadas no texto
  guia/src/evolucao.html            estrutura única; guia/src/evolucao.pt.json = textos (EN/ES pelo inema-traduz, com cache)
Nenhum número de medida é digitado no texto: entra por [[MARCADOR]].

Uso:
  .venv/bin/python guia/src/evolucao.py traduzir [en es]   só o que falta ou mudou
  .venv/bin/python guia/src/evolucao.py pagina [pt en es]  guia/evolucao/, guia/en/evolucao/, guia/es/evolucao/
"""
import html
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import montar            # noqa: E402
import pagina_robo as P  # noqa: E402  (tradutor com cache, tabela, CSS e caminhos)

GUIA, RAIZ, SEM = P.GUIA, P.RAIZ, P.SEM
NOME = "evolucao"
DADOS = GUIA / NOME / "assets" / "dados.json"
PASTA = {"capivara": "capivara", "dino": "dino", "cubo": "cubo"}   # id do modelo → pasta em projetos/ e página em guia/
CSS = """
.par{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.par figure,.ref,.regua figure{margin:0}
.par img,.ref img,.regua img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--line);background:#e9e9ee}
.par figcaption,.regua figcaption{font-size:.86rem;color:var(--mut);margin-top:6px;text-align:center}
.par figcaption b,.regua figcaption b{font-family:Sora;color:var(--txt)}
.par.capa{gap:0;grid-template-columns:repeat(3,minmax(0,1fr))}.par.capa div{position:relative}.par.capa img{border:0;border-radius:0}
.par.capa span{position:absolute;left:10px;top:10px;background:rgba(12,12,16,.78);color:#fff;font:600 .78rem Sora,sans-serif;padding:.25em .6em;border-radius:8px}
@media(max-width:560px){.par.capa span{left:5px;top:5px;font-size:.75rem;padding:.2em .45em}}
.vistas{display:grid;grid-template-columns:1fr;gap:16px;max-width:980px}
.vista h4{font-family:Sora;font-size:1rem;margin:0 0 10px}
.ref{max-width:720px}.ref figcaption{font-size:.82rem;color:var(--mut);margin-top:8px}
.regua{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.regua img{background:#fff}
.iou svg{display:block;width:100%;max-width:440px;height:auto;margin:0 auto 12px}
.iou .legenda{color:var(--txt);font-size:.92rem;line-height:1.9}
.iou .legenda .cor{margin-left:0}
.formula{font-family:Sora;font-weight:600;color:var(--amb)!important;margin-top:.8em!important;font-size:1rem!important}
.bicho .numero b{font-size:1.9rem}
.lista{color:var(--mut)}
#quadrados .cta{display:flex;gap:12px;flex-wrap:wrap}
nav .brand,nav .links a.sec{white-space:nowrap}
@media(max-width:1240px){nav .links .sec{display:none}}
.regua.uma{grid-template-columns:1fr;max-width:980px}
@media(max-width:860px){.regua{grid-template-columns:1fr}}
@media(max-width:560px){.vista.card{padding-left:12px;padding-right:12px}}
"""


def textos(lg):
    pt = P.ler(AQUI / f"{NOME}.pt.json")
    return pt if lg == "pt" else P._carrega(pt, AQUI / f"{NOME}.{lg}.json", AQUI / f"{NOME}.cache.{lg}.json", lg)


def traduzir(lg):
    P._traduz(P.ler(AQUI / f"{NOME}.pt.json"), AQUI / f"{NOME}.{lg}.json", AQUI / f"{NOME}.cache.{lg}.json", lg)


def bicho_html(id, b, tx, n, A, porque=""):
    """Seção de um robô: números, desenho de referência, desenho × antes × depois por vista, tabela, régua e o que mudou.
    Robô sem malha (o cubo) não tem teto nem "caminho"; com uma vista só, a tabela não leva a linha da média.
    `porque` = a explicação da página do robô quando ele não atingiu o alvo."""
    t = tx.__getitem__
    esc = lambda s: html.escape(s, quote=False)
    m = SEM.medida(id)
    por = {v["vista"]: v for v in m["vistas"]}
    f = lambda v: "—" if v is None else n(v, 3)
    vnome = lambda v: t("vista_" + v.replace("-", "_"))
    cols = [k for k in ("antes", "depois", "teto", "alvo") if m[k] is not None]
    o = [f'<section id="{id}" class="bicho"><div class="wrap">', f'  <span class="chip">{t(id + "_chip")}</span>',
         f'  <h2>{t(id + "_h2")}</h2>', f'  <p class="sub">{t(id + "_sub")}</p>', f'  <div class="grid g{len(cols)}">']
    for k in cols:
        rot = "num_alvo_fixo" if k == "alvo" and m["teto"] is None else "num_antes_1" if k == "antes" and len(b["vistas"]) == 1 else "num_" + k
        o.append(f'    <div class="card numero"><b>{f(m[k])}</b><span>{esc(t(rot))}</span></div>')
    res = f'<strong>{esc(t("res_ok" if m["atingiu"] else "res_nao"))}</strong>'
    if m["caminho"] is not None:
        res += " " + esc(t("res_caminho").replace("[[PCT]]", n(m["caminho"] * 100, 0)))
    if not m["atingiu"] and porque:
        res += " " + porque
    o += ["  </div>", f'  <p class="nota">{res}</p>']
    if b.get("referencia"):
        o += [f'  <h3 class="sep3">{esc(t("h_ref"))}</h3>', f'  <p class="sub">{esc(t("ref_p"))}</p>',
              f'  <figure class="ref"><a href="{A}{b["referencia"]}" target="_blank" rel="noopener"><img src="{A}{b["referencia"]}" alt="{html.escape(t("ref_alt_" + id))}"></a><figcaption>{esc(t("ref_cap"))}</figcaption></figure>']
    o += [f'  <h3 class="sep3">{esc(t("h_vistas"))}</h3>', f'  <p class="sub">{esc(t("vistas_p"))}</p>', '  <div class="vistas">']
    linhas, acima = [], []
    for v in b["vistas"]:
        x = por[v["vista"]]
        nome = vnome(v["vista"])
        figs = [(A + v["imagem_ref"], f'{t("alt_ref")} {nome}', esc(t("rot_ref")))]
        figs += [(A + v["imagem_" + k], f'{t("alt_" + k)} {nome}', f'{esc(t("rot_" + k))} · IoU <b>{f(x[k])}</b>') for k in ("antes", "depois")]
        o.append(f'    <div class="card vista"><h4>{esc(nome)}</h4>{montar.figuras(figs)}</div>')
        g = round(x["depois"], 3) - round(x["antes"], 3)              # ganho = diferença dos números exibidos (a conta fecha para quem lê)
        linhas.append([nome, f(x["antes"]), f(x["depois"]), f(x["teto"]), f(x["alvo"]), ("+" if g >= 0 else "−") + n(abs(g), 3)])
        if x["teto"] is not None and round(x["depois"], 3) > round(x["teto"], 3):
            acima.append(nome)
    media = len(linhas) > 1
    if media:
        g = round(m["depois"], 3) - round(m["antes"], 3)
        linhas.append([t("media"), f(m["antes"]), f(m["depois"]), f(m["teto"]), f(m["alvo"]), ("+" if g >= 0 else "−") + n(abs(g), 3)])
    cab = [t(k) for k in ("th_vista", "th_antes", "th_depois", "th_teto", "th_alvo", "th_ganho")]
    o += ["  </div>", f'  <h3 class="sep3">{esc(t("h_tabela"))}</h3>', f'  <p class="arraste">{esc(t("arraste"))}</p>',
          '  <div class="tabela-wrap"><table class="tabela">', "    <thead><tr>" + "".join(f"<th>{esc(c)}</th>" for c in cab) + "</tr></thead>", "    <tbody>"]
    for i, l in enumerate(linhas):
        forte = media and i == len(linhas) - 1
        o.append("      <tr>" + "".join(f"<td>{'<strong>' + esc(c) + '</strong>' if forte else esc(c)}</td>" for c in l) + "</tr>")
    o.append("    </tbody></table></div>")
    if m["teto"] is None:
        o.append(f'  <p class="nota">{esc(t("sem_teto"))}</p>')
    if acima:
        o.append(f'  <p class="nota">{esc(t("acima_teto").replace("[[VISTAS]]", ", ".join(acima)))}</p>')
    larga = len(b["vistas"]) == 1                                       # régua de uma vista só: imagem larga e baixa, uma por linha
    o += [f'  <h3 class="sep3">{esc(t("h_regua"))}</h3>', f'  <p class="sub">{esc(t("regua_p"))}</p>', f'  <div class="regua{" uma" if larga else ""}">']
    for k in ("antes", "depois"):
        img = A + b["regua_" + k]
        o.append(f'    <figure><a href="{img}" target="_blank" rel="noopener"><img src="{img}" alt="{html.escape(t("regua_alt"))} {html.escape(t("regua_" + k))}"></a>'
                 f'<figcaption><b>{esc(t("regua_" + k))}</b></figcaption></figure>')
    rodas = any(x.startswith("componente roda") for x in P.ler(RAIZ / "comparacao" / "semelhanca.json")["resultados"][id]["depois"]["entram"])
    o += ["  </div>", f'  <p class="nota">{esc(t("regua_nota"))}' + (f' {esc(t("regua_nota_rodas"))}' if rodas else "") + "</p>",
          f'  <h3 class="sep3">{esc(t("h_mudou"))}</h3>', '  <div class="grid g2" style="margin-top:22px">']
    for i in range(1, 5):
        o.append(f'    <div class="card"><h3>{esc(t(f"{id}_m{i}_t"))}</h3><p>{t(f"{id}_m{i}_p")}</p></div>')
    o += ["  </div>", f'  <p class="nota">{esc(t(id + "_falta"))} <a href="../{PASTA[id]}/">{esc(t(id + "_link"))}</a>.</p>', "</div></section>"]
    return "\n".join(o)


def nota_arred(id, tx, n):
    """Se o alvo calculado sem arredondar difere do que dá a conta com os números da tabela, explica (hoje: o dinossauro)."""
    m = SEM.medida(id)
    if m["teto"] is None:                                           # sem malha: o alvo é antes + 0,10, sem arredondamento a explicar
        return ""
    a3, t3 = round(m["antes"], 3), round(m["teto"], 3)
    alvo_r = a3 + (t3 - a3) / 2
    if n(alvo_r + 1e-9, 3) == n(m["alvo"], 3):
        return ""
    s = tx["nota_arred"]
    for k, v in {"NOME": tx["nome_" + id], "ALVO": n(m["alvo"], 3), "A4": n(m["antes"], 4), "T4": n(m["teto"], 4), "A3": n(a3, 3), "T3": n(t3, 3), "ALVO_R": n(alvo_r + 1e-9, 3)}.items():
        s = s.replace(f"[[{k}]]", v)
    return f'<p class="nota">{s}</p>'


def pagina(lg):
    tx = textos(lg)
    dados = P.ler(DADOS)
    n = lambda x, casas=0: (f"{x:.{casas}f}" if lg == "en" else f"{x:.{casas}f}".replace(".", ","))
    head, script = montar.cabeca_rodape()
    corpo = (AQUI / f"{NOME}.html").read_text()
    fundo = "../" if lg == "pt" else "../../"                          # da página até guia/
    A = "assets/" if lg == "pt" else f"../../{NOME}/assets/"           # as imagens ficam só em guia/evolucao/assets/
    lang = "".join(f'<a{" class=\"on\"" if k == lg else ""} href="{"./" if k == lg else fundo + ("" if k == "pt" else k + "/") + NOME + "/"}">{k.upper()}</a>' for k in P.IDIOMAS)
    bichos = dados["bichos"]
    assert set(bichos) <= set(PASTA), f"bicho novo em dados.json sem texto nesta página: {sorted(set(bichos) - set(PASTA))}"
    capa = next(v for v in bichos["capivara"]["vistas"] if v["vista"] == "tres-quartos")
    # as frases do resumo dizem quem atingiu o alvo: se isso mudar, o texto tem de ser reescrito
    quem = {id: SEM.medida(id)["atingiu"] for id in bichos}
    assert quem == {"capivara": True, "dino": True, "cubo": False}, f"mudou quem atinge o alvo ({quem}): reescreva `resumo` e `q_p` em evolucao.pt.json"
    porque = {id: P.Tx(P.Robo(PASTA[id]), lg).d.get("sem_extra", "") for id in bichos if not quem[id]}   # a explicação da página do robô
    bn = dados["banner"]
    esc = lambda s: html.escape(s, quote=False)
    banner = montar.figuras([(A + bn["antes"][lg], tx["bn_alt_antes"], f'<b>{esc(tx["bn_antes"])}</b>: {esc(tx["bn_antes_p"])}'),
                             (fundo + "assets/" + bn["depois"][lg], tx["bn_alt_depois"], f'<b>{esc(tx["bn_depois"])}</b>: {esc(tx["bn_depois_p"])}')], "bn")
    fixos = {"LANG": f'<span class="lang">{lang}</span>', "A": A, "G": "../", "REPO": P.REPO, "BLOB": P.BLOB, "VERSAO": montar.VERSAO,
             "HERO_REF": capa["imagem_ref"], "HERO_ANTES": capa["imagem_antes"], "HERO_DEPOIS": capa["imagem_depois"],
             "BANNER": banner,
             "BICHOS": "\n\n".join(bicho_html(id, b, tx, n, A, porque.get(id, "")) for id, b in bichos.items()),
             "NOTAS_ARRED": "\n  ".join(x for x in (nota_arred(id, tx, n) for id in bichos) if x)}
    for id in ("capivara", "dino", "cubo"):
        m = SEM.medida(id)
        for k in ("antes", "depois", "alvo", "teto"):
            if m[k] is not None:
                fixos[f"{id.upper()}_{k.upper()}"] = n(m[k], 3)
    for id, pasta in PASTA.items():
        j = P.ler(RAIZ / "projetos" / pasta / "montagem.json")["juntas"]
        if "mandibula" in j:                                        # só os bichos têm pescoço e boca citados no texto
            fixos[f"{id.upper()}_PESCOCO"] = n(j["pan"]["origem"][2], 0)
            fixos[f"{id.upper()}_BOCA"] = n(j["mandibula"]["lim"][1], 0)
    faltam = set()

    def troca(mo):
        k = mo.group(1)
        if k in fixos:
            return fixos[k]
        if k not in tx:
            faltam.add(k)
            return mo.group(0)
        return tx[k]

    for _ in range(2):                                              # 2 passadas: o texto traz marcadores de número
        corpo = re.sub(r"\[\[([A-Za-z0-9_]+)\]\]", troca, corpo)
    assert not faltam, f"{lg}: textos faltando {sorted(faltam)}"
    assert "[[" not in corpo, "marcador sobrando"
    head = head.replace("{{PROJETO}} — {{TAGLINE}}", tx["titulo"]).replace("{{META_DESCRICAO}}", html.escape(tx["meta"])).replace("{{SLUG}}", "robos-impressos")
    for k in ("en/", "es/", ""):                                    # hreflang desta página
        head = head.replace(f'/guia/{k}">', f'/guia/{k}{NOME}/">')
    head = head.replace('<html lang="pt-BR">', {"pt": '<html lang="pt-BR">', "en": '<html lang="en">', "es": '<html lang="es">'}[lg])
    i = head.rindex("</style>")
    head = head[:i] + P.CSS + montar.CSS_TRIO + CSS + head[i:]
    pag = head + "\n\n" + corpo + "\n" + script.replace("{{SLUG}}", "robos-impressos")
    assert "{{" not in pag.replace("${{", ""), "placeholder do template sobrando"
    destino = GUIA / (f"{NOME}/index.html" if lg == "pt" else f"{lg}/{NOME}/index.html")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pag)
    print(destino.relative_to(RAIZ), len(pag))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "pagina"
    if cmd == "traduzir":
        for lg in (sys.argv[2:] or ["en", "es"]):
            traduzir(lg)
    elif cmd == "pagina":
        for lg in (sys.argv[2:] or P.IDIOMAS):
            pagina(lg)
    else:
        sys.exit(__doc__)
