#!/usr/bin/env python3
# Sistema de Gestión de Aventuras RPG
# Proyecto Final - Juego de Texto Interactivo

import json
import os
import random
from colorama import Fore, Style, init

# Inicializar colorama para colores en consola
init(autoreset=True)

# Archivos de datos
JUGADORES_FILE = "jugadores.json"
PROGRESO_FILE = "progreso.json"

# Clases disponibles con bonificaciones
CLASES = {
    "mago": {"vida": 80, "ataque": 15, "defensa": 5, "magia": 25},
    "guerrero": {"vida": 120, "ataque": 20, "defensa": 15, "magia": 5},
    "explorador": {"vida": 100, "ataque": 12, "defensa": 10, "magia": 8},
    "arquero": {"vida": 90, "ataque": 18, "defensa": 8, "magia": 4}
}

# Items disponibles
ITEMS = {
    "poción_vida": {"tipo": "consumible", "efecto": "restaurar 30 de vida"},
    "poción_mana": {"tipo": "consumible", "efecto": "restaurar 20 de magia"},
    "espada_hierro": {"tipo": "arma", "ataque": 10},
    "armadura_cuero": {"tipo": "armadura", "defensa": 8},
    "libro_hechizos": {"tipo": "magia", "magia": 15}
}

# Enemigos disponibles
ENEMIGOS = {
    "goblin": {"vida": 50, "ataque": 8, "defensa": 3, "experiencia": 20},
    "orco": {"vida": 80, "ataque": 12, "defensa": 6, "experiencia": 35},
    "lobo": {"vida": 40, "ataque": 10, "defensa": 2, "experiencia": 15},
    "esqueleto": {"vida": 60, "ataque": 9, "defensa": 4, "experiencia": 25}
}

def mostrar_titulo():
    """Función para mostrar el título del juego con colores"""
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "      SISTEMA DE GESTIÓN DE AVENTURAS RPG")
    print(Fore.CYAN + "=" * 60)
    print()

def limpiar_pantalla():
    """Función para limpiar la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos(archivo):
    """Cargar datos desde archivo JSON"""
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(datos, archivo):
    """Guardar datos en archivo JSON"""
    with open(archivo, 'w') as f:
        json.dump(datos, f, indent=2)

def registrar_jugador():
    """Registrar un nuevo jugador"""
    print(Fore.GREEN + "\n--- REGISTRO DE NUEVO JUGADOR ---")
    
    nombre = input(Fore.WHITE + "Nombre del jugador: ").strip()
    if not nombre:
        print(Fore.RED + "El nombre no puede estar vacío.")
        return None
    
    print(Fore.CYAN + "\nClases disponibles:")
    for clase, stats in CLASES.items():
        print(Fore.YELLOW + f"{clase.capitalize()}: Vida {stats['vida']}, Ataque {stats['ataque']}, Defensa {stats['defensa']}, Magia {stats['magia']}")
    
    clase = input(Fore.WHITE + "\nElige tu clase: ").lower().strip()
    if clase not in CLASES:
        print(Fore.RED + "Clase no válida.")
        return None
    
    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "experiencia": 0,
        "vida_actual": CLASES[clase]["vida"],
        "vida_maxima": CLASES[clase]["vida"],
        "ataque": CLASES[clase]["ataque"],
        "defensa": CLASES[clase]["defensa"],
        "magia": CLASES[clase]["magia"],
        "inventario": {"poción_vida": 2, "poción_mana": 1},
        "logros": [],
        "misiones_completadas": 0
    }
    
    jugadores = cargar_datos(JUGADORES_FILE)
    jugadores.append(jugador)
    guardar_datos(jugadores, JUGADORES_FILE)
    
    print(Fore.GREEN + f"\n¡Jugador {nombre} registrado exitosamente como {clase}!")
    return jugador

def seleccionar_jugador():
    """Seleccionar jugador existente"""
    jugadores = cargar_datos(JUGADORES_FILE)
    
    if not jugadores:
        print(Fore.RED + "No hay jugadores registrados.")
        return None
    
    print(Fore.GREEN + "\n--- JUGADORES DISPONIBLES ---")
    for i, jugador in enumerate(jugadores, 1):
        print(Fore.YELLOW + f"{i}. {jugador['nombre']} - Nivel {jugador['nivel']} {jugador['clase']}")
    
    try:
        seleccion = int(input(Fore.WHITE + "\nSelecciona un jugador: ")) - 1
        if 0 <= seleccion < len(jugadores):
            return jugadores[seleccion]
        else:
            print(Fore.RED + "Selección inválida.")
            return None
    except ValueError:
        print(Fore.RED + "Por favor, ingresa un número válido.")
        return None

def mostrar_estado(jugador):
    """Mostrar estado del jugador"""
    print(Fore.CYAN + f"\n--- ESTADO DE {jugador['nombre'].upper()} ---")
    print(Fore.YELLOW + f"Nivel: {jugador['nivel']} | EXP: {jugador['experiencia']}/100")
    print(Fore.GREEN + f"Vida: {jugador['vida_actual']}/{jugador['vida_maxima']}")
    print(Fore.BLUE + f"Ataque: {jugador['ataque']} | Defensa: {jugador['defensa']} | Magia: {jugador['magia']}")
    
    if jugador['logros']:
        print(Fore.MAGENTA + f"Logros: {', '.join(jugador['logros'])}")

def mostrar_inventario(jugador):
    """Mostrar inventario del jugador"""
    print(Fore.CYAN + f"\n--- INVENTARIO DE {jugador['nombre'].upper()} ---")
    
    if not jugador['inventario']:
        print(Fore.YELLOW + "El inventario está vacío.")
        return
    
    for item, cantidad in jugador['inventario'].items():
        if cantidad > 0:
            print(Fore.WHITE + f"{item.replace('_', ' ').title()}: {cantidad}")

def usar_item(jugador, *items):
    """Función para usar items con *args"""
    def aplicar_efecto(item, cantidad):
        if item == "poción_vida":
            vida_recuperada = min(30, jugador['vida_maxima'] - jugador['vida_actual'])
            jugador['vida_actual'] += vida_recuperada
            print(Fore.GREEN + f"Usaste {cantidad} poción(es) de vida. Recuperaste {vida_recuperada} de vida.")
        elif item == "poción_mana":
            print(Fore.BLUE + f"Usaste {cantidad} poción(es) de mana. (Sistema de magia en desarrollo)")
        # Más efectos para otros items...
    
    for item in items:
        if item in jugador['inventario'] and jugador['inventario'][item] > 0:
            aplicar_efecto(item, jugador['inventario'][item])
            jugador['inventario'][item] -= 1
            if jugador['inventario'][item] <= 0:
                del jugador['inventario'][item]
        else:
            print(Fore.RED + f"No tienes {item.replace('_', ' ')}.")

def sistema_combate(jugador, enemigo_tipo):
    """Sistema de combate con el jugador"""
    enemigo = ENEMIGOS[enemigo_tipo].copy()
    print(Fore.RED + f"\n¡Te enfrentas a un {enemigo_tipo}!")
    
    # Lambda function para calcular daño
    calcular_daño = lambda atacante, defensor: max(1, atacante - defensor // 2)
    
    turno = 0
    while jugador['vida_actual'] > 0 and enemigo['vida'] > 0:
        turno += 1
        print(Fore.CYAN + f"\n--- TURNO {turno} ---")
        print(Fore.GREEN + f"Tu vida: {jugador['vida_actual']}/{jugador['vida_maxima']}")
        print(Fore.RED + f"{enemigo_tipo.capitalize()} vida: {enemigo['vida']}")
        
        # Turno del jugador
        print(Fore.YELLOW + "\n¿Qué deseas hacer?")
        print("1. Atacar")
        print("2. Usar item")
        print("3. Huir")
        
        try:
            opcion = int(input(Fore.WHITE + "Opción: "))
            
            if opcion == 1:
                daño = calcular_daño(jugador['ataque'], enemigo['defensa'])
                enemigo['vida'] -= daño
                print(Fore.GREEN + f"¡Atacas y haces {daño} de daño!")
                
            elif opcion == 2:
                mostrar_inventario(jugador)
                item = input("¿Qué item quieres usar? (nombre): ").lower().strip()
                usar_item(jugador, item)
                continue
                
            elif opcion == 3:
                if random.random() < 0.5:  # 50% de probabilidad de huir
                    print(Fore.YELLOW + "¡Lograste huir!")
                    return True
                else:
                    print(Fore.RED + "¡No pudiste huir!")
            else:
                print(Fore.RED + "Opción inválida.")
                continue
                
        except ValueError:
            print(Fore.RED + "Por favor, ingresa un número válido.")
            continue
        
        # Turno del enemigo
        if enemigo['vida'] > 0:
            daño_enemigo = calcular_daño(enemigo['ataque'], jugador['defensa'])
            jugador['vida_actual'] -= daño_enemigo
            print(Fore.RED + f"El {enemigo_tipo} te ataca y te hace {daño_enemigo} de daño!")
    
    if jugador['vida_actual'] <= 0:
        print(Fore.RED + "\n¡Has sido derrotado!")
        jugador['vida_actual'] = jugador['vida_maxima'] // 2  # Recuperar mitad de vida
        return False
    else:
        experiencia_ganada = enemigo['experiencia']
        jugador['experiencia'] += experiencia_ganada
        print(Fore.GREEN + f"\n¡Has derrotado al {enemigo_tipo}!")
        print(Fore.YELLOW + f"Ganas {experiencia_ganada} puntos de experiencia!")
        
        # Revisar si sube de nivel
        if jugador['experiencia'] >= 100:
            subir_nivel(jugador)
        
        # Dropear item aleatorio
        item_drop = random.choice(list(ITEMS.keys()))
        jugador['inventario'][item_drop] = jugador['inventario'].get(item_drop, 0) + 1
        print(Fore.MAGENTA + f"¡Encontraste {item_drop.replace('_', ' ')}!")
        
        return True

def subir_nivel(jugador):
    """Función para subir de nivel"""
    jugador['nivel'] += 1
    jugador['experiencia'] = 0
    jugador['vida_maxima'] += 20
    jugador['vida_actual'] = jugador['vida_maxima']
    jugador['ataque'] += 5
    jugador['defensa'] += 3
    jugador['magia'] += 2
    
    print(Fore.CYAN + f"\n⭐ ¡FELICIDADES! ⭐")
    print(Fore.YELLOW + f"¡{jugador['nombre']} ha subido al nivel {jugador['nivel']}!")
    print(Fore.GREEN + "Stats mejorados: +20 Vida, +5 Ataque, +3 Defensa, +2 Magia")

def aventura_principal(jugador):
    """Aventura principal del juego"""
    print(Fore.BLUE + f"\nBienvenido, {jugador['nombre']}, a la Gran Aventura!")
    
    decisiones_criticas = 0
    misiones_completadas = jugador['misiones_completadas']
    
    # Primera decisión crítica
    print(Fore.CYAN + "\nTe encuentras en una encrucijada:")
    print("1. Tomar el camino del bosque")
    print("2. Ir hacia las montañas")
    print("3. Regresar al pueblo")
    
    try:
        decision1 = int(input(Fore.WHITE + "¿Qué camino eliges? "))
        decisiones_criticas += 1
        
        if decision1 == 1:
            print(Fore.GREEN + "\nTe adentras en el bosque misterioso...")
            enemigo = random.choice(["goblin", "lobo"])
            victoria = sistema_combate(jugador, enemigo)
            if victoria:
                misiones_completadas += 1
                jugador['logros'].append("Explorador del Bosque")
            
        elif decision1 == 2:
            print(Fore.YELLOW + "\nAscendes por las escarpadas montañas...")
            # Segunda decisión crítica
            print("\nEncuentras una cueva:")
            print("1. Entrar a la cueva")
            print("2. Rodear la montaña")
            
            decision2 = int(input(Fore.WHITE + "¿Qué haces? "))
            decisiones_criticas += 1
            
            if decision2 == 1:
                print(Fore.RED + "\nLa cueva está llena de peligros...")
                enemigo = random.choice(["orco", "esqueleto"])
                victoria = sistema_combate(jugador, enemigo)
                if victoria:
                    misiones_completadas += 2
                    jugador['logros'].append("Cazador de Cuevas")
            
        elif decision1 == 3:
            print(Fore.BLUE + "\nRegresas al pueblo a descansar...")
            jugador['vida_actual'] = jugador['vida_maxima']
            print(Fore.GREEN + "¡Vida completamente restaurada!")
            
        else:
            print(Fore.RED + "Opción inválida. Pierdes tu oportunidad.")
            
    except ValueError:
        print(Fore.RED + "Decisión inválida. La aventura continúa...")
    
    # Tercera decisión crítica
    if decisiones_criticas < 3:
        print(Fore.CYAN + "\nEncuentras un cofre misterioso:")
        print("1. Abrir el cofre")
        print("2. Dejarlo ahí")
        print("3. Examinarlo con cuidado")
        
        try:
            decision3 = int(input(Fore.WHITE + "¿Qué decides? "))
            decisiones_criticas += 1
            
            if decision3 == 1:
                if random.random() < 0.7:  # 70% de probabilidad de item bueno
                    item = random.choice(list(ITEMS.keys()))
                    jugador['inventario'][item] = jugador['inventario'].get(item, 0) + 1
                    print(Fore.GREEN + f"¡Encontraste {item.replace('_', ' ')} en el cofre!")
                else:
                    print(Fore.RED + "¡Era una trampa! Pierdes 10 de vida.")
                    jugador['vida_actual'] -= 10
            
            elif decision3 == 3:
                print(Fore.YELLOW + "Examinas el cofre y encuentrun mecanismo secreto...")
                jugador['experiencia'] += 25
                print(Fore.GREEN + "¡Ganas 25 puntos de experiencia por tu curiosidad!")
                
        except ValueError:
            print(Fore.RED + "Decisión inválida. El cofre desaparece misteriosamente.")
    
    jugador['misiones_completadas'] = misiones_completadas
    print(Fore.CYAN + f"\nAventura completada. Decisiones tomadas: {decisiones_criticas}/3")
    print(Fore.YELLOW + f"Misiones completadas: {misiones_completadas}")

def guardar_progreso(jugador):
    """Guardar progreso del jugador"""
    jugadores = cargar_datos(JUGADORES_FILE)
    
    for i, j in enumerate(jugadores):
        if j['nombre'] == jugador['nombre']:
            jugadores[i] = jugador
            break
    
    guardar_datos(jugadores, JUGADORES_FILE)
    guardar_datos(jugador, PROGRESO_FILE)
    print(Fore.GREEN + "\n¡Progreso guardado exitosamente!")

def menu_principal():
    """Menú principal del juego"""
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        
        print(Fore.WHITE + "1. Nuevo Jugador")
        print("2. Cargar Jugador")
        print("3. Salir")
        
        try:
            opcion = int(input(Fore.YELLOW + "\nSelecciona una opción: "))
            
            if opcion == 1:
                jugador = registrar_jugador()
                if jugador:
                    input(Fore.WHITE + "Presiona Enter para continuar...")
                    menu_jugador(jugador)
                    
            elif opcion == 2:
                jugador = seleccionar_jugador()
                if jugador:
                    input(Fore.WHITE + "Presiona Enter para continuar...")
                    menu_jugador(jugador)
                    
            elif opcion == 3:
                print(Fore.CYAN + "\n¡Gracias por jugar!")
                break
                
            else:
                print(Fore.RED + "Opción inválida.")
                
        except ValueError:
            print(Fore.RED + "Por favor, ingresa un número válido.")
        
        input(Fore.WHITE + "\nPresiona Enter para continuar...")

def menu_jugador(jugador):
    """Menú del jugador"""
    while True:
        limpiar_pantalla()
        mostrar_estado(jugador)
        
        print(Fore.WHITE + "\n--- MENÚ PRINCIPAL ---")
        print("1. Iniciar Aventura")
        print("2. Ver Inventario")
        print("3. Usar Item")
        print("4. Guardar y Salir")
        print("5. Volver al Menú Principal")
        
        try:
            opcion = int(input(Fore.YELLOW + "\nSelecciona una opción: "))
            
            if opcion == 1:
                aventura_principal(jugador)
                input(Fore.WHITE + "\nPresiona Enter para continuar...")
                
            elif opcion == 2:
                mostrar_inventario(jugador)
                input(Fore.WHITE + "\nPresiona Enter para continuar...")
                
            elif opcion == 3:
                mostrar_inventario(jugador)
                item = input("¿Qué item quieres usar? (nombre): ").lower().strip()
                usar_item(jugador, item)
                input(Fore.WHITE + "\nPresiona Enter para continuar...")
                
            elif opcion == 4:
                guardar_progreso(jugador)
                break
                
            elif opcion == 5:
                break
                
            else:
                print(Fore.RED + "Opción inválida.")
                input(Fore.WHITE + "\nPresiona Enter para continuar...")
                
        except ValueError:
            print(Fore.RED + "Por favor, ingresa un número válido.")
            input(Fore.WHITE + "\nPresiona Enter para continuar...")

# Función principal
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nJuego interrumpido. ¡Hasta pronto!")
    except Exception as e:
        print(Fore.RED + f"\nError inesperado: {e}")
