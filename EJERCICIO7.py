import sys
import random

# Función de orden superior que recibe otra función como argumento
def generar_numeros(cantidad, funcion_generadora):
    return [funcion_generadora() for _ in range(cantidad)]

# Función que genera un número aleatorio entre 1 y 100
def numero_aleatorio():
    return random.randint(1, 100)

# Verificar si el usuario pasó un argumento
if len(sys.argv) < 2:
    print("Uso: python EJERCICIO7.py <cantidad>")
    sys.exit(1)

try:
    # Convertir argumento a entero
    cantidad = int(sys.argv[1])
    
    # Generar la lista de números aleatorios
    lista = generar_numeros(cantidad, numero_aleatorio)
    
    # Mostrar los números separados por espacios
    print(*lista)

except ValueError:
    print(" Debes ingresar un número entero como argumento")
