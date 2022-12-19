from http import HTTPStatus
from os import system #La usaremos para limpiar la terminal con system("cls")
import json
from flask import Flask, jsonify, request, Response

# _______________________________________________________________ Funciones _______________________________________________________________ #

def cargar_películas():
    with open('datos_json/películas.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

def cargar_usuarios():
    with open('datos_json/usuarios.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

# _______________________________________________________________ Código __________________________________________________________________ #

app = Flask(__name__)

@app.route("/")
def Inicio():
    return ("<center><h1>Movie World</h1></center>")
# ______________________________ Usuarios ______________________________ #
@app.route("/users")
def devolver_usuarios():
    datos_usuarios = cargar_usuarios()
    usuarios = []
    for usuario in datos_usuarios["users"]:
        usuarios.append({
            "username": usuario["username"],
            "id": usuario["id"],
            "comments": usuario["comments"]}
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

@app.route("/user/<string:username_search>") 
def buscar_usuario(username_search):
    datos_usuarios = cargar_usuarios()
    for usuario in datos_usuarios["users"]:
        if username_search == usuario["username"]:
            usuario_info={
                "username": usuario["username"],
                "id": usuario["id"],
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
            "comments": {}
        }
        )
        return jsonify(datos_usuarios)
    else:
        return Response("{}",status=HTTPStatus.BAD_REQUEST)


# _____________________________ Peliculas ______________________________ #

@app.route("/films")
def devolver_películas():
    datos_películas = cargar_películas()
    películas = []
    for película in datos_películas["films"]:
        películas.append(
            película
        )
    return jsonify(películas)

@app.route("/films", methods=["POST"])
def crear_película():
    datos_películas = cargar_películas()
    datos_cliente = request.get_json()
    print (datos_cliente["title"])
    existe = False
    if "title" in datos_cliente and "year" in datos_cliente and "director" in datos_cliente and "gender" in datos_cliente and "synopsis" in datos_cliente and "link_image" in datos_cliente:
        for película in datos_películas["films"]:
            print (película["title"])
            print (datos_cliente["title"])
            if datos_cliente["title"] == película["title"]:
                existe = True
    if existe == False:
        datos_películas["films"].append(
        datos_cliente
        )
        return jsonify(datos_películas)
    elif existe == True:
        return Response("Ya hay una película cargada con ese nombre",status=HTTPStatus.BAD_REQUEST)

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

@app.route("/films/directors/<string:director_search>")
def devolver_películas_director(director_search):
    datos_películas = cargar_películas()
    películas = []
    for película in datos_películas["films"]:
        if director_search == película["director"]:
            if película["title"] not in películas:
                películas.append(
                    película
                )
    if películas == []:
        return Response('No hay películas cargadas con ese director', status=HTTPStatus.BAD_REQUEST)
    else:
        return jsonify(películas)

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

@app.route("/films/gender/<string:gender_search>")
def devolver_películas_género(gender_search):
    datos_películas = cargar_películas()
    películas = []
    for película in datos_películas["films"]:
        if gender_search == película["gender"]:
                películas.append(
                    película
                )
    if películas == []:
        return Response('No hay películas cargadas con ese género', status=HTTPStatus.BAD_REQUEST)
    else:
        return jsonify(películas)

@app.route("/films/<string:film_search>")
def buscar_película(film_search):
    datos_películas = cargar_películas()
    films_found = []
    for película in datos_películas["films"]:
        if film_search.lower() in película["title"].lower():
            films_found.append(
                película
            )
    if films_found == []:
        return Response("No existe ninguna película con ese nombre", status=HTTPStatus.BAD_REQUEST)
    else: 
        return jsonify(films_found)

@app.route("/films/<string:film_search>/comments")
def ver_comentarios(film_search):
    datos_usuarios = cargar_usuarios()
    comentarios = []
    for usuario in datos_usuarios["users"]:
        for comentario_película in usuario["comments"]:
            if film_search == comentario_película:
                comentarios.append({
                    "username": usuario["username"],
                    "comment": usuario["comments"][film_search]}
                )
    if comentarios == []:
        return Response("No existe ningún comentario para esa película", status=HTTPStatus.BAD_REQUEST)
    else: 
        return jsonify(comentarios)

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
    películas = []
    for película in reversed(datos_películas["films"]) :
        películas.append(película)
        if len(películas) == 10:
            break
    return jsonify(películas)

app.run(debug=True)