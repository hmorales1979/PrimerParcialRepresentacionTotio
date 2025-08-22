# interfaz gráfica: partidas con click, sorteo de inicio

import tkinter as tk #librería para ventanas, botones, menus, interfaces gráficas
from tkinter import messagebox # cuadro de dialogo emergente

#clases
from tablero import tablero
from reglas import reglas
from conocimiento import conocimiento
from bot import bot
from juego import juego
from utilidades import sortear_quien_inicia

# configuración global simple
tamaño_celda = 100 ##tamaño de cada celda en el totito en pixeles

class interfaz:
    def __init__(self, raiz):  # constructor de la interfaz gráfica
        self.raiz = raiz
        self.raiz.title("Tablero Totito")

        # modelos
        self.t = tablero()   # se instancia un objeto tablero
        self.motor_reglas = reglas("data/reglas.json") #se instancia un objeto de la clase "reglas", cargando el json
        self.memoria = conocimiento("data/base_conocimiento.json") #se instancia un objeto de la clase "conocimiento" cargando el json

        # se sortea quién inicia; quien inicia siempre usa 'x'
        quien = sortear_quien_inicia() #se invoca la clase utilidades para realizar el sorte random
        if quien == "bot":
            self.marca_bot = "x"
            self.marca_humano = "o"
            self.turno = "bot"
            info_inicio = "inicia: bot (x)"
        else:
            self.marca_humano = "x"
            self.marca_bot = "o"
            self.turno = "humano"
            info_inicio = "inicia: humano (x)"

        # instanciar bot con marcas en orden correcto, se crea objeto de la clase bot
        self.bot = bot(mi_marca=self.marca_bot, marca_rival=self.marca_humano, #mi_marca= "X" o "0",   marca_riva= "X" o "0",
                       motor_reglas=self.motor_reglas, memoria=self.memoria) # motor_reglas las jugadas peligrosas de reglas.json, memoria  la base de conocimiento para aprender.
        self.partida = juego(self.t, self.bot, memoria=self.memoria,  #se crea instancia del juego , selft.t =tablero actual, memoria = guarda aprendizaje 
                             marca_humano=self.marca_humano, marca_bot=self.marca_bot) # marca_humano  y marca_bot  define los simbolos del juego

        # ui
        self.etiqueta_turno = tk.Label(self.raiz, text=info_inicio, font=("Arial", 14)) ## muestra quien inicia o turno de quien,  "humano" o "boot"
        self.etiqueta_turno.pack(pady=8) # lo coloca en la interfaz

        self.canvas = tk.Canvas(self.raiz, width=3*tamaño_celda, height=3*tamaño_celda, bg="white") #area donde se dibuja el tablero 3 × tamaño_celda = 300 px,  fondo blanco
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_tablero) # cuando hay un click se llama al método "click_tablero"

        self.boton_reiniciar = tk.Button(self.raiz, text="reiniciar", command=self.reiniciar) #instanciar boton de reinicio,  llama al me´todo "reiniciar"
        self.boton_reiniciar.pack(pady=8)

        self.dibujar_tablero() # llama método dibujar_tablero;  dibuja linesa de speración y fichas.

        # si el bot inicia, juega de una vez
        if self.turno == "bot":
            self.juega_bot()

    def reiniciar(self):
        self.t.reiniciar()
        # sortear de nuevo quién inicia
        quien = sortear_quien_inicia() # metodo de sorteo quien arranca el juego
        if quien == "bot":
            self.marca_bot = "x"
            self.marca_humano = "o"
            self.turno = "bot"
            info_inicio = "inicia: bot (x)"
        else:
            self.marca_humano = "x"
            self.marca_bot = "o"
            self.turno = "humano"
            info_inicio = "inicia: humano (x)"

        self.bot = bot(mi_marca=self.marca_bot, marca_rival=self.marca_humano, #mi_marca= "X" o "0",   marca_riva= "X" o "0",
                       motor_reglas=self.motor_reglas, memoria=self.memoria) # motor_reglas las jugadas peligrosas de reglas.json, memoria  la base de conocimiento para aprender.
        self.partida = juego(self.t, self.bot, memoria=self.memoria,  #se crea instancia del juego , selft.t =tablero actual, memoria = guarda aprendizaje 
                             marca_humano=self.marca_humano, marca_bot=self.marca_bot) # marca_humano  y marca_bot  define los simbolos del juego

        self.etiqueta_turno.config(text=info_inicio)  #muestra la etiqueta de quien juega el siguiente turno
        self.dibujar_tablero() #  redibuja el tablero 
        if self.turno == "bot":
            self.juega_bot()  #llama al metodo juega bot

    def dibujar_tablero(self):
        self.canvas.delete("all")
        # líneas
        for i in range(1,3):
            self.canvas.create_line(i*tamaño_celda, 0, i*tamaño_celda, 3*tamaño_celda)  #Dibuja dos líneas verticales (x=100 y x=200 si tamaño_celda=100).
            self.canvas.create_line(0, i*tamaño_celda, 3*tamaño_celda, i*tamaño_celda)  #Dibuja dos líneas horizontales (y=100 y y=200).
        # marcas
        for f in range(3):  # f= fila (0,1,2)
            for c in range(3):  #c= columna (0,1,2)
                marca = self.t.cuadricula[f][c] # se recorre cada celda del "tablero" que en realidad es una matriz de 3x3 tipo lista, mira qué hay en esa casilla
                #se calcula las coordenadas (tamaño) de los pixdeles del canva 
                x0 = c*tamaño_celda #borde izquierdo de la celda.
                y0 = f*tamaño_celda #borde superior de la celda.
                x1 = x0 + tamaño_celda #borde derecho.
                y1 = y0 + tamaño_celda #borde inferior.
                if marca == "x":
                    # dibujar X
                    self.canvas.create_line(x0+15, y0+15, x1-15, y1-15, width=3)  #dibuja dos lineas diagonales dentro de la casilla del tablero "X"
                    self.canvas.create_line(x0+15, y1-15, x1-15, y0+15, width=3)
                elif marca == "o":
                    # dibujar O
                    self.canvas.create_oval(x0+15, y0+15, x1-15, y1-15, width=3)  #dibuja un ovalo dentro de la casilla.

    def click_tablero(self, evento):  #función  ejecutada cuando el jugador hace click en el tablero
        if self.turno != "humano":   # sí el turno no es del jugador  no se hace nada, "return" 
            return
        c = evento.x // tamaño_celda #coordenadas del "click" en pixeles dentro del Canvas,  eje:  c = 230 // 100 = 2 → columna 2
        f = evento.y // tamaño_celda  #  se  aplica división entera para pasar a indices, de pixeles a indices .   f = 120 // 100 = 1 → fila 1
        if f not in range(3) or c not in range(3): #Si click está fuera del tablero (ejemplo, coordenadas más grandes que 300 px) → no hace nada.
            return
        if self.t.cuadricula[f][c] is not None: #Si ya hay "x" o "o" en esa casilla → no deja colocar nada.
            return
        # partida de jugador humano 
        self.t.colocar(f, c, self.marca_humano)  #actualiza logicamente el tablero, en la matriz 3x3 
        self.dibujar_tablero()  #re dibuja el tablero ya con los valores actalizados

        res = self.partida.resultado()  #validar si hay un resultado, es decir un juego ganado, empatado, perdido.
        if res:
            self.finalizar(res)  # sí juego a finalizado, termina la partida.
            return

        # ahora turno bot
        self.turno = "bot"  
        self.etiqueta_turno.config(text="turno: bot") #actualiza la etiqueta en la ventana, ahora es turno del botcito
        self.raiz.after(150, self.juega_bot)  # pequeña pausa visual

    def juega_bot(self):
        jug = self.partida.turno_bot() # partida del bot  llama a metodo turno_bot de la clase juego
        if jug:
            self.dibujar_tablero() # dibula "x"  o "0"   en la casilla , la jugada que acaba de hacer el bot

        res = self.partida.resultado() # revisa si ya hay un ganado o empate
        if res:
            self.finalizar(res) 
            return

        self.turno = "humano"  #sino se finaliza el juego, se pasa el turno al humano
        self.etiqueta_turno.config(text="turno: humano")

    def finalizar(self, res):   
        # aprendizaje
        self.partida.aprender(res) # se llama al método aprender de la clase juego 

        if res == "gana_bot":
            mensaje = "fin: gana el bot"
        elif res == "gana_humano":
            mensaje = "fin: gana el humano"
        else:
            mensaje = "fin: empate"

        self.etiqueta_turno.config(text=mensaje)
        messagebox.showinfo("resultado", mensaje)

if __name__ == "__main__":
    raiz = tk.Tk()
    app = interfaz(raiz)
    raiz.mainloop()
