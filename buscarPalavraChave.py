import re
import time
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime

# Função para extrair detalhes da linha
def extrair_detalhes(linha):
    # Remove o protocolo e "www" se presentes
    linha_limpa = re.sub(r'^https?:\/\/(www\.)?', '', linha)
    
    # Separa os dados usando múltiplos delimitadores possíveis
    partes = re.split(r'[:;|, ]', linha_limpa, maxsplit=2)
    
    if len(partes) >= 3:
        # Inicialmente atribui as partes extraídas à domínio, usuário e senha
        dominio, usuario, senha = partes[0], partes[1], partes[2]

        # Normaliza os dados para garantir a ordem correta
        dominio, usuario, senha = normalizar_dados(dominio, usuario, senha)

        return dominio, usuario, senha, linha
    else:
        return None, None, None, None

# Função para normalizar os dados extraídos
def normalizar_dados(dominio, usuario, senha):
    # Define a regra para identificar uma URL
    url_pattern = re.compile(r'^(https?:\/\/)?(www\.)?[\w.-]+(\.[a-z]{2,})+\/?')
    
    # Verifica se 'dominio' não parece uma URL (e.g., parece um usuário ou senha),
    # e se 'usuario' ou 'senha' parecem uma URL.
    if not url_pattern.match(dominio) and (url_pattern.match(usuario) or url_pattern.match(senha)):
        # Se 'usuario' parece mais com uma URL, assume que essa é a ordem invertida: usuário, senha, domínio
        if url_pattern.match(usuario):
            dominio, usuario, senha = usuario, senha, dominio
        # Se 'senha' parece mais com uma URL, assume que essa é a ordem: senha, domínio, usuário
        elif url_pattern.match(senha):
            dominio, usuario, senha = senha, dominio, usuario
    
    # Retorna os dados corrigidos
    return dominio, usuario, senha

# Função para criar o objeto JSON
def criar_json(dominio, usuario, senha, linha, timestamp, source, category, email, phone, nick):
    objeto = {
        "url": dominio,
        "username": usuario,
        "password": senha,
        "line": linha,
        "collection_timestamp": timestamp,
        "source": source,
        "category": category,
        "contact_email": email,
        "contact_phone": phone,
        "contact_nick": nick
    }
    return json.dumps(objeto, indent=2)

def processar_arquivo(caminho_do_arquivo, palavra_chave, source, category, email, phone, nick):
    # Obtem a data e hora atual em UTC no formato ISO 8601
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
            resultados = []  # Lista para armazenar os resultados
            for linha in arquivo:
                if palavra_chave.lower() in linha.lower():
                    dominio, usuario, senha, linha = extrair_detalhes(linha.strip())
                    if dominio and usuario and senha:
                        objeto_json = criar_json(dominio, usuario, senha, linha, timestamp, source, category, email, phone, nick)
                        resultados.append(objeto_json)
                        print(objeto_json)

        if resultados:
            salvar_resultados = input("Deseja salvar os resultados em um arquivo? (S/N): ").strip().upper()
            if salvar_resultados == 'S':
                nome_arquivo = input("Digite o nome do arquivo para salvar (sem extensão): ")
                nome_arquivo += ".txt"  # Adicionando a extensão de arquivo
                local_arquivo = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nome_arquivo, title="Salvar como")
                with open(local_arquivo, 'w') as arquivo_saida:
                    for resultado in resultados:
                        arquivo_saida.write(resultado + '\n')
                print(f"Os resultados foram salvos em {local_arquivo}")

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

def selecionar_arquivo_e_palavra_chave():
    root = tk.Tk()
    root.withdraw()  # Esconder a janela principal do Tkinter
    caminho_do_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if caminho_do_arquivo:
        palavra_chave = input("Digite a palavra-chave para filtrar: ")
        # Solicita informações, exceto a data/hora da coleta
        source = input("Origem da Coleta: ")
        category = input("Categoria ou Tipo: ")
        email = input("Informações de Contato - E-mail: ")
        phone = input("Informações de Contato - Telefone: ")
        nick = input("Informações de Contato - @Nick: ")
        
        # A data/hora da coleta é obtida automaticamente
        processar_arquivo(caminho_do_arquivo, palavra_chave, source, category, email, phone, nick)
    else:
        print("Nenhum arquivo foi selecionado.")


if __name__ == "__main__":
    selecionar_arquivo_e_palavra_chave()
