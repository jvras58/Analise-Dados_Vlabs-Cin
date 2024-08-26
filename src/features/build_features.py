"""Módulo para carregar os datasets processar definitivamente os movimentos processuais."""

import json

import pandas as pd
from src.data.make_dataset import get_cnj_grouping


def classificar_movement_detail(row, tpu_cnj):
    """
    Classifica o detalhe do movimento com base em identificadores, contexto, e fases do processo judicial.

    Args:
        row (pd.Series): Linha do DataFrame com os dados de um movimento.
        tpu_cnj (dict): Dicionário que mapeia os identificadores de movimento para categorias da TPU do CNJ.

    Returns:
        str: Detalhe especializado do movimento.
    """
    movimento_id = str(row['movimentoID'])
    documento = row['documento'].lower() if isinstance(row['documento'], str) else 'N/A'
    complemento = row['complemento'].lower() if isinstance(row['complemento'], str) else 'N/A'
    
    categoria = tpu_cnj.get(movimento_id, 'Outros')

    if 'sentença' in documento:
        detalhe = 'Sentença'
    elif 'despacho' in documento:
        detalhe = 'Despacho'
    elif 'decisão' in documento:
        detalhe = 'Decisão'
    elif 'urgente' in complemento:
        detalhe = 'Urgente'
    elif 'prazo' in complemento:
        detalhe = 'Com Prazo'
    elif 'intimação' in complemento:
        detalhe = 'Intimação'
    elif 'distribuição' in row['activity'].lower():
        detalhe = 'Distribuição'
    elif 'audiência' in row['activity'].lower():
        detalhe = 'Audiência'
    elif 'expedição de documento' in row['activity'].lower():
        detalhe = 'Expedição de Documento'
    else:
        detalhe = 'Padrão'
    
    if 'fase' in row:
        if row['fase'] == 'inicial':
            detalhe += ' - Fase Inicial'
        elif row['fase'] == 'contestação':
            detalhe += ' - Fase de Contestação'

    return f"{categoria}: {detalhe}"

def especializar_movimentos(df, tpu_cnj):
    """
    Especializa os movimentos processuais utilizando as colunas 'documento', 'complemento' e identificadores.

    Args:
        df (pd.DataFrame): DataFrame pré-processado com os movimentos.
        tpu_cnj (dict): Dicionário que mapeia os identificadores de movimento para categorias da TPU do CNJ.

    Returns:
        pd.DataFrame: DataFrame com novas features especializadas.
    """
    df['movement_detail'] = df.apply(lambda row: classificar_movement_detail(row, tpu_cnj), axis=1)
    df['complexity'] = df['activity_group'].map(determinar_complexidade)

    return df

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

def especializar_movimentos(df, tpu_cnj):
    """
    Especializa os movimentos processuais utilizando as colunas 'documento', 'complemento' e identificadores.

    Args:
        df (pd.DataFrame): DataFrame pré-processado com os movimentos.
        tpu_cnj (dict): Dicionário que mapeia os identificadores de movimento para categorias da TPU do CNJ.

    Returns:
        pd.DataFrame: DataFrame com novas features especializadas.
    """
    df['movement_detail'] = df.apply(lambda row: classificar_movement_detail(row, tpu_cnj), axis=1)
    df['complexity'] = df['activity_group'].map(determinar_complexidade)

    return df


def specialize_activity(row):
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

def mapear_para_tpu(activity):
    """Mapeia uma atividade para a classificação correspondente na TPU.

    Args:
    ----
        activity (str): Nome ou identificador da atividade.

    Returns:
    -------
        str: Categoria ou agrupamento correspondente na TPU, se encontrado.

    """
    with open('/workspace/data/cnj-movimentos-tree.json') as file:
        cnj_tree = json.load(file)

    def buscar_classe_tpu(node, activity):
        if activity in node:
            return node[activity] if node[activity] else activity

        for sub_node in node.values():
            result = buscar_classe_tpu(sub_node, activity)
            if result:
                return result
        return None

    categoria_tpu = buscar_classe_tpu(cnj_tree, activity)

    return categoria_tpu if categoria_tpu else 'Outro Movimento'


def classificar_por_documento(documento):
    """Classifica o tipo de movimento com base no tipo de documento associado.

    Args:
    ----
        documento (str): Tipo de documento.

    Returns:
    -------
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
    """Classifica o detalhe do movimento com base no complemento do movimento.

    Args:
    ----
        complemento (str): Complemento do movimento.

    Returns:
    -------
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
    """Determina a complexidade do movimento baseado no agrupamento de atividade.

    Args:
    ----
        activity_group (str): Grupo de atividades do movimento.

    Returns:
    -------
        str: Nível de complexidade (simples, médio, complexo).

    """
    activity_group = activity_group.strip().capitalize()
    complexidade_map = {
        'Início do Processo': 'Simples',
        'Notificação': 'Simples',
        'Audiência': 'Médio',
        'Sentença': 'Médio',
        'Decisão': 'Médio',
    }
    return complexidade_map.get(activity_group, 'Complexo')


if __name__ == '__main__':
    # Carregar o primeiro dataset pré-processado
    dataset_path_1 = '/workspace/data/movimentos_unidade_1_pre_processado.csv'
    df_1 = pd.read_csv(dataset_path_1)
    
    # Carregar o segundo dataset pré-processado
    dataset_path_2 = '/workspace/data/movimentos_unidade_2_pre_processado.csv'
    df_2 = pd.read_csv(dataset_path_2)
    
    # Gerar o dicionário de agrupamento CNJ a partir da TPU
    cnj_grouping = get_cnj_grouping()
    
    # Especializar os movimentos usando o DataFrame e o agrupamento CNJ para o primeiro dataset
    df_specialized_1 = especializar_movimentos(df_1, cnj_grouping)
    print(df_specialized_1.head())
    df_specialized_1.to_csv(
        '/workspace/data/movimentos_unidade_1_processado.csv', index=False,
    )
    
    # Especializar os movimentos usando o DataFrame e o agrupamento CNJ para o segundo dataset
    df_specialized_2 = especializar_movimentos(df_2, cnj_grouping)
    print(df_specialized_2.head())
    df_specialized_2.to_csv(
        '/workspace/data/movimentos_unidade_2_processado.csv', index=False,
    )