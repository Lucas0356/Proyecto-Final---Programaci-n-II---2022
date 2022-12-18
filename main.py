from os import system #La usaremos para limpiar la terminal con system("cls")
import requests, json, time

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
        print('          Menu buscar'         )
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
            print ('-------------------------------')
            print ('Título: ', película["title"])
            print ('Director: ', película["director"])
            print ('Género: ', película["gender"])
            print ('Año: ', película["year"])
            print ('Sinopsis: ', película["synopsis"])
            print ('Imagen representativa: ', película["link_image"])
            print ('-------------------------------\n')
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
            print ('-------------------------------')
            print ('Título: ', película["title"])
            print ('Director: ', película["director"])
            print ('Género: ', película["gender"])
            print ('Año: ', película["year"])
            print ('Sinopsis: ', película["synopsis"])
            print ('Imagen representativa: ', película["link_image"])
            print ('-------------------------------\n')
        return
    else:
        print ('\nAún no hay películas publicadas de', director)
        return

def agregar_película():
    comprobador = True
    while comprobador:
        genero = elegir_genero()
        director = elegir_director()
        title_movie = input("Ingrese el titulo de la pelicula que desea añadir: ")
        year_movie = input("Ingrese el año de la pelicula que desea añadir: ")
        synopsis_movie = input("Ingrese la sinopsis de la pelicula que desea añadir: ")
        img_movie = input("Ingrese la URL a la portada de la pelicula que desea añadir: ")
        new_movie ={
            "title": title_movie,
            "year": year_movie,
            "director": director,
            "gender": genero,
            "synopsis": synopsis_movie,
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
    
    return director


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
                time.sleep(0.2)
                print('\nUsted escogió, "Agregar Pelicula". Recuerde que los generos y directores, solo pueden ser escogidos entre los')
                print('ya cargados en el sistema.')
                agregar_película()
                continue
            elif INopcion == '2':
                print('[2] Editar Pelicula')
            elif INopcion == '3':
                print('[3] Agregar Comentario')
            elif INopcion == '4':
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
                    print('opcion3')
                elif INopcion == '0':
                    continue
            elif INopcion == '0':
                break
    elif INopcion == '2':
        ultimas10 = requests.get('http://127.0.0.1:5000/films/last10')
        print(ultimas10.json())
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