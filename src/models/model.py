from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import streamlit as st

def discover_process_model(df):
    """Descobre o modelo de processo utilizando Heuristics Miner."""
    try:
        df.rename(columns={
            "processoID": "case:concept:name",
            "activity": "concept:name",
            "dataInicio": "time:timestamp"
        }, inplace=True)
        df = dataframe_utils.convert_timestamp_columns_in_df(df)
        event_log = log_converter.apply(df)
        heu_net = heuristics_miner.apply_heu(event_log)
        return heu_net
    except Exception as e:
        st.error(f"Erro na descoberta do modelo de processo: {e}")
        return None
    
def visualize_process_model(heu_net, scale=0.1):
    """Visualiza o modelo de processo como SVG."""
    try:
        gviz = hn_visualizer.apply(heu_net, parameters={"format": "svg", "scale": scale})
        hn_visualizer.save(gviz, "heuristics_net.svg")
        with open("heuristics_net.svg", "r") as f:
            return f.read()
    except Exception as e:
        st.error(f"Erro na visualização do modelo de processo: {e}")
        return None