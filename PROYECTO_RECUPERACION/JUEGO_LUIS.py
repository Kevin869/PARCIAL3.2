import random
import time

class Personaje:
    def __init__(self):
        self.nombre = ""
        self.vida = 100
        self.experiencia = 0
        self.nivel = 1
        self.habilidades = {
            "fuerza": 10,
            "agilidad": 10,
            "inteligencia": 10,
            "carisma": 10
        }
        self.inventario = {
            "armas": ["espada básica"],
            "armaduras": ["armadura de cuero"],
            "objetos": ["poción de salud x3"]
        }
        self.oro = 50
        self.historial_decisiones = []
    
    def mostrar_estado(self):
        print(f"\n--- ESTADO DE {self.nombre.upper()} ---")
        print(f"Vida: {self.vida}/100")
        print(f"Nivel: {self.nivel} | Experiencia: {self.experiencia}/100")
        print(f"Oro: {self.oro}")
        print("Habilidades:")
        for habilidad, valor in self.habilidades.items():
            print(f"  {habilidad.capitalize()}: {valor}")
        print("Inventario:")
        for tipo, objetos in self.inventario.items():
            print(f"  {tipo.capitalize()}: {', '.join(objetos)}")
    
    def subir_nivel(self):
        if self.experiencia >= 100:
            self.nivel += 1
            self.experiencia -= 100
            self.vida = 100  # Recuperar toda la vida al subir de nivel
            print(f"\n¡Felicidades! Has subido al nivel {self.nivel}!")
            print("Elige una habilidad para mejorar:")
            habilidades = list(self.habilidades.keys())
            for i, habilidad in enumerate(habilidades, 1):
                print(f"{i}. {habilidad.capitalize()} ({self.habilidades[habilidad]})")
            
            while True:
                try:
                    opcion = int(input("Opción: "))
                    if 1 <= opcion <= len(habilidades):
                        habilidad_elegida = habilidades[opcion-1]
                        self.habilidades[habilidad_elegida] += 5
                        print(f"{habilidad_elegida.capitalize()} mejorada a {self.habilidades[habilidad_elegida]}")
                        break
                    else:
                        print("Opción no válida")
                except ValueError:
                    print("Por favor, ingresa un número")
            
            # Recompensa aleatoria al subir de nivel
            recompensas = [
                "poción de salud", "poción de mana", "espada mejorada",
                "armadura de malla", "50 de oro", "mapa antiguo"
            ]
            recompensa = random.choice(recompensas)
            
            if recompensa in ["poción de salud", "poción de mana"]:
                self.inventario["objetos"].append(recompensa + " x2")
                print(f"Has obtenido: {recompensa} x2")
            elif recompensa == "50 de oro":
                self.oro += 50
                print("Has obtenido: 50 de oro")
            else:
                if "espada" in recompensa:
                    self.inventario["armas"].append(recompensa)
                elif "armadura" in recompensa:
                    self.inventario["armaduras"].append(recompensa)
                else:
                    self.inventario["objetos"].append(recompensa)
                print(f"Has obtenido: {recompensa}")

def combate(jugador, enemigo, enemigo_fuerza):
    print(f"\n¡Te enfrentas a {enemigo}!")
    
    # Estadísticas del enemigo basadas en su fuerza y el nivel del jugador
    vida_enemigo = 30 + (enemigo_fuerza * 10) + (jugador.nivel * 5)
    daño_enemigo = 5 + (enemigo_fuerza * 3) + (jugador.nivel * 2)
    recompensa_oro = 10 + (enemigo_fuerza * 5) + (jugador.nivel * 3)
    recompensa_exp = 20 + (enemigo_fuerza * 8) + (jugador.nivel * 5)
    
    print(f"{enemigo} - Vida: {vida_enemigo} | Daño: {daño_enemigo}")
    
    while vida_enemigo > 0 and jugador.vida > 0:
        print("\n¿Qué deseas hacer?")
        print("1. Atacar")
        print("2. Usar objeto")
        print("3. Intentar huir")
        
        opcion = input("Opción: ")
        
        if opcion == "1":
            # Jugador ataca
            daño_jugador = random.randint(5, 15) + jugador.habilidades["fuerza"] // 2
            vida_enemigo -= daño_jugador
            print(f"Atacas a {enemigo} y le causas {daño_jugador} de daño")
            
            if vida_enemigo <= 0:
                break
                
            # Enemigo ataca
            jugador.vida -= daño_enemigo
            print(f"{enemigo} te ataca y te causa {daño_enemigo} de daño")
            print(f"Tu vida restante: {jugador.vida}")
            
        elif opcion == "2":
            # Usar objeto
            if "poción de salud" in str(jugador.inventario["objetos"]):
                print("Usas una poción de salud y recuperas 30 de vida")
                jugador.vida = min(100, jugador.vida + 30)
                # Eliminar una poción
                for i, obj in enumerate(jugador.inventario["objetos"]):
                    if "poción de salud" in obj:
                        if "x" in obj:
                            cantidad = int(obj.split("x")[1])
                            if cantidad > 1:
                                jugador.inventario["objetos"][i] = f"poción de salud x{cantidad-1}"
                            else:
                                jugador.inventario["objetos"].pop(i)
                        else:
                            jugador.inventario["objetos"].pop(i)
                        break
            else:
                print("No tienes pociones de salud")
                
            # El enemigo ataca incluso si usas objeto
            jugador.vida -= daño_enemigo
            print(f"{enemigo} te ataca y te causa {daño_enemigo} de daño")
            print(f"Tu vida restante: {jugador.vida}")
            
        elif opcion == "3":
            # Intentar huir
            probabilidad_huir = jugador.habilidades["agilidad"] * 2
            if random.randint(1, 100) <= probabilidad_huir:
                print("Logras huir del combate")
                return False
            else:
                print("No logras huir")
                jugador.vida -= daño_enemigo
                print(f"{enemigo} te ataca y te causa {daño_enemigo} de daño")
                print(f"Tu vida restante: {jugador.vida}")
        else:
            print("Opción no válida")
    
    if jugador.vida <= 0:
        print("Has sido derrotado...")
        return False
    else:
        print(f"\n¡Has derrotado a {enemigo}!")
        print(f"Ganas {recompensa_exp} de experiencia y {recompensa_oro} de oro")
        jugador.experiencia += recompensa_exp
        jugador.oro += recompensa_oro
        if jugador.experiencia >= 100:
            jugador.subir_nivel()
        return True

def evento_exploracion(jugador):
    eventos = [
        {
            "descripcion": "Encuentras un cofre antiguo escondido entre la maleza.",
            "opciones": [
                {"texto": "Abrir el cofre", "resultado": "objeto", "riesgo": 20},
                {"texto": "Dejarlo allí (podría estar booby-trapped)", "resultado": "nada", "riesgo": 0}
            ]
        },
        {
            "descripcion": "Un mercader ambulante te ofrece sus productos.",
            "opciones": [
                {"texto": "Comprar una poción de salud (20 oro)", "resultado": "comprar_pocion", "riesgo": 0},
                {"texto": "Comprar una espada mejorada (50 oro)", "resultado": "comprar_espada", "riesgo": 0},
                {"texto": "Ignorar al mercader", "resultado": "nada", "riesgo": 0}
            ]
        },
        {
            "descripcion": "Ves una cueva oscura. Parece peligrosa pero podría haber tesoros.",
            "opciones": [
                {"texto": "Entrar a la cueva", "resultado": "cueva", "riesgo": 40},
                {"texto": "Seguir camino", "resultado": "nada", "riesgo": 0}
            ]
        },
        {
            "descripcion": "Encuentras un herido tirado en el camino.",
            "opciones": [
                {"texto": "Ayudar al herido", "resultado": "ayudar_herido", "riesgo": 10},
                {"texto": "Seguir tu camino", "resultado": "nada", "riesgo": 0}
            ]
        }
    ]
    
    evento = random.choice(eventos)
    print(f"\n{evento['descripcion']}")
    
    for i, opcion in enumerate(evento["opciones"], 1):
        print(f"{i}. {opcion['texto']}")
    
    while True:
        try:
            eleccion = int(input("Opción: "))
            if 1 <= eleccion <= len(evento["opciones"]):
                opcion_elegida = evento["opciones"][eleccion-1]
                break
            else:
                print("Opción no válida")
        except ValueError:
            print("Por favor, ingresa un número")
    
    # Procesar resultado
    if opcion_elegida["resultado"] == "objeto":
        if random.randint(1, 100) > opcion_elegida["riesgo"]:
            objetos = ["poción de salud", "poción de mana", "mapa antiguo", "10 de oro", "gemas brillantes"]
            objeto_obtenido = random.choice(objetos)
            
            if objeto_obtenido == "10 de oro":
                jugador.oro += 10
                print("Encuentras 10 de oro en el cofre")
            else:
                jugador.inventario["objetos"].append(objeto_obtenido)
                print(f"Encuentras {objeto_obtenido} en el cofre")
        else:
            print("El cofre estaba trampeado. Pierdes 15 de vida")
            jugador.vida -= 15
    
    elif opcion_elegida["resultado"] == "comprar_pocion":
        if jugador.oro >= 20:
            jugador.oro -= 20
            jugador.inventario["objetos"].append("poción de salud")
            print("Has comprado una poción de salud")
        else:
            print("No tienes suficiente oro")
    
    elif opcion_elegida["resultado"] == "comprar_espada":
        if jugador.oro >= 50:
            jugador.oro -= 50
            jugador.inventario["armas"].append("espada mejorada")
            print("Has comprado una espada mejorada")
        else:
            print("No tienes suficiente oro")
    
    elif opcion_elegida["resultado"] == "cueva":
        if random.randint(1, 100) > opcion_elegida["riesgo"]:
            print("Encuentras un tesoro escondido en la cueva. Ganas 100 de oro y una armadura mejorada")
            jugador.oro += 100
            jugador.inventario["armaduras"].append("armadura de malla")
        else:
            print("La cueva estaba llena de peligros. Pierdes 30 de vida y huyes")
            jugador.vida -= 30
    
    elif opcion_elegida["resultado"] == "ayudar_herido":
        if random.randint(1, 100) > opcion_elegida["riesgo"]:
            print("El herido resulta ser un noble agradecido. Te recompensa con 50 de oro")
            jugador.oro += 50
        else:
            print("Era una trampa. Unos bandidos te atacan y pierdes 20 de vida y 30 de oro")
            jugador.vida -= 20
            jugador.oro = max(0, jugador.oro - 30)
    
    elif opcion_elegida["resultado"] == "nada":
        print("Decides seguir tu camino.")
    
    # Verificar si el jugador murió por el evento
    if jugador.vida <= 0:
        print("Has muerto...")
        return False
    
    return True

def main():
    print("="*60)
    print("          EL REINO PERDIDO DE ELDORIA")
    print("="*60)
    print("\nUna aventura épica te espera...")
    time.sleep(2)
    
    jugador = Personaje()
    jugador.nombre = input("¿Cuál es tu nombre, aventurero? ")
    
    print(f"\nBienvenido, {jugador.nombre}. Tu aventura está por comenzar...")
    time.sleep(2)
    
    # Capítulo 1: El inicio
    print("\n" + "="*40)
    print("CAPÍTULO 1: EL LLAMADO DE LA AVENTURA")
    print("="*40)
    
    print("\nTe despiertas en una posada tranquila. El anciano del pueblo te busca.")
    print("'¡Aventurero! El reino de Eldoria necesita tu ayuda.'")
    print("'El malvado hechicero Morgath ha robado el Cristal de la Eternidad.'")
    print("'Sin él, nuestro reino caerá en oscuridad para siempre.'")
    
    print("\n¿Aceptas la misión?")
    print("1. Sí, acepto la misión (Camino del Héroe)")
    print("2. No, prefiero seguir con mi vida tranquila (Camino del Aldeano)")
    
    while True:
        decision = input("Opción: ")
        if decision == "1":
            jugador.historial_decisiones.append("Aceptó la misión")
            print("\n'¡Excelente! Toma esta espada y armadura básica para tu viaje.'")
            break
        elif decision == "2":
            jugador.historial_decisiones.append("Rechazó la misión")
            print("\n'¡Qué decepción! Pero tal vez cambies de opinión cuando la oscuridad llegue...'")
            print("Una semana después, el ejército de Morgath arrasa tu aldea.")
            print("Logras escapar por poco, pero ahora buscas venganza.")
            jugador.inventario["armas"].append("espada de venganza")
            jugador.habilidades["fuerza"] += 2
            break
        else:
            print("Opción no válida")
    
    time.sleep(3)
    
    # Primer combate
    print("\nMientras sales de la aldea, unos goblins te atacan!")
    if not combate(jugador, "Goblin", 1):
        print("Game Over - No pudiste con los primeros goblins...")
        return
    
    # Evento de exploración
    if not evento_exploracion(jugador):
        return
    
    # Capítulo 2: El cruce de caminos
    print("\n" + "="*40)
    print("CAPÍTULO 2: EL CRUCE DE CAMINOS")
    print("="*40)
    
    print("\nLlegas a un cruce de caminos. Tres senderos se presentan ante ti:")
    print("1. El camino del bosque (más seguro pero más largo)")
    print("2. El paso de la montaña (peligroso pero rápido)")
    print("3. El pantano olvidado (misterioso y arriesgado)")
    
    while True:
        try:
            camino = int(input("¿Qué camino eliges? "))
            if camino == 1:
                jugador.historial_decisiones.append("Camino del bosque")
                print("\nEmprendes el camino del bosque. La vegetación es espesa pero el aire es tranquilo.")
                # Evento específico del bosque
                print("Encuentras un lobo herido atrapado en una trampa.")
                print("1. Liberar al lobo")
                print("2. Dejarlo allí")
                
                decision_lobo = input("Opción: ")
                if decision_lobo == "1":
                    print("Liberas al lobo, que parece agradecido. Te sigue a distancia.")
                    jugador.historial_decisiones.append("Liberó al lobo")
                    # Más adelante el lobo ayudará
                else:
                    print("Decides no interferir y sigues tu camino.")
                    jugador.historial_decisiones.append("Ignoró al lobo")
                break
                
            elif camino == 2:
                jugador.historial_decisiones.append("Camino de montaña")
                print("\nSubes por el paso de montaña. El aire es frío y el camino peligroso.")
              
                print("Un yeti te bloquea el paso!")
                if combate(jugador, "Yeti", 3):
                    print("Tras derrotar al yeti, encuentras un tesoro en su cueva.")
                    jugador.oro += 75
                    jugador.inventario["objetos"].append("poción de mana x2")
                    print("Ganas 75 de oro y 2 pociones de mana")
                else:
                    return
                break
                
            elif camino == 3:
                jugador.historial_decisiones.append("Camino del pantano")
                print("\nTe adentras en el pantano olvidado. El aire es denso y misterioso.")
                
                print("Una bruja te ofrece un trato desde su choza.")
                print("'Te daré un objeto mágico si me traes 3 hierbas especiales del pantano'")
                print("1. Aceptar el trato")
                print("2. Rechazar y seguir camino")
                
                decision_bruja = input("Opción: ")
                if decision_bruja == "1":
                    print("Aceptas el trato y buscas las hierbas por el pantano.")
              
                    hierbas_encontradas = 0
                    for i in range(3):
                        input("Presiona Enter para buscar una hierba...")
                        if random.random() > 0.3:  
                            hierbas_encontradas += 1
                            print(f"Encuentras una hierba especial ({hierbas_encontradas}/3)")
                        else:
                            print("No encuentras nada aquí...")
                    
                    if hierbas_encontradas == 3:
                        print("Regresas con la bruja, quien cumple su promesa.")
                        jugador.inventario["objetos"].append("amuleto de protección")
                        print("Obtienes el Amuleto de Protección")
                    else:
                        print("La bruja se enfada porque no conseguiste todas las hierbas.")
                        print("Te lanza un hechizo que te debilita.")
                        jugador.vida -= 20
                        jugador.habilidades["fuerza"] -= 2
                        print("Pierdes 20 de vida y 2 puntos de fuerza")
                else:
                    print("Rechazas el trato y continúas por el pantano.")
                break
                
            else:
                print("Opción no válida")
        except ValueError:
            print("Por favor, ingresa un número")
    

    for i in range(2):
        if not evento_exploracion(jugador):
            return
        if not combate(jugador, "Bestia del camino", 2):
            return
    
    
    
    print("\n" + "="*40)
    print("TU AVENTURA CONTINUARÁ...")
    print("="*40)
    print("\nEsta es solo el inicio de tu épica aventura.")
    print("El Reino de Eldoria tiene muchos más secretos por descubrir.")
    print("¿Lograrás recuperar el Cristal de la Eternidad?")
    print("¿Enfrentarás al hechicero Morgath en su fortaleza?")
    print("¿Descubrirás los secretos de tu pasado?")
    
    jugador.mostrar_estado()
    print("\nDecisiones tomadas:")
    for i, decision in enumerate(jugador.historial_decisiones, 1):
        print(f"{i}. {decision}")

if __name__ == "__main__":
    main()