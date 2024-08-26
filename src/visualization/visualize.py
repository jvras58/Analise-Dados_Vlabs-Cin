import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
# from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
# from pm4py.objects.log.util import dataframe_utils
# from pm4py.objects.conversion.log import converter as log_converter

def load_data(file_path):
    """Carrega os dados do arquivo CSV."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# FIXME: INCAPAZ DE VISUALIZAR MODELO NO STREAMLIT
# def discover_process_model(df):
#     """Descobre o modelo de processo utilizando Heuristics Miner."""
#     try:
#         df.rename(columns={
#             "processoID": "case:concept:name",
#             "activity": "concept:name",
#             "dataInicio": "time:timestamp"
#         }, inplace=True)
#         df = dataframe_utils.convert_timestamp_columns_in_df(df)
#         event_log = log_converter.apply(df)

#         # Aplicar o Heuristics Miner
#         heu_net = heuristics_miner.apply_heu(event_log)
        
#         return heu_net
#     except Exception as e:
#         st.error(f"Erro na descoberta do modelo de processo: {e}")
#         return None

# FIXME: INCAPAZ DE VISUALIZAR MODELO NO STREAMLIT
# def visualize_process_model(heu_net, scale=0.5):
#     """Visualiza o modelo de processo como SVG."""
#     try:
#         # Visualizando a Heuristics Net como SVG
#         gviz = hn_visualizer.apply(heu_net, parameters={"format": "svg", "scale": scale})
#         hn_visualizer.save(gviz, "heuristics_net.svg")
#         with open("heuristics_net.svg", "r") as f:
#             svg_content = f.read()
#         return svg_content
#     except Exception as e:
#         st.error(f"Erro na visualização do modelo de processo: {e}")
#         return None

def main():
    st.title("Análise de Movimentos Judiciais Especializados")

    BASE_PATH_DATA = '/workspace/data'
    st.sidebar.header('Configurações')

    dataset_options = {
        'Unidade 1': f'{BASE_PATH_DATA}/movimentos_unidade_1_processado.csv',
        'Unidade 2': f'{BASE_PATH_DATA}/movimentos_unidade_2_processado.csv'
    }
    dataset_selection = st.sidebar.selectbox(
        'Selecione o Dataset:', options=list(dataset_options.keys())
    )

    dataset_path = dataset_options[dataset_selection]
    df = load_data(dataset_path)
    if df is None:
        return

    if 'dataInicio' in df.columns and 'dataFinal' in df.columns:
        df['dataInicio'] = pd.to_datetime(df['dataInicio'])
        df['dataFinal'] = pd.to_datetime(df['dataFinal'])
    else:
        st.error("O DataFrame deve conter as colunas 'dataInicio' e 'dataFinal'.")
        return
    
    st.write(f'## Visualização dos Dados - {dataset_selection}')
    st.dataframe(df.head())

    # FIXME: INCAPAZ DE VISUALIZAR MODELO NO STREAMLIT
    # st.write("## Descoberta de Modelos de Processo")
    # heu_net = discover_process_model(df)
    # if heu_net is None:
    #     return

    # st.write("Modelo de Processo Descoberto:")
    # process_model_svg = visualize_process_model(heu_net)
    # if process_model_svg:
    #     st.markdown(f'<div style="text-align:center">{process_model_svg}</div>', unsafe_allow_html=True)

    st.write("## Análise Estatística")
    st.write("### Distribuição de Movimentos por Tipo")
    st.bar_chart(df['movement_detail'].value_counts())

    st.write("### Distribuição de Movimentos por Complexidade")
    st.bar_chart(df['complexity'].value_counts())

    st.write("### Duração Média dos Movimentos por Tipo")
    st.bar_chart(df.groupby('movement_detail')['duration_calculated'].mean())

    # Histograma usando Matplotlib
    st.write('### Histograma da Duração dos Movimentos')
    fig, ax = plt.subplots()
    ax.hist(df['duration_calculated'].dropna(), bins=30, color='skyblue', edgecolor='black')
    ax.set_xlabel('Duração (segundos)')
    ax.set_ylabel('Frequência')
    ax.set_title('Histograma da Duração dos Movimentos')
    st.pyplot(fig)

    # Box Plot usando Seaborn
    st.write('### Box Plot da Duração dos Movimentos por Complexidade')
    fig, ax = plt.subplots()
    sns.boxplot(x='complexity', y='duration_calculated', data=df, ax=ax)
    ax.set_xlabel('Complexidade')
    ax.set_ylabel('Duração (segundos)')
    ax.set_title('Box Plot da Duração dos Movimentos por Complexidade')
    st.pyplot(fig)

    st.write('## Filtros Personalizados')
    movement_filter = st.sidebar.multiselect(
        'Filtrar por Detalhe de Movimento:', options=df['movement_detail'].unique()
    )
    complexity_filter = st.sidebar.multiselect(
        'Filtrar por Complexidade:', options=df['complexity'].unique()
    )

    if movement_filter:
        df = df[df['movement_detail'].isin(movement_filter)]
    if complexity_filter:
        df = df[df['complexity'].isin(complexity_filter)]

    st.write('## Dados Filtrados')
    st.dataframe(df)

    st.write('### Gráficos Filtrados')
    st.write('Distribuição por Detalhe de Movimento Filtrado')
    st.bar_chart(df['movement_detail'].value_counts())

    st.write('Distribuição por Complexidade Filtrada')
    st.bar_chart(df['complexity'].value_counts())

    st.write('Duração Média dos Movimentos Filtrados por Tipo')
    st.line_chart(df.groupby('movement_detail')['duration_calculated'].mean())

    if st.sidebar.checkbox('Comparar com Outro Dataset'):
        compare_dataset_selection = st.sidebar.selectbox(
            'Selecione o Dataset para Comparação:', 
            options=[key for key in dataset_options.keys() if key != dataset_selection]
        )

        compare_dataset_path = dataset_options[compare_dataset_selection]
        df_compare = load_data(compare_dataset_path)

        st.write(f'## Comparação entre {dataset_selection} e {compare_dataset_selection}')
        st.write('### Distribuição de Movimentos por Tipo (Comparação)')
        st.bar_chart(pd.concat([
            df['movement_detail'].value_counts(),
            df_compare['movement_detail'].value_counts()
        ], axis=1, keys=[dataset_selection, compare_dataset_selection]))

        st.write('### Duração Média dos Movimentos por Tipo (Comparação)')
        combined_means = pd.concat([
            df.groupby('movement_detail')['duration_calculated'].mean(),
            df_compare.groupby('movement_detail')['duration_calculated'].mean()
        ], axis=1, keys=[dataset_selection, compare_dataset_selection])
        st.line_chart(combined_means)

if __name__ == '__main__':
    main()
