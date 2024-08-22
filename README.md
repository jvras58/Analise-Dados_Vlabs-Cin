# V-LAB || Desafio Técnico JuMP — Cientista de Dados :: 🐍
![image](/docs/header.jpg)

Este projeto foi desenvolvido como parte do desafio técnico para a seleção de um bolsista no projeto JuMP, focado na mineração de processos judiciais. O objetivo principal é manipular dados de processos judiciais anonimizados, extraindo insights significativos e aprimorando a visualização dos movimentos processuais.


### Estrutura de diretórios
```
/
├─📁 .devcontainer   ->  [Configurações do devcontainer]
├─📁 docs            ->  [documentação do Desafio]
├─📁 data            ->  [dataset anonimizado]
│      └─📄 movimentos_unidade_1.csv.csv
│      └─📄 movimentos_unidade_2.csv.csv
├─📁 .git            ->  [Configurações do git]
├─📁 notebooks       ->  [Juyter Notebooks]
│   └─📁 util        ->  [Coleção de funções utilitárias para auxiliar na análise de dados.] 
│      └─🐍 tools.py ->  [Abre um arquivo de dados e retorna seu conteúdo]
│ └─ 🐍Analise_inicial.ipynb 
├─📁 src             ->  [entrypoint]
│   └─📁 data              
│      └─🐍 make_dataset.py ->  [Ponto de entrada para o processamento inicial dos dados.]
│      
│   └─📁 features              
│      └─🐍 build_features.py -> [Cria as features necessárias para a modelagem com base no pre-processamento gerado pelo make_dataset]
│
│   └─📁 models              
│      └─🐍 models.py -> [Implementa os modelos de mineração de processos]
│
│   └─📁 visualization              
│      └─🐍 visualize.py -> [Gera visualizações dos insights extraídos.] 
│ 
├─📁 .vscode         ->  [Definições de ambiente para o VSCode]
├─📄 .gitignore
├─📄 Makefile        ->  [Automações para o ambiente]
├─📄 pyproject.toml  ->  [Definições para o projeto]
├─📄 README.md
└─📄 ruff.toml       ->  [Regras de linter e formarter]
```
