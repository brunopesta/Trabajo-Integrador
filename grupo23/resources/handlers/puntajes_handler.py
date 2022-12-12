import PySimpleGUI as sg
from resources.screens.puntajes import puntajes_layout, color_boton, actualizar_ventana_prom, actualizar_ventana_pun


def handler_puntaje():
    """Funcion que maneja todos los eventos dentro de los layouts que corresponda al campo de puntaje, para facilitar lectura y mantener un codigo mas limpio"""
    dificultades = ['-easy-','-normal-','-hard-','-expert-', '-custom-']
    mostrador = ['-pun-','-prom-']
    ordenacion_forma = ['-ascendente-','-descendente-']
    ordenacion_por = ['-puntos-','-nombre-']
    window = sg.Window("Image Viewer", puntajes_layout(), size=(500,500)).Finalize()
    ml_pj = window["dat"]
    ml_pj.Update(disabled=True)
    lvl = '-custom-'
    mostrado = '-pun-'
    ordenar_forma = '-descendente-'
    ordenar_por = '-puntos-'
    while True:
        event, values = window.read()
        
        if event == '-menu-' or event == sg.WIN_CLOSED: # salida a menu
            window.close()
            break
        
        elif event in mostrador:
            lista_eventos = mostrador
            mostrado = event

        elif event in dificultades:
            lista_eventos = dificultades
            lvl = event

        elif event in ordenacion_forma:
            lista_eventos = ordenacion_forma
            ordenar_forma = event

        elif event in ordenacion_por:
            lista_eventos = ordenacion_por
            ordenar_por = event

        buttons = [window[evento] for evento in lista_eventos]
        choosen = window[event]
        color_boton(choosen,buttons)
        if mostrado == '-prom-':
            actualizar_ventana_prom(lvl, window, ordenar_forma)
        else: #mostrado == '-pun-':
            actualizar_ventana_pun(lvl,window, ordenar_forma, ordenar_por)
        window.refresh()

        