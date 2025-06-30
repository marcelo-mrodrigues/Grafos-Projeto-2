import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List


def desenhar_emparelhamento_muitos_para_muitos(emparelhamento: Dict[str, List[str]]):
    """
    Visualiza o grafo bipartido de emparelhamento onde um aluno pode estar em vários projetos.
    """
    G = nx.Graph()

    alunos = list(emparelhamento.keys())
    projetos = list({p for projetos in emparelhamento.values() for p in projetos})

    # Adiciona nós bipartidos
    G.add_nodes_from(alunos, bipartite=0)
    G.add_nodes_from(projetos, bipartite=1)

    # Adiciona arestas aluno → projeto (muitos para muitos)
    for aluno, projetos in emparelhamento.items():
        for projeto in projetos:
            G.add_edge(aluno, projeto)

    # Layout bipartido
    pos = nx.bipartite_layout(G, alunos)

    # Cores: azul para alunos, verde para projetos
    node_colors = [
        "skyblue" if node in alunos else "lightgreen" for node in G.nodes()
    ]

    # Desenho
    plt.figure(figsize=(14, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color="gray",
        node_size=800,
        font_size=8
    )
    plt.title("Grafo de Emparelhamento (Muitos para Muitos)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()