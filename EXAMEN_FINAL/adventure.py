from combat import basic_combat

def start_adventure(player):
    print("\n¡Comienza tu aventura!")

    # Decisión 1
    decision1 = input("Estás en un bosque oscuro. ¿Izquierda o derecha? ").lower()
    if decision1 == "izquierda":
        print("Encuentras un río tranquilo, sin peligro.")
    else:
        print("Te atacan goblins!")
        basic_combat(player)

    # Decisión 2
    decision2 = input("Ves una cueva misteriosa. ¿Entrar o seguir? ").lower()
    if decision2 == "entrar":
        print("¡Encontraste una Espada Mágica!")
        player["inventario"]["Espada Mágica"] = 1
    else:
        print("Decides seguir tu camino y avanzar lentamente.")

    # Decisión 3
    decision3 = input("Un puente se rompe frente a ti. ¿Saltar o retroceder? ").lower()
    if decision3 == "saltar":
        print("Saltaste con éxito y avanzas en la aventura.")
    else:
        print("Decides retroceder y buscar otro camino.")
