import json
import random
import os


enemigos = {
    "goblin": {"vida": 30, "ataque": 5, "experiencia": 10},
    "orco": {"vida": 50, "ataque": 8, "experiencia": 20},
    "lobo": {"vida": 25, "ataque": 6, "experiencia": 8},
    "araña gigante": {"vida": 35, "ataque": 7, "experiencia": 12},
    "esqueleto": {"vida": 40, "ataque": 9, "experiencia": 15},
    "bruja": {"vida": 60, "ataque": 12, "experiencia": 25},
    "dragón": {"vida": 100, "ataque": 15, "experiencia": 50}
}

items = {
    "espada": {"tipo": "arma", "ataque": 10},
    "espada larga": {"tipo": "arma", "ataque": 15},
    "hacha": {"tipo": "arma", "ataque": 12},
    "escudo": {"tipo": "defensa", "defensa": 5},
    "armadura": {"tipo": "defensa", "defensa": 8},
    "poción": {"tipo": "curación", "vida": 20},
    "poción grande": {"tipo": "curación", "vida": 40},
    "mapa": {"tipo": "utilidad", "descripción": "Mapa del tesoro"},
    "llave antigua": {"tipo": "utilidad", "descripción": "Llave para la mazmorra"},
    "amuleto": {"tipo": "magia", "ataque": 5, "defensa": 5}
}

clases = {
    "guerrero": {"vida": 100, "ataque": 15, "defensa": 10},
    "mago": {"vida": 70, "ataque": 20, "defensa": 5},
    "explorador": {"vida": 80, "ataque": 12, "defensa": 8},
    "arquero": {"vida": 75, "ataque": 18, "defensa": 6}
}

historias = {
    "inicio": "Te encuentras en un bosque misterioso. El camino se divide en varias direcciones. El aire es fresco y los pájaros cantan a lo lejos.",
    "cueva": "La entrada de la cueva es oscura y húmeda. Puedes escuchar ruidos extraños provenientes del interior.",
    "pueblo": "El pueblo parece abandonado. Las casas están vacías y el silencio es inquietante. Hay una taberna y una herrería.",
    "rio": "Un río cristalino fluye a través del bosque. El agua parece segura para beber y hay un puente antiguo cruzando hacia el otro lado.",
    "montaña": "El camino serpentea hacia las montañas. Desde aquí puedes ver todo el valle. Hay una cueva en la ladera.",
    "mazmorra": "Una escalera de piedra desciende hacia la oscuridad. El aire es frío y huele a moho. Esta debe ser la mazmorra abandonada.",
    "castillo": "Las ruinas de un antiguo castillo se alzan ante ti. Aunque está en mal estado, aún impresiona.",
    "bosque profundo": "Los árboles son más densos aquí y la luz apenas penetra. Sientes que no estás solo...",
    "taberna": "La taberna 'El Dragón Durmiente' parece ser el único lugar con vida en el pueblo. Hay algunos aldeanos sentados.",
    "herrería": "La herrería está vacía pero el fuego aún arde. Hay herramientas y armas en las paredes.",
    "tesoro": "¡Has encontrado una cámara secreta! Un cofre antiguo descansa en el centro de la habitación."
}

decisiones = {
    "cueva_entrar": "¿Entras en la cueva? (si/no): ",
    "rio_beber": "¿Bebes agua del río? (si/no): ",
    "rio_cruzar": "¿Cruzas el puente? (si/no): ",
    "montaña_subir": "¿Subes la montaña? (si/no): ",
    "mazmorra_entrar": "¿Desciendes a la mazmorra? (si/no): ",
    "castillo_explorar": "¿Exploras el castillo? (si/no): ",
    "bosque_profundizar": "¿Te adentras en el bosque profundo? (si/no): ",
    "taberna_hablar": "¿Hablas con los aldeanos? (si/no): ",
    "herrería_buscar": "¿Buscas algo útil? (si/no): ",
    "tesoro_abrir": "¿Abres el cofre? (si/no): "
}

eventos = {
    "rio_beber_bueno": "El agua es fresca y pura. Te sientes revitalizado! (+10 de vida)",
    "rio_beber_malo": "El agua estaba contaminada. Te sientes enfermo! (-15 de vida)",
    "tesoro_arma": "¡Encontraste una espada larga!",
    "tesoro_armadura": "¡Encontraste una armadura!",
    "tesoro_poción": "¡Encontraste una poción grande!",
    "tesoro_amuleto": "¡Encontraste un amuleto mágico!",
    "tesoro_vacio": "El cofre está vacío...",
    "aldeano_info": "Un aldeano te susurra: 'Cuidado con la bruja del bosque profundo...'",
    "aldeano_poción": "Un aldeano agradecido te da una poción",
    "herrero_arma": "Encuentras un hacha abandonada en la herrería"
}


def guardar_jugadores(jugadores):
    with open('jugadores.json', 'w') as archivo:
        json.dump(jugadores, archivo)

def cargar_jugadores():
    try:
        with open('jugadores.json', 'r') as archivo:
            return json.load(archivo)
    except:
        return {}


def usar_item(jugador):
    if not jugador['inventario']:
        print("❌ No tienes items en el inventario")
        return
    
    print("\n📦 Inventario:")
    for i, item in enumerate(jugador['inventario']):
        print(f"{i+1}. {item.capitalize()}")
    
    try:
        opcion = int(input("Elige el número del item a usar: ")) - 1
        item = jugador['inventario'][opcion]
        
        if item == "poción":
            jugador['vida'] += items[item]["vida"]
            print(f"❤️  Recuperaste {items[item]['vida']} de vida!")
            jugador['inventario'].pop(opcion)
        elif item == "poción grande":
            jugador['vida'] += items[item]["vida"]
            print(f"❤️  Recuperaste {items[item]['vida']} de vida!")
            jugador['inventario'].pop(opcion)
        else:
            print(f"ℹ️  {item.capitalize()} no se puede usar ahora")
            
    except (ValueError, IndexError):
        print("❌ Opción no válida")

def check_nivel(jugador):
    if jugador['experiencia'] >= jugador['nivel'] * 100:
        jugador['nivel'] += 1
        jugador['experiencia'] = 0
        jugador['vida'] += 20
        jugador['ataque'] += 5
        jugador['defensa'] += 3
        print(f"🎊 ¡Subiste al nivel {jugador['nivel']}!")
        print("➕ +20 Vida, +5 Ataque, +3 Defensa")


def crear_jugador():
    print("\n" + "="*40)
    print("CREAR NUEVO JUGADOR")
    print("="*40)
    
    nombre = input("Nombre de tu personaje: ")
    
    print("\nElige tu clase:")
    for clase in clases:
        print(f"- {clase.capitalize()}")
    
    while True:
        clase = input("\nClase elegida: ").lower()
        if clase in clases:
            break
        print("Clase no válida. Intenta otra vez.")
    
    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "experiencia": 0,
        "vida": clases[clase]["vida"],
        "ataque": clases[clase]["ataque"],
        "defensa": clases[clase]["defensa"],
        "inventario": ["poción"],
        "misiones": ["explorar_bosque"],
        "ubicacion": "inicio",
        "historia": {}
    }
    
    return jugador

def mostrar_jugador(jugador):
    print(f"\n{'='*40}")
    print(f"JUGADOR: {jugador['nombre']}")
    print(f"{'='*40}")
    print(f"Clase: {jugador['clase'].capitalize()}")
    print(f"Nivel: {jugador['nivel']}")
    print(f"Experiencia: {jugador['experiencia']}/100")
    print(f"Vida: {jugador['vida']}")
    print(f"Ataque: {jugador['ataque']}")
    print(f"Defensa: {jugador['defensa']}")
    print(f"Ubicación: {jugador['ubicacion'].capitalize()}")
    
    print("\nInventario:")
    for item in jugador['inventario']:
        print(f"- {item.capitalize()}")


def combate(jugador, enemigo_tipo):
    enemigo = enemigos[enemigo_tipo].copy()
    print(f"\n⚔️  COMBATE contra {enemigo_tipo.capitalize()}!")
    print(f"Vida del enemigo: {enemigo['vida']}")
    
    while jugador['vida'] > 0 and enemigo['vida'] > 0:
        print(f"\nTu vida: {jugador['vida']}")
        print(f"Vida enemigo: {enemigo['vida']}")
        
        accion = input("\n¿Qué haces? (atacar/usar item/huir): ").lower()
        
        if accion == "atacar":
            daño = max(0, jugador['ataque'] - random.randint(0, 5))
            enemigo['vida'] -= daño
            print(f"💥 Le hiciste {daño} de daño al enemigo!")
            
            if enemigo['vida'] <= 0:
                break
            
            
            daño_enemigo = max(0, enemigo['ataque'] - jugador['defensa'])
            jugador['vida'] -= daño_enemigo
            print(f"😵 El enemigo te hizo {daño_enemigo} de daño!")
            
        elif accion == "usar item":
            usar_item(jugador)
            
        elif accion == "huir":
            if random.random() < 0.5:
                print("✅ Lograste huir del combate!")
                return False
            else:
                print("❌ No pudiste huir!")
                daño_enemigo = max(0, enemigo['ataque'] - jugador['defensa'])
                jugador['vida'] -= daño_enemigo
                print(f"😵 El enemigo te hizo {daño_enemigo} de daño!")
        
        else:
            print("❌ Acción no válida")
    
    if jugador['vida'] <= 0:
        print("💀 Has sido derrotado...")
        return False
    else:
        print(f"🎉 ¡Derrotaste al {enemigo_tipo}!")
        jugador['experiencia'] += enemigo['experiencia']
        check_nivel(jugador)
        return True


def evento_rio(jugador):
    print("\n" + historias["rio"])
    
    
    if random.random() < 0.2:
        print("¡De repente, un lobo sale de los arbustos!")
        if combate(jugador, "lobo"):
            print("Derrotas al lobo y continúas tu camino.")
    
    decision = input(decisiones["rio_beber"]).lower()
    
    if decision == "si":
        if random.random() < 0.7:
            print(eventos["rio_beber_bueno"])
            jugador['vida'] += 10
        else:
            print(eventos["rio_beber_malo"])
            jugador['vida'] -= 15
    
    decision = input(decisiones["rio_cruzar"]).lower()
    if decision == "si":
        print("Al cruzar el puente, encuentras un camino hacia las montañas...")
        jugador['ubicacion'] = "montaña"
    else:
        jugador['ubicacion'] = "inicio"

def evento_montana(jugador):
    print("\n" + historias["montaña"])
    decision = input(decisiones["montaña_subir"]).lower()
    
    if decision == "si":
        print("Al subir la montaña, encuentras la entrada a una mazmorra...")
        jugador['ubicacion'] = "mazmorra"
    else:
        jugador['ubicacion'] = "inicio"

def evento_mazmorra(jugador):
    print("\n" + historias["mazmorra"])
    
    if "llave antigua" in jugador['inventario']:
        print("Usas la llave antigua para abrir la puerta de la mazmorra...")
        decision = input(decisiones["mazmorra_entrar"]).lower()
        
        if decision == "si":
            
            enemigo_mazmorra = random.choice(["esqueleto", "orco", "bruja"])
            if combate(jugador, enemigo_mazmorra):
                print("Derrotas al enemigo y encuentras un cofre!")
                jugador['ubicacion'] = "tesoro"
        else:
            jugador['ubicacion'] = "inicio"
    else:
        print("La puerta está cerrada. Necesitas una llave para entrar.")
        jugador['ubicacion'] = "inicio"

def evento_tesoro(jugador):
    print("\n" + historias["tesoro"])
    decision = input(decisiones["tesoro_abrir"]).lower()
    
    if decision == "si":
        tesoro = random.choice(["tesoro_arma", "tesoro_armadura", "tesoro_poción", "tesoro_amuleto", "tesoro_vacio"])
        
        if tesoro == "tesoro_arma":
            print(eventos["tesoro_arma"])
            jugador['inventario'].append("espada larga")
        elif tesoro == "tesoro_armadura":
            print(eventos["tesoro_armadura"])
            jugador['inventario'].append("armadura")
        elif tesoro == "tesoro_poción":
            print(eventos["tesoro_poción"])
            jugador['inventario'].append("poción grande")
        elif tesoro == "tesoro_amuleto":
            print(eventos["tesoro_amuleto"])
            jugador['inventario'].append("amuleto")
        else:
            print(eventos["tesoro_vacio"])
    
    jugador['ubicacion'] = "inicio"

def evento_pueblo(jugador):
    print("\n" + historias["pueblo"])
    print("\nLugares en el pueblo:")
    print("1. Taberna")
    print("2. Herrería")
    print("3. Volver al bosque")
    
    opcion = input("\n¿A dónde quieres ir? (1/2/3): ")
    
    if opcion == "1":
        jugador['ubicacion'] = "taberna"
    elif opcion == "2":
        jugador['ubicacion'] = "herrería"
    else:
        jugador['ubicacion'] = "inicio"

def evento_taberna(jugador):
    print("\n" + historias["taberna"])
    decision = input(decisiones["taberna_hablar"]).lower()
    
    if decision == "si":
        if random.random() < 0.5:
            print(eventos["aldeano_info"])
        else:
            print(eventos["aldeano_poción"])
            jugador['inventario'].append("poción")
    
    jugador['ubicacion'] = "pueblo"

def evento_herrería(jugador):
    print("\n" + historias["herrería"])
    decision = input(decisiones["herrería_buscar"]).lower()
    
    if decision == "si":
        print(eventos["herrero_arma"])
        jugador['inventario'].append("hacha")
    
    jugador['ubicacion'] = "pueblo"

def evento_bosque_profundo(jugador):
    print("\n" + historias["bosque profundo"])
    
    if random.random() < 0.7:
        
        enemigo_bosque = random.choice(["lobo", "araña gigante", "bruja", "orco"])
        if combate(jugador, enemigo_bosque):
            if enemigo_bosque == "bruja":
                print("Derrotas a la bruja y encuentras una llave antigua en su bolso!")
                jugador['inventario'].append("llave antigua")
            else:
                
                recompensa = random.choice(["poción", "poción grande", "amuleto"])
                jugador['inventario'].append(recompensa)
                print(f"🏆 ¡Encontraste una {recompensa}!")
    else:
        print("Exploras el bosque pero no encuentras nada interesante.")
    
    jugador['ubicacion'] = "inicio"


def aventura_principal(jugador):
    print(f"\n{historias[jugador['ubicacion']]}")
    
    if jugador['ubicacion'] == "inicio":
        print("\nOpciones:")
        print("1. Ir a la cueva")
        print("2. Ir al pueblo")
        print("3. Ir al río")
        print("4. Ir al bosque profundo")
        print("5. Revisar estadísticas")
        print("6. Guardar y salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            jugador['ubicacion'] = "cueva"
            print(historias["cueva"])
            decision = input(decisiones["cueva_entrar"]).lower()
            if decision == "si":
                
                enemigo_cueva = random.choice(["goblin", "araña gigante", "lobo"])
                if combate(jugador, enemigo_cueva):
                    
                    recompensa = random.choice(["espada", "poción", "poción grande"])
                    jugador['inventario'].append(recompensa)
                    print(f"🏆 ¡Encontraste una {recompensa}!")
            jugador['ubicacion'] = "inicio"
                
        elif opcion == "2":
            jugador['ubicacion'] = "pueblo"
            evento_pueblo(jugador)
            
        elif opcion == "3":
            jugador['ubicacion'] = "rio"
            evento_rio(jugador)
            
        elif opcion == "4":
            jugador['ubicacion'] = "bosque profundo"
            evento_bosque_profundo(jugador)
            
        elif opcion == "5":
            mostrar_jugador(jugador)
            
        elif opcion == "6":
            return False
            
        else:
            print("❌ Opción no válida")
    
    elif jugador['ubicacion'] == "pueblo":
        evento_pueblo(jugador)
        
    elif jugador['ubicacion'] == "taberna":
        evento_taberna(jugador)
        
    elif jugador['ubicacion'] == "herrería":
        evento_herrería(jugador)
        
    elif jugador['ubicacion'] == "montaña":
        evento_montana(jugador)
        
    elif jugador['ubicacion'] == "mazmorra":
        evento_mazmorra(jugador)
        
    elif jugador['ubicacion'] == "tesoro":
        evento_tesoro(jugador)
    
    return True


def menu_principal():
    jugadores = cargar_jugadores()
    
    while True:
        print("\n" + "="*40)
        print("🎮 RPG - AVENTURA EN EL BOSQUE")
        print("="*40)
        print("1. Nuevo juego")
        print("2. Cargar jugador")
        print("3. Ver jugadores")
        print("4. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            jugador = crear_jugador()
            jugadores[jugador['nombre']] = jugador
            guardar_jugadores(jugadores)
            
            while aventura_principal(jugador):
                pass
                
            guardar_jugadores(jugadores)
            
        elif opcion == "2":
            if not jugadores:
                print("❌ No hay jugadores guardados")
                continue
                
            print("\nJugadores disponibles:")
            for nombre in jugadores:
                print(f"- {nombre}")
                
            nombre = input("\nNombre del jugador: ")
            if nombre in jugadores:
                jugador = jugadores[nombre]
                print(f"✅ Jugador {nombre} cargado!")
                mostrar_jugador(jugador)
                
                while aventura_principal(jugador):
                    pass
                    
                guardar_jugadores(jugadores)
            else:
                print("❌ Jugador no encontrado")
                
        elif opcion == "3":
            if not jugadores:
                print("❌ No hay jugadores guardados")
            else:
                print("\nJUGADORES REGISTRADOS:")
                for nombre, datos in jugadores.items():
                    print(f"{nombre} - Nivel {datos['nivel']} {datos['clase']}")
                    
        elif opcion == "4":
            print("¡Hasta pronto!")
            break
            
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    menu_principal()