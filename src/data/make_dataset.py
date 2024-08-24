"""Módulo para carregar e pré-processar o dataset de movimentos processuais."""

import json

import pandas as pd


def load_and_preprocess_data(file_path: pd) -> pd.DataFrame:
    """Carrega o dataset e realiza o pré-processamento inicial:
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
    df = pd.read_csv(file_path)

    df['dataInicio'] = pd.to_datetime(df['dataInicio'], errors='coerce')
    df['dataFinal'] = pd.to_datetime(df['dataFinal'], errors='coerce')

    df['complemento'] = df['complemento'].fillna('N/A')
    df['documento'] = df['documento'].fillna('N/A')

    df = remover_insignificantes_movements(df)

    df['activity_group'] = (
        df['activity'].map(get_cnj_grouping()).fillna(df['activity'])
    )

    df['duration_calculated'] = calcular_duração(df)

    df = filtro_outliers(df)

    df.drop_duplicates(subset=['processoID', 'activity'], inplace=True)

    return df


def remover_insignificantes_movements(df):
    """Remove movimentos insignificantes do DataFrame.

    Args:
    ----
        df (pd.DataFrame): DataFrame original.

    Returns:
    -------
        pd.DataFrame: DataFrame sem movimentos insignificantes.

    """
    movimentos_insignificantes = [
        'Publicação',
        'Decurso de Prazo',
        'Conclusão',
    ]
    return df[~df['activity'].isin(movimentos_insignificantes)]

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


def filtro_outliers(df):
    """Filtra outliers na duração dos movimentos.

    Args:
    ----
        df (pd.DataFrame): DataFrame original.

    Returns:
    -------
        pd.DataFrame: DataFrame sem outliers na duração.

    """
    return df[
        (df['duration_calculated'] > 0) & (df['duration_calculated'] < 1e7)
    ]


if __name__ == '__main__':
    # Carregar o dataset original e realizar o pré-processamento
    # Salvar o DataFrame pré-processado em um novo arquivo CSV
    dataset_path = '/workspace/data/movimentos_unidade_1.csv'
    df_preprocessed = load_and_preprocess_data(dataset_path)
    print(df_preprocessed.head())
    df_preprocessed.to_csv(
        '/workspace/data/movimentos_unidade_1_pre_processado.csv', index=False,
    )
