# knowledge.py
# memoria simple: para cada estado serializado guarda puntajes por movimiento y el mejor.

import json #para leer/escribir archivos JSON.
import os  #para verificar si existe la carpeta/archivo y crearlos si no

class conocimiento:
    def __init__(self, ruta="data/base_conocimiento.json"):
        self.ruta = ruta
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                try:
                    self.bd = json.load(f)   # cargar base existente
                except json.JSONDecodeError:
                    self.bd = {}
        else:
            self.bd = {} # si no existe, iniciar vacío
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            self._guardar()  # guardar archivo vacío

    def mejor_movimiento(self, estado, candidatos):  # "estado"  es una cadena serializada  ejemplo "x__o_____" 
    # el tablero lógico tiene esta distribución matriz 3x3  tablero.serializar   lo convierte en una cadena de 9 caracteres
    #[
    #["x", None, "o"],
    #[None, None, None],
    #[None, None, None]
    # serializado  x__o_____  estado actual del juego  se usa como llave para buscar dentro de la base de conocimiento
    # si no existe, lo agrega con un puntaje vacio
    #{
    #"x__o_____": {
    #"puntajes": {}
    # }
    #}
    # sí lo encuentra, entonces recupera los puntajes anteiores 
 
        """elige el candidato con mayor puntaje conocido; si no hay puntajes, devuelve cualquiera."""
        if not candidatos:
            return None
        registro = self.bd.get(estado, {})
        puntajes = registro.get("puntajes", {})
        return max(candidatos, key=lambda mv: puntajes.get(f"{mv[0]},{mv[1]}", 0))

    def actualizar_despues_partida(self, historial_bot, recompensa):
        """
        historial_bot: lista de tuplas (estado_serializado, (f,c))
        recompensa: +1 victoria del bot, 0 empate, -1 derrota
        """
        for estado, (f,c) in historial_bot:
            reg = self.bd.setdefault(estado, {"puntajes": {}})
            clave = f"{f},{c}"
            reg["puntajes"][clave] = reg["puntajes"].get(clave, 0) + recompensa
            # actualizar recomendado
            mejor = max(reg["puntajes"], key=reg["puntajes"].get)
            reg["recomendado"] = mejor
        self._guardar()

    def _guardar(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(self.bd, f, ensure_ascii=False, indent=2)
