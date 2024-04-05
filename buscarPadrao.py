import tkinter as tk
from tkinter import filedialog
import re

# Função para abrir a janela de seleção de arquivo e retornar o caminho do arquivo escolhido
def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal do Tkinter
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return caminho_arquivo

# Função para processar o arquivo selecionado
def processar_arquivo(caminho_arquivo):
    separadores_comuns = [',', ';', '|', ':', '\t', ' ']
    padrao_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    padrao_site = re.compile(r'\b(?:http://www\.|https://www\.|http://|https://)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?\b')
    
    def identificar_separador(linha):
        for sep in separadores_comuns:
            if sep in linha:
                partes = linha.split(sep)
                if any(padrao_email.match(parte) for parte in partes) and any(padrao_site.match(parte) for parte in partes):
                    return sep
        return None

    separadores_encontrados = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            separador = identificar_separador(linha.strip())
            if separador:
                separadores_encontrados.append(separador)
            print(f'Linha: {linha.strip()} | Separador encontrado: {separador}')


    if separadores_encontrados:
        separador_mais_comum = max(set(separadores_encontrados), key=separadores_encontrados.count)
        print(f'O separador mais comum é: {separador_mais_comum}')
    else:
        print('Não foi possível identificar um separador comum.')

# Executar a função para selecionar o arquivo
caminho_do_arquivo = selecionar_arquivo()

# Se um arquivo foi selecionado, processá-lo
if caminho_do_arquivo:
    processar_arquivo(caminho_do_arquivo)
else:
    print("Nenhum arquivo foi selecionado.")
