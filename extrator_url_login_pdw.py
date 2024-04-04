import os
import ctypes
import re
import random

# Definição das cores para a saída no terminal
black = '\033[0;90m'
red = '\033[0;91m'
green = '\033[0;92m'
yellow = '\033[0;93m'
blue = '\033[0;94m'
purple = '\033[0;95m'
cyan = '\033[0;96m'
white = '\033[0;97m'
off = '\033[0m'
fgreen = '\033[42;97m'
fred = '\033[41;97m'
fblue = '\033[44;97m'

# Solicitação das palavras alvo e do nome do arquivo de saída
palavras_alvo = input(f"{green}[Palavras ou URLs Alvo (separados por espaço)]{off}: ").split()
saida = input(f"{green}[Nome do arquivo de saída (sem a extensão .txt)]{off}: ")
salvar_resultado = input(f"{green}[Deseja salvar o resultado? (S/N)]{off}: ").strip().lower() == 's'

# Definição do diretório pai
diretorio_pai = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clouds")

# Função para verificar se a linha contém todas as palavras alvo
def contem_palavras_alvo(linha):
    return all(palavra.lower() in linha.lower() for palavra in palavras_alvo)

# Variáveis globais para controle
total_success = 0
total_fail = 0
total_processed = 0
total_errors = 0

# Função para atualizar o título da janela do console
def update_window_title(percentage):
    global total_success, total_fail, total_processed
    title = f"Find:{total_success}|All:{total_fail} - {percentage:.2f}% - {palavras_alvo} "
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# Conjunto para armazenar linhas já escritas
linhas_escritas = set()

# Função para extrair URL, login e senha de uma linha
def extract_url_login_password(line):
    regex = r".*?([^:/]+)://([^:/]+):([^:/]+)"
    match = re.search(regex, line)
    if match:
        url = match.group(1)
        login = match.group(2)
        senha = match.group(3)
        return f"URL: {url}, Login: {login}, Senha: {senha}"
    return ""

# Pergunta se deseja processar um único arquivo ou todos do diretório
modo_selecao = input(f"{green}[Deseja processar um único arquivo (1) ou todos do diretório (2)?]{off}: ").strip()

arquivos = []
if modo_selecao == '1':
    arquivo_selecionado = input(f"{green}[Digite o caminho completo do arquivo txt a ser processado]{off}: ").strip()
    arquivos.append(arquivo_selecionado)
elif modo_selecao == '2':
    arquivos = [os.path.join(diretorio_pai, nome_arquivo) for nome_arquivo in os.listdir(diretorio_pai) if nome_arquivo.endswith(".txt")]
else:
    print(f"{red}Opção inválida.{off}")
    exit()

random.shuffle(arquivos)

if salvar_resultado:
    output_file = open(f"{saida}.txt", "w", encoding="utf-8")

# Lógica principal para processamento dos arquivos
for nome_arquivo in arquivos:
    try:
        with open(nome_arquivo, "r", encoding="utf-8", errors="ignore") as arquivo:
            total_lines = sum(1 for _ in arquivo)
            arquivo.seek(0)
            for numero_linha, linha in enumerate(arquivo, 1):
                linha = linha.strip()
                if contem_palavras_alvo(linha):
                    if linha not in linhas_escritas:
                        linhas_escritas.add(linha)
                        total_success += 1
                        if salvar_resultado:
                            output_file.write(f"{linha}\n\n")
                            output_file.flush()
                        print(f"{blue}{linha}{off}")
                    else:
                        total_fail += 1
                total_processed += 1
                if total_processed % 1000 == 0:
                    percentage_complete = (numero_linha / total_lines) * 100
                    update_window_title(percentage_complete)
    except Exception as e:
        total_errors += 1

update_window_title(100.0)

if salvar_resultado:
    output_file.close()
    print(f"Linhas com as palavras '{', '.join(palavras_alvo)}' foram salvas em {saida}.txt")
else:
    print("O resultado não foi salvo em um arquivo.")

print(f"{green}Processamento concluído.{off}")
print(f"{green}Total de linhas processadas: {total_processed}{off}")
print(f"{green}Total de linhas únicas com palavras alvo: {total_success}{off}")
print(f"{yellow}Total de linhas duplicadas ignoradas: {total_fail}{off}")
if total_errors > 0:
    print(f"{red}Total de erros durante o processamento: {total_errors}{off}")

