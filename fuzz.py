import os

def buscar_palavra(base_dir, palavra):
    encontrados = set()  # usar set para evitar arquivos repetidos
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            try:
                with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                    for linha in f:
                        if palavra in linha:
                            encontrados.add(caminho_arquivo)
                            break  # já encontrou no arquivo, não precisa continuar lendo
            except Exception as e:
                print(f"Erro ao ler {caminho_arquivo}: {e}")

    for arquivo in encontrados:
        print(arquivo)

if __name__ == "__main__":
    pasta_base = input("Digite o caminho da pasta onde deseja começar a busca: ").strip()
    palavra_chave = input("Digite a palavra chave para buscar: ").strip()
    buscar_palavra(pasta_base, palavra_chave)
