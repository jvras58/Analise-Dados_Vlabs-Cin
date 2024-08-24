import pandas as pd
import streamlit as st


def load_data(file_path):
    """Carrega os dados especializados do arquivo CSV.

    Args:
    ----
        file_path (str): Caminho para o arquivo CSV.

    Returns:
    -------
        pd.DataFrame: DataFrame com os dados carregados.

    """
    return pd.read_csv(file_path)


def main():
    st.title('Análise de Movimentos Judiciais Especializados')

    # Seleção do arquivo de dados especializado
    BASE_PATH_DATA = '/workspace/data'
    st.sidebar.header('Configurações')
    dataset_path = st.sidebar.text_input(
        'Caminho do arquivo CSV especializado:',
        f'{BASE_PATH_DATA}/movimentos_unidade_1_processado.csv',
    )

    # Carregar e exibir o DataFrame
    df = load_data(dataset_path)
    st.write('## Visualização dos Dados')
    st.dataframe(df.head())

    # Análise básica
    st.write('## Análise Estatística')
    st.write('### Distribuição de Movimentos por Tipo')
    st.bar_chart(df['movement_type'].value_counts())

    st.write('### Distribuição de Movimentos por Complexidade')
    st.bar_chart(df['complexity'].value_counts())

    st.write('### Duração dos Movimentos')
    st.line_chart(df.groupby('movement_type')['duration_calculated'].mean())

    # Análise filtrada
    st.write('## Filtros Personalizados')
    movement_filter = st.sidebar.multiselect(
        'Filtrar por Tipo de Movimento:', options=df['movement_type'].unique(),
    )
    complexity_filter = st.sidebar.multiselect(
        'Filtrar por Complexidade:', options=df['complexity'].unique(),
    )

    if movement_filter:
        df = df[df['movement_type'].isin(movement_filter)]
    if complexity_filter:
        df = df[df['complexity'].isin(complexity_filter)]

    st.write('## Dados Filtrados')
    st.dataframe(df)

    st.write('### Gráficos Filtrados')
    st.write('Distribuição por Tipo de Movimento Filtrado')
    st.bar_chart(df['movement_type'].value_counts())

    st.write('Distribuição por Complexidade Filtrada')
    st.bar_chart(df['complexity'].value_counts())

    st.write('Duração dos Movimentos Filtrados')
    st.line_chart(df.groupby('movement_type')['duration_calculated'].mean())


if __name__ == '__main__':
    main()
