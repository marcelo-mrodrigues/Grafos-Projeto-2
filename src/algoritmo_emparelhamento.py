from typing import Dict, List
from parser import Aluno, Projeto
import copy

def emparelhamento_perfeito_aluno_propoe(alunos_input: Dict[str, Aluno],projetos_input: Dict[str, Projeto]) -> Dict[str, list]:
    """
    Emparelhamento perfeito onde os alunos propõem aos seus projetos preferidos.
    Cada aluno pode ser aceito em até 3 projetos.
    """
    alunos = copy.deepcopy(alunos_input)
    projetos = copy.deepcopy(projetos_input)

    emparelhamento = {aluno_id: [] for aluno_id in alunos}

    for aluno_id, aluno in alunos.items():
        projetos_preferidos = aluno.preferencias[:3]

        for projeto_id in projetos_preferidos:
            if projeto_id not in projetos:
                continue  # projeto inválido (ex: P51, P52...)

            projeto = projetos[projeto_id]

            if aluno.nota < projeto.requisito:
                continue  # aluno não atende o requisito

            if len(projeto.alunos_aceitos) < projeto.vagas:
                # Aceita o aluno no projeto
                projeto.alunos_aceitos.append(aluno_id)
                emparelhamento[aluno_id].append(projeto_id)

                if len(emparelhamento[aluno_id]) == 3:
                    break  # aluno já está em 3 projetos

    return emparelhamento

#----------------------------------------------------------------------------------------------------#
# Não consegui pensar em uma lógica pra fazer com apenas um algoritmo faça ambos, então separei em 2 #
#----------------------------------------------------------------------------------------------------#

def emparelhamento_perfeito_projeto_propoe(alunos_input: Dict[str, Aluno],projetos_input: Dict[str, Projeto], verbose: bool = False) -> Dict[str, list]:
    """
    Emparelhamento perfeito onde os projetos escolhem os alunos que os preferem.
    Cada projeto pode aceitar até sua capacidade máxima.
    Cada aluno pode estar em no máximo 3 projetos.
    """
    alunos = copy.deepcopy(alunos_input)
    projetos = copy.deepcopy(projetos_input)

    emparelhamento = {aluno_id: [] for aluno_id in alunos}
    aluno_cargas = {aluno_id: 0 for aluno_id in alunos}  # controla quantos projetos cada aluno já entrou

    for projeto in projetos.values():
        projeto.alunos_aceitos = []
        
        candidatos = []

        # Alunos que colocaram esse projeto como preferência
        for aluno in alunos.values():
            if projeto.codigo in aluno.preferencias and aluno.nota >= projeto.requisito:
                preferencia_index = aluno.preferencias.index(projeto.codigo)
                candidatos.append((preferencia_index, aluno.codigo))

        # Ordena candidatos pela posição que deram ao projeto (quanto antes, melhor)
        candidatos.sort()

        for _, aluno_id in candidatos:
            if len(projeto.alunos_aceitos) >= projeto.vagas:
                break  # vagas completas

            if aluno_cargas[aluno_id] >= 3:
                continue  # aluno já em 3 projetos

            projeto.alunos_aceitos.append(aluno_id)
            emparelhamento[aluno_id].append(projeto.codigo)
            aluno_cargas[aluno_id] += 1
            
            if verbose:
                print(f"{projeto.codigo} → {aluno_id} (nota OK, vagas OK)")

    return emparelhamento