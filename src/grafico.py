import matplotlib.pyplot as plt
import networkx as nx
from parser import Aluno, Projeto
from typing import Dict

def desenhar_emparelhamento(emparelhamento: Dict[str, str]):
    """
    Gera a visualização do grafo bipartido com os emparelhamentos realizados.
    """
    G = nx.Graph()

    alunos = list(emparelhamento.keys())
    projetos = list(set(emparelhamento.values()))

    # Adiciona nós bipartidos
    G.add_nodes_from(alunos, bipartite=0)
    G.add_nodes_from(projetos, bipartite=1)

    # Adiciona as arestas aluno -> projeto
    edges = [(aluno, projeto) for aluno, projeto in emparelhamento.items()]
    G.add_edges_from(edges)

    # Posições com layout bipartido
    pos = nx.bipartite_layout(G, alunos)

    # Desenha nós e arestas
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=["lightblue" if node in alunos else "lightgreen" for node in G.nodes()],
        edge_color="gray",
        node_size=1000,
        font_size=10
    )
    plt.title("Emparelhamento Aluno ↔ Projeto")
    plt.axis("off")
    plt.tight_layout()
    plt.show()