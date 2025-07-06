# 📘 GRAFOS-PROJETO-2 — Emparelhamento Estável entre Alunos e Projetos
Projeto de Alocação de Estudantes a Projetos Usando Algoritmo de Emparelhamento da Disciplina de Teoria e Aplicação de Grafos da Universidade de Brasília

## 🧷 Autores

- João Victor Pereira - 211036114
- Marcelo Marques Rodrigues - 221018960

## 🧩 Emparelhamento Estável em Grafos Bipartidos

Este projeto foi desenvolvido para a disciplina de **Teoria e Aplicação de Grafos (TAG)** e tem como objetivo aplicar algoritmos baseados no problema do casamento estável, estendido para o modelo muitos-para-muitos, com restrições de preferências, notas e vagas.

---

## 🧠 Objetivo

Simular o processo de emparelhamento entre 200 alunos e 50 projetos, garantindo **estabilidade** entre as escolhas, ou seja, evitando situações em que alunos e projetos prefeririam estar emparelhados de forma diferente da alocação final.

---

## 📁 Estrutura do Projeto

```plaintext
GRAFOS-PROJETO-2/
│
├── data/                                        # Dados fixos de entrada
│   ├── alunodata.txt                            # Alunos com nota e preferências
│   └── projetodata.txt                          # Projetos com vagas e requisitos
│
├── src/                                         # Código-fonte modular
│   ├── algoritmo_emparelhamento.py             # Algoritmos de emparelhamento estável
│   ├── grafico.py                              # Visualização dos grafos bipartidos
│   ├── iteracoes.py                            # Execução das 10 iterações com diferentes ordens
│   ├── parser.py                               # Leitura e estruturação dos dados
│   └── visualizar.py                           # Funções auxiliares de visualização
│
├── analise.ipynb                               # Notebook com testes, gráficos e métricas
├── proj2-tag-a-2025-1.pdf                      # Especificação do trabalho (PDF fornecido pelo professor)
├── requirements.txt                            # Dependências do projeto
└── README.md                                   # Este arquivo
```
## ⚙️ Como rodar o projeto

1. **Instale as dependências** 

🧪 Requisitos
- Python 3.9+

- NetworkX

- Matplotlib

- Pandas

- notebook (Jupyter)

*Instale tudo com:*
```bash
pip install -r requirements.txt
```
2. **Se quiser, abra o notebook no navegador utlizando no terminal o código (opcional)**

```bash
jupyter notebook
```
   Ou

```bash
jupyter lab
``` 

# 🔧 Funcionalidades
As principais funções implementadas são:

### 📌 1. Emparelhamento Estável

*Dois algoritmos implementados:*

- **emparelhamento_estavel_aluno_propoe:** cada aluno propõe a até 3 projetos; substituições ocorrem se o aluno tiver nota melhor.

- **emparelhamento_estavel_projeto_propoe:** cada projeto propõe a alunos que o preferem; alunos podem trocar projetos menos desejados.
```plaintext
# Carregamento de dados e execução do algoritmo
from src.parser import carregar_projetos, carregar_alunos

if __name__ == "__main__":
    projetos = carregar_projetos("data/projetodata.txt")
    alunos = carregar_alunos("data/alunodata.txt")
```
```plaintext
from src.algoritmo_emparelhamento import emparelhamento_estavel_aluno_propoe, emparelhamento_estavel_projeto_propoe

resultado_estavel_aluno = emparelhamento_estavel_aluno_propoe(alunos, projetos)
resultado_estavel_proj = emparelhamento_estavel_projeto_propoe(alunos, projetos)
```
### 📌 2. Dez (10) Iterações Estratégicas
Para testar a robustez do emparelhamento, o projeto executa 10 iterações variando:

- Quem propõe (aluno ou projeto);

- Ordem de entrada (original, reversa, aleatória, por nota ou requisito).

```plaintext
CONFIGURACOES_ITERACOES = [
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
```

```plaintext
from iteracoes import executar_10_iteracoes

alunos = carregar_alunos("data/alunodata.txt")
projetos = carregar_projetos("data/projetodata.txt")

iteracoes = executar_10_iteracoes(alunos, projetos)

# Exemplo: total de vínculos por iteração
for i, it in enumerate(iteracoes, 1):
    total = sum(len(projetos) for projetos in it.values())
    print(f"Iteração {i}: {total} vínculos")
```
### 📌 3. Visualização dos Grafos

Geração de grafos bipartidos com `networkx` e `matplotlib`:

```plaintext
from src.visualizar import visualizar_iteracao_por_indice

# Visualizar_iteracao_por_indice(iteracoes, 3) # O 3 por exemplo mostra a iteração 3 (aluno -> aleatória)    # Comente aqui para usar o trecho abaixo

# Ou executar

for i in range(1,11):                                       # Descomente esse
    visualizar_iteracao_por_indice(iteracoes, i)            # trecho e comente o de cima

# Para visualizar todas as iteracoes uma seguida da outra
```
Cada aluno pode estar em até 3 projetos, e os projetos respeitam suas vagas. Os nós são separados visualmente e rotulados com cores diferentes.
