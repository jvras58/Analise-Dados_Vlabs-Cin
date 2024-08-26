"""Módulo para carregar e pré-processar o dataset de movimentos processuais."""

import json

import pandas as pd


def load_and_preprocess_data(file_path: pd) -> pd.DataFrame:
    """Carrega o dataset e realiza o pré-processamento inicial.

    - Converte as colunas de datas para o formato datetime.
    - Trata valores nulos em 'complemento' e 'documento'.
    - Remove movimentos insignificantes.
    - Agrupa movimentos conforme árvore CNJ.
    - Calcula duração dos movimentos quando possível.

    Args:
    ----
        file_path (str): Caminho para o arquivo CSV.

    Returns:
    -------
        pd.DataFrame: DataFrame pré-processado.

    """
    dados = pd.read_csv(file_path)

    dados['dataInicio'] = pd.to_datetime(dados['dataInicio'], errors='coerce')
    dados['dataFinal'] = pd.to_datetime(dados['dataFinal'], errors='coerce')

    dados['complemento'] = dados['complemento'].fillna('N/A')
    dados['documento'] = dados['documento'].fillna('N/A')

    cnj_grouping = get_cnj_grouping()

    dados = remover_insignificantes_movements(dados, cnj_grouping)

    dados['activity_group'] = (
        dados['activity'].map(get_cnj_grouping()).fillna(dados['activity'])
    )

    dados['duration_calculated'] = calcular_duração(dados)

    return dados.drop_duplicates(subset=['processoID', 'activity'])


def remover_insignificantes_movements(df: pd.DataFrame, cnj_grouping: dict) -> pd.DataFrame:
    """Remove movimentos insignificantes do DataFrame baseado na árvore CNJ.

    Args:
    ----
        df (pd.DataFrame): DataFrame original.
        cnj_grouping (dict): Dicionário de agrupamento CNJ que mapeia movimentoID para categorias.

    Returns:
    -------
        pd.DataFrame: DataFrame sem movimentos insignificantes.
    """
    # Categorias de movimentos considerados insignificantes na árvore CNJ e de acordo com a documentação do desafio técnico
    categorias_insignificantes = ['publicação', 'decurso de prazo', 'conclusão', 'mero expediente']

    df['grupo_movimento'] = df['movimentoID'].map(cnj_grouping).fillna('Outros')

    df = df[~df['grupo_movimento'].str.lower().isin(categorias_insignificantes)]

    return df

# def remover_insignificantes_movements(df: pd.DataFrame, cnj_grouping: dict, limiar: int = 10) -> pd.DataFrame:
#     """Remove movimentos insignificantes do DataFrame baseado na árvore CNJ e na frequência dos movimentos.

#     Args:
#     ----
#         df (pd.DataFrame): DataFrame original.
#         cnj_grouping (dict): Dicionário de agrupamento CNJ que mapeia movimentoID para categorias.
#         limiar (int): Frequência mínima para um movimento ser considerado significativo.

#     Returns:
#     -------
#         pd.DataFrame: DataFrame sem movimentos insignificantes.
#     """
#     # Mapear os movimentoIDs para seus respectivos grupos usando o cnj_grouping
#     df['grupo_movimento'] = df['movimentoID'].map(cnj_grouping).fillna('Outros')

#     # Contar a frequência de cada grupo de movimento
#     frequencia_grupos = df['grupo_movimento'].value_counts()

#     # Identificar grupos insignificantes com base no limiar
#     grupos_insignificantes = frequencia_grupos[frequencia_grupos < limiar].index.tolist()

#     # Remover movimentos insignificantes baseados na frequência
#     df = df[~df['grupo_movimento'].isin(grupos_insignificantes)]

#     return df

def get_cnj_grouping():
    """Constrói um dicionário de agrupamento CNJ com base na estrutura da Tabela de Padronização de Unidades (TPU).

    Returns
    -------
        dict: Dicionário onde as chaves são identificadores de movimentos e os valores são categorias ou grupos.

    """
    with open('/workspace/data/cnj-movimentos-tree.json') as file:
        cnj_tree = json.load(file)

    cnj_grouping = {}

    def preencher_grupo(node, current_group=None):
        """Função recursiva para preencher o dicionário de agrupamento a partir da estrutura hierárquica da TPU.

        Args:
        ----
            node (dict): O nó atual da árvore TPU.
            current_group (str): O grupo atual ao qual o nó pertence.

        """
        for key, sub_node in node.items():
            if not sub_node:
                cnj_grouping[int(key)] = (
                    current_group if current_group else 'Outro Movimento'
                )
            else:
                preencher_grupo(sub_node, current_group or key)

    preencher_grupo(cnj_tree)

    return cnj_grouping


def calcular_duração(df):
    """Calcula a duração dos movimentos em segundos.

    Args:
    ----
        df (pd.DataFrame): DataFrame original.

    Returns:
    -------
        pd.Series: Série com a duração calculada dos movimentos.

    """
    return (df['dataFinal'] - df['dataInicio']).dt.total_seconds()

if __name__ == '__main__':
    # Carregar o primeiro dataset e realizar o pré-processamento
    dataset_path_1 = '/workspace/data/movimentos_unidade_1.csv'
    df_preprocessed_1 = load_and_preprocess_data(dataset_path_1)
    print(df_preprocessed_1.head())
    df_preprocessed_1.to_csv(
        '/workspace/data/movimentos_unidade_1_pre_processado.csv', index=False,
    )

    # Carregar o segundo dataset e realizar o pré-processamento
    dataset_path_2 = '/workspace/data/movimentos_unidade_2.csv'
    df_preprocessed_2 = load_and_preprocess_data(dataset_path_2)
    print(df_preprocessed_2.head())
    df_preprocessed_2.to_csv(
        '/workspace/data/movimentos_unidade_2_pre_processado.csv', index=False,
    )