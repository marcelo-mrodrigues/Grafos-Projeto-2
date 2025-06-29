from dataclasses import dataclass
from typing import List, Dict
import re

# Representa um projeto com código, vagas disponíveis e requisito mínimo de nota
@dataclass
class Projeto:
    codigo: str
    vagas: int
    requisito: int
    alunos_aceitos: List[str] = None

    def __post_init__(self):
        # Inicializa a lista de alunos aceitos se não for fornecida
        self.alunos_aceitos = []


# Representa um aluno com código, lista de projetos preferenciais e sua nota
@dataclass
class Aluno:
    codigo: str
    preferencias: List[str]
    nota: int


# Função para carregar projetos a partir do arquivo data/projetodata.txt
def carregar_projetos(caminho: str) -> Dict[str, Projeto]:
    projetos = {}
    with open(caminho, 'r') as f:
        for linha in f:
            match = re.match(r"\((P\d+),\s*(\d+),\s*(\d+)\)", linha.strip())
            if match:
                codigo, vagas, requisito = match.groups()
                projetos[codigo] = Projeto(codigo, int(vagas), int(requisito))
    return projetos


# Função para carregar alunos a partir do arquivo data/alunodata.txt
def carregar_alunos(caminho: str) -> Dict[str, Aluno]:
    alunos = {}
    with open(caminho, 'r') as f:
        for linha in f:
            match = re.match(r"\((A\d+)\):\(([^)]+)\)\s+\((\d+)\)", linha.strip())
            if match:
                codigo, preferencias_str, nota = match.groups()
                preferencias = [p.strip() for p in preferencias_str.split(',')]
                alunos[codigo] = Aluno(codigo, preferencias, int(nota))
    return alunos