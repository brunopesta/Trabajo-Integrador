import json
from tkinter import CENTER
import PySimpleGUI as sg
from resources.config import USUARIOS_ROOT


#---------------------------------------#
#       Funciones a la Estructura       #
#---------------------------------------#


def reset_estructura():
    """Crea la estructura en el usuarios.json desde cero"""
    with open(USUARIOS_ROOT, 'w', encoding='utf-8')as usuarios:
        estructura = {}
        json.dump(estructura, usuarios)


def write_data(data):
    """Escribe en usuarios.json"""
    with open(USUARIOS_ROOT, 'w', encoding='utf-8')as usuarios:
        json.dump(data, usuarios)


def read_data():
    """Devuelve toda la estructura almacenada en el usuarios.json"""
    with open(USUARIOS_ROOT, 'r', encoding='utf-8')as usuarios:
        data = json.load(usuarios)
    return data


#-----------------------------------#
#       Usuarios Modificaciones     #
#-----------------------------------#


def delet_usuario(usuario):
    """Borra la clave (Perfil/Usuario) pasada como parametro de la estructura de usuarios.json"""
    data = read_data()
    if usuario in data.keys():
        del data[usuario]
    else:
        [sg.Popup("Error, no se encontro el usuario"),
         sg.Button('Vovler', key='-user-')]
    write_data(data)


def change_usuario(usuario, edad, *generos):
    """Modifica los datos del usuario pasado como parametro invocation: change_usuario(name, age, genre)"""
    data = read_data()
    lista_generos = ['m', 'f', 'x']
    # encuentra la pos de generos que fue seleccionada y lo pasa como texto
    for b in range(len(generos)):
        if generos[b]:
            genero = lista_generos[b]

    if usuario in data.keys():
        data[usuario]['edad'] = int(edad)
        data[usuario]['genero'] = genero
        write_data(data)
        [sg.Popup(f'Datos de {usuario} modificados correctamente'), sg.Button(
            'Volver', key='-user-')]
    else:
        [sg.Popup("Error, no se encontro el usuario"),
         sg.Button('Volver', key='-user-')]


def append_usuario(usuario, edad, genero):
    """Agrega a la estructura usuarios.json el nuevo usuario aprobado invocation: append_usuario(name, age, genre) """
    datos = read_data()
    datos[usuario] = {"edad": edad, "genero": genero, "puntajes": {"facil": [0], "normal": [0],
                                                                   "dificil": [0], "experto": [0], "personalizado": [0]},  # Todos inicializados en cero
                      "config": {"rondas": 0, "tiempo": 0, "acierto": 0, "error": 0, "pistas": 0, "dificultad": "facil"}}
    write_data(datos)


def verify_usuario(usuario, edad, *generos):
    """Verifica que los datos ingresados para un nuevo usuario sean aprobados es decir: que se ingrese un nombre, edad, genero y que el nombre de usuario no este repetido invocation: verify_usuario(name, age, genre)"""
    lista_generos = ['m', 'f', 'x']
    # encuentra la pos de generos que fue seleccionada y lo pasa como texto
    for b in range(len(generos)):
        if generos[b]:
            genero = lista_generos[b]

    data = read_data()
    # Ordenamiento de Strings al standar (sin espacios antes o despues, mayuscula en la primera letra de cada palabra, todo lo demas en minuscula)
    usuario = usuario.strip().lower().title()
    if (usuario != '') and (usuario not in data.keys()):  # Validacion de nombre
        # aprobacion de usuario para cargarlo a  usuario.json (CUIDADO QUE ESTE EN USUARIO.JSON NO SIGNIFICA QUE ESTE EN PUNTAJE)
        append_usuario(usuario, int(edad), genero)
        return '-user-'
    else:
        [sg.Popup('El nombre no es valido o ya existe'),
         sg.Button('OK', key='-new_user-')]


#-----------------------#
#        Layouts        #
#-----------------------#


def string_usuarios():
    """Devuelve una string de todos los usuarios"""
    data = read_data()
    usuarios = list(data.keys())
    usuarios.sort()
    string_users = ('\n'.join(usuarios))
    return string_users

def informacion_usuario(user):
    """"Retorna la edad y el genero del usuario"""
    data = read_data()
    age = data[user]['edad']
    gender = data[user]['genero']
    if gender == 'm':
        gender = 1
    elif gender == 'f':
        gender = 2
    else: # gender == 'x'
        gender = 3
    return age, gender

def lista_usuarios():
    """Retorna una lista con todos los usuarios"""
    data = read_data()
    usuarios = list(data.keys())
    return usuarios


def nuevo_usuario_layout():
    """Lasyout de un nuevo Usuario"""
    layout = [
        [sg.Text('Creacion de Nuevo Usuario', justification=CENTER)],
        [sg.Text('Ingrese su nombre : '), sg.Input(
            do_not_clear=True, enable_events=True, key='-name-')],
        [sg.Text('Ingrese su edad : '), sg.Slider(orientation='h',
                                                  key='-age-', range=(1, 100), size=(50, 10), default_value=int)],
        [sg.Text('Ingrese su genero : '), sg.Radio('Masculino', "Genero", default=True, size=(10, 1), k='-m-'), sg.Radio('Femenino',
                                                                                                                         "Genero", default=False, size=(10, 1), k='-f-'), sg.Radio('X', "Genero", default=False, size=(10, 1), k='-x-')],
        [sg.Button('Confirmar', key='-add-'),
         sg.Button('Cancelar', key='-user-')]
    ]
    return layout


def eliminar_usuario_layout():
    """Layout para seleccionar un usuario a eliminar"""
    layout = [
        [sg.Text('Eliminacion de Usuarios', size=(50, 2), justification=CENTER)],
        [sg.Listbox(values=lista_usuarios(), size=(20, 12),
                    key='-delet_listbox-', enable_events=True)],
        [sg.Button("Borrar", key='-delet-')],
        [sg.Button('Volver', key='-user-')]
    ]
    return layout


def modificar_usuario_layout():
    """Layout para seleccionar un usuario a modificar"""
    layout = [
        [sg.Text('Modificacion de Usuarios', size=(50, 2), justification=CENTER)],
        [sg.Listbox(values=lista_usuarios(), size=(20, 12),
                    key='-THEME LISTBOX-', enable_events=True)],
        [sg.Button("Modificar", key='-mod-')],
        [sg.Button('Volver', key='-user-')]
    ]
    return layout




def change_layout(user):
    """Layout para cambiar datos de un usuario"""
    edad,genero = informacion_usuario(user) # -> genero (1,2,3) con una expresion booleana dependiendo que entero es, son seteados los sg.Radio
    layout = [
        [sg.Text('Ingrese su nueva edad : '), sg.Slider(orientation='h', key='-age-', range=(1, 100),
                                                        size=(50, 10), default_value=edad), sg.Button('Volver', key='-modify_user-', size=(5, 2))],
        [sg.Text('Ingrese su nuevo genero : '), sg.Radio('Masculino', "RadioDemo", default= (genero==1), size=(10, 1), k='-m-'), sg.Radio('Femenino',"RadioDemo", default=(genero== 2), size=(10, 1), k='-f-'), sg.Radio('X', "RadioDemo", default=(genero==3), size=(10, 1), k='-x-')],
        [sg.Button('Confirmar', key='-change-')]
    ]
    return layout


def usuarios_layout():
    """Layout para la creacion de un nuevo usuario"""
    layout = [[sg.Text('Menu de Usuarios', size=(50, 2), justification=CENTER, auto_size_text=True), sg.Button('Menu', key='-menu-', auto_size_button=True)],
              [sg.Button('Nuevo Usuario', key='-new_user-', auto_size_button=True), sg.Button('Modificar Usuario',
                                                                                              auto_size_button=True, key='-modify_user-'), sg.Button('Eliminar Usuario', key='-delet_user-', auto_size_button=True)],
              [sg.Text('Perfiles Existentes')],
              [sg.Multiline(default_text=string_usuarios(),
                            key='ml', size=(16, 13), auto_size_text=True)],
              ]
    return layout

