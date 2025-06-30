import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List


def desenhar_emparelhamento_muitos_para_muitos(emparelhamento: Dict[str, List[str]],iteracao: int = None,lado: str = None, ordem: str = None):
    """
    Visualiza o grafo bipartido de emparelhamento onde um aluno pode estar em vários projetos.
    
    Parâmetros:
    - emparelhamento: dict de aluno -> lista de projetos
    - iteracao: número da iteração (1 a 10)
    - lado: "aluno" ou "projeto", indica quem propôs nessa iteração
    """
    G = nx.Graph()

    alunos = list(emparelhamento.keys())
    projetos = list({p for projetos in emparelhamento.values() for p in projetos})

    # Adiciona nós bipartidos
    G.add_nodes_from(alunos, bipartite=0)
    G.add_nodes_from(projetos, bipartite=1)

    # Adiciona arestas aluno → projeto
    for aluno, lista_projetos in emparelhamento.items():
        for projeto in lista_projetos:
            G.add_edge(aluno, projeto)

     # Layout com mais espaçamento manual
    spacing = 1.5
    pos = {}
    for i, node in enumerate(alunos):
        pos[node] = (0, i * spacing)
    for i, node in enumerate(projetos):
        pos[node] = (10, i * spacing)

    node_colors = ["skyblue" if n in alunos else "lightgreen" for n in G.nodes()]

    # Título completo da iteração
    titulo = "Grafo de Emparelhamento"
    if iteracao and lado and ordem:
        titulo = f"Iteração {iteracao} — {lado} propõe (ordem: {ordem})"

    plt.figure(figsize=(18, 30))  # pode ajustar a altura
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color="gray",
        node_size=800,
        font_size=8
    )
    plt.title(titulo)
    plt.axis("off")
    plt.tight_layout()
    plt.show()