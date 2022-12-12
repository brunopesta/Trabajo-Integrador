from resources.estadistica.estadistica import obtener_ultimo_id_archivo

class EstadoPartida:

    def __init__(self, rondas, dificultad):
        self._total_rondas = rondas
        self._ronda_actual = 1
        self._timer_iniciado = False
        self._dificultad = dificultad
        self._historial_partida = []
        self._ultimo_id = obtener_ultimo_id_archivo() + 1

    def get_estado(self, key):
        return self._estado[key]

    def get_timer_iniciado(self):
        return self._timer_iniciado

    def get_dificultad(self):
        return self._dificultad
    
    def get_total_rondas(self):
        return self._total_rondas
    
    def get_ronda_actual(self):
        return self._ronda_actual

    def set_estado(self, key, nuevo_estado):
        self._estado[key] = nuevo_estado
    
    def set_dificultad(self, nueva_dificultad):
        self._dificultad = nueva_dificultad
    
    def set_timer_iniciado(self):
        self._timer_iniciado = True

    def set_total_rondas(self, tot):
        self._total_rondas = tot

    def incrementar_ronda_actual(self):
        self._ronda_actual = self.get_ronda_actual() + 1

    def get_ultimo_id(self):
        return self._ultimo_id


    def set_log(self,timestamp, evento, usuario, estado, texto_ingresado, respuesta):
        log = {
            "timestamp":timestamp,
            "id": self.get_ultimo_id(),
            "evento":evento,
            "usuario":usuario,
            "estado": estado,
            "texto_ingresado":texto_ingresado,
            "respuesta":respuesta,
            "nivel":self.get_dificultad()
        }
        self._historial_partida.append(log)
    
    def get_historial_partida(self):
        return self._historial_partida
    