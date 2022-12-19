import json

def cargar_películas():
    with open('datos_json/películas.json') as archivo_películass:
        películas = json.load(archivo_películass)
        return películas

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
print (directores_json)