def show_inventory(player):
    print("\nInventario:")
    for item, cantidad in player["inventario"].items():
        print(f"{item}: {cantidad}")

def use_item(player):
    show_inventory(player)
    item = input("¿Qué ítem deseas usar? ").strip()
    if item in player["inventario"] and player["inventario"][item] > 0:
        print(f"Usaste {item}.")
        player["inventario"][item] -= 1
        if item.lower() == "poción":
            player["vida"] += 20
            print(f"Recuperaste 20 de vida. Vida actual: {player['vida']}")
    else:
        print("No tienes ese ítem.")
