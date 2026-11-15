#!/usr/bin/env python3
"""Ferramentas de desenho dos esquemas de ligação (SVG) dos robôs que não são o cubo de mesa.
O desenho do cubo continua em pagina_robo.py › esquema_svg (não mexer: está publicado).

Uso, num módulo esquema_<robô>.py:
    from esquema_base import Desenho
    def svg(X, R):                      # X = textos do idioma (X.t("sv_...")), R = o robô (R.d = <robô>.dados.json)
        D = Desenho(760, 1100, X.t("sv_titulo"), X.t("sv_aviso"))
        D.fio([(x, y), ...], "v")       # fios primeiro: as pontas ficam por baixo das caixas
        D.caixa(x, y, w, h); D.txt(x, y, "texto")
        return D.svg()
Todo texto que aparece vem das chaves sv_* de guia/src/robos/<robô>.pt.json (elas passam pelo tradutor).
Os fios seguem a lista `ligacoes` do <robô>.dados.json: mudou um, mude o outro.
"""
import html

# v vermelho (positivo) · p preto (negativo) · a amarelo (ponto do meio) · g verde e z azul (serial) · l laranja (cabo
# de servo) · c cinza (encaixe) · r roxo (sinais do driver dos motores) · m marrom (fios do motor)
COR = {"v": "#d62828", "p": "#22232b", "a": "#e3a500", "g": "#2a9d4b", "z": "#1d6fd6", "l": "#e07a1f", "c": "#8a8f9c",
       "r": "#7b3fb5", "m": "#8a5a2b"}
TINTA = "#1a1a22"
AVISO = "#a14a00"
CINZA = "#4c4f5c"
ZONA = "#6b7080"
# fundos de caixa: placa comum, placa de controle (verde), servo/motor (laranja claro), peça pequena (amarelo), neutro
F_PLACA, F_CTRL, F_MOTOR, F_PECA, F_NEUTRO, F_CEL, F_AZUL = "#f4f5f8", "#eef6ee", "#fdebd9", "#fff4d6", "#e8eaf0", "#dfe6f3", "#e6f1ff"
B_PLACA, B_CTRL, B_MOTOR, B_PECA, B_CEL, B_AZUL = "#3b3d4a", "#2f6b3a", "#a8581a", "#a17400", "#6b7896", "#3565a8"


class Desenho:
    def __init__(self, larg, alt, titulo, aviso):
        self.w, self.h, self.titulo = larg, alt, titulo
        self.o = [f'<rect x="0" y="0" width="{larg}" height="{alt}" fill="#ffffff"/>']
        self.txt(20, 28, titulo, 17, peso=700)
        self.txt(20, 47, aviso, 12, cor=AVISO, peso=600)

    def txt(self, x, y, s, tam=12, anc="start", peso=400, cor=TINTA, extra=""):
        self.o.append(f'<text x="{x}" y="{y}" font-size="{tam}" text-anchor="{anc}" font-weight="{peso}" fill="{cor}"{extra}>{html.escape(s, quote=False)}</text>')

    def caixa(self, x, y, w, h, fundo=F_PLACA, borda=B_PLACA, raio=8, traco=""):
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raio}" fill="{fundo}" stroke="{borda}" stroke-width="1.5"{traco}/>')

    def zona(self, x, y, w, h, rotulo):
        """Moldura tracejada de uma região do robô (corpo, cabeça...), com o nome no canto."""
        self.caixa(x, y, w, h, fundo="none", borda="#9aa0ad", raio=12, traco=' stroke-dasharray="6 5"')
        self.txt(x + 12, y + 17, rotulo, 11, cor=ZONA, peso=700, extra=' letter-spacing="1.5"')

    def faixa(self, x, y, w, h, rotulo):
        """Faixa cheia (passagem de fios entre duas regiões)."""
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#e9ecf2"/>')
        self._faixas = getattr(self, "_faixas", []) + [(x + w / 2, y + h / 2 + 4, rotulo)]

    def fio(self, pts, cor, esp=3.2):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.o.append(f'<polyline points="{p}" fill="none" stroke="#fff" stroke-width="{esp + 3.6}" stroke-linejoin="round"/>')
        self.o.append(f'<polyline points="{p}" fill="none" stroke="{COR[cor]}" stroke-width="{esp}" stroke-linejoin="round" stroke-linecap="round"/>')

    def no(self, x, y, cor):
        self.o.append(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{COR[cor]}" stroke="#fff" stroke-width="1"/>')

    def rotulos_das_faixas(self):
        """Chame depois dos fios: o nome da faixa fica por cima deles."""
        for x, y, s in getattr(self, "_faixas", []):
            self.txt(x, y, s, 11, anc="middle", cor=B_PLACA, peso=700)

    def bloco(self, x, y, w, h, titulo, sub="", fundo=F_PLACA, borda=B_PLACA, tam=12, cx=None, cy=None, cor_sub=CINZA):
        """Caixa com título (e subtítulo) centrados; cx, cy deslocam o centro do texto."""
        self.caixa(x, y, w, h, fundo, borda)
        cx = x + w / 2 if cx is None else cx
        cy = y + h / 2 + (0 if sub else 4) if cy is None else cy
        self.txt(cx, cy, titulo, tam, anc="middle", peso=700)
        if sub:
            self.txt(cx, cy + 15, sub, 10.5, anc="middle", cor=cor_sub, peso=600 if cor_sub == AVISO else 400)

    def pino(self, x, y, s, anc="middle", cor=TINTA, tam=11):
        """Nome de um borne, ilha ou pino, em negrito."""
        self.txt(x, y, s, tam, anc=anc, peso=700, cor=cor)

    def legenda(self, y, itens, linhas=()):
        """itens = [(cores, texto)] em 3 colunas; cores = letras de COR ("" = ponto cheio). linhas = frases em negrito."""
        for k, (cores, s) in enumerate(itens):
            x, yy = 20 + 245 * (k % 3), y + 22 * (k // 3)
            if not cores:
                self.o.append(f'<circle cx="{x + 12}" cy="{yy - 4}" r="4.6" fill="#22232b"/>')
            for i, c in enumerate(cores):
                w = 24 / len(cores)
                self.o.append(f'<line x1="{x + i * w}" y1="{yy - 4}" x2="{x + (i + 1) * w}" y2="{yy - 4}" stroke="{COR[c]}" stroke-width="4"/>')
            self.txt(x + 32, yy, s, 11.5)
        y += 22 * ((len(itens) + 2) // 3) + 2
        for s in linhas:
            self.txt(20, y, s, 11.5, peso=600)
            y += 20

    def svg(self):
        corpo = "\n".join(self.o)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif" role="img"><title>{html.escape(self.titulo, quote=False)}</title>\n{corpo}\n</svg>\n')
