"""

Modularizar o Código

"""

import pandas as pd
from preparacao_dados import criar_preferencias_projetos, preparar_listas_preferencia
from carregamento_dados import carregar_data

def emparelhamento_estavel_V1(df_projetos, df_alunos):
    # Inicializa dicionários para armazenar emparelhamentos
    alunos_emparelhados = {aluno_id: None for aluno_id in df_alunos.index}
    projetos_emparelhados = {proj_id: [] for proj_id in df_projetos.index}

    # Alunos não emparelhados iniciam com todas as preferências válidas
    alunos_nao_emparelhados = list(df_alunos.index)
    
    while alunos_nao_emparelhados:
        aluno_id = alunos_nao_emparelhados.pop(0)
        prefs_aluno = df_alunos.loc[aluno_id, "prefs_validadas"]
        
        for proj_id in prefs_aluno:
            vagas_disponiveis = df_projetos.loc[proj_id, "vagas"]
            candidatos_atual = projetos_emparelhados[proj_id]
            
            # Verifica se o projeto tem vaga ou se o aluno é melhor que os atuais
            if len(candidatos_atual) < vagas_disponiveis:
                projetos_emparelhados[proj_id].append(aluno_id)
                alunos_emparelhados[aluno_id] = proj_id
                break
            else:
                # Compara a nota do aluno com a pior nota atual no projeto
                notas_candidatos = [df_alunos.loc[cand, "nota"] for cand in candidatos_atual]
                min_nota = min(notas_candidatos)
                aluno_nota = df_alunos.loc[aluno_id, "nota"]
                
                if aluno_nota > min_nota:
                    # Substitui o pior candidato
                    pior_candidato_idx = notas_candidatos.index(min_nota)
                    pior_candidato = candidatos_atual[pior_candidato_idx]
                    
                    projetos_emparelhados[proj_id][pior_candidato_idx] = aluno_id
                    alunos_emparelhados[aluno_id] = proj_id
                    alunos_nao_emparelhados.append(pior_candidato)
                    break

    return alunos_emparelhados, projetos_emparelhados