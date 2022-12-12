import os
import csv
from resources.config import ESTADISTICA_ROOT

def obtener_ultimo_id_archivo():
    """ Abre el archivo csv con el historial de las partidas y devuelve el ultimo ID de partida que opera de manera 
    autoincremental desde una instancia de estado_partida cuando hay una partida activa."""
    with open(os.path.join(ESTADISTICA_ROOT, "historial_partidas.csv"), 'r', encoding='utf-8')as historial:
        csv_reader = csv.reader(historial, delimiter=",")
        next(csv_reader)                    #descarto encabezado
        datos = list(csv_reader)
        if datos:    
            return int(datos[len(datos)-1][1])      #devuelve el id de la ultima linea del csv
        else:
            return 0

def transferir_data(historial_partida):
    """ transfiere la informacion del historial de la partida realizada, desde que se inicio hasta que se finalizo o 
    abandono al archivo csv que almacenara todos los logs"""
    with open(os.path.join(ESTADISTICA_ROOT, "historial_partidas.csv"), 'a', encoding='utf-8', newline='')as archivo:
        #dic_writer = csv.DictWriter(archivo, fieldnames=historial_partida[0].keys())
        csv_writer = csv.writer(archivo)
        for log in historial_partida:
            csv_writer.writerow([log["timestamp"],log["id"],log["evento"], log["usuario"],log["estado"], log["texto_ingresado"], log["respuesta"], log["nivel"]])
           
         