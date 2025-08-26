
import json
import os
import random
import time
from colorama import Fore, Style, init

# Inicializar colorama para colores en la consola
init(autoreset=True)

# Archivo para guardar jugadores (JSON Lines: 1 jugador por línea)
PLAYER_FILE = "jugadores.json"

# Clases disponibles con estadísticas base
CLASES = {
    "mago": {"vida": 60, "ataque": 8, "defensa": 3, "mana": 100},
    "guerrero": {"vida": 100, "ataque": 12, "defensa": 8, "mana": 20},
    "explorador": {"vida": 80, "ataque": 10, "defensa": 5, "mana": 40}
}

# Enemigos disponibles
ENEMIGOS = {
    "goblin": {"vida": 30, "ataque": 6, "defensa": 2, "xp": 15},
    "orco": {"vida": 50, "ataque": 10, "defensa": 4, "xp": 25},
    "lobo": {"vida": 25, "ataque": 8, "defensa": 1, "xp": 10},
    "esqueleto": {"vida": 35, "ataque": 7, "defensa": 3, "xp": 18}
}

# Items disponibles
ITEMS = {
    "poción_vida": {"tipo": "consumible", "efecto": "restaurar 30 de vida"},
    "poción_mana": {"tipo": "consumible", "efecto": "restaurar 25 de mana"},
    # Nota: Los equipamientos están definidos, pero en esta versión
    # nos centramos en consumibles para simplificar la jugabilidad.
    "espada_hierro": {"tipo": "equipamiento", "efecto": "+3 ataque"},
    "escudo_madera": {"tipo": "equipamiento", "efecto": "+2 defensa"},
    "amuleto_suerte": {"tipo": "equipamiento", "efecto": "+5% experiencia"}
}

# ---------------------------------------------------------------------
# Utilidades de consola
# ---------------------------------------------------------------------
def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    """Muestra el título del juego con estilo"""
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "       SISTEMA DE GESTIÓN DE AVENTURAS RPG")
    print(Fore.CYAN + "=" * 60)
    print()

# ---------------------------------------------------------------------
# Persistencia de jugadores (formato JSON Lines)
# ---------------------------------------------------------------------
def cargar_jugadores():
    """Carga los jugadores desde el archivo JSON (uno por línea)"""
    jugadores = []
    if os.path.exists(PLAYER_FILE):
        try:
            with open(PLAYER_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        jugadores.append(json.loads(line))
            print(Fore.GREEN + f"✅ {len(jugadores)} jugador(es) cargado(s) correctamente.")
        except Exception as e:
            print(Fore.RED + f"❌ Error al cargar jugadores: {e}")
            return []
    return jugadores

def guardar_jugador(jugador):
    """Guarda un jugador en el archivo JSON (en una nueva línea)"""
    try:
        with open(PLAYER_FILE, 'a', encoding='utf-8') as f:
            json.dump(jugador, f, ensure_ascii=False)
            f.write('\n')
        return True
    except Exception as e:
        print(Fore.RED + f"❌ Error al guardar jugador: {e}")
        return False

def actualizar_jugador(jugador_actual):
    """Actualiza la información del jugador en el archivo"""
    jugadores = cargar_jugadores()
    jugadores_actualizados = []
    for jugador in jugadores:
        if jugador['nombre'] == jugador_actual['nombre']:
            jugadores_actualizados.append(jugador_actual)
        else:
            jugadores_actualizados.append(jugador)
    try:
        with open(PLAYER_FILE, 'w', encoding='utf-8') as f:
            for jugador in jugadores_actualizados:
                json.dump(jugador, f, ensure_ascii=False)
                f.write('\n')
        return True
    except Exception as e:
        print(Fore.RED + f"❌ Error al actualizar jugador: {e}")
        return False

# ---------------------------------------------------------------------
# Registro / selección
# ---------------------------------------------------------------------
def registrar_jugador():
    """Registra un nuevo jugador"""
    limpiar_pantalla()
    mostrar_titulo()

    print(Fore.MAGENTA + "🎮 REGISTRO DE NUEVO JUGADOR")
    print(Fore.CYAN + "-" * 40)

    nombre = input(Fore.WHITE + "📝 Introduce tu nombre: ").strip()
    if not nombre:
        print(Fore.RED + "❌ El nombre no puede estar vacío.")
        time.sleep(2)
        return None

    # Mostrar clases disponibles
    print(Fore.YELLOW + "\n🏆 Clases disponibles:")
    for clase, stats in CLASES.items():
        print(
            Fore.WHITE
            + f"  {clase.capitalize():<12} - Vida: {stats['vida']} | Ataque: {stats['ataque']} | Defensa: {stats['defensa']} | Maná: {stats['mana']}"
        )

    while True:
        clase = input(Fore.WHITE + "\n🎯 Elige tu clase (mago, guerrero, explorador): ").lower().strip()
        if clase in CLASES:
            break
        print(Fore.RED + "❌ Clase no válida. Elige entre: mago, guerrero, explorador")

    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "experiencia": 0,
        "experiencia_necesaria": 100,
        "vida": CLASES[clase]["vida"],
        "vida_maxima": CLASES[clase]["vida"],
        "ataque": CLASES[clase]["ataque"],
        "defensa": CLASES[clase]["defensa"],
        "mana": CLASES[clase]["mana"],
        "mana_maximo": CLASES[clase]["mana"],
        "inventario": {
            "poción_vida": 2,
            "poción_mana": 1
        },
        "logros": [],
        "misiones_completadas": 0,
        "enemigos_derrotados": 0,
        "ultima_aventura": None
    }

    if guardar_jugador(jugador):
        print(Fore.GREEN + f"\n✅ ¡Jugador {nombre} registrado con éxito como {clase.capitalize()}!")
        time.sleep(1.4)
        return jugador
    return None

def seleccionar_jugador(jugadores):
    """Permite seleccionar un jugador existente"""
    limpiar_pantalla()
    mostrar_titulo()

    print(Fore.MAGENTA + "👥 SELECCIONAR JUGADOR")
    print(Fore.CYAN + "-" * 40)

    if not jugadores:
        print(Fore.YELLOW + "📝 No hay jugadores registrados. Creando uno nuevo...")
        time.sleep(1.2)
        return registrar_jugador()

    for i, jugador in enumerate(jugadores, 1):
        print(Fore.WHITE + f"{i}. {jugador['nombre']} - Nivel {jugador['nivel']} {jugador['clase'].capitalize()}")

    try:
        seleccion = int(input(Fore.WHITE + "\n🎯 Selecciona un jugador (número): "))
        if 1 <= seleccion <= len(jugadores):
            return jugadores[seleccion - 1]
        else:
            print(Fore.RED + "❌ Selección no válida.")
            time.sleep(1.2)
            return None
    except ValueError:
        print(Fore.RED + "❌ Por favor ingresa un número válido.")
        time.sleep(1.2)
        return None

# ---------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------
def mostrar_estado(jugador):
    """Muestra el estado actual del jugador"""
    print(Fore.GREEN + f"\n📊 ESTADO DE {jugador['nombre'].upper()}")
    print(Fore.CYAN + "-" * 40)
    print(Fore.WHITE + f"🏆 Nivel: {jugador['nivel']} ({jugador['experiencia']}/{jugador['experiencia_necesaria']} XP)")
    print(Fore.RED + f"❤️  Vida: {jugador['vida']}/{jugador['vida_maxima']}")
    print(Fore.BLUE + f"💧 Maná: {jugador['mana']}/{jugador['mana_maximo']}")
    print(Fore.YELLOW + f"⚔️  Ataque: {jugador['ataque']}")
    print(Fore.YELLOW + f"🛡️  Defensa: {jugador['defensa']}")
    print(Fore.MAGENTA + f"⭐ Logros: {len(jugador['logros'])}")
    print(Fore.CYAN + f"🎯 Misiones: {jugador['misiones_completadas']}")
    print(Fore.RED + f"💀 Enemigos: {jugador['enemigos_derrotados']}")

def mostrar_inventario(jugador):
    """Muestra el inventario del jugador"""
    print(Fore.GREEN + f"\n🎒 INVENTARIO DE {jugador['nombre'].upper()}")
    print(Fore.CYAN + "-" * 40)
    if not jugador['inventario']:
        print(Fore.YELLOW + "📦 El inventario está vacío.")
        return
    for item, cantidad in jugador['inventario'].items():
        if cantidad > 0:
            descripcion = ITEMS.get(item, {}).get('efecto', 'Efecto desconocido')
            print(Fore.WHITE + f"• {item.replace('_', ' ').title()}: {cantidad} - {descripcion}")

def ver_logros(jugador):
    """Muestra los logros del jugador"""
    print(Fore.MAGENTA + f"\n🏆 LOGROS DE {jugador['nombre'].upper()}")
    print(Fore.CYAN + "-" * 40)
    if not jugador['logros']:
        print(Fore.YELLOW + "Aún no tienes logros. ¡Sigue aventurándote!")
        return
    for i, logro in enumerate(jugador['logros'], 1):
        print(Fore.WHITE + f"{i}. {logro['titulo']} — {logro.get('descripcion','')}")

# ---------------------------------------------------------------------
# Ítems
# ---------------------------------------------------------------------
def usar_item(jugador):
    """Permite al jugador usar un item del inventario"""
    mostrar_inventario(jugador)

    if not any(cantidad > 0 for cantidad in jugador['inventario'].values()):
        print(Fore.YELLOW + "📦 No tienes items para usar.")
        return False

    item = input(Fore.WHITE + "\n🎯 ¿Qué item quieres usar? (deja vacío para cancelar): ").lower().strip()
    if not item:
        return False

    # Convertir entrada a formato de clave
    item_key = item.replace(' ', '_')

    if item_key not in jugador['inventario'] or jugador['inventario'][item_key] <= 0:
        print(Fore.RED + "❌ No tienes ese item o la cantidad es insuficiente.")
        return False

    # Aplicar efectos del item
    if item_key == "poción_vida":
        curacion = min(30, jugador['vida_maxima'] - jugador['vida'])
        jugador['vida'] += curacion
        print(Fore.GREEN + f"💚 Usaste poción de vida. +{curacion} de vida.")

    elif item_key == "poción_mana":
        regeneracion = min(25, jugador['mana_maximo'] - jugador['mana'])
        jugador['mana'] += regeneracion
        print(Fore.BLUE + f"💙 Usaste poción de maná. +{regeneracion} de maná.")

    # Reducir la cantidad del item
    jugador['inventario'][item_key] -= 1
    if jugador['inventario'][item_key] <= 0:
        del jugador['inventario'][item_key]

    return True

# ---------------------------------------------------------------------
# Combate
# ---------------------------------------------------------------------
def combate(jugador, enemigo_tipo):
    """Simula un combate contra un enemigo"""
    enemigo = ENEMIGOS[enemigo_tipo].copy()
    enemigo_nombre = enemigo_tipo.capitalize()

    print(Fore.RED + f"\n⚔️  ¡COMBATE CONTRA UN {enemigo_nombre.upper()}!")
    print(Fore.CYAN + "-" * 50)

    # Función anidada + *args: aplica multiplicadores encadenados al daño
    def aplicar_mods(daño_base, *mods):
        mult = 1.0
        for m in mods:
            mult *= m
        return max(1, int(daño_base * mult))

    # Lambda para crítico
    es_critico = lambda prob=0.15: random.random() < prob

    turno = 0
    while jugador['vida'] > 0 and enemigo['vida'] > 0:
        turno += 1
        print(Fore.YELLOW + f"\n🔄 Turno {turno}")
        print(Fore.WHITE + f"❤️  Tu vida: {jugador['vida']}/{jugador['vida_maxima']}")
        print(Fore.RED + f"💀 Vida del {enemigo_nombre}: {enemigo['vida']}")

        # Turno del jugador
        print(Fore.GREEN + "\n🎯 Tu turno:")
        print("1. Atacar")
        print("2. Usar item")
        print("3. Huir")

        try:
            accion = int(input(Fore.WHITE + "Elige una acción (1-3): "))
        except ValueError:
            accion = 0

        if accion == 1:  # Atacar
            variacion = random.uniform(0.9, 1.1)
            base = max(1, jugador['ataque'] - enemigo['defensa'] // 2 + random.randint(-2, 2))
            crit_mult = 2.0 if es_critico() else 1.0
            daño = aplicar_mods(base, variacion, crit_mult)
            enemigo['vida'] -= daño
            if crit_mult > 1:
                print(Fore.LIGHTRED_EX + f"🔥 ¡Golpe crítico! Haces {daño} de daño.")
            else:
                print(Fore.GREEN + f"⚔️  Atacas al {enemigo_nombre} y haces {daño} de daño!")

        elif accion == 2:  # Usar item
            if usar_item(jugador):
                # Usar un ítem consume el turno (decisión de diseño)
                pass
            else:
                print(Fore.YELLOW + "No usaste ningún ítem este turno.")

        elif accion == 3:  # Huir
            if random.random() < 0.6:  # 60% de probabilidad de huir
                print(Fore.YELLOW + "🏃‍♂️ ¡Logras huir del combate!")
                return False
            else:
                print(Fore.RED + "❌ No logras huir. ¡El enemigo te alcanza!")
        else:
            print(Fore.RED + "❌ Acción no válida. Pierdes tu turno.")

        # Turno del enemigo (si sigue vivo)
        if enemigo['vida'] > 0:
            variacion_e = random.uniform(0.9, 1.1)
            base_e = max(1, enemigo['ataque'] - jugador['defensa'] // 2 + random.randint(-2, 2))
            crit_e = 1.5 if random.random() < 0.1 else 1.0
            daño_enemigo = aplicar_mods(base_e, variacion_e, crit_e)
            jugador['vida'] -= daño_enemigo
            if crit_e > 1:
                print(Fore.RED + f"💥 ¡Crítico del {enemigo_nombre}! Te hace {daño_enemigo} de daño.")
            else:
                print(Fore.RED + f"💀 El {enemigo_nombre} te ataca y te hace {daño_enemigo} de daño.")

    # Resultado del combate
    if jugador['vida'] <= 0:
        print(Fore.RED + f"\n💀 Has sido derrotado por el {enemigo_nombre}...")
        # Restaurar algo de vida después de la derrota (no perder progreso del todo)
        jugador['vida'] = max(1, jugador['vida_maxima'] // 4)
        print(Fore.YELLOW + f"💚 Te recuperas con {jugador['vida']} de vida.")
        return False
    else:
        xp_ganada = enemigo['xp']
        jugador['experiencia'] += xp_ganada
        jugador['enemigos_derrotados'] += 1

        # Posible botín
        if random.random() < 0.4:  # 40% de probabilidad de botín
            items_posibles = ["poción_vida", "poción_mana"]
            item_ganado = random.choice(items_posibles)
            jugador['inventario'][item_ganado] = jugador['inventario'].get(item_ganado, 0) + 1
            print(Fore.GREEN + f"🎁 ¡Has obtenido una {item_ganado.replace('_', ' ')}!")

        print(Fore.GREEN + f"\n🎉 ¡Has derrotado al {enemigo_nombre}!")
        print(Fore.YELLOW + f"⭐ +{xp_ganada} puntos de experiencia!")
        return True

# ---------------------------------------------------------------------
# Progresión
# ---------------------------------------------------------------------
def ganar_experiencia(jugador, cantidad):
    """Añade experiencia al jugador y comprueba subida de nivel"""
    jugador['experiencia'] += cantidad

    # Comprobar subida de nivel
    while jugador['experiencia'] >= jugador['experiencia_necesaria']:
        jugador['nivel'] += 1
        exceso = jugador['experiencia'] - jugador['experiencia_necesaria']
        jugador['experiencia'] = exceso
        jugador['experiencia_necesaria'] = int(jugador['experiencia_necesaria'] * 1.5)

        # Mejoras por nivel (base)
        jugador['vida_maxima'] += 10
        jugador['ataque'] += 2
        jugador['defensa'] += 1
        jugador['mana_maximo'] += 5

        # Ajuste por clase (un toque de identidad)
        if jugador['clase'] == 'guerrero':
            jugador['vida_maxima'] += 5
        elif jugador['clase'] == 'mago':
            jugador['ataque'] += 1
            jugador['mana_maximo'] += 5
        elif jugador['clase'] == 'explorador':
            jugador['ataque'] += 1

        # Restauros tras subir
        jugador['vida'] = jugador['vida_maxima']
        jugador['mana'] = jugador['mana_maximo']

        print(Fore.CYAN + f"\n🎉 ¡SUBISTE AL NIVEL {jugador['nivel']}!")
        print(Fore.GREEN + f"❤️  Vida máxima: {jugador['vida_maxima']}")
        print(Fore.GREEN + f"⚔️  Ataque: {jugador['ataque']}")
        print(Fore.GREEN + f"🛡️  Defensa: {jugador['defensa']}")

        # Logros por nivel
        if jugador['nivel'] == 5:
            agregar_logro(jugador, "Novato experimentado", "Alcanzaste el nivel 5")
        elif jugador['nivel'] == 10:
            agregar_logro(jugador, "Maestro aventurero", "Alcanzaste el nivel 10")

def agregar_logro(jugador, titulo, descripcion):
    """Añade un logro al jugador si no lo tiene ya"""
    logro = {"titulo": titulo, "descripcion": descripcion}
    if logro not in jugador['logros']:
        jugador['logros'].append(logro)
        print(Fore.MAGENTA + f"\n🏆 ¡LOGRO DESBLOQUEADO: {titulo}!")
        print(Fore.WHITE + f"📝 {descripcion}")

# ---------------------------------------------------------------------
# Aventura
# ---------------------------------------------------------------------
def aventura_principal(jugador):
    """Aventura principal con decisiones interactivas"""
    limpiar_pantalla()
    mostrar_titulo()

    print(Fore.BLUE + "🌲 AVENTURA: EL BOSQUE ENCANTADO")
    print(Fore.CYAN + "=" * 50)

    # Decisión 1
    print(Fore.WHITE + "\nTe encuentras en la entrada de un bosque misterioso.")
    print("El camino se divide en dos senderos:")
    print("1. Tomar el sendero de la izquierda (parece más seguro)")
    print("2. Tomar el sendero de la derecha (se escuchan ruidos extraños)")

    try:
        decision1 = int(input(Fore.YELLOW + "\n¿Qué camino eliges? (1-2): "))
    except ValueError:
        decision1 = 1

    if decision1 == 1:
        print(Fore.GREEN + "\n🌳 Tomas el sendero de la izquierda...")
        print("El camino es tranquilo y encuentras un arroyo cristalino.")
        print("Bebes agua y recuperas 10 de vida.")
        jugador['vida'] = min(jugador['vida_maxima'], jugador['vida'] + 10)
        xp_ganada = 20

    else:  # decision1 == 2
        print(Fore.RED + "\n🌲 Tomas el sendero de la derecha...")
        print("¡Te encuentras con un lobo hambriento!")
        if combate(jugador, "lobo"):
            xp_ganada = 25
        else:
            xp_ganada = 10

    # Decisión 2
    print(Fore.WHITE + "\n\nContinúas tu camino y encuentras una cabaña abandonada.")
    print("1. Entrar a la cabaña a investigar")
    print("2. Continuar por el camino principal")
    print("3. Buscar alrededor de la cabaña")

    try:
        decision2 = int(input(Fore.YELLOW + "\n¿Qué decides hacer? (1-3): "))
    except ValueError:
        decision2 = 2

    if decision2 == 1:
        print(Fore.YELLOW + "\n🏚️ Entras a la cabaña...")
        print("Encuentras un cofre con una poción de vida y algo de oro.")
        jugador['inventario']['poción_vida'] = jugador['inventario'].get('poción_vida', 0) + 1
        xp_ganada += 15
        print(Fore.GREEN + "💚 ¡Has encontrado una poción de vida!")

    elif decision2 == 2:
        print(Fore.GREEN + "\n🛣️ Continúas por el camino principal...")
        print("El camino es seguro pero no encuentras nada interesante.")
        xp_ganada += 10

    else:  # decision2 == 3
        print(Fore.RED + "\n🔍 Buscas alrededor de la cabaña...")
        print("¡Te sorprende un goblin escondido!")
        if combate(jugador, "goblin"):
            xp_ganada += 20
        else:
            xp_ganada += 5

    # Decisión 3 (crítica)
    print(Fore.WHITE + "\n\nLlegas a un claro en el bosque donde hay un altar antiguo.")
    print("1. Investigar el altar")
    print("2. Ignorar el altar y continuar")
    print("3. Descansar cerca del altar")

    try:
        decision3 = int(input(Fore.YELLOW + "\n¿Qué haces con el altar? (1-3): "))
    except ValueError:
        decision3 = 1

    if decision3 == 1:
        print(Fore.MAGENTA + "\n✨ Investigas el altar...")
        print("Encuentras una inscripción mágica que te otorga conocimiento.")
        print("+2 de ataque permanente!")
        jugador['ataque'] += 2
        xp_ganada += 30
        agregar_logro(jugador, "Sabio del altar", "Descubriste los secretos del altar antiguo")

    elif decision3 == 2:
        print(Fore.YELLOW + "\n🚶‍♂️ Decides ignorar el altar...")
        print("Continúas tu camino sin incidentes.")
        xp_ganada += 15

    else:  # decision3 == 3
        print(Fore.RED + "\n😴 Te recuestas a descansar...")
        print("¡Eres emboscado por un orco!")
        if combate(jugador, "orco"):
            xp_ganada += 35
            agregar_logro(jugador, "Supervivencia extrema", "Sobreviviste a una emboscada")
        else:
            xp_ganada += 10

    # Final de la aventura
    print(Fore.CYAN + "\n" + "=" * 50)
    print(Fore.GREEN + "🏁 ¡Has completado la aventura!")
    ganar_experiencia(jugador, xp_ganada)
    jugador['misiones_completadas'] += 1
    jugador['ultima_aventura'] = time.strftime("%Y-%m-%d %H:%M:%S")

    # Logro por completar primera misión
    if jugador['misiones_completadas'] == 1:
        agregar_logro(jugador, "Primeros pasos", "Completaste tu primera aventura")

    input(Fore.YELLOW + "\nPresiona Enter para continuar...")

# ---------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------
def menu_principal(jugador):
    """Menú principal del juego"""
    while True:
        limpiar_pantalla()
        mostrar_titulo()
        mostrar_estado(jugador)

        print(Fore.MAGENTA + "\n🎮 MENÚ PRINCIPAL")
        print(Fore.CYAN + "-" * 30)
        print(Fore.WHITE + "1. 🏃‍♂️ Iniciar aventura")
        print(Fore.WHITE + "2. 🎒 Ver inventario")
        print(Fore.WHITE + "3. 💊 Usar item")
        print(Fore.WHITE + "4. 🏆 Ver logros")
        print(Fore.WHITE + "5. 💾 Guardar y salir")
        print(Fore.WHITE + "6. 🚪 Salir sin guardar")

        try:
            opcion = int(input(Fore.YELLOW + "\n🎯 Selecciona una opción (1-6): "))
        except ValueError:
            opcion = 0

        if opcion == 1:
            aventura_principal(jugador)

        elif opcion == 2:
            limpiar_pantalla()
            mostrar_inventario(jugador)
            input(Fore.YELLOW + "\nPresiona Enter para continuar...")

        elif opcion == 3:
            limpiar_pantalla()
            usar_item(jugador)
            input(Fore.YELLOW + "\nPresiona Enter para continuar...")

        elif opcion == 4:
            limpiar_pantalla()
            ver_logros(jugador)
            input(Fore.YELLOW + "\nPresiona Enter para continuar...")

        elif opcion == 5:
            if actualizar_jugador(jugador):
                print(Fore.GREEN + "💾 Progreso guardado. ¡Hasta la próxima!")
            else:
                print(Fore.RED + "❌ No se pudo guardar el progreso, pero no se perderá la sesión actual.")
            time.sleep(1.2)
            break

        elif opcion == 6:
            print(Fore.YELLOW + "Saliendo sin guardar…")
            time.sleep(1.0)
            break

        else:
            print(Fore.RED + "❌ Opción no válida.")
            time.sleep(1.0)

# ---------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------
def main():
    limpiar_pantalla()
    mostrar_titulo()
    print(Fore.WHITE + "Bienvenido al mundo de PyRPG")
    print(Fore.CYAN + "-" * 30)
    print("1. Registrar nuevo jugador")
    print("2. Cargar jugador existente")

    elec = input(Fore.YELLOW + "> ").strip()
    if elec == "1":
        jugador = registrar_jugador()
        if not jugador:
            return
    else:
        jugadores = cargar_jugadores()
        jugador = seleccionar_jugador(jugadores)
        if not jugador:
            return

    print(Fore.GREEN + f"\n¡Bienvenido, {jugador['nombre']} el {jugador['clase'].capitalize()}!")
    time.sleep(1.0)
    menu_principal(jugador)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Style.RESET_ALL + "\n\n👋 Interrumpido por el usuario.")