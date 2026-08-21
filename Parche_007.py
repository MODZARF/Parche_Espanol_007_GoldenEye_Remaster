import os
import sys
import hashlib
import tkinter as tk
from tkinter import filedialog
import time


os.system("")

print(r"""

            ________      ________      ________      ________ 
---------- |\_____  \    |\   __  \    |\   __  \    |\  _____\----------------
----------  \|___/  /|   \ \  \|\  \   \ \  \|\  \   \ \  \__/ ---------------
--------------  /  / /    \ \   __  \   \ \   _  _\   \ \   __\--------------
-------------- /  /_/__    \ \  \ \  \   \ \  \\  \|   \ \  \_|----------------
------------- |\________\   \ \__\ \__\   \ \__\\ _\    \ \__\ ----------------
-------------- \|_______|    \|__|\|__|    \|__|\|__|    \|__| -----------------

""")

def calcular_hash(archivo):
    h = hashlib.sha256()
    with open(archivo, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def aplicar_parche(ruta_zarf, ruta_original):
    with open(ruta_zarf, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = f.readlines()

    # Agrupamos todo por archivo para abrir cada archivo solo 1 vez
    parches_por_archivo = {}
    archivo_actual = None
    ruta_actual = ""
    hash_actual = ""

    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if not linea:
            continue
        if linea.startswith('Archivo ='):
            archivo_actual = linea.split('=', 1)[1].strip().strip('"')
        elif linea.startswith('Ruta ='):
            ruta_actual = linea.split('=', 1)[1].strip().strip('"')
        elif linea.startswith('Hash ='):
            hash_actual = linea.split('=', 1)[1].strip().strip('"')
        elif linea.startswith('O ='):
            try:
                offset = int(linea.split('=', 1)[1].strip(), 16)
                # La siguiente linea son los bytes
                bytes_hex_line = lineas[i+1].strip().split('=', 1)[1].strip()
                key = (archivo_actual, ruta_actual, hash_actual)
                if key not in parches_por_archivo:
                    parches_por_archivo[key] = []
                parches_por_archivo[key].append((offset, bytes_hex_line))
            except:
                continue

    total_archivos = len(parches_por_archivo)
    print(f"\nSe encontraron {total_archivos} archivos para parchear\n")

    for idx, ((archivo, ruta, hash_esperado), ops) in enumerate(parches_por_archivo.items(), 1):
        ruta_completa = os.path.join(ruta_original, ruta, archivo) if ruta else os.path.join(ruta_original, archivo)
        print(f"\033[93m[{idx}/{total_archivos}] {ruta_completa}\033[0m", end='\r')

        if not os.path.exists(ruta_completa):
            print(f"\n\033[91mError: No existe {ruta_completa}\033[0m")
            input("Enter para salir...")
            sys.exit(1)

        if calcular_hash(ruta_completa)!= hash_esperado:
            print(f"\n\033[91mError de hash en {archivo}. El archivo no es la versión esperada.\033[0m")
            print("Busca ayuda en https://youtube.com/@MODZARF")
            input("Enter para salir...")
            sys.exit(1)

        with open(ruta_completa, 'r+b') as fo:
            for offset, hex_data in ops:
                fo.seek(offset)
                fo.write(bytes.fromhex(hex_data.replace(" ", "")))

        print(f"\033[92m[{idx}/{total_archivos}] OK - {archivo} ({len(ops)} cambios)\033[0m")

def main():
    if getattr(sys, 'frozen', False):
        ruta_script = os.path.dirname(sys.executable)
    else:
        ruta_script = os.path.dirname(os.path.abspath(__file__))

    ruta_zarf = os.path.join(ruta_script, 'parche.ZARF')

    if not os.path.exists(ruta_zarf):
        print(f"\033[91mError: No se encontró parche.ZARF en {ruta_script}\033[0m")
        input("Enter para salir...")
        sys.exit(1)

    print("""
  Parche textos ESPAÑOL-007 Goldeneye Remaster-Xbox360
    """)
    print("Selecciona la carpeta raíz del juego...")
    for i in range(3, 0, -1):
        print(f"Abriendo ventana en {i}...", end='\r')
        time.sleep(1)

    root = tk.Tk()
    root.withdraw()
    ruta_original = filedialog.askdirectory(title="Selecciona la carpeta de GoldenEye 007")

    if not ruta_original:
        print("Cancelado por el usuario.")
        sys.exit()

    print(f"\n\033[96mAplicando parche en: {ruta_original}\033[0m\n")
    aplicar_parche(ruta_zarf, ruta_original)
    print(f"\n\033[92m¡Parche aplicado con éxito! :)\033[0m")
    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()