# Falhas (só acrescentar; ao fim, a menor correção vira linha no FALHAS.md do projeto)

| data | o que quebrou | tentativa | resultado | prompt \| infra |
|---|---|---|---|---|
| 14/11 | E5b: `dino-traseira` sem mapa de balanços: o Blender 4.0 recusa o PLY binário do trimesh (`PLY Importer: failed importing, unknown error`), sempre nessa peça | repetir o render | `mapas_balancos.py` regrava o PLY em ASCII e tenta de novo (o `imprimibilidade.py --mapa` não tem o contorno) | infra |
| 14/11 | E5b: ponto VERDE dentro da pupila da capivara no render de frente (é a placa da câmera da fase 2, `Comp` com cor de placa, vista pelo furo da pupila) | — | `render_blender.py --sem-fase2` no montado, no esqueleto, nas vistas e no banner (o explodido segue mostrando a fase 2) | prompt |
| 14/11 | E5b: robô pequeno no quadro (dino a ~65 %) e mesa da ponta cortada no `<id>-mesas.jpg` | `--zoom` à mão por imagem | enquadramento pelos vértices (perspectiva) e pelas placas (mesas) dentro do `render_blender.py` | prompt |
