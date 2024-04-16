import re
import os
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime

# Função para extrair detalhes da linha
def extrair_detalhes(linha):
    linha_limpa = re.sub(r'^https?:\/\/(www\.)?', '', linha)
    partes = re.split(r'[:;|, ]', linha_limpa, maxsplit=2)
    if len(partes) >= 3:
        dominio, usuario, senha = partes[0], partes[1], partes[2]
        dominio, usuario, senha = normalizar_dados(dominio, usuario, senha)
        return dominio, usuario, senha, linha
    else:
        return None, None, None, None

# Função para normalizar os dados extraídos
def normalizar_dados(dominio, usuario, senha):
    url_pattern = re.compile(r'^(https?:\/\/)?(www\.)?[\w.-]+(\.[a-z]{2,})+\/?')
    if not url_pattern.match(dominio) and (url_pattern.match(usuario) or url_pattern.match(senha)):
        if url_pattern.match(usuario):
            dominio, usuario, senha = usuario, senha, dominio
        elif url_pattern.match(senha):
            dominio, usuario, senha = senha, dominio, usuario
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
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
            resultados = []
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
                    nome_arquivo += ".txt"
                    local_arquivo = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nome_arquivo, title="Salvar como")
                    with open(local_arquivo, 'w') as arquivo_saida:
                        for resultado in resultados:
                            arquivo_saida.write(resultado + '\n')
                    print(f"Os resultados foram salvos em {local_arquivo}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

def processar_diretorio(diretorio, palavra_chave, source, category, email, phone, nick):
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt"):
            caminho_completo = os.path.join(diretorio, arquivo)
            print(f"Processando arquivo: {caminho_completo}")
            processar_arquivo(caminho_completo, palavra_chave, source, category, email, phone, nick)

def selecionar_arquivo_ou_diretorio():
    root = tk.Tk()
    root.withdraw()
    escolha = input("Você deseja selecionar um arquivo ('a') ou um diretório ('d')? ").strip().lower()
    if escolha == 'a':
        caminho = filedialog.askopenfilename(title="Selecione o arquivo TXT", filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")))
    elif escolha == 'd':
        caminho = filedialog.askdirectory(title="Selecione o Diretório")
    else:
        print("Opção inválida. Tente novamente.")
        return None, None
    return caminho, escolha

def coletar_dados_e_processar():
    caminho, tipo = selecionar_arquivo_ou_diretorio()
    if caminho:
        palavra_chave = input("Digite a palavra-chave para filtrar: ")
        source = input("Origem da Coleta: ")
        category = input("Categoria ou Tipo: ")
        email = input("Informações de Contato - E-mail: ")
        phone = input("Informações de Contato - Telefone: ")
        nick = input("Informações de Contato - @Nick: ")
        if tipo == 'a':
            processar_arquivo(caminho, palavra_chave, source, category, email, phone, nick)
        elif tipo == 'd':
            processar_diretorio(caminho, palavra_chave, source, category, email, phone, nick)
    else:
        print("Nenhuma seleção foi feita.")

if __name__ == "__main__":
    coletar_dados_e_processar()
