import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List

def desenhar_emparelhamento_muitos_para_muitos(
    emparelhamento: Dict[str, List[str]],
    iteracao: int = None,
    lado: str = None,
    ordem: str = None,
):
    """
    Visualiza o grafo bipartido de emparelhamento onde um aluno pode estar em vários projetos.
    
    Parâmetros:
    - emparelhamento: dict de aluno -> lista de projetos
    - iteracao: número da iteração (1 a 10)
    - lado: "aluno" ou "projeto", indica quem propôs nessa iteração
    """
    G = nx.DiGraph()

    alunos = list(emparelhamento.keys())
    projetos = list({p for projetos_alocados in emparelhamento.values() for p in projetos_alocados})

    # Adiciona nós bipartidos
    G.add_nodes_from(alunos, bipartite=0)
    G.add_nodes_from(projetos, bipartite=1)

    for aluno, lista_projetos in emparelhamento.items():
        for projeto in lista_projetos:
            G.add_edge(aluno, projeto)

    # Distancia ajustável
    spacing = 5.0
    # variável para controlar a separação horizontal
    distancia_horizontal = 50  # [alterar se necessário]

    pos = {}
    
    for i, node in enumerate(alunos):
        pos[node] = (0, i * spacing)

    altura_alunos = (len(alunos) - 1) * spacing
    altura_projetos = (len(projetos) - 1) * spacing
    offset_y = (altura_alunos - altura_projetos) / 2

    for i, node in enumerate(projetos):
        # MUDANÇA: Usa a variável 'distancia_horizontal' no lugar do valor '1'
        pos[node] = (distancia_horizontal, (i * spacing) + offset_y)


    tamanho_no_aluno = 2000
    tamanho_no_projeto = 1200
    node_sizes = [tamanho_no_aluno if n in alunos else tamanho_no_projeto for n in G.nodes()]
    node_colors = ["skyblue" if n in alunos else "lightgreen" for n in G.nodes()]
    
    # Título completo da iteração
    titulo = "Grafo de Emparelhamento"
    if iteracao and lado and ordem:
        titulo = f"Iteração {iteracao} — {lado} propõe (ordem: {ordem})"

    plt.figure(figsize=(20, 35))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color="gray",
        font_size=9,
        font_weight="bold",
        width=1.0,
        arrowsize=15,
    )
    
    plt.margins(x=0.1, y=0.05)
    plt.title(titulo, size=20)
    plt.show()