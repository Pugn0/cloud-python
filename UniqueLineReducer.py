import tkinter as tk
from tkinter import filedialog
from collections import OrderedDict
import os

def remove_duplicates_and_count(filename):
    seen = OrderedDict()
    total_duplicates = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line in seen:
                total_duplicates += 1
            seen[line] = seen.get(line, 0) + 1

    with open(filename, 'w', encoding='utf-8') as f:
        for line in seen.keys():
            f.write(line)

    return total_duplicates

def get_file_size_kb(filename):
    # Retorna o tamanho do arquivo em kilobytes (KB) e arredonda para duas casas decimais
    size_bytes = os.path.getsize(filename)
    return round(size_bytes / 1024, 2)

def select_file():
    root = tk.Tk()
    root.withdraw()  # Para não abrir a janela principal do Tkinter.
    filename = filedialog.askopenfilename()
    if filename:
        print(f"Arquivo selecionado: {filename}")
        size_before = get_file_size_kb(filename)
        print(f"Tamanho antes: {size_before} KB")
        total_duplicates = remove_duplicates_and_count(filename)
        size_after = get_file_size_kb(filename)
        print(f"Tamanho depois: {size_after} KB")
        print(f"Total de linhas duplicadas removidas: {total_duplicates}")
        print(f"Redução de tamanho: {size_before - size_after} KB")
    else:
        print("Nenhum arquivo foi selecionado.")

if __name__ == "__main__":
    select_file()
