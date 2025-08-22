import random

def basic_combat(player):
    enemigos = ["Goblin", "Orco", "Lobo"]
    enemigo = random.choice(enemigos)
    vida_enemigo = random.randint(40, 70)
    print(f"\n¡Un {enemigo} aparece!")
    
    while player["vida"] > 0 and vida_enemigo > 0:
        ataque = random.randint(10, 20)
        vida_enemigo -= ataque
        print(f"Atacas al {enemigo} y le haces {ataque} de daño.")
        if vida_enemigo <= 0:
            print(f"¡Has derrotado al {enemigo}!")
            player["xp"] += 20
            if player["xp"] >= 100:
                player["nivel"] += 1
                player["xp"] = 0
                print(f"¡Has subido al nivel {player['nivel']}!")
            return
        
        daño = random.randint(5, 15)
        player["vida"] -= daño
        print(f"El {enemigo} te ataca y te hace {daño} de daño.")
    
    if player["vida"] <= 0:
        print("¡Has sido derrotado! La aventura termina aquí.")
