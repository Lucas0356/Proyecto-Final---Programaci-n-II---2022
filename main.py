from os import system #La usaremos para limpiar la terminal con system("cls")
import requests, json, time, re

# _______________________________________________________________ Funciones _______________________________________________________________

def menu_principal():
    while True:
        system("cls") #Limpia la terminal
        print('-------------------------------')
        print('       Nombre Programa         ')
        print('-------------------------------')
        print('[1] Iniciar sesión')
        print('[2] Modo público')
        print('[3] Registrarse')
        print('[0] Salir')
        print('-------------------------------')
        INopcion = input("\nIngrese una opción: ")
        if INopcion.isdigit() == True:
            if int(INopcion) >= 0 and int(INopcion) <= 3:
                return (INopcion)
            else:
                print("\nIngrese una opción válida")
                time.sleep(1)
                continue
        else:
            print("\nIngrese una opción válida")
            time.sleep(1)
            continue

def menu_usuario(usuario):
    while True:
        system("cls") #Limpia la terminal
        print('\n-------------------------------')
        print('         ',usuario)
        print('-------------------------------')
        print('[1] Agregar Pelicula')
        print('[2] Editar Pelicula')
        print('[3] Agregar Comentario')
        print('[4] Editar Comentario')
        print('[5] Buscar')
        print('[0] Salir')
        print('-------------------------------')
        INopcion = input("\nIngrese una opción: ")
        if INopcion.isdigit() == True:
            if int(INopcion) >= 0 and int(INopcion) <= 5:
                return (INopcion)
            else:
                print("\nIngrese una opción válida")
                time.sleep(1)
                continue
        else:
            print("\nIngrese una opción válida")
            time.sleep(1)
            continue

def menu_buscar(): 
    while True:
        system("cls") #Limpia la terminal
        print('\n-------------------------------')
        print('          Menú buscar'         )
        print('-------------------------------')
        print('[1] Buscar por nombre')
        print('[2] Buscar por director')
        print('[3] Buscar por género')
        print('[0] Salir')
        print('-------------------------------')
        INopcion = input("\nIngrese una opción: ")
        if INopcion.isdigit() == True:
            if int(INopcion) >= 0 and int(INopcion) <= 3:
                return (INopcion)
            else:
                print("\nIngrese una opción válida")
                time.sleep(1)
                continue
        else:
            print("\nIngrese una opción válida")
            time.sleep(1)
            continue

def menu_genero():
    print('\n-------------------------------')
    print('       Escogedor de Genero       ')
    print('-------------------------------\n')

def menu_director():
    print('\n-------------------------------')
    print('      Escogedor de Director      ')
    print('-------------------------------\n')

def menu_editor():
    print('\n-------------------------------')
    print('       Editor de Peliculas       ')
    print('-------------------------------\n')

def cargar_usuarios():
    with open('datos_json/usuarios.json') as archivo:
        datos_json = json.load(archivo)
        return datos_json

def cargar_generos():
    with open('datos_json/generos.json') as archivo_generos:
        generos = json.load(archivo_generos)
        return generos

def cargar_directores():
    with open('datos_json/directores.json') as archivo_directores:
        directores = json.load(archivo_directores)
        return directores

def cargar_películas():
    with open('datos_json/películas.json') as archivo_películass:
        películas = json.load(archivo_películass)
        return películas

def iniciar_sesión():
    usuarios = (requests.get('http://127.0.0.1:5000/users').json())
    while True:
        system("cls") #Limpia la terminal
        INusuario = input("\nIngrese su nombre de usuario: ")
        contador_max = len(usuarios)
        contador = 0
        for usuario in usuarios:
            if INusuario != usuario["username"]:
                contador = contador + 1
                if contador == contador_max:
                    print("\nNombre de usuario inexistente")
                    INopcion = input('\n[1] Para continuar [0] Para salir: ')
                    if INopcion =='1':
                        continue
                    else:
                        return
            elif INusuario == usuario["username"]:
                INcontraseña = input ("\nIngrese su contraseña: ")
                datos_usuarios = cargar_usuarios()
                for usuario in datos_usuarios["users"]:
                    if usuario["username"] == INusuario:
                        if INcontraseña == usuario["password"]:
                            print('\nBienvenido ' + INusuario + '!')
                            return INusuario
                        else: 
                            print ("\nContraseña incorrecta")
                            INopcion = input('\n[1] Para continuar [0] Para salir: ')
                            if INopcion =='1':
                                continue
                            else:
                                return

def registrar_usuario():
    while True:
        system("cls") #Limpia la terminal
        print('\n--------------------------------')
        print('    Registrar nuevo usuario   ')
        print('--------------------------------')
        INnombre_usuario = input("\nIngrese su nombre de usuario: ")
        usuarios = (requests.get('http://127.0.0.1:5000/users').json())
        contador_max = len(usuarios)
        contador = 0
        for usuario in usuarios:
            if INnombre_usuario != usuario["username"]:
                contador = contador + 1 
                if contador == contador_max: # Con esto nos aseguramos que recorra todos los usuarios, y que no sea igual a otro username
                    INcontraseña_usuario = input("\nIngrese su contraseña: ")
                    print ('\nNombre de usuario: ' +  INnombre_usuario)
                    print('Contraseña: ' +  INcontraseña_usuario)
                    print('¿Los datos son correctos?')
                    INopcion = input("\n[1] Para sí [0] Para no: ")
                    if INopcion == '1':
                        nuevo_usuario={
                            "username": INnombre_usuario,
                            "password": INcontraseña_usuario
                        }
                        usuarios = requests.post('http://127.0.0.1:5000/users',json=nuevo_usuario)
                        modificar_json_usuarios(usuarios.json()) # Función que agrega el nuevo usuario al json
                        system("cls") #Limpia la terminal
                        print("¡Usuario creado con éxito!")
                        return (nuevo_usuario["username"])
                    else:
                        return
            else:
                print('\nEl nombre de usuario ', INnombre_usuario, ' ya existe')
                time.sleep(2)
                continue

def modificar_json_usuarios(usuarios_actualizado):
    usuarios_json = open ("datos_json/usuarios.json", 'w', encoding='utf-8')
    json.dump(usuarios_actualizado, usuarios_json, indent = 4)
    usuarios_json.close()
    return 

def modificar_json_películas(películas_actualizado):
    películas_json = open ("datos_json/películas.json" , "w" , encoding='utf-8')
    json.dump(películas_actualizado, películas_json, indent = 4)
    películas_json.close()
    return

def buscar_película_nombre():
    system("cls") #Limpia la terminal
    print('\n--------------------------------')
    print('Buscador de películas por nombre')
    print('--------------------------------\n')
    INpelícula = input("Ingrese el nombre de la película que desea buscar: ")
    film_search = requests.get('http://127.0.0.1:5000/films/'+INpelícula)
    if str(film_search) != '<Response [400]>':
        system("cls") #Limpia la terminal
        print('\nResultados obtenidos = ', len(film_search.json()),"\n")
        for película in film_search.json():
            time.sleep(1)
            print ('===============================')
            print ('Título: ', película["title"])
            print ('Director: ', película["director"])
            print ('Género: ', película["gender"])
            print ('Año: ', película["year"])
            print ('Sinopsis: ', película["synopsis"])
            print ('Imagen representativa: ', película["link_image"])
            print ('-------------------------------')
            print ('Comentarios:')
            print ('-------------------------------')
            buscar_comentarios(película["title"])
            print ('===============================\n')
        return
    else:
        print ("\nPelícula inexistente")
        return

def buscar_película_director():
    system("cls") #Limpia la terminal
    director = elegir_director()
    director_search = requests.get('http://127.0.0.1:5000/films/directors/'+director)
    if str(director_search) != '<Response [400]>':
        system("cls") #Limpia la terminal
        print ('\nPelículas disponibles de ', director, len(director_search.json()),"\n")
        for película in director_search.json():
            time.sleep(1)
            print ('===============================')
            print ('Título: ', película["title"])
            print ('Director: ', película["director"])
            print ('Género: ', película["gender"])
            print ('Año: ', película["year"])
            print ('Sinopsis: ', película["synopsis"])
            print ('Imagen representativa: ', película["link_image"])
            print ('-------------------------------')
            print ('Comentarios:')
            print ('-------------------------------')
            buscar_comentarios(película["title"])
            print ('===============================\n')
        return
    else:
        print ('\nAún no hay películas publicadas de', director)
        return

def buscar_película_género():
    system("cls") #Limpia la terminal
    genero = elegir_genero()
    genero_search = requests.get('http://127.0.0.1:5000/films/gender/'+genero)
    if str(genero_search) != '<Response [400]>':
        system("cls") #Limpia la terminal
        print ('\nPelículas disponibles de ', genero, len(genero_search.json()),"\n")
        for película in genero_search.json():
            time.sleep(1)
            print ('===============================')
            print ('Título: ', película["title"])
            print ('Director: ', película["director"])
            print ('Género: ', película["gender"])
            print ('Año: ', película["year"])
            print ('Sinopsis: ', película["synopsis"])
            print ('Imagen representativa: ', película["link_image"])
            print ('-------------------------------')
            print ('Comentarios:')
            print ('-------------------------------')
            buscar_comentarios(película["title"])
            print ('===============================\n')
        return
    else:
        print ('\nAún no hay películas publicadas de', genero)
        return

def comprobar_url():
    while True:
        url_imagen = input("Ingrese la URL a la portada de la pelicula: ")
        url = re.compile("^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$")
        if url.search(url_imagen): # Comprobemos que sea una URL válida
            print("URL válida")
            return(url_imagen)
        else:
            print("URL no válida")
            print("Ejemplo URL válida: https://www.google.com/")
            continue

def comprobar_año():
    while True:
        año = input("Ingrese el año de la pelicula: ")
        if año.isdigit():
            if int(año) >= 1900 and int(año) <= 2023:
                return (año)
        print("Año no válido")

def agregar_película():
    time.sleep(0.2)
    print('\nUsted escogió, "Agregar Pelicula". Recuerde que los generos y directores, solo pueden ser escogidos entre los')
    print('ya cargados en el sistema.')
    comprobador = True
    while comprobador:
        genero = elegir_genero()
        director = elegir_director()
        title_movie = input("Ingrese el titulo de la pelicula que desea añadir: ")
        year_movie = comprobar_año()
        synopsis_movie = input("Ingrese la sinopsis de la pelicula que desea añadir: ")
        img_movie = comprobar_url()
        new_movie ={
            "title": title_movie.capitalize(),
            "year": year_movie,
            "director": director,
            "gender": genero,
            "synopsis": synopsis_movie.capitalize(),
            "link_image": img_movie
            }
        print("\nEsta seguro que desea añadir esta pelicula?\n")
        print (new_movie)
        op = input("\nOpcion [1] Si [2] No : ")
        if op == "1":
            películas = requests.post('http://127.0.0.1:5000/films',json=new_movie)
            modificar_json_películas(películas.json())
            print("\nUsted añadio correctamente su pelicula!")
            comprobador = False
        if op == "2":
            return
        continue

def editar_película():
    menu_editor()
    time.sleep(0.2)
    pelicula = elegir_película_a_editar()
    películas = cargar_películas()
    for película in películas["films"]:
        if película["title"] == pelicula:
            print("\nDesea editar el director? [Director Actual: " + str(película["director"] + "] "))
            op = input("\n[Presione 1 para sí] [Cualquier otra tecla para no]: ")
            if op == "1":
                new_director = elegir_director()
                película["director"] = new_director
            print("\nDesea editar el genero? [Genero Actual: " + str(película["gender"] + "] "))
            op = input("\n[Presione 1 para sí] [Cualquier otra tecla para no]: ")
            if op == "1":
                new_gender = elegir_genero()
                película["gender"] = new_gender
            print("\nDesea editar la URL a la portada? [URL Actual: " + str(película["link_image"] + "] "))
            op = input("\n[Presione 1 para sí] [Cualquier otra tecla para no]: ")
            if op == "1":
                new_url = comprobar_url()
                película["link_image"] = new_url
            print("\nDesea editar la sinopsis? [Sinopsis Actual: " + str(película["synopsis"] + "] "))
            op = input("\n[Presione 1 para sí] [Cualquier otra tecla para no]: ")
            if op == "1":
                new_synopsis = input("Ingrese la nueva sinopsis: ")
                película["synopsis"] = new_synopsis
            print("\nDesea editar el año? [Año Actual: " + str(película["year"] + "] "))
            op = input("\n[Presione 1 para sí] [Cualquier otra tecla para no]: ")
            if op == "1":
                new_year = comprobar_año()
                película["year"] = new_year
            
def editar_comentario():
    usuarios = cargar_usuarios()
    for usuario in usuarios["users"]:
        if usuario["username"] == usuarioIN:
            print("\nQue comentario desea modificar?\n")
            i = 0
            for comentario in usuario["comments"]:
                print("[" + str(i) + "] " + comentario + " - " + str(usuario["comments"][comentario]))
                i = i + 1


def elegir_película_a_editar():
    print("\nA continuación se mostrarán las peliculas disponibles ...\n")
    print("[Recuerde que el genero y el director, solo se pueden elegir segun los ya cargados en el sistema.]\n")
    películas = cargar_películas()
    i = 0
    time.sleep(2)
    for película in películas["films"]:
        print ('[' + str(i) + '] ' + str(película["title"]))
        i = i + 1
        time.sleep(0.5)
    película = "vacío"
    while película == "vacío":
        opcion_película = input("\nQue pelicula desea editar? ")
        if opcion_película == '0':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '1':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '2':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '3':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '4':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '5':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '6':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '7':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '8':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '9':
            película = películas["films"][int(opcion_película)]["title"]
        elif opcion_película == '10':
            película = películas["films"][int(opcion_película)]["title"]
        else:
            print("\nError! Debe ingresar el numero que corresponda segun el genero que desea.")
    return película

def elegir_genero():
    menu_genero()
    generos = cargar_generos()
    print("A continuación se mostrarán los generos disponibles ...\n")
    time.sleep(2)
    i = 0
    for genero in generos["genders"]:
        print ('[' + str(i) + '] ' + str(genero["gender"]))
        time.sleep(0.5)
        i = i + 1
    genero = "vacío"
    while genero == "vacío":
        opcion_genero = input("\nIngrese el genero que desea: ")
        if opcion_genero == '0':
            genero = "Accion"
        elif opcion_genero == '1':
            genero = "Aventura"
        elif opcion_genero == '2':
            genero = "Ciencia Ficcion"
        elif opcion_genero == '3':
            genero = "Comedia"
        elif opcion_genero == '4':
            genero = "Drama"
        elif opcion_genero == '5':
            genero = "Fantasia"
        elif opcion_genero == '6':
            genero = "Suspenso"
        elif opcion_genero == '7':
            genero = "Terror"
        else:
            print("\nError! Debe ingresar el numero que corresponda segun el genero que desea.")
    return genero

def elegir_director():
    menu_director()
    directores = cargar_directores()
    print("A continuacion se mostrarán los directores disponibles ...\n")
    time.sleep(2)
    i = 0
    for director in directores["directors"]:
        print ('[' + str(i) + '] ' + str(director["director"]))
        time.sleep(0.5)
        i = i + 1
    director = "vacío"
    while director == "vacío":
        opcion_genero = input("\nIngrese el director que desea: ")
        if opcion_genero == '0':
            director = "Alfonso Cuaron"
        elif opcion_genero == '1':
            director = "Clint Eastwood"
        elif opcion_genero == '2':
            director = "Francis Ford Coppola"
        elif opcion_genero == '3':
            director = "Gore Verbinski"
        elif opcion_genero == '4':
            director = "Goro Taniguchi"
        elif opcion_genero == '5':
            director = "James Cameron"
        elif opcion_genero == '6':
            director = "Jeff Fowler"
        elif opcion_genero == '7':
            director = "Quentin Tarantino"
        elif opcion_genero == '8':
            director = "Robert Zemeckis"
        elif opcion_genero == '9':
            director = "Sam Raimi"
        elif opcion_genero == '10':
            director = "Steven Spielberg"
        elif opcion_genero == '11':
            director = "Tetsuro Kodama"
        elif opcion_genero == '12':
            director = "Tim Burton"
        elif opcion_genero == '13':
            director = "Woody Allen"
        else:
            print("Error! Debe ingresar el numero que corresponda segun el director que desea.")
        
    return director

def ultimas_diez():
    ultimas10 = requests.get('http://127.0.0.1:5000/films/last10')
    system("cls") #Limpia la terminal
    print('\nÚltimas 10 películas cargadas al sistema:',"\n")
    for película in ultimas10.json():
        time.sleep(1)
        print ('===============================')
        print ('Título: ', película["title"])
        print ('Director: ', película["director"])
        print ('Género: ', película["gender"])
        print ('Año: ', película["year"])
        print ('Sinopsis: ', película["synopsis"])
        print ('Imagen representativa: ', película["link_image"])
        print ('-------------------------------')
        print ('Comentarios:')
        print ('-------------------------------')
        buscar_comentarios(película["title"])
        print ('===============================\n')
    return

def buscar_comentarios(film_title):
    comentarios_película = requests.get('http://127.0.0.1:5000/films/'+film_title+'/comments')
    if str(comentarios_película) != '<Response [400]>':
        for comentario in comentarios_película.json():
            print ('Usuario: ', comentario["username"])
            print ('Comentario: ', comentario["comment"])
            print ('-------------------------------')
    else:
        print ("Sin comentarios")
        print ('-------------------------------')
        return

# _______________________________________________________________ Código _______________________________________________________________

bucle = 1 # Lo usaremos para luego romper el bucle
while bucle == 1:
    INopcion = menu_principal()
    if INopcion == '1':
        usuarioIN = iniciar_sesión()
        if usuarioIN == None:
            continue
        while True: 
            INopcion = menu_usuario(usuarioIN)
            if INopcion == '1':
                agregar_película()
                continue
            elif INopcion == '2':
                editar_película()
                print('[2] Editar Pelicula')
            elif INopcion == '3':
                print('[3] Agregar Comentario')
            elif INopcion == '4':
                editar_comentario()
                print('[4] Editar Comentario')
            elif INopcion == '5':
                INopcion = menu_buscar()
                if INopcion == '1':
                    buscar_película_nombre()
                    INopcion = input("\nIngrese algo para volver al menú: ")
                    continue
                elif INopcion == '2':
                    buscar_película_director()
                    INopcion = input("\nIngrese algo para volver al menú: ")
                    continue
                elif INopcion == '3':
                    buscar_película_género()
                    INopcion = input("\nIngrese algo para volver al menú: ")
                    continue
                elif INopcion == '0':
                    continue
            elif INopcion == '0':
                break
    elif INopcion == '2':
        ultimas_diez()
        INopcion = input("\nIngrese algo para volver al menú: ")
        continue
    elif INopcion == '3':
        nuevo_usuario = registrar_usuario()
        if nuevo_usuario == None:
            continue
        else:
            time.sleep(3)
            continue
    elif INopcion == '0':
        exit
    bucle = 0 # Para romper el bucle