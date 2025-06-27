""" 

Separar a lógica da visualização do grafo em tabelas

"""

import networkx as nx
import matplotlib.pyplot as plt

def plotar_emparelhamento(df_projetos, df_alunos, alunos_emparelhados):
    G = nx.Graph()
    
    # Adiciona nós de alunos e projetos
    G.add_nodes_from(df_alunos.index, bipartite=0, node_color='lightblue')
    G.add_nodes_from(df_projetos.index, bipartite=1, node_color='lightgreen')
    
    # Adiciona arestas de emparelhamento
    for aluno, projeto in alunos_emparelhados.items():
        if projeto is not None:
            G.add_edge(aluno, projeto, color='red', width=2)
    
    # Posicionamento dos nós
    pos = {}
    pos.update({aluno: (1, i) for i, aluno in enumerate(df_alunos.index)})
    pos.update({projeto: (2, i) for i, projeto in enumerate(df_projetos.index)})
    
    # Desenha o grafo
    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    widths = [G[u][v]['width'] for u, v in edges]
    
    nx.draw(G, pos, with_labels=True, edge_color=colors, width=widths, 
            node_color=['lightblue' if node in df_alunos.index else 'lightgreen' for node in G.nodes()])
    
    plt.title("Emparelhamento Alunos-Projetos")
    plt.show()