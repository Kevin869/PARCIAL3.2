import json, os

def load_players(filename="players.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def save_players(players, filename="players.json"):
    with open(filename, "w") as file:
        json.dump(players, file, indent=4)

def register_player(players):
    name = input("Ingresa tu nombre: ").strip()
    if name in players:
        print(f"Bienvenido de nuevo, {name}!")
        return name
    clase = input("Elige tu clase (Guerrero, Mago, Explorador): ").strip()
    players[name] = {
        "clase": clase,
        "nivel": 1,
        "xp": 0,
        "vida": 100,
        "inventario": {"Poción": 2}
    }
    print(f"Jugador {name} registrado con clase {clase}!")
    return name
