import pandas as pd
import re

CAMINHO_PROJETOS = "data/projetodata.txt"
CAMINHO_ALUNOS = "data/alunodata.txt"


def carregar_data(CAMINHO_PROJETOS, CAMINHO_ALUNOS):
    try:
        with open(CAMINHO_PROJETOS, "r", encoding="utf-8") as arquivo:
            linhas_projetos = arquivo.readlines()  # Carregamento de projetos

        dados_projetos = []
        padrao_projeto = re.compile(
            r"\(P(\d+),\s*(\d+),\s*(\d+)\)"
        )  # Captura (P<id>, <vagas>, <nota_min>)

        for linha in linhas_projetos:
            match = padrao_projeto.search(linha)
            if match:
                pid, vagas, nota_minima = match.groups()
                dados_projetos.append([f"P{pid}",
                                       int(vagas),
                                       float(nota_minima)])
            
            ################################################
            else:
                print(f"Linha ignorada no arquivo de projetos: {linha.strip()}")
            # Para DEBUG, comentar se não estiver utilizando

        df_projetos = pd.DataFrame(
            dados_projetos, columns=["id", "vagas", "nota_minima"]
        )
        df_projetos = df_projetos.set_index("id")

        with open(CAMINHO_ALUNOS, "r", encoding="utf-8") as arquivo:
            linhas_alunos = arquivo.readlines()  # Carregamento de alunos

            dados_alunos = []
            padrao_aluno = re.compile(
                r"\(A(\d+)\):\((.*?)\)\s*\((\d+)\)"
            )  # Capturamos (A<id>):(<preferencias>) (<nota>)

        for linha in linhas_alunos:
            match = padrao_aluno.search(linha)
            if match:
                aid, preferencia, nota = match.groups()
                # Trata a string das prefeências pra lista
                preferencias = [p.strip() for p in preferencia.split(",")]
                dados_alunos.append([f"A{aid}", preferencias, int(nota)])

        df_alunos = pd.DataFrame(dados_alunos, columns=["id", "preferencia", "nota"])
        df_alunos = df_alunos.set_index("id")

        return df_projetos, df_alunos

    except FileNotFoundError as e:
        print(f"ERRO de arquivo não encontrado no caminho: {e.filename}")
        return None, None
