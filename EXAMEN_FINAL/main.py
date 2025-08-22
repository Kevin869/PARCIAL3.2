from utils import load_players, save_players, register_player
from adventure import start_adventure
from inventory import show_inventory, use_item

def main():
    players = load_players()
    name = register_player(players)
    player = players[name]
    player["name"] = name
    
    while True:
        print("\n1. Empezar aventura\n2. Inventario\n3. Guardar y salir")
        choice = input("Elige una opción: ").strip()
        if choice == "1":
            start_adventure(player)
        elif choice == "2":
            show_inventory(player)
            use_item(player)
        elif choice == "3":
            save_players(players)
            print("Progreso guardado. ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
