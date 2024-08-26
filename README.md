# V-LAB || Desafio Técnico JuMP — Cientista de Dados :: 🐍
![image](/docs/header.jpg)

Este projeto foi desenvolvido como parte do desafio técnico para a seleção de um bolsista no projeto JuMP, focado na mineração de processos judiciais. O objetivo principal é manipular dados de processos judiciais anonimizados, extraindo insights significativos e aprimorando a visualização dos movimentos processuais.



## Stack do projeto


Essas e outras libs e tecnologias usadas neste projeto são:
|  Lib      | Versão    |
|-----------|-----------|
| **Runtime**           |
| Python    | v3.12.x   |
| streamlit | v1.36.x   |
| **Devtime**           |
| Ruff                          | v0.4.x    |
| Docker Engine                 | vx.x.x    |
| Taskipy                       | v1.12.x   |

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
│      └─🐍 models.py -> [Implementa os modelos de mineração de processos usando o pm4py]
│
│   └─📁 visualization              
│      └─🐍 visualize.py -> [Gera visualizações dos insights extraídos.]
│      └─🐍 filters.py -> [Filtros do streamlit para o usuario.]
│      └─🐍 graphs.py -> [Graficos com os insights.] 
│      └─🐍 load_data.py -> [dados processados.] 
│ 
├─📁 .vscode         ->  [Definições de ambiente para o VSCode]
├─📄 .gitignore
├─📄 Makefile        ->  [Automações para o ambiente]
├─📄 pyproject.toml  ->  [Definições para o projeto]
├─📄 README.md
└─📄 ruff.toml       ->  [Regras de linter e formarter]
```

## Montando o ambiente

Este repositório esta organizando em um devcontainer.
E para instacia-lo no VSCODE é recomendado as seguintes configurações:

#### Extenções recomendadas

- Name: Remote Development
- Id: ms-vscode-remote.vscode-remote-extensionpack
- Description: An extension pack that lets you open any folder in a container, on a remote machine, or in WSL and take advantage of VS Code's full feature set.
- Version: 0.25.0
- Publisher: Microsoft
- VSCode Marketplace Link: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack

#### Docker Engine

É obrigatório ter o Docker Engine já instalado e configurado. Para mais informações de como instalar o Docker Engine em seu SO, ver em:

- Instruções para instalação do Docker Engine: [Ver o link](https://docs.docker.com/engine/install/)

#### Procedimento para instanciar o projeto no VSCODE
1. Com o pack de extenções instalado,
1. Realize o clone/fork deste repositório,
1. Abra o diretorio deste repositorio no VSCODE como um projeto,
1. Use o Comando _Dev Containers: Reopen in Container_ da paleta de comandos do VSCODE. _(F1, Ctrl+Shift+P)_.

Depois da compilação do container o VSCode abrirá o repositório em um ambiente encapsulado e executando diretamente de dentro do container como configurado nas definições do **/.devconainer**.


#### Procedimento para iniciar:

#### Iniciar o ambiente de desenvolvimento:

```
$> make venv
```

#### Limpeza é organização de movimentos apartir do dataset (movimentos_unidade_1.csv)

```
$> make run
```

#### Levantar o dashboard
```
$> make start
```

#### CheckList:

- [pdf](docs/CHECKLIST.md)

#### Desafio:

- [pdf](docs/Desafio_Técnico.pdf)