def notas():
    notas = []
    cantidad =int(input("cuantas notas quieres ingresar?: "))
    for i in range (cantidad):
        while True:
            try:
                nota = float(input(f"ingrese la nota {i+1}:"))
                if 0 <= nota <= 10:
                    notas.append(nota)
                    break
                else:
                    print("la nota debe ser entre 0 y 10")
            except ValueError:
                print("por favor ingrese un valor numerico")
    return notas

