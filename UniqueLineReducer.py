import hashlib
import tkinter as tk
from tkinter import filedialog
import os
import shutil

def hash_line(line):
    return hashlib.md5(line).hexdigest()

def remove_duplicates_and_count_chunked(filename, target_directory, chunk_size=100000):
    seen_hashes = set()
    total_duplicates = 0
    original_filename = os.path.basename(filename)
    output_filename = os.path.join(target_directory, original_filename) + ".unique"
    
    with open(filename, 'rb') as infile, open(output_filename, 'wb') as outfile:
        lines = infile.readlines(chunk_size)
        while lines:
            for line in lines:
                line_hash = hash_line(line)
                if line_hash not in seen_hashes:
                    seen_hashes.add(line_hash)
                    outfile.write(line)
                else:
                    total_duplicates += 1
            lines = infile.readlines(chunk_size)
    
    os.remove(filename)
    os.rename(output_filename, os.path.join(target_directory, original_filename))
    return total_duplicates, os.path.join(target_directory, original_filename)

def get_file_size_kb(filename):
    size_bytes = os.path.getsize(filename)
    return round(size_bytes / 1024, 2)

def process_file(filename, target_directory):
    print(f"Processando arquivo: {filename}")
    size_before = get_file_size_kb(filename)
    total_duplicates, output_filename = remove_duplicates_and_count_chunked(filename, target_directory)
    size_after = get_file_size_kb(output_filename)
    print(f"Tamanho antes: {size_before} KB, depois: {size_after} KB")
    print(f"Total de linhas duplicadas removidas: {total_duplicates}")
    print(f"Arquivo processado salvo em: {output_filename}\n")

def select_file_or_directory(target_directory):
    root = tk.Tk()
    root.withdraw()
    choice = input("Digite '1' para selecionar um arquivo, ou '2' para selecionar um diretório: ")
    if choice == '1':
        filename = filedialog.askopenfilename()
        if filename:
            process_file(filename, target_directory)
        else:
            print("Nenhum arquivo foi selecionado.")
    elif choice == '2':
        directory = filedialog.askdirectory()
        if directory:
            for filename in os.listdir(directory):
                if filename.endswith('.txt'):
                    full_path = os.path.join(directory, filename)
                    process_file(full_path, target_directory)
        else:
            print("Nenhum diretório foi selecionado.")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    target_directory = "F:/programacao/python/kadu/cloud/db/limpo"
    select_file_or_directory(target_directory)
