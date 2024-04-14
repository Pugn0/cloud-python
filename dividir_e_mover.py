import os
from datetime import datetime

def dividir_arquivo(nome_arquivo, linhas_por_arquivo, pasta_destino, codificacao='utf-8', estrategia_erro='replace'):
    # Certifique-se de que a pasta de destino existe
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        with open(nome_arquivo, 'r', encoding=codificacao, errors=estrategia_erro) as arquivo:
            contador_partes = 0
            linhas_contador = 0
            arquivo_destino = None

            for linha in arquivo:
                if linhas_contador == 0:
                    contador_partes += 1
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    nome_arquivo_destino = os.path.join(pasta_destino, f"parte_{contador_partes}_{timestamp}.txt")
                    arquivo_destino = open(nome_arquivo_destino, 'w', encoding=codificacao, errors=estrategia_erro)
                    print(f"Criando arquivo: {nome_arquivo_destino}")

                arquivo_destino.write(linha)
                linhas_contador += 1

                if linhas_contador == linhas_por_arquivo:
                    arquivo_destino.close()
                    linhas_contador = 0

            # Fecha o último arquivo se não tiver sido fechado ainda
            if arquivo_destino and not arquivo_destino.closed:
                arquivo_destino.close()

        print("Processamento concluído. Todos os arquivos foram criados com sucesso.")
    except UnicodeDecodeError as e:
        print(f"Erro de decodificação: {e}. O arquivo pode não ser totalmente compatível com a codificação '{codificacao}' ou contém caracteres não decodificáveis.")
        # Remove o último arquivo se estiver incompleto devido ao erro
        if arquivo_destino and not arquivo_destino.closed:
            arquivo_destino.close()
            os.remove(nome_arquivo_destino)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Parâmetros
nome_arquivo_original = "https.txt"
linhas_por_arquivo = 100000  # Defina o número desejado de linhas por arquivo
pasta_destino = "F:/programacao/python/kadu/cloud/db/filtro/http/"

# Execução
dividir_arquivo(nome_arquivo_original, linhas_por_arquivo, pasta_destino)
