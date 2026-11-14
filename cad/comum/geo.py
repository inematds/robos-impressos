"""Geometria comum: sólidos exatos (Manifold) + pele orgânica por campo de distância.

Convenção de eixos (mm): X = esquerda/direita (plano de simetria X=0), +Y = frente, Z = cima, chão em Z=0.

A pele dos bichos nasce de um campo (união suave de elipsoides) avaliado numa grade e extraído por
marching cubes. O deslocamento (cavidade interna, folga de "abraço" entre cascas) usa a distância
euclidiana REAL até a superfície (árvore k-d nos pontos da malha), não o valor do campo: é isso que
garante a parede mínima. Furos, bolsos, cortes e orelhas são CSG exato do Manifold.
"""
from __future__ import annotations

import numpy as np
from manifold3d import CrossSection, Manifold, Mesh
from scipy import ndimage
from scipy.spatial import cKDTree
from skimage import measure

SEG = 48  # segmentos por círculo nos sólidos exatos


# ---------------------------------------------------------------- sólidos exatos
def caixa(x0, x1, y0, y1, z0, z1) -> Manifold:
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def caixa_c(c, t) -> Manifold:
    """Caixa pelo centro e pelo tamanho total."""
    return Manifold.cube(list(t), True).translate(list(c))


def cil(p0, p1, r, r1=None, seg=SEG) -> Manifold:
    """Cilindro (ou cone, com r1) do ponto p0 ao ponto p1."""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    v = p1 - p0
    h = float(np.linalg.norm(v))
    m = Manifold.cylinder(h, r, r if r1 is None else r1, seg)
    z = np.array([0, 0, 1.0])
    d = v / h
    eixo = np.cross(z, d)
    s = np.linalg.norm(eixo)
    if s < 1e-9:
        R = np.eye(3) if d[2] > 0 else np.diag([1, -1, -1.0])
    else:
        eixo /= s
        ang = np.arctan2(s, float(np.dot(z, d)))
        K = np.array([[0, -eixo[2], eixo[1]], [eixo[2], 0, -eixo[0]], [-eixo[1], eixo[0], 0]])
        R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
    M = np.hstack([R, p0.reshape(3, 1)])
    return m.transform(M)


def esfera(c, r, seg=64) -> Manifold:
    return Manifold.sphere(r, seg).translate(list(c))


def elipsoide(c, r, seg=64) -> Manifold:
    return Manifold.sphere(1.0, seg).scale(list(r)).translate(list(c))


def uniao(*ms) -> Manifold:
    ms = [m for m in ms if m is not None]
    return Manifold.batch_boolean(ms, __import__("manifold3d").OpType.Add) if len(ms) > 1 else ms[0]


def casco(*ms) -> Manifold:
    """Casco convexo de vários sólidos (rampas autoportantes, orelhas)."""
    return Manifold.batch_hull(list(ms))


def girar(m: Manifold, origem, eixo, graus) -> Manifold:
    """Gira em torno de uma reta (ponto + direção)."""
    return m.transform(mat_giro(origem, eixo, graus)[:3, :])


def mat_giro(origem, eixo, graus) -> np.ndarray:
    o = np.asarray(origem, float)
    e = np.asarray(eixo, float)
    e = e / np.linalg.norm(e)
    a = np.radians(graus)
    K = np.array([[0, -e[2], e[1]], [e[2], 0, -e[0]], [-e[1], e[0], 0]])
    R = np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = o - R @ o
    return M


def mat_trans(v) -> np.ndarray:
    M = np.eye(4)
    M[:3, 3] = v
    return M


def aplicar(m: Manifold, M4) -> Manifold:
    return m.transform(np.asarray(M4)[:3, :])


def espelho_x(m: Manifold) -> Manifold:
    return m.mirror([1, 0, 0])


def prisma(pts, eixo: str, a: float, b: float) -> Manifold:
    """Prisma de um polígono 2D extrudado ao longo de um eixo.
    eixo 'z': pts=(x,y) · eixo 'x': pts=(y,z) · eixo 'y': pts=(x,z). De a até b no eixo."""
    pts = [tuple(map(float, q)) for q in pts]
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    if area < 0:
        pts = pts[::-1]
    cs = CrossSection([pts])
    m = Manifold.extrude(cs, b - a).translate([0, 0, a])
    if eixo == "z":
        return m
    if eixo == "x":  # (y,z) no plano, extrusão em x: x<-z, y<-x, z<-y
        return m.transform([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]])
    if eixo == "y":  # (x,z) no plano, extrusão em y
        return m.transform([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0]])
    raise ValueError(eixo)


def secao(cs: CrossSection, eixo: str, a: float, b: float) -> Manifold:
    m = Manifold.extrude(cs, b - a).translate([0, 0, a])
    if eixo == "z":
        return m
    if eixo == "x":
        return m.transform([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]])
    if eixo == "y":
        return m.transform([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0]])
    raise ValueError(eixo)


def limites(m: Manifold):
    b = m.bounding_box()
    return np.array(b[:3]), np.array(b[3:])


def para_numpy(m: Manifold):
    me = m.to_mesh()
    return np.asarray(me.vert_properties)[:, :3].astype(np.float64), np.asarray(me.tri_verts).astype(np.int64)


def de_numpy(v, f) -> Manifold:
    m = Manifold(Mesh(vert_properties=np.asarray(v, np.float32), tri_verts=np.asarray(f, np.uint32)))
    if m.status().name != "NoError":
        raise RuntimeError(f"malha não é variedade: {m.status()}")
    if m.volume() < 0:
        m = Manifold(Mesh(vert_properties=np.asarray(v, np.float32), tri_verts=np.asarray(f, np.uint32)[:, ::-1].copy()))
    return m


# ---------------------------------------------------------------- campos
def sdf_elipsoide(P, c, r):
    """Distância aproximada (1ª ordem perto da superfície) a um elipsoide."""
    q = (P - np.asarray(c, np.float32)) / np.asarray(r, np.float32)
    k0 = np.linalg.norm(q, axis=-1)
    k1 = np.linalg.norm(q / np.asarray(r, np.float32), axis=-1)
    return np.where(k1 > 1e-9, k0 * (k0 - 1.0) / np.maximum(k1, 1e-9), -float(min(r)))


def smin(a, b, k):
    """União suave (polinomial); k = largura da concordância em mm."""
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def campo_blobs(blobs, k=10.0):
    """blobs = [(centro, raios[, k_proprio])]. Devolve f(P) com união suave."""

    def f(P):
        d = None
        for b in blobs:
            c, r = b[0], b[1]
            kk = b[2] if len(b) > 2 else k
            e = sdf_elipsoide(P, c, r)
            d = e if d is None else smin(d, e, kk)
        return d

    return f


class Pele:
    """Sólido orgânico definido por um campo f(P)<0, amostrado numa grade de passo h."""

    def __init__(self, f, lim_min, lim_max, h=1.25, margem=8.0, reduzir=0.75):
        self.h = h
        self.reduzir = reduzir
        lo = np.asarray(lim_min, float) - margem
        hi = np.asarray(lim_max, float) + margem
        self.eixos = [np.arange(lo[i], hi[i] + h, h, dtype=np.float32) for i in range(3)]
        X, Y, Z = np.meshgrid(*self.eixos, indexing="ij")
        P = np.stack([X, Y, Z], axis=-1)
        self.F = f(P).astype(np.float32)
        self.P = P
        self._D = None
        self._v, self._f = self._mc(self.F, 0.0, bruto=True)

    def _mc(self, campo, nivel, bruto=False):
        c = campo.copy()
        # nó com o valor EXATO do nível (acontece na pele em grade, gravada em passos de 0,1 mm) gera triângulo
        # degenerado e a malha deixa de ser variedade: empurra 1 µm para fora
        c[np.abs(c - nivel) < 1e-3] = nivel + 1e-3
        # fecha a superfície na borda da grade
        for ax in range(3):
            sl = [slice(None)] * 3
            for i in (0, -1):
                sl[ax] = i
                c[tuple(sl)] = np.maximum(c[tuple(sl)], nivel + 1.0)
        v, f, _, _ = measure.marching_cubes(c, nivel, spacing=(self.h,) * 3)
        v = v + np.array([e[0] for e in self.eixos])
        if bruto:
            return v, f
        return v, f

    def _manifold(self, v, f) -> Manifold:
        if self.reduzir:
            try:
                import fast_simplification as fs

                v2, f2 = fs.simplify(v.astype(np.float32), f.astype(np.int32), target_reduction=self.reduzir, agg=3)
                return de_numpy(v2, f2)
            except Exception:  # decimação quebrou a variedade: usa a malha cheia
                pass
        return de_numpy(v, f)

    def solido(self) -> Manifold:
        return self._manifold(self._v, self._f)

    def distancia(self, faixa=10.0):
        """Distância com sinal (negativa dentro) REAL até a superfície, numa faixa em torno dela."""
        if self._D is not None and self._faixa >= faixa:
            return self._D
        dentro = self.F < 0
        aprox = (ndimage.distance_transform_edt(~dentro) - ndimage.distance_transform_edt(dentro)) * self.h
        tri = self._v[self._f]
        pts = np.vstack([self._v, tri.mean(axis=1), (tri[:, 0] + tri[:, 1]) / 2, (tri[:, 1] + tri[:, 2]) / 2, (tri[:, 2] + tri[:, 0]) / 2])
        arv = cKDTree(pts)
        sel = np.abs(aprox) < faixa + 2 * self.h
        d, _ = arv.query(self.P[sel], workers=-1)
        D = aprox.astype(np.float32)
        D[sel] = np.where(dentro[sel], -d, d)
        self._D = D
        self._faixa = faixa
        return D

    def deslocado(self, delta) -> Manifold:
        """Sólido deslocado: delta<0 encolhe (cavidade), delta>0 engorda (folga)."""
        D = self.distancia(abs(delta) + 3.0)
        v, f = self._mc(D - delta, 0.0)
        return self._manifold(v, f)

    def casca(self, parede) -> Manifold:
        return self.solido() - self.deslocado(-parede)

    def ponto_na_pele(self, origem, direcao, t0=0.0, t1=400.0):
        """Primeiro ponto, andando de `origem` em `direcao`, onde o campo troca de sinal (interpola)."""
        o = np.asarray(origem, np.float32)
        d = np.asarray(direcao, np.float32)
        d = d / np.linalg.norm(d)
        ts = np.arange(t0, t1, 0.25, dtype=np.float32)
        val = self.f_pontos(o + ts[:, None] * d)
        s = np.sign(val)
        i = np.where(s[1:] != s[:-1])[0]
        if len(i) == 0:
            raise ValueError("raio não cruza a pele")
        i = i[0]
        t = ts[i] + 0.25 * val[i] / (val[i] - val[i + 1])
        return o + t * d

    def f_pontos(self, pts):
        """Interpola o campo da grade em pontos soltos."""
        idx = [(np.asarray(pts)[:, i] - self.eixos[i][0]) / self.h for i in range(3)]
        return ndimage.map_coordinates(self.F, idx, order=1, mode="nearest")


class PeleGrade(Pele):
    """Pele que nasce de uma grade de distância com sinal JÁ PRONTA (malha de image-to-3D convertida por
    cad/pele_malha.py e gravada em cad/peles/<bicho>.npz), em vez de um campo de blobs. Mesma interface da `Pele`
    (`.solido()`, `.deslocado()`, `.ponto_na_pele()`, `.f_pontos()`), então o resto do pipeline de casca não muda.

    Regiões e remendos saem por `combinar`: a função recebe (P, F) da grade e devolve o campo novo. Exemplos:
      torso  = pele.combinar(lambda P, F: np.maximum(F, mascara(P)))          # interseção com uma região (máscara < 0 dentro)
      gordo  = pele.combinar(lambda P, F: smin(F, sdf_elipsoide(P, c, r), 6))  # soma suave de um blob (cobrir uma roda)
    `recortar(lo, hi)` devolve a mesma pele numa grade menor (mais rápido quando a região é só a cabeça, por exemplo)."""

    def __init__(self, eixos, F, reduzir=0.75, P=None):
        self.eixos = [np.asarray(e, np.float32) for e in eixos]
        self.h = float(self.eixos[0][1] - self.eixos[0][0])
        self.reduzir = reduzir
        self.F = np.asarray(F, np.float32)
        if P is None:
            X, Y, Z = np.meshgrid(*self.eixos, indexing="ij")
            P = np.stack([X, Y, Z], axis=-1)
        self.P = P
        self._D = None
        self._v, self._f = self._mc(self.F, 0.0, bruto=True)

    @classmethod
    def de_arquivo(cls, caminho, dy=0.0, dz=0.0, reduzir=0.75):
        """Lê cad/peles/<bicho>.npz. `dy` desloca o bicho em relação ao eixo das rodas (Y=0); `dz` em relação ao chão."""
        z = np.load(caminho)
        d = z["d"].astype(np.float32) * float(z["escala"])
        o, h = z["origem"].astype(np.float64), float(z["passo"])
        eixos = [(o[i] + (0.0, dy, dz)[i] + np.arange(d.shape[i]) * h).astype(np.float32) for i in range(3)]
        return cls(eixos, d, reduzir=reduzir)

    def combinar(self, g, reduzir=None):
        return PeleGrade(self.eixos, g(self.P, self.F), reduzir=self.reduzir if reduzir is None else reduzir, P=self.P)

    def recortar(self, lo, hi, margem=6.0):
        idx = []
        for i in range(3):
            e = self.eixos[i]
            a = max(int(np.searchsorted(e, lo[i] - margem)) - 1, 0)
            b = min(int(np.searchsorted(e, hi[i] + margem)) + 1, len(e))
            idx.append(slice(a, b))
        return PeleGrade([self.eixos[i][idx[i]] for i in range(3)], self.F[tuple(idx)], reduzir=self.reduzir, P=self.P[tuple(idx)])


def limpar(m: Manifold, minimo=5.0) -> Manifold:
    """Tira poeira: componentes soltos com menos de `minimo` mm³ (restos numéricos de booleanas)."""
    cs = m.decompose()
    if len(cs) <= 1:
        return m
    bons = [c for c in cs if abs(c.volume()) >= minimo]
    return Manifold.compose(bons) if len(bons) != len(cs) else m


def medir_parede(ext: Manifold, inte: Manifold, n=4000, semente=0):
    """Espessura REAL da casca: distância de pontos da superfície de dentro até a superfície de fora."""
    import trimesh

    vo, fo = para_numpy(ext)
    vi, fi = para_numpy(inte)
    mo = trimesh.Trimesh(vo, fo, process=False)
    idx = np.random.default_rng(semente).choice(len(vi), min(n, len(vi)), replace=False)
    d = trimesh.proximity.closest_point(mo, vi[idx])[1]
    return {"min": round(float(d.min()), 2), "med": round(float(d.mean()), 2), "max": round(float(d.max()), 2), "amostras": int(len(idx))}


def arestas_beliscadas(m: Manifold):
    """Arestas que, depois de soldar os vértices por posição (como faz o STL), ficam com mais de 2 faces."""
    v, f = para_numpy(m)
    _, inv = np.unique(np.round(v, 4), axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    fi = inv[f]
    e = np.sort(np.vstack([fi[:, [0, 1]], fi[:, [1, 2]], fi[:, [2, 0]]]), axis=1)
    u, primeiro, c = np.unique(e, axis=0, return_index=True, return_counts=True)
    ruins = u[c != 2]
    if len(ruins) == 0:
        return np.zeros((0, 2, 3))
    rep = np.zeros((inv.max() + 1, 3))
    rep[inv] = v
    return rep[ruins]


def desbeliscar(m: Manifold, rodadas=6) -> Manifold:
    """Desfaz arestas beliscadas (dois volumes que só se tocam numa aresta): tenta fundir ou abrir a aresta
    com uma cápsula de 0,2–0,4 mm e fica com a variante que diminui a contagem. Sem isso o STL soldado
    deixa de ser variedade, embora o sólido esteja fechado."""
    rng = np.random.default_rng(7)
    r = 0.2
    for _ in range(rodadas):
        ar = arestas_beliscadas(m)
        if len(ar) == 0:
            return m
        caps = []
        for (a, b) in ar:
            d = b - a
            L = np.linalg.norm(d)
            d = d / L if L > 1e-6 else np.array([0, 0, 1.0])
            j = rng.normal(0, 0.03, 3)
            caps.append(cil(a - d * (r + 0.1) + j, b + d * (r + 0.1) + j, r, seg=10))
        ferr = uniao(*caps) if len(caps) > 1 else caps[0]
        melhor = (len(ar), m)
        for cand in (m + ferr, m - ferr):
            cand = limpar(cand, 0.5)
            n = len(arestas_beliscadas(cand))
            if n < melhor[0]:
                melhor = (n, cand)
        m = melhor[1]
        r *= 1.35
    return m


def engrenagem(z, m, z0, z1, folga=0.2, ang_pressao=20.0, fase=0.0, pts_flanco=8) -> Manifold:
    """Engrenagem de dentes retos (evolvente), eixo em Z na origem, de z0 a z1.
    z = nº de dentes, m = módulo, folga = jogo no primitivo, fase = giro inicial (rad; 0 = um dente em +X)."""
    a = np.radians(ang_pressao)
    rp = m * z / 2
    rb = rp * np.cos(a)
    ra = rp + m
    rf = rp - 1.25 * m
    inv = lambda t: np.tan(t) - t
    sp = np.pi * m / 2 - folga / 2                      # espessura do dente no primitivo
    r0 = max(rb, rf)
    rs = np.linspace(r0, ra, pts_flanco)
    psi = sp / (2 * rp) + inv(a) - inv(np.arccos(np.clip(rb / rs, -1, 1)))   # meio-ângulo do dente em cada raio
    pts = []
    passo = 2 * np.pi / z
    for k in range(z):
        c = fase + k * passo
        if rf < r0:
            pts.append((rf * np.cos(c - psi[0]), rf * np.sin(c - psi[0])))
        for r, p in zip(rs, psi):
            pts.append((r * np.cos(c - p), r * np.sin(c - p)))
        for r, p in zip(rs[::-1], psi[::-1]):
            pts.append((r * np.cos(c + p), r * np.sin(c + p)))
        if rf < r0:
            pts.append((rf * np.cos(c + psi[0]), rf * np.sin(c + psi[0])))
        meio = c + passo / 2                            # fundo entre dentes
        pts.append((rf * np.cos(meio), rf * np.sin(meio)))
    return prisma(pts, "z", z0, z1)


def ret_arredondado(lx, ly, r, seg=24) -> CrossSection:
    """Retângulo centrado com cantos de raio r (seção para extrudar)."""
    from manifold3d import JoinType

    return CrossSection.square([lx - 2 * r, ly - 2 * r], True).offset(r, JoinType.Round, circular_segments=seg * 4)


def maior_corpo(m: Manifold) -> Manifold:
    """Fica só com o maior componente (use logo depois de um corte que pode deixar ilhas)."""
    cs = m.decompose()
    return max(cs, key=lambda c: c.volume()) if len(cs) > 1 else m


def arrastar(m: Manifold, direcao, comprimento=240.0, passo=4.0) -> Manifold:
    """Volume varrido por m ao andar `comprimento` na `direcao` (união de cópias a cada `passo` mm)."""
    d = np.asarray(direcao, float)
    d = d / np.linalg.norm(d)
    return uniao(*[m.translate(list(d * k)) for k in np.arange(0.0, comprimento + passo, passo)])


def _mat_z_para(n, origem) -> np.ndarray:
    """Matriz 3x4 que leva o eixo local +Z para a direção n e a origem local para `origem`."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    z = np.array([0, 0, 1.0])
    eixo = np.cross(z, n)
    s = np.linalg.norm(eixo)
    if s < 1e-9:
        R = np.eye(3) if n[2] > 0 else np.diag([1, -1, -1.0])
    else:
        eixo /= s
        ang = np.arctan2(s, float(np.dot(z, n)))
        K = np.array([[0, -eixo[2], eixo[1]], [eixo[2], 0, -eixo[0]], [-eixo[1], eixo[0], 0]])
        R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
    return np.hstack([R, np.asarray(origem, float).reshape(3, 1)])


def ressalto_nervurado(p, direcao, altura, d_inserto=4.0, n_nervuras=3, d_ext=None, ang0=0.0, nervura_esp=2.4,
                       nervura_alt=None, angulos=None, seg=32) -> Manifold:
    """Ressalto (poste) para inserto/parafuso, com nervuras triangulares a 45° que o ligam à parede.

    p          boca do furo (por onde o parafuso entra), igual ao `p` de `inserto(p, direcao)`
    direcao    para onde o furo ENTRA no ressalto (da boca para a parede em que o ressalto nasce)
    altura     comprimento do ressalto, da boca até a parede (a base fica em p + direcao*altura)
    d_inserto  Ø do furo (inserto M3 = 4,0; piloto M3 = 2,7); o Ø externo padrão é 2,5x isso (mínimo 2x)
    n_nervuras 2 a 4 nervuras; `ang0` (graus) gira a primeira em volta do eixo; `angulos` (lista, graus)
               escolhe cada uma à mão (ex.: ressalto encostado numa parede: só as do lado livre)
    nervura_alt cateto da nervura (padrão: min(altura, 1,5 x Ø externo)); 45° = imprime sem suporte com a
               parede na mesa OU com a boca para cima
    Devolve SÓ o material (ressalto + nervuras): quem chama soma na peça e depois subtrai `inserto(p, direcao)`
    (ou o furo piloto). O referencial das nervuras: ângulo 0 = eixo local +X de `_mat_z_para(-direcao)`.
    """
    d = np.asarray(direcao, float)
    d = d / np.linalg.norm(d)
    de = max(d_ext if d_ext is not None else 2.5 * d_inserto, 2.0 * d_inserto)
    r = de / 2
    h = float(altura)
    hn = min(h, 1.5 * de) if nervura_alt is None else min(h, float(nervura_alt))
    corpo = Manifold.cylinder(h, r, r, seg)
    angs = angulos if angulos is not None else [ang0 + k * 360.0 / n_nervuras for k in range(n_nervuras)]
    partes = [corpo]
    for a in angs:
        tri = prisma([(r - 0.6, 0.0), (r + hn, 0.0), (r - 0.6, hn)], "y", -nervura_esp / 2, nervura_esp / 2)
        partes.append(tri.rotate([0, 0, float(a)]))
    m = uniao(*partes)
    base = np.asarray(p, float) + d * h
    return m.transform(_mat_z_para(-d, base))


def berco_modulo(cx, folga=0.4, alt=4.0, esp=1.6, canto=7.0, fita=(4.4, 2.2), piso=3.0, canal=1.2, pontas=False):
    """Berço para módulo eletrônico SEM furo confiável (step-down, UBEC, carregador, BMS): 4 cantoneiras baixas em
    volta da caixa do módulo + 2 rasgos para UMA abraçadeira de nylon de 3,6 mm que passa por cima do módulo e por
    baixo do piso. Não depende de furo de placa. Tudo vertical: imprime sem suporte com o piso na mesa.

    cx     (comprimento, largura, altura) do módulo, ou o próprio namespace de parametros.py (usa `.cx`)
    Local  igual ao de componentes.modulo(): centrado em XY, comprimento em X, z=0 = face de cima do piso (assento)
    alt    altura das cantoneiras; esp = espessura; canto = comprimento de cada perna do "L"
    fita   (largura, espessura) do rasgo da abraçadeira; piso = espessura do piso que os rasgos atravessam
    canal  profundidade do canal por baixo do piso, entre os dois rasgos, para a abraçadeira não fazer calço
           (0 = sem canal: use quando há vão livre embaixo, como num deck). O canal é uma ponte de 4,4 mm: imprime.
    pontas True = rasgos além das duas PONTAS do comprimento (a abraçadeira corre ao comprido): para módulo encostado
           numa parede lateral. fita=None = sem abraçadeira (só as cantoneiras; prenda com fita dupla-face): corte = None.
    Devolve (soma, corte): some `soma` na peça e depois subtraia `corte`, os dois já levados ao lugar com
    .transform()/.translate(), igual ao envelope do componente.
    """
    L, W, _ = getattr(cx, "cx", cx)
    hx, hy = L / 2 + folga, W / 2 + folga
    partes = []
    for sx in (1, -1):
        for sy in (1, -1):
            x0, x1 = sorted((sx * (hx - canto), sx * (hx + esp)))
            y0, y1 = sorted((sy * hy, sy * (hy + esp)))
            partes.append(caixa(x0, x1, y0, y1, -0.01, alt))                 # perna ao longo de X
            x0, x1 = sorted((sx * hx, sx * (hx + esp)))
            y0, y1 = sorted((sy * (hy - min(canto, hy)), sy * (hy + esp)))
            partes.append(caixa(x0, x1, y0, y1, -0.01, alt))                 # perna ao longo de Y
    soma = uniao(*partes)
    if fita is None:
        return soma, None
    ys = (hx if pontas else hy) + esp + 0.3 + fita[1] / 2                    # rasgo logo por fora das cantoneiras
    cortes = [caixa(-fita[0] / 2, fita[0] / 2, s * ys - fita[1] / 2, s * ys + fita[1] / 2, -piso - 0.01, 0.01) for s in (1, -1)]
    if canal > 0:
        cortes.append(caixa(-fita[0] / 2, fita[0] / 2, -ys - fita[1] / 2, ys + fita[1] / 2, -piso - 0.01, -piso + canal))
    corte = uniao(*cortes)
    return soma, (corte.rotate([0, 0, 90]) if pontas else corte)
