import json
import os
import random
from colorama import Fore, Style, init

init(autoreset=True)

SAVE_FILE = "players.json"

def load_players():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_players(players):
    with open(SAVE_FILE, "w") as f:
        json.dump(players, f, indent=4)

def menu_input(prompt, options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        else:
            print(Fore.RED + "Opción no válida, intenta de nuevo.")

def register_player(players):
    name = input("Nombre del jugador: ").strip()
    print("Elige clase: 1) Guerrero 2) Mago 3) Explorador")
    classes = {"1": "Guerrero", "2": "Mago", "3": "Explorador"}
    choice = menu_input("> ", classes.keys())
    player = {
        "name": name,
        "class": classes[choice],
        "level": 1,
        "xp": 0,
        "money": 100,
        "hp": 30,
        "inventory": {"Poción": 2},
        "wanted": 0
    }
    players[name] = player
    save_players(players)
    return player

def choose_player(players):
    if not players:
        print("No hay jugadores registrados.")
        return None
    print("Jugadores disponibles:")
    for i, p in enumerate(players.keys(), start=1):
        print(f"{i}) {p}")
    while True:
        try:
            idx = int(input("> "))
            if 1 <= idx <= len(players):
                return list(players.values())[idx-1]
            else:
                print(Fore.RED + "Número no válido.")
        except ValueError:
            print(Fore.RED + "Entrada inválida, usa números.")

def main_menu():
    players = load_players()
    print(Fore.CYAN + "Bienvenido a PyGTA RPG")
    print("1. Registrar nuevo jugador")
    print("2. Cargar jugador existente")
    choice = menu_input("> ", ["1", "2"])
    if choice == "1":
        player = register_player(players)
    else:
        player = choose_player(players)
        if player is None:
            return
    start_adventure(player, players)

def start_adventure(player, players):
    print(Fore.GREEN + f"¡Bienvenido, {player['name']} el {player['class']}!")
    print("Te encuentras en Los PySantos...")
    while True:
        print("\n¿Qué deseas hacer?")
        print("1) Ir a una misión")
        print("2) Comprar en la tienda")
        print("3) Revisar inventario")
        print("4) Salir y guardar")
        choice = menu_input("> ", ["1","2","3","4"])
        if choice == "1":
            mission(player)
        elif choice == "2":
            shop(player)
        elif choice == "3":
            inventory(player)
        elif choice == "4":
            players[player['name']] = player
            save_players(players)
            print(Fore.YELLOW + "Progreso guardado. ¡Hasta luego!")
            break

def mission(player):
    print("\nElige tu misión:")
    print("A) Robo al banco")
    print("B) Carrera ilegal")
    print("C) Rescate de un amigo")
    choice = menu_input("> ", ["a","b","c"])
    if choice == "a":
        bank_heist(player)
    elif choice == "b":
        street_race(player)
    elif choice == "c":
        rescue(player)

def combat(player, enemy):
    print(Fore.RED + f"Combate contra {enemy['name']}!")
    while player['hp'] > 0 and enemy['hp'] > 0:
        action = menu_input("Atacar (a) o Huir (h)? ", ["a","h"])
        if action == "a":
            dmg = random.randint(5, 10)
            enemy['hp'] -= dmg
            print(f"Golpeas a {enemy['name']} por {dmg} de daño.")
        elif action == "h":
            print("Escapas del combate!")
            return False
        if enemy['hp'] > 0:
            edmg = random.randint(3, 7)
            player['hp'] -= edmg
            print(f"{enemy['name']} te golpea por {edmg}.")
    if player['hp'] > 0:
        print(Fore.GREEN + f"Venciste a {enemy['name']}!")
        player['xp'] += 10
        player['money'] += enemy.get('money', 20)
        return True
    else:
        print(Fore.RED + "Has sido derrotado...")
        return False

def bank_heist(player):
    print("Intentas un robo al banco...")
    if combat(player, {"name":"Guardia","hp":15,"money":50}):
        print("¡Robaste 200$!")
        player['money'] += 200
        player['wanted'] += 2

def street_race(player):
    print("Participas en una carrera ilegal...")
    if random.choice([True, False]):
        print("¡Ganaste la carrera y obtuviste 150$!")
        player['money'] += 150
    else:
        print("Perdiste la carrera y la policía te persigue!")
        player['wanted'] += 1

def rescue(player):
    print("Tu amigo fue secuestrado...")
    combat(player, {"name":"Secuestrador","hp":20,"money":30})

def shop(player):
    items = {"poción": 50, "espada": 120}
    print("\nTienda disponible:")
    for item, price in items.items():
        print(f"{item.capitalize()} - ${price}")
    choice = input("¿Qué deseas comprar? (o escribe nada para salir) ").strip().lower()
    if choice in items:
        if player['money'] >= items[choice]:
            player['money'] -= items[choice]
            player['inventory'][choice] = player['inventory'].get(choice, 0) + 1
            print(Fore.GREEN + f"Compraste {choice}!")
        else:
            print(Fore.RED + "No tienes suficiente dinero.")
    elif choice == "":
        print("Sales de la tienda.")
    else:
        print(Fore.RED + "Ese objeto no existe.")

def inventory(player):
    print("\nTu inventario:")
    for item, qty in player['inventory'].items():
        print(f"{item}: {qty}")
    choice = input("¿Quieres usar algún ítem? ").strip().lower()
    if choice in player['inventory'] and player['inventory'][choice] > 0:
        if choice == "poción":
            player['hp'] += 10
            player['inventory'][choice] -= 1
            print("Usaste una poción y recuperaste 10 de vida!")
    elif choice == "":
        pass
    else:
        print(Fore.RED + "No tienes ese ítem.")

if __name__ == "__main__":
    main_menu()
