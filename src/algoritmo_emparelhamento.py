from typing import Dict, List
from parser import Aluno, Projeto
import copy

def gale_shapley_aluno_propoe(alunos: Dict[str, Aluno], projetos: Dict[str, Projeto]) -> Dict[str, str]:
    """
    Executa uma iteração do algoritmo de emparelhamento onde alunos fazem propostas
    Retorna um dicionário com {aluno_id: projeto_id} para os emparelhamentos finais
    """
    # Dicionário que mapeia cada aluno para o índice de qual projeto ele vai propor
    proposta_atual = {aluno_id: 0 for aluno_id in alunos}
    # Resultado final: emparelhamentos aluno -> projeto
    emparelhamento = {}

    # Lista de alunos ainda não emparelhados e com preferências restantes
    livres = list(alunos.keys())

    while livres:
        aluno_id = livres.pop(0)
        aluno = alunos[aluno_id]

        if proposta_atual[aluno_id] >= len(aluno.preferencias):
            continue  # Aluno não tem mais projetos para tentar

        projeto_id = aluno.preferencias[proposta_atual[aluno_id]]
        proposta_atual[aluno_id] += 1

        if projeto_id not in projetos:
            # Caso de erro no dado (ex: projeto inexistente), ignora
            continue

        projeto = projetos[projeto_id]

        # Verifica se o aluno atende ao requisito mínimo
        if aluno.nota < projeto.requisito:
            livres.append(aluno_id)
            continue

        # Se ainda há vagas no projeto, aceita diretamente
        if len(projeto.alunos_aceitos) < projeto.vagas:
            projeto.alunos_aceitos.append(aluno_id)
            emparelhamento[aluno_id] = projeto_id
        else:
            # Projeto está cheio — rejeita proposta atual
            # (futuramente podemos tentar uma lógica de substituição, se desejar)
            livres.append(aluno_id)

    return emparelhamento

#----------------------------------------------------------------------------------------------------#
# Não consegui pensar em uma lógica pra fazer com apenas um algoritmo faça ambos, então separei em 2 #
#----------------------------------------------------------------------------------------------------#

def gale_shapley_projeto_propoe(alunos: Dict[str, Aluno], projetos: Dict[str, Projeto]) -> Dict[str, str]:
    """
    Emparelhamento onde os projetos fazem propostas aos alunos que preferem e atendem os critérios.
    """
    # Deepcopy para evitar efeitos colaterais
    alunos = copy.deepcopy(alunos)
    projetos = copy.deepcopy(projetos)

    # Inicializa emparelhamento e lista de alunos ocupados
    emparelhamento = {}
    alunos_ocupados = set()

    # Cada projeto tentará preencher suas vagas com alunos que o tenham listado nas preferências
    for projeto in projetos.values():
        candidatos_ordenados = [
            aluno for aluno in alunos.values()
            if projeto.codigo in aluno.preferencias and aluno.nota >= projeto.requisito
        ]

        # Ordenar candidatos com base na ordem de preferência (quanto mais cedo listou o projeto, melhor)
        candidatos_ordenados.sort(
            key=lambda a: a.preferencias.index(projeto.codigo)
        )

        for candidato in candidatos_ordenados:
            if len(projeto.alunos_aceitos) >= projeto.vagas:
                break

            if candidato.codigo in alunos_ocupados:
                continue

            projeto.alunos_aceitos.append(candidato.codigo)
            emparelhamento[candidato.codigo] = projeto.codigo
            alunos_ocupados.add(candidato.codigo)

    return emparelhamento