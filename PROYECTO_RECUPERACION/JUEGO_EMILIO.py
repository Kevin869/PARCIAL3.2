import json
import random
from colorama import Fore, Style, init

init(autoreset=True)

def cargar_jugadores():
    try:
        with open("jugadores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_jugadores(jugadores):
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f, indent=4)

def registrar_jugador(jugadores):
    nombre = input("Nombre del jugador: ")
    print("Elige clase: 1) Guerrero 2) Mago 3) Explorador")

    eleccion = ""
    while eleccion not in ["1", "2", "3"]:
        eleccion = input("> ")
        if eleccion not in ["1", "2", "3"]:
            print(Fore.RED + "¡Opción inválida! Elige 1, 2 o 3.")

    clases = {"1": "Guerrero", "2": "Mago", "3": "Explorador"}
    clase = clases[eleccion]

    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "vida": 30,
        "inventario": {"pociones": 2}
    }
    jugadores[nombre] = jugador
    guardar_jugadores(jugadores)
    print(Fore.GREEN + f"¡Bienvenido, {nombre} el {clase}!")
    return jugador

def cargar_jugador(jugadores):
    if not jugadores:
        print(Fore.RED + "No hay jugadores registrados.")
        return None
    print("Jugadores disponibles:")
    for nombre in jugadores:
        print("-", nombre)
    nombre = input("Elige jugador: ")
    return jugadores.get(nombre)

def aventura(jugador):
    print(Style.BRIGHT + "\nTu aventura comienza en la aldea de Eldoria, un lugar lleno de misterios y leyendas...")
    print("Los aldeanos murmuran sobre una antigua profecía que habla de un héroe que salvará el reino de una gran oscuridad.")
    print("Te acercas a una bifurcación en el bosque, donde se dice que los espíritus de los ancestros guían a los valientes.")

    decision1 = ""
    while decision1 not in ["A", "B"]:
        decision1 = input("A) Ir por el camino oscuro, donde se dice que habita un dragón.\nB) Tomar el sendero iluminado, que lleva a la Torre del Mago.\n> ").upper()
        if decision1 not in ["A", "B"]:
            print(Fore.RED + "¡Opción inválida! Elige A o B.")

    if decision1 == "A":
        print("Te adentras en la oscuridad... ¡Felipe Salvaje Homosexual aparece, un temido guardián del dragón!")
        combate(jugador, {"nombre": "Felipe Salvaje Homosexual", "vida": 10, "ataque": 3})
    else:
        print("El sendero iluminado parece tranquilo... pero escuchas pasos pesados.")
        print("¡Es un Brandosaurio, un antiguo protector de la Torre del Mago!")
        combate(jugador, {"nombre": "Brandosaurio", "vida": 12, "ataque": 4})

    print("\nTras el combate, encuentras la entrada a una cueva misteriosa, donde se dice que los ecos del pasado resuenan.")
    decision2 = ""
    while decision2 not in ["C", "S"]:
        decision2 = input("¿Quieres entrar en la cueva (C) o seguir el camino (S)? ").upper()
        if decision2 not in ["C", "S"]:
            print(Fore.RED + "¡Opción inválida! Elige C o S.")

    if decision2 == "C":
        print("Entras en la cueva... y un murciélago gigante desciende del techo, custodiando un antiguo secreto.")
        combate(jugador, {"nombre": "Murciélago Gigante", "vida": 14, "ataque": 5})
    else:
        print("Sigues el camino y disfrutas de un momento de calma... recuperas un poco de energía.")
        jugador["vida"] += 5
        print(Fore.GREEN + f"Tu vida aumenta a {jugador['vida']}.")

    print("\nMás adelante, encuentras un cofre antiguo en medio del sendero, cubierto de runas mágicas.")
    decision3 = ""
    while decision3 not in ["A", "I"]:
        decision3 = input("¿Abrir el cofre (A) o ignorarlo (I)? ").upper()
        if decision3 not in ["A", "I"]:
            print(Fore.RED + "¡Opción inválida! Elige A o I.")

    if decision3 == "A":
        suerte = random.choice(["scar", "espada", "trampa"])
        if suerte == "scar":
            print(Fore.YELLOW + "¡Increíble! Encuentras una Scar Dorada 🔫, un arma de leyenda.")
            jugador["inventario"]["Scar Dorada"] = 1
        elif suerte == "espada":
            print(Fore.YELLOW + "¡Encuentras una Espada Legendaria, forjada en el fuego de los dioses!")
            jugador["inventario"]["Espada Legendaria"] = 1
        else:
            print(Fore.RED + "¡Era una trampa! El cofre explota y pierdes 8 de vida.")
            jugador["vida"] -= 8
    else:
        print("Decides no arriesgarte y dejas el cofre atrás, sintiendo que el verdadero tesoro está en la aventura misma.")

    print(Fore.CYAN + "\nTu aventura por hoy termina. ¡Buen trabajo, valiente héroe! El reino de Eldoria te necesita.")

def combate(jugador, enemigo):
    print(Fore.RED + f"\nCombate: ¡Un {enemigo['nombre']} te ataca!")
    vida_jugador = jugador["vida"]
    vida_enemigo = enemigo["vida"]

    while vida_jugador > 0 and vida_enemigo > 0:
        print(f"\nTu vida: {vida_jugador} | Vida del {enemigo['nombre']}: {vida_enemigo}")

        accion = ""
        while accion not in ["A", "P"]:
            accion = input("¿Atacar (A) o usar poción (P)? ").upper()
            if accion not in ["A", "P"]:
                print(Fore.RED + "¡Opción inválida! Elige A o P.")

        if accion == "A":
            daño = random.randint(3, 8)
            vida_enemigo -= daño
            print(Fore.CYAN + f"Atacas y haces {daño} de daño.")
        elif accion == "P" and jugador["inventario"].get("pociones", 0) > 0:
            vida_jugador += 10
            jugador["inventario"]["pociones"] -= 1
            print(Fore.GREEN + f"Usas una poción. Vida restaurada a {vida_jugador}.")
        else:
            print(Fore.RED + "¡No tienes pociones!")

        if vida_enemigo > 0:
            daño_enemigo = random.randint(1, enemigo["ataque"])
            vida_jugador -= daño_enemigo
            print(Fore.RED + f"El {enemigo['nombre']} te golpea por {daño_enemigo}.")

    jugador["vida"] = max(vida_jugador, 0)  # actualizar vida real

    if vida_jugador > 0:
        print(Fore.YELLOW + f"\n¡Has derrotado al {enemigo['nombre']}! Tu valentía es admirable.")
        jugador["nivel"] += 1
        print(Fore.MAGENTA + f"¡Subes a nivel {jugador['nivel']}! Tu leyenda crece.")
    else:
        print(Fore.RED + "\nHas sido derrotado... pero tu espíritu de lucha será recordado.")

def main():
    jugadores = cargar_jugadores()
    print("Bienvenido al mundo de PyRPG")
    print("1. Registrar nuevo jugador")
    print("2. Cargar jugador existente")

    opcion = ""
    while opcion not in ["1", "2"]:
        opcion = input("> ")
        if opcion not in ["1", "2"]:
            print(Fore.RED + "¡Opción inválida! Elige 1 o 2.")

    if opcion == "1":
        jugador = registrar_jugador(jugadores)
    else:
        jugador = cargar_jugador(jugadores)
        if not jugador:
            return

    aventura(jugador)
    jugadores[jugador["nombre"]] = jugador
    guardar_jugadores(jugadores)

if __name__ == "__main__":
    main()