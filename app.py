# from flask import Response, 

import urllib
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

def cargar_archivo():
    with open("datos.json") as archivo:
        datos_json = json.load(archivo)
        return datos_json

def usernames(datos_json):
    x = len(datos_json["users"])
    usernames = []
    i = 0
    while i < x:
        usernames.append(datos_json["users"][i]["username"])
        i= i + 1
    return (usernames)
    

def iniciar_sesión(usernames):
    system("cls")
    INnombre_usuario = input("Ingrese su nombre de usuario: ")
    INcontraseña = input("ingrese su contraseña: ")
    for i in usernames:
        if i == INnombre_usuario:
            print("Nombre correcto")

# Código:

app = Flask(__name__)

datos_json = cargar_archivo()
users = datos_json["users"]

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
    x = len(datos_json["users"])
    usernames = []
    i = 0
    while i < x:
        usernames.append(datos_json["users"][i]["username"])
        i= i + 1
    return Response(jsonify(usernames), status = HTTPStatus.OK)

@app.route("/users/<id>", methods=["GET", "POST"])
def devolver_usuario(id):
    id_int = int(id)
    print(request.method)
    print('Me solicitaron: ' + id)
    x = len(users)
    i = 0
    while i < x:
        usuario_id = users[i]["id"]
        if id_int == usuario_id:
            return Response(users[i]["username"], status = HTTPStatus.OK)
        i = i + 1
    return Response("No existe ningún usuario con ese ID", status=HTTPStatus.BAD_REQUEST)                    

@app.route("/users/<string:usernameSearch>")
def buscar_usuario(usernameSearch):
    for i in users:
        if i["username"] == usernameSearch:
            # usernameFound = i['username']
            return ("encontrado")
            # return jsonify({"user": usernameFound})
    return Response("No existe ningún usuario con ese USERNAME", status=HTTPStatus.BAD_REQUEST)                    

@app.route("/users/<id>/comments")
def devolver_comentarios(id):
    id_int = int(id)
    print('Me solicitaron: ' + id)
    x = len(users)
    i = 0
    comentarios = []
    while i < x:
        usuario_id = users[i]["id"]
        if id_int == usuario_id:
            for comentario in (users[i]["comments"]):
                comentarios.append(comentario)
            comentarios_string = 'Comentarios: ', ', '.join(comentarios)
            return Response(comentarios_string, status = HTTPStatus.OK)
        i = i + 1
    return Response("No existe ningún usuario con ese ID", status=HTTPStatus.BAD_REQUEST)  


app.run(debug=True)