import pandas as pd
import streamlit as st

from src.visualization.filters import apply_filters
from src.visualization.graphs import plot_bar_chart, plot_boxplot, plot_histogram, plot_line_chart
from src.visualization.load_Data import DATASET_OPTIONS, load_data

def main():
    st.title("Análise de Movimentos Judiciais Especializados")
    st.sidebar.header('Configurações')

    dataset_selection = st.sidebar.selectbox('Selecione o Dataset:', options=list(DATASET_OPTIONS.keys()))
    df = load_data(DATASET_OPTIONS[dataset_selection])
    if df is None:
        return

    st.write(f'## Visualização dos Dados - {dataset_selection}')
    st.dataframe(df.head())

    st.write("## Análise Estatística")
    plot_bar_chart(df, 'movement_detail')
    plot_bar_chart(df, 'complexity')
    plot_line_chart(df, 'movement_detail', 'duration_calculated')
    
    st.write('### Histograma da Duração dos Movimentos')
    plot_histogram(df, 'duration_calculated')

    st.write('### Box Plot da Duração dos Movimentos por Complexidade')
    plot_boxplot(df, 'complexity', 'duration_calculated')

    st.write('## Filtros Personalizados')
    movement_filter = st.sidebar.multiselect('Filtrar por Detalhe de Movimento:', options=df['movement_detail'].unique())
    complexity_filter = st.sidebar.multiselect('Filtrar por Complexidade:', options=df['complexity'].unique())

    df_filtered = apply_filters(df, movement_filter, complexity_filter)
    
    st.write('## Dados Filtrados')
    st.dataframe(df_filtered)

    st.write('### Gráficos Filtrados')
    plot_bar_chart(df_filtered, 'movement_detail')
    plot_bar_chart(df_filtered, 'complexity')
    plot_line_chart(df_filtered, 'movement_detail', 'duration_calculated')

    if st.sidebar.checkbox('Comparar com Outro Dataset'):
        compare_dataset_selection = st.sidebar.selectbox(
            'Selecione o Dataset para Comparação:', 
            options=[key for key in DATASET_OPTIONS.keys() if key != dataset_selection]
        )
        df_compare = load_data(DATASET_OPTIONS[compare_dataset_selection])

        st.write(f'## Comparação entre {dataset_selection} e {compare_dataset_selection}')
        st.write('### Distribuição de Movimentos por Tipo (Comparação)')
        combined_counts = pd.concat([
            df_filtered['movement_detail'].value_counts(),
            df_compare['movement_detail'].value_counts()
        ], axis=1, keys=[dataset_selection, compare_dataset_selection])
        st.bar_chart(combined_counts)

        st.write('### Duração Média dos Movimentos por Tipo (Comparação)')
        combined_means = pd.concat([
            df_filtered.groupby('movement_detail')['duration_calculated'].mean(),
            df_compare.groupby('movement_detail')['duration_calculated'].mean()
        ], axis=1, keys=[dataset_selection, compare_dataset_selection])
        st.line_chart(combined_means)

if __name__ == '__main__':
    main()
