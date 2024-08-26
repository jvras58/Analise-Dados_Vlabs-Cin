import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def plot_histogram(df, column, bins=30):
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
    ax.set_xlabel('Duração (segundos)')
    ax.set_ylabel('Frequência')
    ax.set_title(f'Histograma da {column}')
    st.pyplot(fig)

def plot_boxplot(df, x, y):
    fig, ax = plt.subplots()
    sns.boxplot(x=x, y=y, data=df, ax=ax)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'Box Plot de {y} por {x}')
    st.pyplot(fig)

def plot_bar_chart(df, column):
    st.bar_chart(df[column].value_counts())

def plot_line_chart(df, group_by_col, calc_col):
    st.line_chart(df.groupby(group_by_col)[calc_col].mean())