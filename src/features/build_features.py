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
    df['movement_type'] = df['documento'].map(classificar_por_documento)
    df['movement_detail'] = df['complemento'].map(classificar_por_complemento)
    df['complexity'] = df['activity_group'].map(determinar_complexidade)

    return df

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

if __name__ == "__main__":
    # Carregar o dataset pré-processado
    # Salvar o DataFrame processado em um novo arquivo CSV
    dataset_path = '/workspace/data/movimentos_unidade_1_pre_processado.csv'
    df = pd.read_csv(dataset_path)
    df_specialized = especializar_movimentos(df)
    print(df_specialized.head())
    df_specialized.to_csv('/workspace/data/movimentos_unidade_1_processado.csv', index=False)