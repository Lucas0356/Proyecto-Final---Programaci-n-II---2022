from http import HTTPStatus
from os import system #La usaremos para limpiar la terminal con system("cls")
import json
from flask import Flask, jsonify, request, Response

#Funciones:

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
    id_nuevo_usuario = len(datos_usuarios["users"])
    if "username" in datos_cliente and "password" in datos_cliente:
        datos_usuarios["users"].append({
            "username": datos_cliente["username"],
            "id":id_nuevo_usuario,
            "password": datos_cliente["password"],
            "contributions": 0,
            "comments": {}
        }
        )
        return jsonify(datos_usuarios)
    else:
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


#Películas:

@app.route("/films")
def devolver_películas():
    datos_películas = cargar_películas()
    películas = []
    for película in datos_películas["films"]:
        películas.append(
            película
        )
    return jsonify(películas)

@app.route("/films/directors")
def devolver_directores():
    datos_películas = cargar_películas()
    directores = []
    for película in datos_películas["films"]:
        if película["director"] not in directores:
            directores.append({
                "director": película["director"]}
            )
    return jsonify(directores)

@app.route("/films/gender")
def devolver_generos():
    datos_películas = cargar_películas()
    generos = []
    for película in datos_películas["films"]:
        if {"gender": película["gender"]} not in generos:
            generos.append({
                "gender": película["gender"]}
            )
    return jsonify(generos)

@app.route("/films/<string:film_search>")
def buscar_película(film_search):
    datos_películas = cargar_películas()
    for película in datos_películas["films"]:
        if film_search == película["title"]:
            return jsonify(película)
    return Response("No existe ninguna película con ese nombre", status=HTTPStatus.BAD_REQUEST)

@app.route("/films/<string:film_search>", methods=["DELETE"])
def borrar_película(film_search):
    datos_películas = cargar_películas()
    for película in datos_películas["films"]:
        if film_search == película["title"]:
            datos_películas["films"].remove(película)
            print ('Se borro correctamente', film_search)
            return Response(status=HTTPStatus.OK)
    return Response("No existe ninguna película con ese nombre", status=HTTPStatus.BAD_REQUEST)

@app.route("/films/last10")
def mostrar_ultimas10():
    datos_películas = cargar_películas()
    peliculas = []
    for i in reversed(datos_películas["films"]) :
        peliculas.append(i)
        if len(peliculas) == 10:
            break
    return jsonify(peliculas)

app.run(debug=True)



            # "title": película["title"],
            # "director": película["director"],
            # "year": película["year"],
            # "gender": película["gender"],
            # "synopsis": película["synopsis"],
            # "link_image": película["link_image"]}