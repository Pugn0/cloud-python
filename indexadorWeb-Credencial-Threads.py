import re
import os
import ssl
import json
import urllib3
import hashlib
import warnings
import tkinter as tk
from tkinter import filedialog, simpledialog
from datetime import datetime, timezone
from elasticsearch import Elasticsearch
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed


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

def processar_arquivo(caminho_do_arquivo, filtrar_por_palavra_chave, palavra_chave):
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    caminho_temporario = caminho_do_arquivo + ".tmp"
    objetos_para_indexar = []

    try:
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo, open(caminho_temporario, 'w', encoding='utf-8', errors='ignore') as temp_file:
            for linha in arquivo:
                condicao = (palavra_chave.lower() in linha.lower()) if filtrar_por_palavra_chave else True
                if condicao:
                    dominio, usuario, senha, linha_limpa = extrair_detalhes(linha.strip())
                    if dominio and usuario and senha:
                        objeto = {
                            "url": dominio,
                            "username": usuario,
                            "password": senha,
                            "line": linha_limpa,
                            "collection_timestamp": timestamp
                        }
                        objetos_para_indexar.append(objeto)
                        continue
                temp_file.write(linha + "\n")

        if objetos_para_indexar:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_objeto = {executor.submit(indexar_no_elasticsearch, obj): obj for obj in objetos_para_indexar}
                for future in as_completed(future_to_objeto):
                    obj = future_to_objeto[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(f'Erro ao indexar objeto {obj}: {exc}')

        os.replace(caminho_temporario, caminho_do_arquivo)
                    
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")


def selecionar_arquivos_e_palavra_chave():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter

    decisao = simpledialog.askstring("Seleção de Arquivo", "Digite '1' para selecionar um arquivo específico ou '2' para selecionar todos os arquivos em um diretório")

    if decisao == '1':
        caminho_do_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo TXT",
            filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        arquivos_para_processar = [caminho_do_arquivo] if caminho_do_arquivo else []
    elif decisao == '2':
        caminho_do_diretorio = filedialog.askdirectory(title="Selecione o diretório")
        arquivos_para_processar = [os.path.join(caminho_do_diretorio, f) for f in os.listdir(caminho_do_diretorio) if f.endswith('.txt')]
    else:
        print("Opção inválida. Por favor, escolha '1' ou '2'.")
        root.destroy()
        return

    for arquivo in arquivos_para_processar:
        if arquivo:
            decisao_palavra_chave = simpledialog.askstring("Filtro", "Deseja buscar por uma palavra-chave? (S/N): ")
            if decisao_palavra_chave and decisao_palavra_chave.lower() == 's':
                palavra_chave = simpledialog.askstring("Palavra-chave", "Digite a palavra-chave para filtrar: ")
                filtrar_por_palavra_chave = True
            else:
                palavra_chave = ""
                filtrar_por_palavra_chave = False

            processar_arquivo(arquivo, filtrar_por_palavra_chave, palavra_chave)
        else:
            print("Nenhum arquivo foi selecionado.")

    root.destroy()

if __name__ == "__main__":
    selecionar_arquivos_e_palavra_chave()



# Este script é projetado para processar documentos de texto contendo informações de
# credenciais vazadas, como URLs, nomes de usuário e senhas. Ele permite ao usuário escolher 
# entre filtrar as linhas por uma palavra-chave específica ou processar todas as linhas do 
# documento. As informações extraídas são então indexadas em um banco de dados Elasticsearch 
# para análise e monitoramento. Durante o processo, o script remove do arquivo original as linhas 
# que foram processadas, ajudando a gerenciar o espaço de armazenamento ao evitar duplicações 
# no banco de dados.
# I Love chatGPT and by Pugno > t.me/pugno_fc