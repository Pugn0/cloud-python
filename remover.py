import os

# Definindo a pasta onde os arquivos .txt estão localizados
pasta = 'clouds/'
limpo_pasta = os.path.join(pasta, "limpo")
os.makedirs(limpo_pasta, exist_ok=True)

def remover_linhas_duplicadas_arquivo(caminho_arquivo):
    linhas_unicas = set()
    linhas_para_manter = []

    # Lendo o arquivo e removendo linhas duplicadas
    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
        for linha in arquivo:
            if linha not in linhas_unicas:
                linhas_unicas.add(linha)
                linhas_para_manter.append(linha)

    # Reescrevendo o arquivo com as linhas únicas
    with open(caminho_arquivo, 'w', encoding='utf-8', errors='ignore') as arquivo:
        arquivo.writelines(linhas_para_manter)

    # Movendo o arquivo para a pasta "limpo"
    nome_arquivo = os.path.basename(caminho_arquivo)
    novo_caminho = os.path.join(limpo_pasta, nome_arquivo)
    os.replace(caminho_arquivo, novo_caminho)

# Percorrendo os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_arquivo = os.path.join(pasta, arquivo)
        remover_linhas_duplicadas_arquivo(caminho_arquivo)

print("Linhas duplicadas removidas de todos os arquivos .txt dentro da pasta '/filtro/'.")
print("Arquivos movidos para a pasta 'limpo'.")
