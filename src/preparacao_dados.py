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
        print(f"{a_id}: {prefs_validadas_aluno}")

    df_alunos ['prefs_validadas'] = prefs_validadas

    print(f" preferências validadas para o aluno 200  {a_id}: {prefs_validadas_aluno}") #ultimo aluno

df_projetos, df_alunos = carregar_data(CAMINHO_PROJETOS, CAMINHO_ALUNOS)
preparar_listas_preferencia(df_projetos, df_alunos)

