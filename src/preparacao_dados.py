import pandas as pd
from carregamento_dados import carregar_data, CAMINHO_PROJETOS, CAMINHO_ALUNOS #teste

def preparar_listas_preferencia( df_projetos , df_alunos ):  # validacao das preferencias dos alunos
   
    prefs_validadas = []

    for a_id, aluno in df_alunos.iterrows():
        
        nota_aluno = aluno ['nota']
        prefs_validadas_aluno = []

        for proj_id in aluno['preferencia']:
            
            if proj_id in df_projetos.index:

                nota_minima_proj = df_projetos.loc[proj_id, 'nota_minima']

                if nota_aluno >= nota_minima_proj:

                    prefs_validadas_aluno.append(proj_id)

        prefs_validadas.append(prefs_validadas_aluno)
        """print(f"{a_id}: {prefs_validadas_aluno}")"""

    df_alunos ['prefs_validadas'] = prefs_validadas

    """print(f" preferências validadas para o aluno 200  {a_id}: {prefs_validadas_aluno}") #ultimo aluno"""
"""
df_projetos, df_alunos = carregar_data(CAMINHO_PROJETOS, CAMINHO_ALUNOS)
preparar_listas_preferencia(df_projetos, df_alunos) """

def criar_preferencias_projetos( df_projetos , df_alunos ):

    candidatos_por_projeto = {proj_id:[] for proj_id in df_projetos.index}

    for aluno_id , aluno_data in df_alunos.iterrows():
        
        for proj_id in aluno_data ['prefs_validadas']:
            
            candidatos_por_projeto[proj_id].append({ 'id' : aluno_id , 'nota' : aluno_data['nota'] })

    dict_projetos_final = {}

    for proj_id, candidatos in candidatos_por_projeto.items():

        candidatos.sort( key = lambda x: x['nota'] , reverse=True )

        dict_projetos_final[proj_id] = [ candidato['id'] for candidato in candidatos ]

    df_projetos ['preferencia'] = pd.Series(dict_projetos_final)  # isso adiciona nova coluna no datafra,e

    """print('passou por aqui')"""

    return df_projetos
    
### teste ###

if __name__ == "__main__":
    from carregamento_dados import carregar_data, CAMINHO_PROJETOS, CAMINHO_ALUNOS

    print('--'*20)

    df_projetos, df_alunos = carregar_data(CAMINHO_PROJETOS, CAMINHO_ALUNOS)

    preparar_listas_preferencia(df_projetos, df_alunos)

    df_projetos = criar_preferencias_projetos(df_projetos, df_alunos)

    print('--'*8 + 'Carregou' + '--'*8)

    
    print(df_alunos.loc['A1'][[ 'nota' , 'prefs_validadas' ]])
    print(df_alunos.loc['A77'][[ 'nota' , 'prefs_validadas' ]])  # aluno 77 com suas preferencias validadas

    print(df_projetos.loc['P1'][['vagas', 'nota_minima', 'preferencia']])  # projeto 1 com suas preferencias
    print(df_projetos.loc['P37'][['vagas', 'nota_minima', 'preferencia']])  # 2

    pd.set_option('display.max_seq_items', None)
    print(df_projetos.loc['P37']['preferencia'])
