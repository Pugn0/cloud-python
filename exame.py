import os

pasta = 'clouds/'
protocolos = ['http://', 'https://', 'ftp://']
contagem_protocolos = {protocolo: 0 for protocolo in protocolos}

for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                for protocolo in protocolos:
                    contagem_protocolos[protocolo] += linha.count(protocolo)

        atualizacao = ' '.join([f"{proto}: {cont}" for proto, cont in contagem_protocolos.items()])
        print(f"\r{atualizacao}", end="", flush=True)

print("\n\nContagem final de protocolos encontrados:")
for protocolo, contagem in contagem_protocolos.items():
    print(f"{protocolo}: {contagem}")
