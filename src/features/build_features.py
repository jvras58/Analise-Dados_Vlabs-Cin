import pandas as pd

def especializar_movimentos(df):
    """
    Especializa os movimentos processuais utilizando as colunas 'documento' e 'complemento'.
    - Adiciona novas colunas para classificar ou agrupar os movimentos.
    
    Args:
        df (pd.DataFrame): DataFrame pré-processado com os movimentos.

    Returns:
        pd.DataFrame: DataFrame com novas features especializadas.
    """
    df['atividade_especializada'] = df.apply(especializar_movimento_row, axis=1)
    df['movement_type'] = df['documento'].map(classificar_por_documento)
    df['movement_detail'] = df['complemento'].map(classificar_por_complemento)
    df['complexity'] = df['activity_group'].map(determinar_complexidade)

    return df

def especializar_movimento_row(row):
    """Especializa uma atividade específica com base em seu identificador `movimentoID`.

    Args:
    ----
        row (pd.Series): Linha do DataFrame contendo as informações do movimento.

    Returns:
    -------
        str: Classificação especializada do movimento.

    """
    identificadores_especializados = {
        85: "Petição Inicial",
        12271: "Petição Contestação",
        60: "Expedição de Documento",
        11010: "Mero Expediente",
        106: "Mandado Judicial",
        985: "Mandado de Citação",
        970: "Audiência",
    }
    if row['movimentoID'] in identificadores_especializados:
        return identificadores_especializados[row['movimentoID']]
    return "Outros Movimentos"

def classificar_por_documento(documento):
    """
    Classifica o tipo de movimento com base no tipo de documento associado.
    
    Args:
        documento (str): Tipo de documento.

    Returns:
        str: Tipo de movimento especializado.
    """
    if isinstance(documento, str):
        documento = documento.lower()
        if 'sentença' in documento:
            return 'Sentença'
        elif 'despacho' in documento:
            return 'Despacho'
        elif 'decisão' in documento:
            return 'Decisão'
        elif 'ofício' in documento:
            return 'Ofício'
        else:
            return 'Outro Movimento'

def classificar_por_complemento(complemento):
    """
    Classifica o detalhe do movimento com base no complemento do movimento.
    
    Args:
        complemento (str): Complemento do movimento.

    Returns:
        str: Detalhe especializado do movimento.
    """
    if isinstance(complemento, str):
        complemento = complemento.lower()
        if 'urgente' in complemento:
            return 'Urgente'
        elif 'prazo' in complemento:
            return 'Com Prazo'
        elif 'intimação' in complemento:
            return 'Intimação'
        else:
            return 'Padrão'
    
def determinar_complexidade(activity_group):
    """
    Determina a complexidade do movimento baseado no agrupamento de atividade.
    
    Args:
        activity_group (str): Grupo de atividades do movimento.

    Returns:
        str: Nível de complexidade (simples, médio, complexo).
    """
    if activity_group in ['Início do Processo', 'Notificação']:
        return 'Simples'
    elif activity_group in ['Audiência', 'Sentença', 'Decisão']:
        return 'Médio'
    return 'Complexo'

if __name__ == '__main__':
    # Carregar o primeiro dataset pré-processado
    dataset_path_1 = '/workspace/data/movimentos_unidade_1_pre_processado.csv'
    df_1 = pd.read_csv(dataset_path_1)
    
    # Carregar o segundo dataset pré-processado
    dataset_path_2 = '/workspace/data/movimentos_unidade_2_pre_processado.csv'
    df_2 = pd.read_csv(dataset_path_2)
    
    # Especializar os movimentos usando o DataFrame
    df_specialized_1 = especializar_movimentos(df_1)
    print(df_specialized_1.head())
    df_specialized_1.to_csv(
        '/workspace/data/movimentos_unidade_1_processado.csv', index=False,
    )
    
    # Especializar os movimentos usando o DataFrame
    df_specialized_2 = especializar_movimentos(df_2)
    print(df_specialized_2.head())
    df_specialized_2.to_csv(
        '/workspace/data/movimentos_unidade_2_processado.csv', index=False,
    )