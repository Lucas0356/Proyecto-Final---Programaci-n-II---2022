from os import system #La usaremos para limpiar la terminal con system("cls")
import requests, json

#funciones

def menu_principal():
    system("cls") #Limpia la terminal
    print('-------------------------------')
    print('       Nombre Programa         ')
    print('-------------------------------')
    print('[1] Iniciar sesión')
    print('[2] Modo público')
    print('[0] Salir')
    print('-------------------------------')
    return

def cargar_usuarios():
    with open('datos_json/usuarios.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

def iniciar_sesión(usuarios):
    while True:
        INusuario = input("\nIngrese su nombre de usuario: ")
        contador_max = len(usuarios)
        contador = 0
        for usuario in usuarios:
            if INusuario != usuario["username"]:
                if contador == contador_max:
                    contador= contador + 1
                    print ("\nNombre de usuario inexistente")
                    continue
            elif INusuario == usuario["username"]:
                INcontraseña = input ("\ningrese su contraseña: ")
                datos_usuarios = cargar_usuarios()
                for usuario in datos_usuarios["users"]:
                    if usuario["username"] == INusuario:
                        if INcontraseña == usuario["password"]:
                            print('\nBienvenido ' + INusuario + '!')
                            return
                        else: 
                            print ("\nContraseña incorrecta")
                            continue


menu_principal()
opcion = input("ingrese una opción: ")
if opcion == '1':
    usuarios = requests.get('http://127.0.0.1:5000/users')
    iniciar_sesión(usuarios.json())
    print("\nque desea hacer?")
elif opcion == '2':
    ultimas10 = requests.get('http://127.0.0.1:5000/films/last10')
    print(ultimas10.json())
elif opcion == '0':
    exit