import os

# Definindo a pasta onde os arquivos .txt estão localizados
pasta = 'clouds/'

# Lista de protocolos para procurar
protocolos = ['http://', 'https://', 'ftp://']

# Inicializando um dicionário para contar as ocorrências de cada protocolo
contagem_protocolos = {protocolo: 0 for protocolo in protocolos}

# Percorrendo os arquivos na pasta
for arquivo in os.listdir(pasta):
    # Certifique-se de que estamos trabalhando apenas com arquivos .txt
    if arquivo.endswith('.txt'):
        # Construindo o caminho completo para o arquivo
        caminho_completo = os.path.join(pasta, arquivo)

        # Abrindo e lendo o arquivo linha por linha
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            for linha in f:
                # Contando as ocorrências de cada protocolo na linha
                for protocolo in protocolos:
                    contagem_protocolos[protocolo] += linha.count(protocolo)

        # Atualizando a contagem em tempo real
        atualizacao = ' '.join([f"{proto}: {cont}" for proto, cont in contagem_protocolos.items()])
        print(f"\r{atualizacao}", end="", flush=True)

# Quebra de linha final após o loop completar
print("\n\nContagem final de protocolos encontrados:")
for protocolo, contagem in contagem_protocolos.items():
    print
