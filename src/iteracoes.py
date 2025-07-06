from parser import Aluno, Projeto
from algoritmo_emparelhamento import emparelhamento_estavel_aluno_propoe, emparelhamento_estavel_projeto_propoe
from typing import Dict, List
import random
import copy


def aplicar_variacao_ordem(lista: List[str], tipo: str) -> List[str]:
    """
    Aplica uma variação na ordem da lista conforme o tipo indicado.
    """
    if tipo == "normal":
        return lista
    elif tipo == "reversa":
        return list(reversed(lista))
    elif tipo == "aleatoria":
        random.shuffle(lista)
        return lista
    elif tipo == "meio":
        meio = len(lista) // 2
        return lista[meio:] + lista[:meio]
    elif tipo == "nota_desc":
        # usado apenas para alunos
        return sorted(lista, key=lambda x: -alunos_ref[x].nota)
    elif tipo == "requisito_desc":
        # usado apenas para projetos
        return sorted(lista, key=lambda x: -projetos_ref[x].requisito)
    else:
        return lista


# Essas referências globais são usadas dentro de `aplicar_variacao_ordem` para ordenações por nota ou requisito
alunos_ref: Dict[str, Aluno] = {}
projetos_ref: Dict[str, Projeto] = {}


def executar_10_iteracoes(
    alunos_input: Dict[str, Aluno],
    projetos_input: Dict[str, Projeto]
) -> List[Dict[str, str]]:
    """
    Executa as 10 iterações do algoritmo com diferentes ordens e lados proponentes.
    Retorna uma lista com 10 dicionários de emparelhamento.
    """
    global alunos_ref, projetos_ref
    alunos_ref = alunos_input
    projetos_ref = projetos_input

    resultados = []

    # Configurações das 10 iterações
    configuracoes = [
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

    for i, (lado, ordem) in enumerate(configuracoes):
        alunos = copy.deepcopy(alunos_input)
        projetos = copy.deepcopy(projetos_input)

        if lado == "aluno":
            ordem_ids = aplicar_variacao_ordem(list(alunos.keys()), ordem)
            alunos = {aid: alunos[aid] for aid in ordem_ids}
            resultado = emparelhamento_estavel_aluno_propoe(alunos, projetos)
        else:
            ordem_ids = aplicar_variacao_ordem(list(projetos.keys()), ordem)
            projetos = {pid: projetos[pid] for pid in ordem_ids}
            resultado = emparelhamento_estavel_projeto_propoe(alunos, projetos)

        resultados.append(resultado)

    return resultados