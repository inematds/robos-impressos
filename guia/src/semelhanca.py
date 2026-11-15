#!/usr/bin/env python3
"""Números de semelhança (IoU de silhueta) de um robô, lidos de comparacao/semelhanca.json.

Uma conta só para as páginas dos robôs, a entrada do guia e a página de evolução, igual à de
comum/cad/tabelas.py › linhas_semelhanca: teto = a melhor malha crua (maior média); alvo = metade do caminho entre o
antes e o teto, ou antes + 0,10 quando não há malha; tudo calculado com os valores SEM arredondar (por isso o alvo do
dinossauro é 0,855 e não 0,856, que é o que dá a mesma conta feita com os números já arredondados da tabela).

Uso (conferência): .venv/bin/python guia/src/semelhanca.py [id]
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def medida(id):
    """dict(antes, depois, teto, alvo, atingiu, novo, malha, vistas=[dict(vista, antes, depois, teto, alvo)]).
    Campos sem medida vêm None. `novo` = robô sem "antes" (não tem meta)."""
    r = json.loads((RAIZ / "comparacao" / "semelhanca.json").read_text())["resultados"].get(id, {})
    malhas = {k: v for k, v in r.items() if k.startswith("malha")}
    nome_teto = max(malhas, key=lambda k: malhas[k]["media"]) if malhas else None
    antes, depois = r.get("antes", {}).get("media"), r.get("depois", {}).get("media")
    teto = malhas[nome_teto]["media"] if nome_teto else None
    alvo = None if antes is None else (antes + (teto - antes) / 2 if teto else antes + 0.10)
    por = lambda k: {v["vista"]: v["iou"] for v in r.get(k, {}).get("vistas", [])}
    va, vd, vt = por("antes"), por("depois"), (por(nome_teto) if nome_teto else {})
    vistas = []
    for v in (r.get("depois") or r.get("antes") or {}).get("vistas", []):
        n = v["vista"]
        a, t = va.get(n), vt.get(n)
        vistas.append(dict(vista=n, antes=a, depois=vd.get(n), teto=t,
                           alvo=None if a is None else (a + (t - a) / 2 if t else a + 0.10)))
    return dict(antes=antes, depois=depois, teto=teto, alvo=alvo, novo=antes is None, malha=nome_teto,
                atingiu=None if (alvo is None or depois is None) else depois >= alvo,
                caminho=None if not (teto and antes is not None and depois is not None) else (depois - antes) / (teto - antes),
                vistas=vistas)


if __name__ == "__main__":
    for m in (sys.argv[1:] or ["dino", "capivara", "cubo", "cubo_rodas"]):
        x = medida(m)
        f = lambda v: "—" if v is None else f"{v:.3f}"
        print(f"{m}: antes {f(x['antes'])} depois {f(x['depois'])} teto {f(x['teto'])} alvo {f(x['alvo'])} atingiu={x['atingiu']}")
        for v in x["vistas"]:
            print(f"   {v['vista']}: {f(v['antes'])} → {f(v['depois'])} (teto {f(v['teto'])}, alvo {f(v['alvo'])})")
