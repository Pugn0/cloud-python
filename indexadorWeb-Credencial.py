import re
import os
import hashlib
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime, timezone
import ssl
from elasticsearch import Elasticsearch
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


# Cria um contexto SSL que não verifica certificados
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Conectar ao Elasticsearch
es = Elasticsearch(
    ["https://172.18.228.239:9200"],
    http_auth=('elastic', 'fo6MOtArAjkSdmj+bBqK'),
    verify_certs=False,
    ssl_context=context,
)



# O restante do seu código aqui

def gerar_id_documento(url, username, password):
    id_string = f"{url}{username}{password}"
    id_hash = hashlib.sha256(id_string.encode('utf-8')).hexdigest()
    return id_hash

def indexar_no_elasticsearch(objeto):
    documento_id = gerar_id_documento(objeto['url'], objeto['username'], objeto['password'])
    try:
        # A opção op_type='create' garante que o documento só será criado se não existir um documento com o mesmo ID
        res = es.index(index="leaked_credentials", id=documento_id, document=objeto, op_type='create')
        #print("Document ID:", res['_id'], "indexado com sucesso.")
    except Exception as e:
        if 'document already exists' in str(e):
            print(f"Documento com ID {documento_id} já existe e foi ignorado.")
        else:
            print(f"Erro ao indexar documento: {e}")

def extrair_detalhes(linha):
    linha_limpa = re.sub(r'^https?:\/\/(www\.)?', '', linha)
    partes = re.split(r'[:;|, ]', linha_limpa, maxsplit=2)
    
    if len(partes) >= 3:
        dominio, usuario, senha = partes[0], partes[1], partes[2]
        dominio, usuario, senha = normalizar_dados(dominio, usuario, senha)
        return dominio, usuario, senha, linha
    return None, None, None, None

def normalizar_dados(dominio, usuario, senha):
    url_pattern = re.compile(r'^(https?:\/\/)?(www\.)?[\w.-]+(\.[a-z]{2,})+\/?')
    
    if not url_pattern.match(dominio) and (url_pattern.match(usuario) or url_pattern.match(senha)):
        if url_pattern.match(usuario):
            dominio, usuario, senha = usuario, senha, dominio
        elif url_pattern.match(senha):
            dominio, usuario, senha = senha, dominio, usuario
    return dominio, usuario, senha

def processar_arquivo(caminho_do_arquivo, filtrar_por_palavra_chave, palavra_chave, source, category, email, phone, nick):
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    caminho_temporario = caminho_do_arquivo + ".tmp"
    
    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo, open(caminho_temporario, 'w', encoding='utf-8', errors='ignore') as temp_file:
            for linha in arquivo:
                # Se filtrar_por_palavra_chave for True, verifique a condição da palavra-chave
                condicao = (palavra_chave.lower() in linha.lower()) if filtrar_por_palavra_chave else True
                if condicao:
                    dominio, usuario, senha, linha_limpa = extrair_detalhes(linha.strip())
                    if dominio and usuario and senha:
                        objeto = {
                            "url": dominio,
                            "username": usuario,
                            "password": senha,
                            "line": linha_limpa,
                            "collection_timestamp": timestamp,
                            "source": source,
                            "category": category,
                            "contact_email": email,
                            "contact_phone": phone,
                            "contact_nick": nick
                        }
                        indexar_no_elasticsearch(objeto)
                        # Não escreva a linha processada no arquivo temporário
                        continue
                # Escreva a linha no arquivo temporário se não atender às condições de indexação ou se a palavra-chave não for encontrada
                temp_file.write(linha + "\n")
                
        # Substitua o arquivo original pelo temporário
        os.replace(caminho_temporario, caminho_do_arquivo)
                    
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")

def selecionar_arquivo_e_palavra_chave():
    root = tk.Tk()
    root.withdraw()
    caminho_do_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo TXT",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    
    if caminho_do_arquivo:
        decisao = input("Deseja buscar por uma palavra-chave? (S/N): ")
        if decisao.lower() == 's':
            filtrar_por_palavra_chave = True
            palavra_chave = input("Digite a palavra-chave para filtrar: ")
        else:
            filtrar_por_palavra_chave = False
            palavra_chave = ""
        
        source = input("Origem da Coleta: ")
        category = input("Categoria ou Tipo: ")
        email = input("Informações de Contato - E-mail: ")
        phone = input("Informações de Contato - Telefone: ")
        nick = input("Informações de Contato - @Nick: ")
        
        processar_arquivo(caminho_do_arquivo, filtrar_por_palavra_chave, palavra_chave, source, category, email, phone, nick)
    else:
        print("Nenhum arquivo foi selecionado.")

if __name__ == "__main__":
    selecionar_arquivo_e_palavra_chave()



#