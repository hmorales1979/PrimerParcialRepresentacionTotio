# board.py
# clase 'tablero' para administrar el estado 3x3, validaciones y serialización.

class tablero:
    def __init__(self):
        self.reiniciar()  ## inicia el tablero vacio

    def reiniciar(self):
        self.cuadricula = [[None for _ in range(3)] for _ in range(3)]  # crea matris 3x3 vacia 

   # def clonar(self):
   #     t = tablero()
   #     t.cuadricula = [fila[:] for fila in self.cuadricula]
   #     return t

    def colocar(self, f, c, marca):
        """coloca 'marca' (x/o) si la casilla está vacía."""
        if self.cuadricula[f][c] is None:
            self.cuadricula[f][c] = marca
            return True
        return False

    def casillas_vacias(self):  #Devuelve una lista con todas las posiciones libres.
        return [(f, c) for f in range(3) for c in range(3) if self.cuadricula[f][c] is None]

    def hay_ganador(self, marca):
    #Revisa todas las filas, columnas y diagonales.
    #Si encuentra que las 3 posiciones de una línea son de la misma marca, devuelve True.
    #Si no, devuelve False.    
        lineas = (
            # filas
            *[[ (i,0), (i,1), (i,2) ] for i in range(3)],
            # columnas
            *[[ (0,i), (1,i), (2,i) ] for i in range(3)],
            # diagonales
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
        )
        for linea in lineas:
            if all(self.cuadricula[f][c] == marca for f,c in linea):
                return True
        return False

    def esta_lleno(self):
        #Revisa si todas las casillas están ocupadas.
        #Si sí → empate posible.
        #Si no → todavía hay jugadas disponibles.
        return all(self.cuadricula[f][c] is not None for f in range(3) for c in range(3))

    def serializar(self): #Convierte el tablero en un string de 9 caracteres.
        """convierte el tablero en cadena 9 caracteres: x, o, _ (para base de conocimiento)."""
        mapa = {None: '_'}
        return ''.join(mapa.get(self.cuadricula[f][c], self.cuadricula[f][c]) for f in range(3) for c in range(3))
