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

def emparelhamento_estavel_aluno_propoe( # Gale-Shapley
    alunos_input, projetos_input
):
    alunos = copy.deepcopy(alunos_input)
    projetos = copy.deepcopy(projetos_input)

    emparelhamento = {aluno_id: [] for aluno_id in alunos} # alocações finais

    alunos_livres = list(alunos.keys()) # alocações finais

    # dicionário para rastrear o progresso de cada aluno em sua lista de preferências
    propostas_feitas = {aluno_id: 0 for aluno_id in alunos}

    # O loop continua enquanto houver alunos livres com propostas
    while alunos_livres:
        aluno_id = alunos_livres.pop(0)
        aluno = alunos[aluno_id]

        # Se o aluno já está em 3 projetos, ele não faz mais propostas
        if len(emparelhamento[aluno_id]) >= 3:
            continue

        # Verifica se o aluno ainda tem projetos em sua lista para propor
        if propostas_feitas[aluno_id] < len(aluno.preferencias):
            # Pega o próximo projeto da lista de preferências
            projeto_id = aluno.preferencias[propostas_feitas[aluno_id]]
            propostas_feitas[aluno_id] += 1

            # ignora projetos inválidos e nota insuficiente.
            if projeto_id not in projetos or aluno.nota < projetos[projeto_id].requisito:
                alunos_livres.append(aluno_id)  # Devolve o aluno à fila para tentar o próximo
                continue

            projeto = projetos[projeto_id]

            # Projeto tem uma vaga livre. Aceita o aluno.
            if len(projeto.alunos_aceitos) < projeto.vagas:
                projeto.alunos_aceitos.append(aluno_id)
                emparelhamento[aluno_id].append(projeto_id)
            else:
                # CASO O Projeto está cheio. Compara o aluno atual com o pior nota já alocado.
                # Em caso de empate, o primeiro será retirado
                pior_aluno_id = min(projeto.alunos_aceitos, key=lambda id: alunos[id].nota)
                
                if aluno.nota > alunos[pior_aluno_id].nota:
                    # faz a troca
                    projeto.alunos_aceitos.remove(pior_aluno_id)
                    projeto.alunos_aceitos.append(aluno_id)
                    
                    # -> dicionário de emparelhamento
                    emparelhamento[pior_aluno_id].remove(projeto_id)
                    emparelhamento[aluno_id].append(projeto_id)

                    # O aluno rejeitado volta para a fila para tentar sua próxima opção
                    alunos_livres.append(pior_aluno_id)
                else:
                    # ele continua livre porque não é melhor
                    alunos_livres.append(aluno_id)
        
    return emparelhamento
