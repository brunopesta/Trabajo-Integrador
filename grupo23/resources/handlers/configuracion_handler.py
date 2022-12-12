import PySimpleGUI as sg
from resources.screens.configuracion import configuracion_layout, lectura, save_dificultad, set_dificultad

def handler_config(values, usuario):
    """Funcion que maneja todos los eventos dentro de los layouts que corresponda al campo de configuracion, para facilitar lectura y mantener un codigo mas limpio"""
    window = sg.Window("Image Viewer", configuracion_layout(values['-usuario-']))
    lvl = lectura(usuario)['dificultad']
    dificultades = ['facil', 'normal','dificil', 'experto', 'personalizado']
    while True:
                event, values = window.read()
                if event == "-menu-" or event == sg.WIN_CLOSED:         # salida
                    window.close()
                    break

                elif event == '-save-':  # guardado
                    save_dificultad(usuario, lvl, values)
                    [sg.Popup('Configuracion Guardada'),sg.Button('OK', key='-menu-')]
                    window.close()
                    break

                elif event in dificultades:  # evento botones de dificultad, sliders y colores de botones
                    lvl = event
                    set_dificultad(event, usuario, window)
                    window.refresh()