import PySimpleGUI as sg
from resources.screens.usuarios import delet_usuario, usuarios_layout, nuevo_usuario_layout, verify_usuario, modificar_usuario_layout, change_layout, change_usuario, eliminar_usuario_layout, delet_usuario

def handler_usuario():
    """Funcion que maneja todos los eventos dentro de los layouts que corresponda al campo de usuario, para facilitar lectura y mantener un codigo mas limpio"""
    window = sg.Window("Image Viewer", usuarios_layout()).Finalize()
    ml_obj = window["ml"]
    ml_obj.Update(disabled=True)
    while True:
        event, values = window.read()
        if event == '-new_user-':  # Layout para carga de nuevos usuarios
                window.close()
                window = sg.Window("Image Viewer", nuevo_usuario_layout())
        try:
            # Limitador de rango para la introduccion de caracteres en el nombre
            if len(values['-name-']) > 15:
                window.Element('-name-').Update(values['-name-'][:-1])
        except:
            pass

        if event == '-add-':  # Validacion de datos para un nuevo usuario y su creacion en usuarios.json
            llave = verify_usuario(
                values['-name-'], values['-age-'], values['-m-'], values['-f-'], values['-x-'])
            if llave == '-user-':
                window.close()
                [sg.Popup('Usuario Cargado Correctamente'),
                 sg.Button('OK', key='-prueba-')]
                window = sg.Window(
                    "Image Viewer", usuarios_layout()).Finalize()
                multiline_obj = window["ml"]
                multiline_obj.Update(disabled=True)
            
        if event == '-user-':
            window.close()
            window = sg.Window("Image Viewer", usuarios_layout()).Finalize()
            ml_obj = window["ml"]
            ml_obj.Update(disabled=True)
    
         #___Apartado Modificacion de Usuarios___#
        if event == '-modify_user-':  # Layout para cambiar datos de usuarios
            window.close()
            window = sg.Window("Image Viewer", modificar_usuario_layout())

        if event == '-mod-':  # Modificacion de usuarios
            try:
                aux_values = values['-THEME LISTBOX-'][0]
                window.close()
                window = sg.Window("Image Viewer", change_layout(aux_values))
            except:
                [sg.Popup('No hay un usuario seleccionado para modificar'),
                 sg.Button('OK', key='-modify_user-')]

        if event == '-change-':  # Confirmacion de cambios en un usuario y su guardado en usuarios.json
            change_usuario(
                aux_values, values['-age-'], values['-m-'], values['-f-'], values['-x-'])
            window.close()
            window = sg.Window("Image Viewer", modificar_usuario_layout())

        #___Apartado Eliminacion___#

        if event == '-delet_user-':  # Layout de eliminar Usuarios
            window.close()
            window = sg.Window("Image Viewer", eliminar_usuario_layout())

        if event == '-delet-':  # Evento para eliminar un usuario
            try:
                aux_values = values['-delet_listbox-'][0]
                delet_usuario(aux_values)
            except:
                [sg.Popup('No hay un usuario seleccionado para eliminar'),
                 sg.Button('OK', key='-delet_user-')]
            window.close()
            window = sg.Window("Image Viewer", eliminar_usuario_layout())

        if event == '-menu-' or event == sg.WIN_CLOSED: # salida a menu
            window.close()
            break
