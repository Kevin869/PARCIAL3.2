import os
import subprocess

# Todos los juegos y la miniconsola están dentro de PROYECTO_RECUPERACION
juegos = {
    "Kevin": {"archivo": "JUEGO_KEVIN.py", "autor": "Kevin"},
    "Martin": {"archivo": "JUEGO_MARTIN.py", "autor": "Martin"},
    "Fabian": {"archivo": "JUEGO_FABIAN.py", "autor": "Ana"},
    "Brandon": {"archivo": "JUEGO_BRANDON.py", "autor": "Brandon"},
    "Luis": {"archivo": "JUEGO_LUIS.py", "autor": "Luis"},
    "Enrique": {"archivo": "JUEGO_ENRIQUE.py", "autor": "Enrique"},
    "Daniel": {"archivo": "JUEGO_DANIEL.py", "autor": "Daniel"},
    "Emily": {"archivo": "JUEGO_EMILY.py", "autor": "Emily"},
    "Emilio": {"archivo": "JUEGO_EMILIO.py", "autor": "Emilio"},
    "Itzel": {"archivo": "JUEGO_ITZEL.py", "autor": "Itzel"}
}

def mostrar_menu():
    print("=== 🎮 MiniConsola de Juegos ===")
    for i, (nombre, datos) in enumerate(juegos.items(), start=1):
        print(f"{i}. {nombre} (Creado por {datos['autor']})")
    print("0. Salir")

def ejecutar_juego(opcion):
    if opcion == "0":
        print("👋 Saliendo de la miniconsola...")
        exit()

    try:
        indice = int(opcion) - 1
        nombre_juego = list(juegos.keys())[indice]
        archivo = juegos[nombre_juego]["archivo"]

        if os.path.exists(archivo):
            print(f"\n▶ Ejecutando {nombre_juego}...\n")
            subprocess.run(["python", archivo])  
        else:
            print("⚠️ No se encontró el archivo del juego:", archivo)
    except (ValueError, IndexError):
        print("❌ Opción inválida, intenta de nuevo.")

while True:
    mostrar_menu()
    opcion = input("Selecciona un juego: ")
    ejecutar_juego(opcion)
    print("\n" + "-"*40 + "\n")
