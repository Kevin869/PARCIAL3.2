# main.py - Gestión de estudiantes con menú

def leer_estudiantes(archivo):
    try:
        with open(archivo, "r") as f:
            lineas = f.readlines()
        
        estudiantes = []
        for linea in lineas:
            try:
                nombre, calificacion = linea.strip().split(",")
                estudiantes.append((nombre, float(calificacion)))
            except ValueError:
                print(f"⚠️ Línea con formato incorrecto: {linea.strip()}")
        return estudiantes

    except FileNotFoundError:
        print(f"❌ El archivo '{archivo}' no existe.")
        return []


def calcular_promedio(estudiantes):
    if not estudiantes:
        return 0
    total = sum(calificacion for _, calificacion in estudiantes)
    return total / len(estudiantes)


def guardar_reporte(estudiantes, archivo_reporte, promedio):
    with open(archivo_reporte, "w") as f:
        for nombre, calificacion in estudiantes:
            f.write(f"{nombre},{calificacion}\n")
        f.write(f"Promedio general: {promedio:.1f}\n")
    print(f"✅ Reporte guardado en '{archivo_reporte}'")


def agregar_estudiante(archivo):
    nombre = input("Ingrese el nombre del estudiante: ")
    while True:
        try:
            calificacion = float(input("Ingrese la calificación (0-100): "))
            if 0 <= calificacion <= 100:
                break
            else:
                print("⚠️ La calificación debe estar entre 0 y 100.")
        except ValueError:
            print("⚠️ Por favor ingrese un número válido.")

    with open(archivo, "a") as f:
        f.write(f"{nombre},{calificacion}\n")
    print(f"✅ {nombre} agregado con éxito.")


def mostrar_estudiantes(archivo):
    estudiantes = leer_estudiantes(archivo)
    if not estudiantes:
        print("⚠️ No hay estudiantes registrados.")
        return
    print("\n📋 Lista de estudiantes:")
    for i, (nombre, calificacion) in enumerate(estudiantes, start=1):
        print(f"{i}. {nombre} - {calificacion}")


# -------------------
# FLUJO PRINCIPAL CON MENÚ
# -------------------
ARCHIVO_ESTUDIANTES = "estudiantes.txt"
ARCHIVO_REPORTE = "reporte.txt"

while True:
    print("\n📚 MENÚ DE GESTIÓN DE ESTUDIANTES")
    print("1. Ver promedio general")
    print("2. Agregar nuevo estudiante")
    print("3. Generar reporte")
    print("4. Mostrar estudiantes")
    print("5. Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        estudiantes = leer_estudiantes(ARCHIVO_ESTUDIANTES)
        if estudiantes:
            promedio = calcular_promedio(estudiantes)
            print(f"📊 Promedio actual: {promedio:.1f}")
        else:
            print("⚠️ No hay datos para calcular el promedio.")

    elif opcion == "2":
        agregar_estudiante(ARCHIVO_ESTUDIANTES)

    elif opcion == "3":
        estudiantes = leer_estudiantes(ARCHIVO_ESTUDIANTES)
        if estudiantes:
            promedio = calcular_promedio(estudiantes)
            guardar_reporte(estudiantes, ARCHIVO_REPORTE, promedio)
        else:
            print("⚠️ No hay datos para generar el reporte.")

    elif opcion == "4":
        mostrar_estudiantes(ARCHIVO_ESTUDIANTES)

    elif opcion == "5":
        print("👋 Saliendo del programa...")
        break

    else:
        print("⚠️ Opción no válida. Intente de nuevo.")
