"""Coleção de funções utilitárias para auxiliar na análise de dados."""

from pathlib import Path


def open_data_file(file_path: str) -> str:
    """Abre um arquivo de dados e retorna seu conteúdo."""
    with Path.open(file_path) as file:
        return file.read()
