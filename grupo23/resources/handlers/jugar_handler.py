from time import time
import PySimpleGUI as sg
from resources.jugador import Jugador
from resources.estado_partida import EstadoPartida
from resources.screens.configuracion import lectura_completa
from resources.screens.puntajes import actualizar_puntajes_json
from resources.screens.jugar import jugar_layout, tiempo_inicial, get_total_rondas,mostrar_contenido_jugar, conversion_timer, cambiar_tarjeta,lista_rondas,comparar_respuestas, color_boton
from resources.estadistica.estadistica import transferir_data


def handler_jugar(usuario):
    """Funcion que maneja todos los eventos dentro de los layouts que corresponda al campo de jugar, para facilitar lectura y mantener un codigo mas limpio"""
    jugador = Jugador(usuario, lectura_completa(usuario))                                                           # 
    layout, respuesta_correcta, listado_de_rondas = jugar_layout(jugador)
                                                                                                                    #
    dificultad = jugador.get_valores()['config']['dificultad']                                                      #
    if dificultad == 'personalizado':                                                                               # Lectura de datos para empezar el juego
        criterio_dificultad = jugador.get_valores()["config"]                                                       #
    else:                                                                                                           #
        criterio_dificultad = jugador.get_config_default()[dificultad]                                              #
    
    window = sg.Window("Jugando", layout)                                                                           #
    tiempo_ronda = tiempo_inicial(jugador)                                                                          # Inicio del juego
    restantes = None                                                                                                #
    
    estado_partida = EstadoPartida(get_total_rondas(jugador, dificultad), dificultad )
    estado_partida.set_log(time(), 'inicio_partida', jugador.get_nombre(),"-","-","-")  
    while True:  
        if (estado_partida.get_ronda_actual() <= estado_partida.get_total_rondas()):
            event, values = window.read(timeout=250)

            
            if not estado_partida.get_timer_iniciado():                                                        
                if event == "-START-":       
                    mostrar_contenido_jugar(window)                                 
                    window['-START-'].Update(disabled=True)                         
                    window['-COUNTDOWN-'].Update(conversion_timer(tiempo_ronda))    
                    hora_inicial = time()                                           
                    estado_partida.set_timer_iniciado()                                                 
            else:                                                                   
                if hora_inicial:                                                    
                    transcurridos = int(time() - hora_inicial)                      
                    restantes = tiempo_ronda - transcurridos                        
                    if restantes <= 0:           
                        estado_partida.set_log(time(), 'intento', jugador.get_nombre(),'timeout','-',respuesta_correcta)                                                                         
                        window['-COUNTDOWN-'].Update('00:00')  
                        estado_partida.incrementar_ronda_actual()                                                                                                        #
                        window['-RESPUESTAS_POR_RONDAS-'].update('\n'.join(lista_rondas(jugador, estado_partida.get_ronda_actual(),True, listado_de_rondas, False, True)))  #       
                        respuesta_correcta = cambiar_tarjeta(window, jugador)
                        hora_inicial = time() 
                        window.refresh()
                    else:                                                           
                        window['-COUNTDOWN-'].Update(conversion_timer(restantes)) 

            
            if event == '-opcion1-' or event == '-opcion2-' or event == '-opcion3-' or event == '-opcion4-' or event == '-opcion5-':                                           
                window["-ok-"].Update(disabled=False)
                jugador.set_respuesta_actual(window[event].get_text())
                botones = [window['-opcion1-'], window['-opcion2-'],window['-opcion3-'], window['-opcion4-'], window['-opcion5-']]
                color_boton(window[event] , botones)                    
            
            
            if event == '-ok-':                                                                                                         
                estado_partida.incrementar_ronda_actual()
                info_estado = 'ok' if respuesta_correcta == jugador.get_respuesta_actual() else 'error'
                estado_partida.set_log(time(), 'intento', jugador.get_nombre(),info_estado,jugador.get_respuesta_actual(),respuesta_correcta)                                                                                                       
                comparar_respuestas(jugador, window, respuesta_correcta, criterio_dificultad,listado_de_rondas,estado_partida.get_ronda_actual())                                                                                                                                                                                                                                                         # volcar datos al csv estadisticos del acierto u error
                respuesta_correcta = cambiar_tarjeta(window, jugador)
                hora_inicial = time() 
                window.refresh()  
                                                                           
                                                                                                                                                                                                                                                  
            if event == '-pass-':                                                                                                       
                estado_partida.incrementar_ronda_actual()
                info_estado = 'ok' if respuesta_correcta == jugador.get_respuesta_actual() else 'error'
                estado_partida.set_log(time(), 'intento', jugador.get_nombre(),info_estado,jugador.get_respuesta_actual(),respuesta_correcta)                                                                                                        
                window['-RESPUESTAS_POR_RONDAS-'].update('\n'.join(lista_rondas(jugador, estado_partida.get_ronda_actual(),True, listado_de_rondas, True)))         
                respuesta_correcta = cambiar_tarjeta(window, jugador)
                hora_inicial = time() 
                window.refresh()                                                                                                                  
        
            
            if event == "-exit-" or event == sg.WIN_CLOSED: # salida por abandono                                       
                estado_partida.set_log(time(), 'fin', jugador.get_nombre(),'abandonada','-','-')
                transferir_data(estado_partida.get_historial_partida())                  
                window.close()                                                                                        
                break                                                                                                                                     
            

        else:
            estado_partida.set_log(time(), 'fin', jugador.get_nombre(),'finalizada','-','-')
            actualizar_puntajes_json(jugador, dificultad)
            transferir_data(estado_partida.get_historial_partida())
            window.close() 
            window = sg.Popup(f"""La partida ha terminado {usuario}:
            Acumulaste un Total de: {int(jugador.get_puntaje_actual())} puntos
            En el modo {dificultad.upper()} """)
            break
            