# Plano (etapas com agentes de contexto novo; o orquestrador só confere e encadeia)

| Etapa | O quê | Arquivos que toca | Depende de |
|---|---|---|---|
| E1 | cubo: energia (step-down, UBEC, carregador) + redesenho (cantos, rosto, base baixa e larga) · **cubo-rodas** novo | `cad/modelos/cubo.py`, `cad/modelos/cubo_rodas.py` (novo), `cad/parametros.py`, `cad/comum/componentes.py`, listas MODELOS | — |
| E2 | ferramenta de semelhança (`cad/comparar.py`: máscaras, lado a lado, IoU) + números "antes" (tag v1.0.2) + image-to-3D local (malhas em `referencia/malhas/`) | arquivos NOVOS apenas | — (paralela à E1) |
| E3 | dino + capivara: forma perto da referência (malha ou escultura) + auditoria de energia dos bichos | `cad/comum/base.py`, `bicho.py`, `cad/modelos/{dino,capivara}.py`, seções BASE/PESCOCO/DINO/CAPIVARA | E1 (componentes de energia), E2 |
| E4 | números "depois" de todos + lado a lado final | `cad/comparar.py`, imagens | E1, E3 |
| E5 | reorganizar em `projetos/` + `comum/`, docs por robô, listas de compras com links ML, guia (entrada + 4 páginas × 3 idiomas), banner, renders, v1.1.2, revisor, commit + push | tudo | E4 |
