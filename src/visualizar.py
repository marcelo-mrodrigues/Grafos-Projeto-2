from grafico import desenhar_emparelhamento_muitos_para_muitos

# As mesmas configurações usadas na função de iterações
CONFIGURACOES_ITERACOES = [
    ("aluno", "normal"),
    ("aluno", "reversa"),
    ("aluno", "aleatoria"),
    ("aluno", "meio"),
    ("aluno", "nota_desc"),
    ("projeto", "normal"),
    ("projeto", "reversa"),
    ("projeto", "aleatoria"),
    ("projeto", "meio"),
    ("projeto", "requisito_desc"),
]


def visualizar_iteracao_por_indice(iteracoes: list, indice: int):
    """
    Visualiza uma iteração específica (1 a 10) de um emparelhamento.
    """
    if indice < 1 or indice > 10:
        raise ValueError("Índice deve estar entre 1 e 10")

    emp = iteracoes[indice - 1]
    lado, ordem = CONFIGURACOES_ITERACOES[indice - 1]

    desenhar_emparelhamento_muitos_para_muitos(
        emp,
        iteracao=indice,
        lado=lado,
        ordem=ordem
    )