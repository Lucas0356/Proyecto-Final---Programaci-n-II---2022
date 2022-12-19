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

def cargar_comentarios():
    with open('datos_json/comentarios.json') as archivo:
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
            "id": usuario["id"],}
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

# ___________________________ Crear Usuario ____________________________ #

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

@app.route("/films/directors")
def devolver_directores():
    datos_películas = cargar_películas()
    lista_directores = []
    directores_json = {"directors": []}
    for película in datos_películas["films"]:
        coincidencias = 0
        if lista_directores == []:
            lista_directores.append(película["director"])
        else:
            for director in lista_directores:
                if película["director"] == director:
                    coincidencias = coincidencias = + 1
        if coincidencias == 0:
            lista_directores.append(película["director"])
            directores_json["directors"].append({
                "name": película["director"]}
            )
    return jsonify(directores_json)

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

# ____________________________ Comentarios ____________________________ #

@app.route("/films/<string:film_search>/comments") # Buscar todos los comentarios de una película
def ver_comentarios(film_search):
    datos_comentarios = cargar_comentarios()
    comentarios = []
    for comentario in datos_comentarios["comments"]:
        if comentario["film"] == film_search:
                comentarios.append(comentario)
    if comentarios == []:
        return Response("No existe ningún comentario para esa película", status=HTTPStatus.BAD_REQUEST)
    else: 
        return jsonify(comentarios)

@app.route("/users/<string:username>/comments") # Ver comentarios de un usuario
def buscar_comentarios_usuario(username):
    datos_comentarios = cargar_comentarios()
    comentarios = []
    for comentario in datos_comentarios["comments"]:
        if comentario["username"] == username:
            comentarios.append(username)
    if comentarios == []:
        return Response("Error!", status=HTTPStatus.BAD_REQUEST)
    else:
        return jsonify(datos_comentarios)

# @app.route("/users/<id>/comments", methods=["POST"]) # Agregar comentarios
# def modificar_comentario(id):
#     id_int = int(id)
#     datos_usuarios = cargar_usuarios()
#     datos_cliente = request.get_json()
#     key_datos_cliente = []
#     contador = 0
#     comentarios = {}
#     for dato in datos_cliente:
#         if contador == 0:
#             key_datos_cliente.append(dato)
#     for usuario in datos_usuarios["users"]:
#         if id_int == usuario["id"]:
#             for pelicula_comentario in usuario["comments"]:
#                 coincidencias = 0
#                 if pelicula_comentario == key_datos_cliente[0]:
#                     coincidencias = coincidencias + 1
#                 else:
#                     print("printa")
#             if coincidencias == 0:
#                 datos_usuarios["users"][contador]["comments"][pelicula_comentario] = datos_cliente[key_datos_cliente[0]]
#                 return jsonify(datos_usuarios)
#         contador = 0 + 1
#     return Response("Error!", status=HTTPStatus.BAD_REQUEST)

@app.route("/users/<string:username>/comments", methods=["PUT"]) # Editar comentarios
def modificar_comentario(username):
    datos_comentarios = cargar_comentarios()
    datos_cliente = request.get_json()
    print (datos_cliente)
    if "comment" in datos_cliente and "film" in datos_cliente:
        for comentario in datos_comentarios["comments"]:
            índice = datos_comentarios["comments"].index(comentario)
            if comentario["username"] == username:
                if  comentario["film"] == datos_cliente["film"]:
                    datos_comentarios["comments"][índice]["comment"] = datos_cliente["comment"]
                    return jsonify(datos_comentarios)
    else:
        return Response("Error!", status=HTTPStatus.BAD_REQUEST)

@app.route("/films/<string:film_search>/comments", methods=["DELETE"])
def borrar_comentario(film_search):
    datos_usuarios = cargar_usuarios()
    comentarios = []
    user = request.get_json()
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
        for coment in comentarios:
            if coment["username"] == user["username"]:
                comentarios.remove(coment)
        return jsonify(comentarios)
        

# ___________________________ ABM Peliculas ___________________________ #

@app.route("/films", methods=["POST"]) # Agregar película
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

@app.route("/films/<string:film_search>", methods=["DELETE"]) # Borrar película
def borrar_película(film_search):
    datos_películas = cargar_películas()
    for película in datos_películas["films"]:
        if film_search == película["title"]:
            datos_películas["films"].remove(película)
            return jsonify(datos_películas)
    return Response("No existe ninguna película con ese nombre", status=HTTPStatus.BAD_REQUEST)

@app.route("/films/<string:film_search>", methods=["PUT"]) # Modificar película
def editar_pelicula(film_search):
    datos_peliculas = cargar_películas()
    datos_editados = request.get_json()
    for pelicula in datos_peliculas["films"]:
        if pelicula["title"] == film_search:
            if "title" in datos_editados:
                pelicula["title"] = datos_editados["title"]
            if "year" in datos_editados:
                pelicula["year"] = datos_editados["year"]
            if "link_image" in datos_editados:
                pelicula["link image"] = datos_editados["link_image"]
            if "gender" in datos_editados:
                pelicula["gender"] = datos_editados["gender"]
            if "synopsis" in datos_editados:
                pelicula["synopsis"] = datos_editados["synopsis"]
            if "director" in datos_editados:
                pelicula["director"] = datos_editados["director"]
            return jsonify(datos_peliculas)
    return Response("No existe ninguna película con ese nombre", status=HTTPStatus.BAD_REQUEST)

# _______________________ Ultimas 10 Peliculas _______________________ #
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