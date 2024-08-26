import pandas as pd
import streamlit as st


BASE_PATH_DATA = '/workspace/data'
DATASET_OPTIONS = {
    'Unidade 1': f'{BASE_PATH_DATA}/movimentos_unidade_1_processado.csv',
    'Unidade 2': f'{BASE_PATH_DATA}/movimentos_unidade_2_processado.csv'
}


def load_data(file_path):
    """Carrega os dados do arquivo CSV."""
    try:
        df = pd.read_csv(file_path)
        if 'dataInicio' in df.columns and 'dataFinal' in df.columns:
            df['dataInicio'] = pd.to_datetime(df['dataInicio'])
            df['dataFinal'] = pd.to_datetime(df['dataFinal'])
        else:
            st.error("O DataFrame deve conter as colunas 'dataInicio' e 'dataFinal'.")
            return None
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None