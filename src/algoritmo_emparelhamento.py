from typing import Dict, List
from parser import Aluno, Projeto
import copy


def emparelhamento_estavel_aluno_propoe(alunos_input: Dict[str, Aluno],projetos_input: Dict[str, Projeto]) -> Dict[str, list]:
    """
    Emparelhamento estável (muitos-para-muitos) onde os alunos propõem e projetos podem substituir.
    Cada aluno pode estar em até 3 projetos.
    Projetos substituem alunos com nota mais baixa.
    """
    alunos = copy.deepcopy(alunos_input)
    projetos = copy.deepcopy(projetos_input)

    emparelhamento = {aluno_id: [] for aluno_id in alunos}
    aluno_cargas = {aluno_id: 0 for aluno_id in alunos}
    proposta_atual = {aluno_id: 0 for aluno_id in alunos}
    
    livres = list(alunos.keys())

    # O loop continua enquanto houver alunos livres com propostas
    while livres:
        aluno_id = livres.pop(0)
        aluno = alunos[aluno_id]

        # Se o aluno já está em 3 projetos, ele não faz mais propostas
        if aluno_cargas[aluno_id] >= 3:
            continue  
        
        # Verifica se o aluno ainda tem projetos em sua lista para propor
        if proposta_atual[aluno_id] >= len(aluno.preferencias):
            continue  
        
        # Pega o próximo projeto da lista de preferências
        projeto_id = aluno.preferencias[proposta_atual[aluno_id]]
        proposta_atual[aluno_id] += 1
        
        # ignora projetos inválidos 
        if projeto_id not in projetos:
            continue

        projeto = projetos[projeto_id]
        
        # ignora projetos com nota insuficiente
        if aluno.nota < projeto.requisito:
            continue

        if projeto.alunos_aceitos is None:
            projeto.alunos_aceitos = []

        # Vaga disponível
        if len(projeto.alunos_aceitos) < projeto.vagas:
            projeto.alunos_aceitos.append(aluno_id)
            emparelhamento[aluno_id].append(projeto_id)
            aluno_cargas[aluno_id] += 1
        else:
            # Tenta substituir o pior aluno atual
            pior_aluno = min(
                projeto.alunos_aceitos,
                key=lambda a_id: alunos[a_id].nota
            )

            if aluno.nota > alunos[pior_aluno].nota:
                # Substitui o pior aluno inserido no projeto
                projeto.alunos_aceitos.remove(pior_aluno)
                projeto.alunos_aceitos.append(aluno_id)

                # O aluno rejeitado volta para a fila para tentar sua próxima opção
                emparelhamento[pior_aluno].remove(projeto_id)
                aluno_cargas[pior_aluno] -= 1
                livres.append(pior_aluno)  

                emparelhamento[aluno_id].append(projeto_id)
                aluno_cargas[aluno_id] += 1
            else:
                # Aluno rejeitado e continua livre por ser pior
                livres.append(aluno_id)

    return emparelhamento

#----------------------------------------------------------------------------------------------------#
# Não consegui pensar em uma lógica pra fazer com apenas um algoritmo faça ambos, então separei em 2 #
#----------------------------------------------------------------------------------------------------#

def emparelhamento_estavel_projeto_propoe(alunos_input: Dict[str, Aluno],projetos_input: Dict[str, Projeto], verbose: bool = False) -> Dict[str, list]:
    """
    Emparelhamento estável (muitos-para-muitos) onde os projetos propõem.
    Alunos aceitam até 3 projetos, substituindo os menos desejados.
    Projetos selecionam candidatos por preferência e nota.
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
                break

            projetos_do_aluno = emparelhamento[aluno_id]

            if len(projetos_do_aluno) < 3:
                # Aluno ainda tem espaço
                projeto.alunos_aceitos.append(aluno_id)
                emparelhamento[aluno_id].append(projeto.codigo)
                aluno_cargas[aluno_id] += 1
            else:
                # Aluno já está em 3 projetos — verificar se quer trocar
                # Critério de substituição: substituir o projeto menos preferido
                preferencias = alunos[aluno_id].preferencias
                atuais = emparelhamento[aluno_id]

                menos_desejado = max(
                    atuais,
                    key=lambda p_id: preferencias.index(p_id)
                )

                # Se projeto atual é mais desejado que o menos desejado
                if preferencias.index(projeto.codigo) < preferencias.index(menos_desejado):
                    # Substitui
                    emparelhamento[aluno_id].remove(menos_desejado)
                    emparelhamento[aluno_id].append(projeto.codigo)

                    # Atualiza projeto antigo
                    for p in projetos.values():
                        if menos_desejado in p.codigo and aluno_id in p.alunos_aceitos:
                            p.alunos_aceitos.remove(aluno_id)
                            break

                    projeto.alunos_aceitos.append(aluno_id)

    return emparelhamento

