import numpy as np

def ingresar_matriz(nombre):
    filas = int(input(f"Ingresa el número de filas de la matriz {nombre}: "))
    columnas = int(input(f"Ingresa el número de columnas de la matriz {nombre}: "))
    print(f"Ingresa los elementos de la matriz {nombre}, fila por fila (separados por espacios):")
    matriz = []
    for i in range(filas):
        fila = list(map(float, input(f"Fila {i+1}: ").split()))
        while len(fila) != columnas:
            print("Cantidad incorrecta de elementos. Intenta nuevamente.")
            fila = list(map(float, input(f"Fila {i+1}: ").split()))
        matriz.append(fila)
    return np.array(matriz)

def mostrar_menu():
    print("\n===== CALCULADORA MATRICIAL =====")
    print("1. Sumar matrices")
    print("2. Restar matrices")
    print("3. Multiplicar matrices")
    print("4. Transponer una matriz")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            print("\n-- Suma de matrices --")
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape != B.shape:
                print("Error: Las matrices deben tener las mismas dimensiones para sumar.")
            else:
                print("Resultado de A + B:\n", A + B)

        elif opcion == "2":
            print("\n-- Resta de matrices --")
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape != B.shape:
                print("Error: Las matrices deben tener las mismas dimensiones para restar.")
            else:
                print("Resultado de A - B:\n", A - B)

        elif opcion == "3":
            print("\n-- Multiplicación de matrices --")
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape[1] != B.shape[0]:
                print("Error: Las matrices no son compatibles para multiplicación (columnas de A deben ser igual a filas de B).")
            else:
                print("Resultado de A x B:\n", A @ B)

        elif opcion == "4":
            print("\n-- Transposición de matriz --")
            A = ingresar_matriz("A")
            print("Matriz transpuesta:\n", A.T)

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
