
from time import time
from tkinter import CENTER, LEFT
import PySimpleGUI as sg
from resources.config import DATASET_ROOT, IMAGES_ROOT
import os
import pandas as pd
import random

#-------------------#
#       Logica      #
#-------------------#



def comparar_respuestas(jugador, window, respuesta_correcta, criterio_dificultad,listado_de_rondas,ronda_actual):
    """Funcion que compara la opcion elegida con la correcta, acutaliza puntaje,  rondas y pantalla. """
    if jugador.get_respuesta_actual() != '':                                                    
        if jugador.get_respuesta_actual() == respuesta_correcta:             
            jugador.incrementar_puntaje_actual(criterio_dificultad['acierto'])                  
            window['-RESPUESTAS_POR_RONDAS-'].update('\n'.join(lista_rondas(jugador, ronda_actual,True,listado_de_rondas)))
        else:                                                                                  
            jugador.decrementar_puntaje_actual(criterio_dificultad['error'])                   
            window['-RESPUESTAS_POR_RONDAS-'].update('\n'.join(lista_rondas(jugador, ronda_actual,False, listado_de_rondas)))
        window['-puntaje-'].update(f'PUNTAJE ACTUAL: {int(jugador.get_puntaje_actual())}')              
        window.refresh() 

def tiempo_inicial(jugador):
    """ Recibe el jugador activo de la sesion, y devuelve el tiempo inicial en segundos correspondiente a la 
    configuracion del seleccionada por dicho jugador"""
    dificultad = jugador.get_valores()["config"]["dificultad"]
    if dificultad == 'personalizado':
        return int(jugador.get_valores()["config"]["tiempo"])
    else:
        return jugador.get_config_default()[dificultad]["tiempo"]


def conversion_timer(tiempo):
    """ Convierte una cantidad X de segundos, recibida por parametro en un formato de dos digitos para minutos
    y dos digitos para segundos(00:00), devolviendo dicho formato de timer en un String"""
    unidad_minutos = tiempo/60
    min = int(tiempo/60)
    sec = int(tiempo % 60)
    return '{:02d}:{:02d}'.format(min, sec)

def get_total_rondas(jugador, dificultad):
    if dificultad == "personalizado":
        return int(jugador.get_valores()["config"]["rondas"])
    else:
        return int(jugador.get_config_default()[dificultad]["rondas"])

def lista_rondas(jugador, ronda_actual=1, correcta=True, listado_de_rondas=None, pasar=False, timeout=False):
    """ Recibe el jugador actual de la sesion, de acuerdo a la dificultad de juego seleccionada, si el juego recien inicia,
    crea una lista por list comprehention de strings vacios de la longitud igual a la cantidad de rondas de la dificultad (que luego se usara
    para actualizar si la respuesta de esa ronda fue correcta o incorrecta. Luego retorna una lista por de tuplas con el numero de ronda
    en pos 0 y la respuesta(o string vacio) en pos 1"""
    dificultad = jugador.get_valores()['config']['dificultad']
    if ronda_actual == 1:
        if dificultad == 'personalizado':
            listado_de_rondas = ["" for elem in range(1, get_total_rondas(jugador, dificultad)+1)]
            return [f"{ronda[0]+1}. {ronda[1]}" for ronda in enumerate(listado_de_rondas)]
        else:
            listado_de_rondas = ["" for elem in range(1, get_total_rondas(jugador, dificultad )+1)]
            return [f"{ronda[0]+1}. {ronda[1]}" for ronda in enumerate(listado_de_rondas)]
    elif pasar:
        listado_de_rondas[ronda_actual-2] = f"{listado_de_rondas[ronda_actual-2]} Passsss!"
    elif timeout:
        listado_de_rondas[ronda_actual-2] = f"{listado_de_rondas[ronda_actual-2]} Timeout"
    else:
        if correcta:
                listado_de_rondas[ronda_actual-2] = f"{listado_de_rondas[ronda_actual-2]} Correcta!"
        else:
                listado_de_rondas[ronda_actual-2] = f"{listado_de_rondas[ronda_actual-2]} Error! :("
    return listado_de_rondas


def seleccion_dataset():
    """Genera un numero aleatorio entre 1 y 3, y asigna de forma aleatoria de acuerdo a dicho numero, el dataset
    del cual se va a extraer la informacion para dicha ronda. Como resultado de la funcion, devuelve: la categoria
    del dataset, el encabezado y los datos por separado"""
    opcion = random.randint(1, 3)
    match opcion:
        case 1:
            cat = "LAGOS"
            data_frame = pd.read_csv(os.path.join(DATASET_ROOT, 'lagos_filtrado_pandas.csv'), sep=',', encoding="utf-8")

        case 2:
            cat = "JUGADORES FIFA"
            data_frame = pd.read_csv(os.path.join(DATASET_ROOT, 'fifa_filtrado_pandas.csv'), sep=',', encoding="utf-8")
        
        case 3:
            cat = "TEMAS MUSICALES"
            data_frame = pd.read_csv(os.path.join(DATASET_ROOT, 'spotify_filtrado_pandas.csv'), sep=',', encoding="utf-8")
        
    return cat, list(data_frame.columns), data_frame


def opciones_botones(data_frame, seleccionada):
    """"Recibe el dataset con el cual trabajar y el dato en la columna "nombre" de la carta seleccionada 
    previamente, es decir, el dato a adivinar. Filtra el dataset para quedarse con los nombres de todas las
    opciones menos la seleccionada, e incorpora a una lista, la opcion seleccionada y  otras 4 opciones de 
    nombres aleatoriamente elegidas que seran devueltas por la funcion y posteriormente utilizadas como
    opciones de respuesta para los botones"
    """
    lista_nombres_opciones = list(filter(lambda nombre: nombre != seleccionada, data_frame.iloc[:,6]))
    
    lista_cartas_seleccionadas = [seleccionada]
    while len(lista_cartas_seleccionadas) < 5:
        nom = lista_nombres_opciones[random.randint(0, len(lista_nombres_opciones)-1)]
        if nom not in lista_cartas_seleccionadas:
            lista_cartas_seleccionadas.append(nom)

    return lista_cartas_seleccionadas


def descripciones(encabezado, carta, jugador):
    """Recibe el encabezado del dataset, la carta seleccionada para la ronda y el jugador activo de la sesion.
    De acuerdo a la dificultad activamente seleccionada para la partida, crea y devuelve un string con la 
    cantidad de pistas correspondientes al nivel de dificultad, que seran mostradas de la carta seleccionada
    Notar: el chequeo de campo vacio en las columnas [2] y [3] es debido a que el dataset de lagos puede 
    contener algunas cartas con informacion faltante.
    """
    if jugador.get_valores()['config']['dificultad'] in jugador.get_config_default().keys():
        pistas = jugador.get_config_default()[jugador.get_valores()[
            'config']['dificultad']]['pistas']
    else:
        pistas = jugador.get_valores()['config']['pistas']

    
    
    match pistas:
        case 5:
            aux = f"""
                {encabezado[1]}: {carta.iloc[1]}
                {encabezado[2]}: {carta.iloc[2]}
                {encabezado[3]}: {carta.iloc[3]}
                {encabezado[4]}: {carta.iloc[4]}
                {encabezado[5]}: {carta.iloc[5]}
                {encabezado[6]}:
            """
        case 4:
            aux = f"""
                {encabezado[1]}: {carta.iloc[1]}
                {encabezado[2]}: {carta.iloc[2]}
                {encabezado[3]}: {carta.iloc[3]}
                {encabezado[4]}: {carta.iloc[4]}
                {encabezado[6]}:
            """
        case 3:
            aux = f"""
                {encabezado[1]}: {carta.iloc[1]}
                {encabezado[2]}: {carta.iloc[2]}
                {encabezado[3]}: {carta.iloc[3]} 
                {encabezado[6]}:
            """
        case 2:
            aux = f"""
                {encabezado[1]}: {carta.iloc[1]}
                {encabezado[2]}: {carta.iloc[2]}
                {encabezado[6]}:
            """

    
    return aux


def mezclar_opciones(nombres):
    """ Recibe la lista de nombres que seran las opciones a mostrar. Inserta los nombres en en una nueva lista 
    con orden aleatorio de los nombres hasta completar las 5 posiciones necesarias para luego mostrar en los
    botones de opciones. Retorna la lista de nombres mezclada."""
    mezclados = []
    while len(mezclados) < 5:
        carta_seleccionada = nombres[random.randint(0, 4)]
        if carta_seleccionada not in mezclados:
            mezclados.append(carta_seleccionada)
    return mezclados


def color_boton(elegido, botones):
    """ Cambia el color del boton que se encuentra seleccionado al momento que clickean una opcion de respuesta
    y actualiza el color del resto de los botones si es que habia otro seleccionado previamente."""
    for bt in botones:
        if bt == elegido:
            bt.update(button_color='#273E5B')
        else:
            bt.update(button_color='#516F95')


def imagen_a_mostrar(cat):
    """ Recibe la categoria con la que esta jugando la ronda, genera un numero aleatorio entre 1 y la cantidad
    de imagenes disponibles para las categorias, de forma aleatoria, para formar la ruta de acceso a una imagen
    elegida de forma aleatoria a mostrar en la pantalla jugar. Se devuelve la ruta completa a dicha imagen que
    sera el "source" del sg.Image."""
    num = str(random.randint(1, 3))
    match cat:
        case "LAGOS":
            ruta_completa = os.path.join(IMAGES_ROOT, f'lagos{num}.png')
        case "JUGADORES FIFA":
            ruta_completa = os.path.join(IMAGES_ROOT, f'fifa{num}.png')
        case "TEMAS MUSICALES":
            ruta_completa = os.path.join(IMAGES_ROOT, f'spotify{num}.png')
    return ruta_completa

def mostrar_contenido_jugar(window):
    """ habilita la visualizacion del contenido de la pantalla jugar cuando se da click al boton que incia el timer"""
    window["-opcion1-"].Update(visible=True)
    window["-opcion2-"].Update(visible=True)
    window["-opcion3-"].Update(visible=True)
    window["-opcion4-"].Update(visible=True)
    window["-opcion5-"].Update(visible=True)
    window["-ok-"].Update(visible=True)
    window["-pass-"].Update(visible=True)
    window["-pistas-"].Update(visible=True)

def cambiar_tarjeta(window, jugador):
    """ Recibe la pantalla y el jugador actual de la partida, actualiza los datos a mostrar con una nueva carta para adivinar y lo vuelca al 
    layout actual"""
    cat, encabezado, data_frame = seleccion_dataset()
    carta_correcta = data_frame.iloc[random.randint(1, len(data_frame.index)-1)]
    respuesta_correcta = carta_correcta.iloc[6]
    botones_opciones = mezclar_opciones(opciones_botones(data_frame, respuesta_correcta))
    window["-Encabezado-"].Update(f'Categoria: {cat.title()}  -  Dificultad: {jugador.get_valores()["config"]["dificultad"].title()}  - Usuario: {jugador.get_nombre()}')
    window["-imagen-"].Update(source=imagen_a_mostrar(cat))
    window["-COUNTDOWN-"].Update(conversion_timer(tiempo_inicial(jugador)))
    window["-opcion1-"].Update(botones_opciones[0], button_color='#516F95')
    window["-opcion2-"].Update(botones_opciones[1], button_color='#516F95')
    window["-opcion3-"].Update(botones_opciones[2], button_color='#516F95')
    window["-opcion4-"].Update(botones_opciones[3], button_color='#516F95')
    window["-opcion5-"].Update(botones_opciones[4], button_color='#516F95')
    window["-ok-"].Update(disabled=True)
    window["-pistas-"].Update(descripciones(encabezado, carta_correcta, jugador))

    return respuesta_correcta


#-------------------#
#       layout      #
#-------------------#

def jugar_layout(jugador):
    """Funcion que retorna el layout del juego y la respuesta correcta, ya que es desde donde se implementa el mezclado de opciones"""
    cat, encabezado, data_frame = seleccion_dataset()
    carta_correcta = data_frame.iloc[random.randint(1, len(data_frame.index)-1)]
    respuesta_correcta = carta_correcta.iloc[6]
    botones_opciones = mezclar_opciones(opciones_botones(data_frame, respuesta_correcta))
    listado_de_rondas = lista_rondas(jugador)
    x = 30
    y = 1
    layout = [[sg.Button("Comenzar", key="-START-"),            sg.Button('Abandonar el Juego', key='-exit-')],
              [sg.Text(f'Categoria: {cat.title()}  -  Dificultad: {jugador.get_valores()["config"]["dificultad"].title()}  - Usuario: {jugador.get_nombre()}', size=(50, 2), justification=CENTER, key="-Encabezado-")],
              [sg.Text(f'PUNTAJE ACTUAL: {jugador.get_puntaje_actual()}', size=(50, 2), justification=CENTER, key='-puntaje-')],
              [sg.Text("--:--", size=(20, 3), auto_size_text=15, border_width=3, justification=CENTER, background_color='#273E5B', key="-COUNTDOWN-"),
               sg.Image(source=imagen_a_mostrar(cat), key="-imagen-"), sg.Text('\n'.join(listado_de_rondas), background_color='#173E5B', expand_y=True, key="-RESPUESTAS_POR_RONDAS-")],
              [sg.Text(descripciones(encabezado, carta_correcta, jugador),justification=LEFT,visible=False, border_width=3, key="-pistas-")],
              [[sg.Button(botones_opciones[0], size=(x,y), button_color='#516F95',visible=False, key='-opcion1-')],
               [sg.Button(botones_opciones[1], size=(x,y), button_color='#516F95',visible=False, key='-opcion2-')],
               [sg.Button(botones_opciones[2], size=(x,y), button_color='#516F95',visible=False, key='-opcion3-')],
               [sg.Button(botones_opciones[3], size=(x,y), button_color='#516F95',visible=False, key='-opcion4-')],
               [sg.Button(botones_opciones[4], size=(x,y), button_color='#516F95',visible=False, key='-opcion5-'), sg.Button('Ok', size=(10,1),disabled=True, visible=False, key='-ok-'), sg.Button('Pasar >', size=(10,1),visible=False,  key="-pass-")],
               ]
              ]
    return layout, respuesta_correcta, listado_de_rondas 
