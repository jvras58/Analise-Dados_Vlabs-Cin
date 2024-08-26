import pandas as pd

def load_and_preprocess_data(file_path):
    """
    Carrega o dataset e realiza o pré-processamento inicial:
    - Converte as colunas de datas para o formato datetime.
    - Trata valores nulos em 'complemento' e 'documento'.
    - Remove movimentos insignificantes.
    - Agrupa movimentos conforme árvore CNJ.
    - Calcula duração dos movimentos quando possível.

    Args:
        file_path (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame pré-processado.
    """
    df = pd.read_csv(file_path)

    df['dataInicio'] = pd.to_datetime(df['dataInicio'], errors='coerce')
    df['dataFinal'] = pd.to_datetime(df['dataFinal'], errors='coerce')

    df['complemento'] = df['complemento'].fillna('N/A')
    df['documento'] = df['documento'].fillna('N/A')

    df = remover_insignificantes_movements(df)

    df['activity_group'] = df['activity'].map(get_cnj_grouping()).fillna(df['activity'])

    df['duration_calculated'] = calcular_duração(df)

    df = filtro_outliers(df)

    df.drop_duplicates(subset=['processoID', 'activity'], inplace=True)

    return df

def remover_insignificantes_movements(df):
    """
    Remove movimentos insignificantes do DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame sem movimentos insignificantes.
    """
    movimentos_insignificantes = [
        'Publicação', 'Decurso de Prazo', 'Conclusão',
        # add outros movimentos irrelevantes
    ]
    return df[~df['activity'].isin(movimentos_insignificantes)]

def get_cnj_grouping():
    """
    Retorna o dicionário de agrupamento CNJ.
    
    Returns:
        dict: Dicionário de agrupamento CNJ.
    """
    return {
        'Distribuição': 'Início do Processo',
        'Citação': 'Notificação',
        'Audiência de Instrução': 'Audiência',
    }

def calcular_duração(df):
    """
    Calcula a duração dos movimentos em segundos.
    
    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.Series: Série com a duração calculada dos movimentos.
    """
    return (df['dataFinal'] - df['dataInicio']).dt.total_seconds()

def filtro_outliers(df):
    """
    Filtra outliers na duração dos movimentos.
    
    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame sem outliers na duração.
    """
    return df[(df['duration_calculated'] > 0) & (df['duration_calculated'] < 1e7)]

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