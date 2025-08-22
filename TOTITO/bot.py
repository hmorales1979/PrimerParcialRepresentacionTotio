# bot.py
# estrategia del bot con prioridades y uso de reglas + conocimiento.

class bot:
    def __init__(self, mi_marca="x", marca_rival="o", motor_reglas=None, memoria=None):
        self.mi_marca = mi_marca  # símbolo del bot: "x" o "o"
        self.marca_rival = marca_rival   # símbolo del rival
        self.motor_reglas = motor_reglas # acceso a reglas.json (bloqueos rápidos)
        self.memoria = memoria   # acceso a base_conocimiento.json (aprendizaje)

    def elegir_jugada(self, t):  #prioridad de decisionees 
        """
        prioridades:
        1) ganar si se puede                  
        2) bloquear (reglas + genérico)
        3) centro
        4) esquinas
        5) lados
        6) usar memoria para desempatar
        """
        # 1) ganar Busca si el bot ya tiene 2 en línea y falta una para ganar; si existe, juega ahí.
        jug = self._completar_linea(t, self.mi_marca)
        if jug: return jug

        # 2) bloquear con reglas si existen
        if self.motor_reglas:
            jug = self.motor_reglas.buscar_bloqueo(t.cuadricula, self.marca_rival)
            if jug: return jug

        # 2b) bloqueo genérico (por si no hay reglas)
        jug = self._completar_linea(t, self.marca_rival)
        if jug: return jug

        # 3) centro si esta vacio, lo toma 
        if t.cuadricula[1][1] is None:
            return (1,1)

        # 4) esquinas , toma la primera que encuetra vacia
        for f,c in [(0,0),(0,2),(2,0),(2,2)]:
            if t.cuadricula[f][c] is None:
                return (f,c)

        # 5) lados
        for f,c in [(0,1),(1,0),(1,2),(2,1)]:
            if t.cuadricula[f][c] is None:
                return (f,c)

        # 6) memoria para desempatar entre las vacías , consulta la base de conocimiento
        if self.memoria:
            estado = t.serializar()
            return self.memoria.mejor_movimiento(estado, t.casillas_vacias())

        #  ultima estrategia si no están cubiertas 
        vacias = t.casillas_vacias()
        return vacias[0] if vacias else None

    def _completar_linea(self, t, marca):  #Define todas las 8 líneas posibles (3 filas, 3 columnas, 2 diagonales).
        #Para cada línea, cuenta: si hay 2 marcas del jugador (marca) y 1 vacío (None),  Si sí, devuelve la celda vacía de esa línea (la jugada ganadora o de bloqueo).
        """si hay 2 de 'marca' + 1 vacío en alguna línea, devuelve la casilla vacía."""
        lineas = (
            *[[ (i,0), (i,1), (i,2) ] for i in range(3)], # 3 filas
            *[[ (0,i), (1,i), (2,i) ] for i in range(3)],  # 3 columnas
            [(0,0),(1,1),(2,2)],  # diagonal principal
            [(0,2),(1,1),(2,0)] # diagonal secundaria
        )
        for linea in lineas:
            valores = [t.cuadricula[f][c] for f,c in linea]
            if valores.count(marca) == 2 and valores.count(None) == 1:
                k = valores.index(None)
                return linea[k]
        return None
