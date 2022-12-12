from tkinter import CENTER, LEFT
import PySimpleGUI as sg
from resources.screens.jugar import color_boton
from resources.screens.usuarios import read_data, write_data




#-----------------------------------#
#       Usuarios Modificaciones     #
#-----------------------------------#

def promedio_ordenados(dificultad,ordenar_forma):
    """Retorna un String con todos los usuarios ordenados por promedio y una dificultad especifica"""
    usuarios = read_data()
    lista = [[round(sum(usuarios[usu]['puntajes'][dificultad])/len(usuarios[usu]['puntajes'][dificultad]),2), usu] for usu in usuarios] # -> structure: [  [[p1, p2,pn], usuario1], ... [[p1,...pn], usuarioN] ]
                                                                                                                                               
    lista.sort(reverse=ordenar_forma)  # -> sort structure by average score, and is sort in a descending order 
 
    tabla = "Posicion   |    Nombre:Promedio  \n"
    tabla+='--------------------------------------------------\n'                             
    for usuario in enumerate(lista[0:20]):
        tabla += f'{str(usuario[0]+1)+"°":<14} {"|":<3} {""+str(usuario[1][1])+":"+str(usuario[1][0]):<20}\n'
        tabla+='--------------------------------------------------\n'
    return tabla.strip()

def tomar_segundo(elemento):
    return elemento[1]

def puntajes_ordenados(dificultad, ordenar_forma, ordenar_por):
    """Retorna un String con todos los usuarios ordenados por puntaje y una dificultad especifica"""
    usuarios = read_data()
    lista = [[max(usuarios[usu]['puntajes'][dificultad]), usu] for usu in usuarios]
    if ordenar_por == '-nombre-':
        ordenada = sorted(lista, reverse=ordenar_forma, key=tomar_segundo)
    else:
        ordenada = sorted(lista, reverse=ordenar_forma)
    
    # Cabecera de la tabla puntajes
    tabla = "Posicion   |     Nombre:Puntaje  (Tokens) \n"
    tabla+='--------------------------------------------------\n'                             
    for usuario in enumerate(ordenada[0:20]):
        tabla += f'{str(usuario[0]+1)+"°":<14} {"|":<3} {""+str(usuario[1][1])+":"+str(usuario[1][0]):<20}{"("+str(int(usuario[1][0] / 3))+" Tokens)" :>5}\n'  
        tabla+='--------------------------------------------------\n'
    return tabla.strip()


def actualizar_ventana_prom(dificultad, window, orden):
    """Actualiza la ventana de puntajes con su dificultad correspondiente"""
    eventos = {'-easy-':'facil', '-normal-':'normal','-hard-':'dificil','-expert-':'experto','-custom-':'personalizado'}
    window['dat'].update(promedio_ordenados(eventos[dificultad], orden=='-descendente-'))
    window['texto'].update('Top 20 de promedios')
    window['-puntos-'].Update(visible=False)
    window['-nombre-'].Update(visible=False)


def actualizar_ventana_pun(dificultad, window, orden, orden_puntajes):
    """Actualiza la ventana de puntajes con su dificultad correspondiente"""
    eventos = {'-easy-':'facil', '-normal-':'normal','-hard-':'dificil','-expert-':'experto','-custom-':'personalizado'}
    window['dat'].update(puntajes_ordenados(eventos[dificultad], orden=='-descendente-', orden_puntajes))
    window['texto'].update('Top 20 de puntajes')
    window['-puntos-'].Update(visible=True)
    window['-nombre-'].Update(visible=True)


def actualizar_puntajes_json(jugador, dificultad):
    archivo_json = read_data()
    archivo_json[jugador.get_nombre()]['puntajes'][dificultad].append(int(jugador.get_puntaje_actual()))
    write_data(archivo_json)
    

#-----------------------------------#
#       Puntaje  Layouts            #
#-----------------------------------#

def puntajes_layout():
    layout = [
        [sg.Text('Menu de Puntajes', size=(50, 2), justification=CENTER,auto_size_text=True), sg.Button('Menu', key='-menu-', auto_size_button=True)],
        
        [sg.Button('Puntajes', key='-pun-', button_color=('#273E5B')), sg.Button('Promedio', key='-prom-', button_color=('#516F95'))],
        [sg.Button('Puntos', key='-puntos-', button_color=('#273E5B'), visible=True), sg.Button('Nombre', key='-nombre-',button_color=('#516F95'),visible=True)],
        
        [sg.Button('Facil', key='-easy-', button_color=('#516F95')), sg.Button('Normal', key='-normal-', button_color=('#516F95')), sg.Button('Dificil', key='-hard-',
                                          button_color=('#516F95')), sg.Button('Experto', key='-expert-', button_color=('#516F95'),), sg.Button('Personalizado', key='-custom-', button_color=('#273E5B'))],
        [sg.Button('Ascendente', key='-ascendente-', button_color=('#516F95')), sg.Button('Descendente', key='-descendente-', button_color=('#273E5B'))],
        [[sg.Text('Top 20 de puntajes',key='texto')], sg.Multiline(default_text=puntajes_ordenados('personalizado', True, '-puntos-'), key='dat', size=(40, 50), auto_size_text=True, justification=LEFT)],
    ]
    return layout

