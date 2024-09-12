import re
import os
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime, timezone
from tqdm import tqdm
from colorama import init, Fore

init(autoreset=True)  # Inicializa colorama

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
def criar_json(dominio, usuario, senha, linha):
    objeto = {
        "url": dominio,
        "username": usuario,
        "password": senha,
        "line": linha
    }
    return json.dumps(objeto, indent=2)

def processar_arquivo(caminho_do_arquivo, palavra_chave, resultados, pbar):
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"
    try:
        total_resultados = 0
        with open(caminho_do_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
            for linha in arquivo:
                if palavra_chave.lower() in linha.lower():
                    dominio, usuario, senha, linha = extrair_detalhes(linha.strip())
                    if dominio and usuario and senha:
                        objeto_json = criar_json(dominio, usuario, senha, linha)
                        resultados.append(objeto_json)
                        total_resultados += 1
                        # Atualiza a descrição da barra de progresso com a quantidade de resultados encontrados
                        pbar.set_description(f"{Fore.BLUE}Progresso - {total_resultados} resultados encontrados")
        pbar.update(1)  # Incrementa o progresso da barra
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro ao processar o arquivo: {e}")



def processar_diretorio(diretorio, palavra_chave):
    resultados = []
    arquivos = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(".txt")]
    with tqdm(total=len(arquivos), desc=f"{Fore.BLUE}Progresso", unit="arquivos", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)) as pbar:
        for arquivo in arquivos:
            caminho_completo = os.path.join(diretorio, arquivo)
            processar_arquivo(caminho_completo, palavra_chave, resultados, pbar)  # Adiciona o argumento pbar
    return resultados


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
        if tipo == 'a':
            resultados = []
            processar_arquivo(caminho, palavra_chave, resultados)
            mostrar_resultados(resultados)
        elif tipo == 'd':
            resultados = processar_diretorio(caminho, palavra_chave)
            mostrar_resultados(resultados)
    else:
        print("Nenhuma seleção foi feita.")

def mostrar_resultados(resultados):
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
    else:
        print(f"{Fore.YELLOW}Nenhum resultado encontrado.")

if __name__ == "__main__":
    while True:
        try:
            opcao = int(input("Escolha uma opção: \n1 - Continuar \n2 - Fechar \n> "))
            if opcao == 1:
                coletar_dados_e_processar()
            elif opcao == 2:
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Por favor, escolha 1 ou 2.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")