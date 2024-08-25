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

    # dados = remover_insignificantes_movements(dados)

    dados['activity_group'] = (
        dados['activity'].map(get_cnj_grouping()).fillna(dados['activity'])
    )

    dados['duration_calculated'] = calcular_duração(dados)

    # dados = filtro_outliers(dados)

    return dados.drop_duplicates(subset=['processoID', 'activity'])


# TODO: decifir oq fazer com os movimentos insignificantes (remover ou agrupar) é não é assim que se decide é sim usando o CNJ-tree

# def remover_insignificantes_movements(df: pd.DataFrame) -> pd.DataFrame:
#     """Remove movimentos insignificantes do DataFrame.

#     Args:
#     ----
#         df (pd.DataFrame): DataFrame original.

#     Returns:
#     -------
#         pd.DataFrame: DataFrame sem movimentos insignificantes.

#     """
#     movimentos_insignificantes = [
#         'Publicação',
#         'Decurso de Prazo',
#         'Conclusão',
#     ]
#     return df[~df['activity'].isin(movimentos_insignificantes)]

# TODO: Iniciando padronização de movimentos
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

# TODO: analisar se é necessário filtrar outliers ou seu impacto no desafio
# def filtro_outliers(df):
#     """Filtra outliers na duração dos movimentos.

#     Args:
#     ----
#         df (pd.DataFrame): DataFrame original.

#     Returns:
#     -------
#         pd.DataFrame: DataFrame sem outliers na duração.

#     """
#     return df[
#         (df['duration_calculated'] > 0) & (df['duration_calculated'] < 1e7)
#     ]


if __name__ == '__main__':
    # Carregar o dataset original e realizar o pré-processamento
    # Salvar o DataFrame pré-processado em um novo arquivo CSV
    dataset_path = '/workspace/data/movimentos_unidade_1.csv'
    df_preprocessed = load_and_preprocess_data(dataset_path)
    print(df_preprocessed.head())
    df_preprocessed.to_csv(
        '/workspace/data/movimentos_unidade_1_pre_processado.csv', index=False,
    )
