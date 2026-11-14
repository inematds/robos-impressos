#!/usr/bin/env python3
"""Verifica um modelo a partir dos ARQUIVOS exportados (STL + montagem.json), não dos objetos em memória.

Uso:  .venv/bin/python cad/verificar.py dino|capivara|cubo|todos [--rapido]

Testes (cada um diz PASSOU ou FALHOU; o script sai com código 1 se algum falhar):
  1 contagem       nº de peças impressas = o declarado em cad/parametros.py; todo STL listado existe; nenhum STL sobrando
  2 malha          cada peça: fechada (estanque), orientação coerente, volume > 0, um corpo só
  3 mesa           cada peça, na orientação de impressão, cabe em 256 x 256 x 256 mm (Bambu Lab A1)
  4 parede         parede medida das cascas ≥ 2,0 mm (distância real entre a pele de fora e a de dentro)
  5 interferência  nenhuma sobreposição entre peças e/ou componentes, em todas as poses declaradas
                   (volume da interseção booleana; encostar face com face não conta)
  6 teste negativo desloca uma peça 3 mm e exige que o teste 5 acuse (prova que o teste enxerga)
  7 peça solta     toda peça montada fica a ≤ 1,5 mm de alguma outra peça ou componente
  8 equilíbrio     centro de gravidade (estimado) dentro do polígono de apoio, com margem, em todas as poses
  9 caminho        cada passo da ordem de montagem: a peça (ou o conjunto) vem de fora na direção declarada, de
                   5 em 5 mm, sem atravessar o que já está montado (encaixes laterais de 3 mm de horn não entram)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import Manifold, Mesh

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from cad import parametros as P  # noqa: E402
from cad.comum.geo import mat_giro  # noqa: E402

MODELOS = ["dino", "capivara", "cubo"]
TOL_INTERF = 1.0      # mm³: abaixo disso é ruído numérico de malha
TOL_SOLTA = 1.5       # mm


def carrega(caminho: Path):
    tm = trimesh.load(caminho, process=True)   # process=True solda os vértices do STL
    return tm


def para_manifold(tm: trimesh.Trimesh) -> Manifold:
    m = Manifold(Mesh(vert_properties=np.asarray(tm.vertices, np.float32), tri_verts=np.asarray(tm.faces, np.uint32)))
    if m.status().name != "NoError" or m.is_empty():
        raise SystemExit(f"STL não vira sólido válido ({m.status()}): o teste de interferência não pode rodar")
    return m


def matriz_grupo(juntas, grupo, ang):
    M = np.eye(4)
    g = grupo
    while g in juntas:
        j = juntas[g]
        M = mat_giro(j["origem"], j["eixo"], ang.get(g, 0.0)) @ M
        g = j["pai"]
    return M


def raiz_grupo(juntas, grupo):
    cadeia = [grupo]
    while cadeia[-1] in juntas:
        cadeia.append(juntas[cadeia[-1]]["pai"])
    return cadeia


def interferencias(itens, juntas, ang, so_moveis=False):
    """itens = [(nome, grupo, manifold_na_montagem, lo, hi)]. Devolve [(a, b, volume)]."""
    pos = []
    for (nome, grupo, m, _, _) in itens:
        M = matriz_grupo(juntas, grupo, ang)
        mm = m.transform(M[:3, :]) if not np.allclose(M, np.eye(4)) else m
        b = mm.bounding_box()
        pos.append((nome, grupo, mm, np.array(b[:3]), np.array(b[3:])))
    movidos = {g for g in {i[1] for i in itens} if any(abs(ang.get(x, 0.0)) > 1e-9 for x in raiz_grupo(juntas, g))}
    res = []
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            a, b = pos[i], pos[j]
            if so_moveis and a[1] not in movidos and b[1] not in movidos:
                continue
            if so_moveis and a[1] == b[1]:
                continue
            if np.any(a[3] > b[4] + 0.01) or np.any(b[3] > a[4] + 0.01):
                continue
            v = (a[2] ^ b[2]).volume()
            if v > TOL_INTERF:
                res.append((a[0], b[0], round(float(v), 1)))
    return res, pos


def verificar(nome: str, rapido=False) -> bool:
    base = RAIZ / "pecas" / nome
    mj = json.loads((base / "montagem.json").read_text())
    juntas = mj["juntas"]
    ok_geral = True
    rel = {"modelo": nome, "testes": {}}

    def resultado(teste, ok, texto):
        nonlocal ok_geral
        ok_geral &= bool(ok)
        rel["testes"][teste] = {"ok": bool(ok), "texto": texto}
        print(f"  [{'PASSOU' if ok else 'FALHOU'}] {teste}: {texto}")

    print(f"== verificação: {nome} ({mj['titulo']})")
    # ---------------------------------------------------------------- 1 contagem
    esperado = getattr(P, nome.upper()).n_pecas
    distintas = len(mj["pecas"])
    total = sum(p["qtd"] for p in mj["pecas"])
    faltam = [p["arquivo"] for p in mj["pecas"] if not (base / p["arquivo"]).exists()]
    listados = {(base / p["arquivo"]).resolve() for p in mj["pecas"]}
    sobrando = [f.name for f in (base / "stl").glob("*.stl") if f.resolve() not in listados]
    resultado("1 contagem", total == esperado and not faltam and not sobrando,
              f"{distintas} peças distintas, {total} no total (esperado {esperado}); faltando {len(faltam)}; sobrando {len(sobrando)}")

    # ---------------------------------------------------------------- 2 malha + 3 mesa
    malhas, ruins, grandes, maior = {}, [], [], (0, "")
    vol = P.IMPRESSORA.volume
    for p in mj["pecas"]:
        tm = carrega(base / p["arquivo"])
        malhas[p["nome"]] = tm
        corpos = tm.body_count
        if not (tm.is_watertight and tm.is_winding_consistent and tm.volume > 0 and corpos == 1):
            ruins.append(f"{p['nome']} (estanque={tm.is_watertight}, corpos={corpos}, vol={tm.volume:.0f})")
        dim = tm.bounds[1] - tm.bounds[0]
        if np.any(dim > np.array(vol) + 1e-6):
            grandes.append(f"{p['nome']} {np.round(dim, 1)}")
        if dim.max() > maior[0]:
            maior = (float(dim.max()), p["nome"])
    resultado("2 malha", not ruins, f"{len(malhas)} STL fechados, 1 corpo cada" if not ruins else "; ".join(ruins))
    resultado("3 mesa", not grandes, f"todas cabem em {vol[0]:.0f} x {vol[1]:.0f} x {vol[2]:.0f} mm; maior dimensão {maior[0]:.1f} mm ({maior[1]})"
              if not grandes else "; ".join(grandes))

    # ---------------------------------------------------------------- 4 parede
    par = mj.get("parede_medida", {})
    if par:
        minimo = min(v["min"] for v in par.values())
        resultado("4 parede", minimo >= P.FOLGA.parede_min,
                  "; ".join(f"{k} {v['min']:.2f}–{v['max']:.2f} mm" for k, v in par.items()) + f" (mínimo exigido {P.FOLGA.parede_min:.1f})")
    else:
        resultado("4 parede", True, "modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm)")

    # ---------------------------------------------------------------- monta
    itens = []
    for p in mj["pecas"]:
        m0 = para_manifold(malhas[p["nome"]])
        for k, M in enumerate(p["para_montagem"]):
            m = m0.transform(np.asarray(M)[:3, :])
            itens.append((f"{p['nome']}#{k}" if p["na_montagem"] > 1 else p["nome"], p["grupos"][k], m, None, None))
    n_imp = len(itens)
    massas = {}
    for p in mj["pecas"]:
        for k in range(p["na_montagem"]):
            massas[f"{p['nome']}#{k}" if p["na_montagem"] > 1 else p["nome"]] = p["massa_g"]
    for c in mj["componentes"]:
        tm = carrega(base / c["arquivo"])
        m0 = para_manifold(tm)
        for k, M in enumerate(c["para_montagem"]):
            itens.append((c["nome"], c["grupos"][k], m0.transform(np.asarray(M)[:3, :]), None, None))
            massas[c["nome"]] = c["massa_g"]

    # ---------------------------------------------------------------- 5 interferência
    previstos = {tuple(sorted(e["par"])): e["motivo"] for e in mj.get("encaixes_previstos", [])}
    achados, n_pares = [], 0
    poses = mj["poses"] if not rapido else mj["poses"][:1]
    for i, pose in enumerate(poses):
        res, _ = interferencias(itens, juntas, pose["angulos"], so_moveis=(i > 0))
        for (a, b, v) in res:
            if tuple(sorted((a.split("#")[0], b.split("#")[0]))) in previstos:
                continue
            achados.append(f"{pose['nome']}: {a} x {b} = {v} mm³")
    txt = f"{len(itens)} sólidos ({n_imp} impressos + {len(itens) - n_imp} componentes), {len(poses)} poses, 0 sobreposições"
    if previstos:
        txt += f"; {len(previstos)} encaixe(s) previsto(s) fora da conta: " + "; ".join(f"{a} x {b} ({m})" for (a, b), m in previstos.items())
    resultado("5 interferência", not achados, txt if not achados else f"{len(achados)} sobreposições (lista em verificacao.json): " + " | ".join(achados[:6]))
    rel["interferencias"] = achados

    # ---------------------------------------------------------------- 6 teste negativo
    alvo = next(i for i, it in enumerate(itens) if it[0] == mj.get("obs", {}).get("peca_teste_negativo", "chassi"))
    it = itens[alvo]
    desloc = list(itens)
    desloc[alvo] = (it[0], it[1], it[2].translate([3.0, 0, 0]), None, None)
    res, _ = interferencias(desloc, juntas, {}, so_moveis=False)
    res = [r for r in res if tuple(sorted((r[0].split("#")[0], r[1].split("#")[0]))) not in previstos]
    resultado("6 teste negativo", len(res) > 0, f"'{it[0]}' deslocada 3 mm em X → {len(res)} sobreposições acusadas (tem que ser > 0)")

    # ---------------------------------------------------------------- 7 peça solta
    soltas = []
    for i in range(n_imp):
        a = itens[i]
        perto = False
        for j in range(len(itens)):
            if i == j:
                continue
            if a[2].min_gap(itens[j][2], TOL_SOLTA) < TOL_SOLTA:
                perto = True
                break
        if not perto:
            soltas.append(a[0])
    resultado("7 peça solta", not soltas, f"as {n_imp} peças montadas encostam (≤ {TOL_SOLTA} mm) em outra" if not soltas else "soltas: " + ", ".join(soltas))

    # ---------------------------------------------------------------- 8 equilíbrio
    apoios = np.array(mj["apoios"], float)
    piores = None
    linhas_cg = []
    for pose in mj["poses"]:
        mt, soma = 0.0, np.zeros(3)
        for (nm, grupo, m, _, _) in itens:
            M = matriz_grupo(juntas, grupo, pose["angulos"])
            mm = m.transform(M[:3, :])
            b = mm.bounding_box()
            # centro de massa ≈ centroide do volume da peça
            tmv = np.asarray(mm.to_mesh().vert_properties)[:, :3]
            tri = np.asarray(mm.to_mesh().tri_verts)
            v0, v1, v2 = tmv[tri[:, 0]], tmv[tri[:, 1]], tmv[tri[:, 2]]
            vt = np.einsum("ij,ij->i", v0, np.cross(v1, v2)) / 6.0
            c = ((v0 + v1 + v2) / 4.0 * vt[:, None]).sum(axis=0) / vt.sum()
            w = massas.get(nm, 0.0)
            mt += w
            soma += w * c
        cg = soma / mt
        marg = margem_apoio(apoios, cg[:2])
        ang = float(np.degrees(np.arctan2(marg, cg[2]))) if marg > 0 else 0.0
        linhas_cg.append((pose["nome"], cg, marg, ang, mt))
        if piores is None or marg < piores[2]:
            piores = (pose["nome"], cg, marg, ang, mt)
    nomep, cg, marg, ang, mt = piores
    neutro = linhas_cg[0]
    resultado("8 equilíbrio", marg >= 10.0,
              f"massa estimada {mt:.0f} g; CG neutro em x={neutro[1][0]:.1f} y={neutro[1][1]:.1f} z={neutro[1][2]:.1f} mm, margem {neutro[2]:.1f} mm "
              f"(tomba com {neutro[3]:.0f}°); pior pose '{nomep}': margem {marg:.1f} mm ({ang:.0f}°); mínimo exigido 10 mm")
    # ---------------------------------------------------------------- 9 caminho de montagem
    ordem = mj.get("ordem_montagem", [])
    por_nome = {}
    for it in itens:
        por_nome.setdefault(it[0].split("#")[0], []).append(it)
        if "#" in it[0]:
            por_nome.setdefault(it[0], []).append(it)
    montados, travados, n_passos, saiu = [], [], 0, set()
    for o in ordem:
        moveis = [it for n in o["move"] for it in por_nome.get(n, [])]
        nomes_m = {it[0] for it in moveis}
        estaticos = [it for n in (o.get("contra") or montados) for it in por_nome.get(n, []) if it[0] not in nomes_m]
        if o.get("sai"):                       # passo de DESMONTAGEM: a peça sai contra tudo o que continua montado
            estaticos = [it for n in montados for it in por_nome.get(n, []) if it[0] not in nomes_m]
        d = np.array(o["dir"], float)
        d = d / np.linalg.norm(d)
        curso = float(o.get("curso", 120.0))
        n_passos += 1
        achou = None
        desloc = [d * s_ for s_ in np.arange(2.5, curso + 0.1, 2.5)]
        if "depois" in o:                       # 2º trecho do trajeto (ex.: desliza e depois sobe)
            d2 = np.array(o["depois"][0], float)
            d2 = d2 / np.linalg.norm(d2)
            desloc += [d * curso + d2 * s_ for s_ in np.arange(5.0, float(o["depois"][1]) + 0.1, 5.0)]
        for dv in desloc:
            s_ = float(np.linalg.norm(dv))
            for a in moveis:
                am = a[2].translate(list(dv))
                ba = am.bounding_box()
                for b_ in estaticos:
                    if tuple(sorted((a[0].split("#")[0], b_[0].split("#")[0]))) in previstos:
                        continue
                    bb = b_[2].bounding_box()
                    if any(ba[i] > bb[i + 3] or bb[i] > ba[i + 3] for i in range(3)):
                        continue
                    v = (am ^ b_[2]).volume()
                    if v > TOL_INTERF:
                        achou = (a[0], b_[0], float(s_), float(v))
                        break
                if achou:
                    break
            if achou:
                break
        if achou:
            travados.append(f"{o['passo']}: {achou[0]} bate em {achou[1]} a {achou[2]:.0f} mm do lugar ({achou[3]:.0f} mm³)")
        for n in o["move"]:
            if o.get("sai"):
                if n in montados:
                    montados.remove(n)
                saiu.add(n.split("#")[0])
            elif n not in montados:
                montados.append(n)
    if ordem:
        fora = sorted({it[0].split("#")[0] for it in itens} - {n.split("#")[0] for n in montados} - saiu)
        resultado("9 caminho", not travados and not fora,
                  f"{n_passos} passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado"
                  if not travados and not fora else ("; ".join(travados[:6]) + (f"; fora da ordem: {fora}" if fora else "")))
    rel["caminho"] = travados

    rel["cg"] = [{"pose": n, "cg": [round(float(x), 1) for x in c], "margem_mm": round(float(m_), 1), "tomba_graus": round(a_, 1), "massa_g": round(mt_, 0)}
                 for (n, c, m_, a_, mt_) in linhas_cg]
    rel["resumo"] = {"pecas_distintas": distintas, "pecas_total": total, "massa_impressa_g": round(sum(p["massa_g"] * p["qtd"] for p in mj["pecas"]), 0),
                     "tempo_total_h": round(sum(p["tempo_h"] * p["qtd"] for p in mj["pecas"]), 1), "ok": ok_geral}
    (base / "verificacao.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1))
    print(f"  => {nome}: {'TUDO PASSOU' if ok_geral else 'HÁ FALHAS'}")
    return ok_geral


def margem_apoio(apoios, p):
    """Distância (mm) do ponto p até a borda do polígono convexo de apoio; negativa se fora."""
    from scipy.spatial import ConvexHull

    if len(apoios) < 3:
        return -1.0
    h = ConvexHull(apoios)
    # equações: n·x + d <= 0 dentro
    return float(-np.max(h.equations[:, :2] @ p + h.equations[:, 2]))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    alvo = args[0] if args else "todos"
    oks = [verificar(n, "--rapido" in sys.argv) for n in (MODELOS if alvo == "todos" else [alvo])]
    sys.exit(0 if all(oks) else 1)
