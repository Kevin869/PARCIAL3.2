# 📌 Gestor de Estudiantes con Diccionarios Anidados

# Diccionario principal
estudiantes = {}

# ------------------ FUNCIONES ------------------

def agregar_estudiante():
    id_est = input("Ingrese el ID del estudiante: ").strip()
    if id_est in estudiantes:
        print("⚠️ Este ID ya existe. Intente con otro.")
        return

    nombre = input("Ingrese el nombre completo: ").strip()
    try:
        edad = int(input("Ingrese la edad: "))
    except ValueError:
        print("⚠️ La edad debe ser un número entero.")
        return

    calificaciones = []
    while True:
        try:
            nota = input("Ingrese una calificación (o 'fin' para terminar): ").strip()
            if nota.lower() == "fin":
                break
            calificaciones.append(float(nota))
        except ValueError:
            print("⚠️ Debe ingresar un número válido.")

    estudiantes[id_est] = {
        "nombre": nombre,
        "edad": edad,
        "calificaciones": calificaciones
    }
    print("✅ Estudiante agregado con éxito.")


def mostrar_estudiantes():
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
        return
    print("\n📋 Lista de Estudiantes:")
    for id_est, datos in estudiantes.items():
        print(f"ID: {id_est} | Nombre: {datos['nombre']} | Edad: {datos['edad']} | Calificaciones: {datos['calificaciones']}")


def calcular_promedio():
    id_est = input("Ingrese el ID del estudiante: ").strip()
    if id_est not in estudiantes:
        print("⚠️ Estudiante no encontrado.")
        return
    calificaciones = estudiantes[id_est]["calificaciones"]
    if not calificaciones:
        print("⚠️ Este estudiante no tiene calificaciones registradas.")
        return
    promedio = sum(calificaciones) / len(calificaciones)
    print(f"📊 Estudiante {id_est} - {estudiantes[id_est]['nombre']} - Promedio: {promedio:.2f}")


def eliminar_estudiante():
    id_est = input("Ingrese el ID del estudiante a eliminar: ").strip()
    if id_est in estudiantes:
        del estudiantes[id_est]
        print("🗑️ Estudiante eliminado con éxito.")
    else:
        print("⚠️ Estudiante no encontrado.")

# ------------------ MENÚ PRINCIPAL ------------------

def menu():
    while True:
        print("\n===== 📚 GESTOR DE ESTUDIANTES =====")
        print("1. Agregar estudiante")
        print("2. Mostrar todos los estudiantes")
        print("3. Calcular promedio de un estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            calcular_promedio()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente de nuevo.")

# Ejecutar programa
menu()
