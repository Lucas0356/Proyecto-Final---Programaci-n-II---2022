from os import system #La usaremos para limpiar la terminal con system("cls")
import json
from flask import request

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

menu_principal()
opcion = input("ingrese una opción: ")
if opcion == '1':
    usuarios = request.get('http://127.0.0.1:5000/users')
    print(usuarios.json())