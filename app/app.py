# from flask import Response, 

from http import HTTPStatus
from os import system #La usaremos para limpiar la terminal con system("cls")
import json
from flask import Flask, jsonify, request, Response

#Funciones:

def menu_principal():
    system("cls") #Limpia la terminal
    print('-------------------------------')
    print('       Nombre Programa         ')
    print('-------------------------------')
    print('[1] Iniciar sesión')
    print('[2] Modo invitado')
    print('[0] Salir')
    print('-------------------------------')
    return

def cargar_películas():
    with open('datos_json/películas.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

def cargar_usuarios():
    with open('datos_json/usuarios.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

# Código:

app = Flask(__name__)

# menu_principal()
# opcion = input("ingrese una opción: ")
# if opcion == '1':
#     # usernames = usernames(datos_json)
#     usernames = requests.get('http://127.0.0.1:5000/users')
#     iniciar_sesión(usernames)


@app.route("/")
def Inicio():
    return ("<center><h1>Movie World</h1></center>")

@app.route("/users")
def devolver_usuarios():
    datos_usuarios = cargar_usuarios()
    usuarios = []
    for usuario in datos_usuarios["users"]:
        usuarios.append({
            "username": usuario["username"],
            "id": usuario["id"]}
        )
    return jsonify(usuarios)

@app.route("/users/<id>")
def devolver_usuario(id):
    id_int = int(id)
    print('Me solicitaron: ' + id)
    datos_usuarios = cargar_usuarios()
    for usuario in datos_usuarios["users"]:
        if id_int == usuario["id"]:
            usuario_info={
                "username": usuario["username"],
                "id": usuario["id"],
                "contributions": usuario["contributions"],
                "comments": usuario["comments"]
                }
            return jsonify(usuario_info)
    return Response("No existe ningún usuario con ese ID", status=HTTPStatus.BAD_REQUEST)

@app.route("/users/<id>/comments")
def devolver_comentarios(id):
    id_int = int(id)
    datos_usuarios = cargar_usuarios()
    print('Me solicitaron: ' + id)
    for usuario in datos_usuarios["users"]:
        if id_int == usuario["id"]:
            return jsonify(usuario["comments"])
    return Response("No existe ningún usuario con ese ID", status=HTTPStatus.BAD_REQUEST)

@app.route("/<string:username_search>") #Tuve que quitar el /users pq sino iba al del id
def buscar_usuario(username_search):
    datos_usuarios = cargar_usuarios()
    for usuario in datos_usuarios["users"]:
        if username_search == usuario["username"]:
            usuario_info={
                "username": usuario["username"],
                "id": usuario["id"],
                "contributions": usuario["contributions"],
                "comments": usuario["comments"]
                }
            return jsonify(usuario_info)
    return Response("No existe ningún usuario con ese nombre", status=HTTPStatus.BAD_REQUEST)

@app.route("/users", methods=["POST"])
def crear_usuario():
    datos_usuarios = cargar_usuarios()
    datos_cliente =request.get_json()
    if "username" in datos_cliente and "password" in datos_cliente:
        datos_usuarios["users"].append({
            "username": datos_cliente["username"],
            "id":1,
            "password": datos_cliente["password"],
            "contributions": 0,
            "comments": {}
        }
        )
        return jsonify(datos_usuarios)
    else:
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


app.run(debug=True)