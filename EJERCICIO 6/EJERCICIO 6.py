import requests
import os

URL = "https://httpbin.org/post"

def probar_contrasenas():
    try:
        
        

        
        with open(r"C:\Users\kevin\OneDrive\Escritorio\xamp\htdocs\CODE.VISUAL\PARCIAL3.2\EJERCICIO 6\contrasenas.txt", "r", encoding="utf-8") as archivo:
            contrasenas = archivo.readlines()

        
        for contrasena in contrasenas:
            contrasena = contrasena.strip()  
            if not contrasena:  
                continue

            print(f"Probando contrasena: {contrasena}")

            
            data = {
                "usuario": "admin",    
                "password": contrasena
            }

            respuesta = requests.post(URL, data=data)

            
            if respuesta.status_code == 200:
                print(f" Login exitoso con contrasena: {contrasena}\n")
            else:
                print(f" Fallo con contrasena: {contrasena}\n")

    except FileNotFoundError:
        print(" Error: El archivo 'contrasenas.txt' no existe.")
    except requests.exceptions.RequestException as e:
        print(f" Error en la conexion: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")


if __name__ == "__main__":
    probar_contrasenas()
