import re
import time
import tkinter as tk
from tkinter import filedialog
import json

# Função para extrair detalhes da linha
def extrair_detalhes(linha):
    # Remove o protocolo e "www" se presentes
    linha_limpa = re.sub(r'^https?:\/\/(www\.)?', '', linha)
    
    # Separa os dados usando múltiplos delimitadores possíveis
    partes = re.split(r'[:;|, ]', linha_limpa, maxsplit=2)
    
    if len(partes) >= 3:
        # Extrai o domínio, que pode incluir caminhos após o nome de domínio principal
        # Até o primeiro delimitador de detalhes de login (usuário/senha)
        dominio = partes[0]
        # Assume que as partes restantes são o usuário e a senha, respectivamente
        usuario = partes[1]
        senha = partes[2]
        
        return dominio, usuario, senha
    else:
        return None, None, None

# Função para criar o objeto JSON
def criar_json(dominio, usuario, senha):
    objeto = {
        "url": dominio,
        "username": usuario,
        "password": senha
    }
    return json.dumps(objeto, indent=2)

# Função para processar o arquivo com filtro de palavra-chave
def processar_arquivo(caminho_do_arquivo, palavra_chave):
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
            for linha in arquivo:
                if palavra_chave.lower() in linha.lower():
                    dominio, usuario, senha = extrair_detalhes(linha.strip())
                    if dominio and usuario and senha:
                        objeto_json = criar_json(dominio, usuario, senha)
                        print(objeto_json)

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")


# Inicializar a interface gráfica para seleção do arquivo e inserir palavra-chave
def selecionar_arquivo_e_palavra_chave():
    root = tk.Tk()
    root.withdraw()  # Esconder a janela principal do Tkinter
    caminho_do_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if caminho_do_arquivo:
        palavra_chave = input("Digite a palavra-chave para filtrar: ")
        processar_arquivo(caminho_do_arquivo, palavra_chave)
    else:
        print("Nenhum arquivo foi selecionado.")

if __name__ == "__main__":
    selecionar_arquivo_e_palavra_chave()
