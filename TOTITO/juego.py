# game.py
# orquesta la partida, registra historial del bot y calcula resultado.

class juego:
    def __init__(self, tablero, bot, memoria=None, marca_humano="o", marca_bot="x"):
        self.t = tablero
        self.bot = bot
        self.memoria = memoria
        self.marca_humano = marca_humano
        self.marca_bot = marca_bot
        self.historial_bot = []  # [(estado_serializado, (f,c)), ...]

    def turno_bot(self):
        estado = self.t.serializar()
        jug = self.bot.elegir_jugada(self.t)
        if jug:
            f,c = jug
            self.t.colocar(f, c, self.marca_bot)
            # guardamos para aprendizaje
            self.historial_bot.append((estado, (f,c)))
        return jug

    def turno_humano(self, f, c):
        return self.t.colocar(f, c, self.marca_humano)

    def resultado(self):
        if self.t.hay_ganador(self.marca_bot):
            return "gana_bot"
        if self.t.hay_ganador(self.marca_humano):
            return "gana_humano"
        if self.t.esta_lleno():
            return "empate"
        return None

    def aprender(self, resultado):
        if not self.memoria:
            return
        recompensa = {"gana_bot": +1, "empate": 0, "gana_humano": -1}.get(resultado, 0)
        self.memoria.actualizar_despues_partida(self.historial_bot, recompensa)
