import tkinter as tk
from tkinter import filedialog
import re
from tqdm import tqdm
from collections import Counter

# Função para abrir a janela de seleção de arquivo
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return caminho_arquivo

# Função para processar o arquivo selecionado
def processar_arquivo(caminho_arquivo):
    separadores_comuns = [',', ';', '|', ':', '\t', ' ']
    separadores_encontrados = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Usar tqdm para mostrar a barra de progresso
    for linha in tqdm(linhas, desc="Processando"):
        for sep in separadores_comuns:
            if sep in linha:
                separadores_encontrados.append(sep)
                break  # Assumindo que cada linha usa apenas um tipo de separador

    # Contar a frequência de cada separador
    contador_separadores = Counter(separadores_encontrados)
    total_separadores = sum(contador_separadores.values())

    # Imprimir estatísticas
    print("\nEstatísticas de Separadores:")
    for separador, contagem in contador_separadores.items():
        porcentagem = (contagem / total_separadores) * 100
        print(f"Separador '{separador}': {contagem} ocorrências, {porcentagem:.2f}%")

# Executar a função para selecionar o arquivo
caminho_do_arquivo = selecionar_arquivo()

# Se um arquivo foi selecionado, processá-lo
if caminho_do_arquivo:
    processar_arquivo(caminho_do_arquivo)
else:
    print("Nenhum arquivo foi selecionado.")
