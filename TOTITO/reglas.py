# rules.py
# carga reglas de bloqueo desde data/reglas.json. Si no existen, genera reglas básicas.

import json
import os

class reglas:
    def __init__(self, ruta="data/reglas.json"):
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                self.reglas = json.load(f)
        else:
            self.reglas = self._generar_reglas_basicas()
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(self.reglas, f, ensure_ascii=False, indent=2)

    def buscar_bloqueo(self, cuadricula, marca_rival):  ## recorre las reglas de bloque buscando coincidencia  con las jugadas del jugador humano, para proceder a bloquear
        """
        si alguna regla coincide (dos 'ocupadas' del rival y la celda 'bloqueo' vacía),
        devuelve la posición (f,c) para bloquear.
        """
        for _, reg in self.reglas.items():
            (f1,c1), (f2,c2) = reg["ocupadas"]
            fb, cb = reg["bloqueo"]
            if (cuadricula[f1][c1] == marca_rival and
                cuadricula[f2][c2] == marca_rival and
                cuadricula[fb][cb] is None):
                return (fb, cb)
        return None

    def _generar_reglas_basicas(self): #crea el archvo de reglas en caso no existiera
        """
        Genera todas las combinaciones de dos-en-línea + celda faltante (24 reglas),
        para filas, columnas y diagonales. Útil si el archivo no existe.
        """
        reglas = {}
        idx = 1

        # filas
        for f in range(3):
            pos = [(f,0),(f,1),(f,2)]
            pares = [([pos[0],pos[1]], pos[2]), ([pos[1],pos[2]], pos[0]), ([pos[0],pos[2]], pos[1])]
            for ocupadas, bloqueo in pares:
                reglas[f"jugada_{idx}"] = {"ocupadas": ocupadas, "bloqueo": bloqueo, "tipo": "horizontal"}
                idx += 1

        # columnas
        for c in range(3):
            pos = [(0,c),(1,c),(2,c)]
            pares = [([pos[0],pos[1]], pos[2]), ([pos[1],pos[2]], pos[0]), ([pos[0],pos[2]], pos[1])]
            for ocupadas, bloqueo in pares:
                reglas[f"jugada_{idx}"] = {"ocupadas": ocupadas, "bloqueo": bloqueo, "tipo": "vertical"}
                idx += 1

        # diagonales
        diag1 = [(0,0),(1,1),(2,2)]
        diag2 = [(0,2),(1,1),(2,0)]
        for pos in (diag1, diag2):
            pares = [([pos[0],pos[1]], pos[2]), ([pos[1],pos[2]], pos[0]), ([pos[0],pos[2]], pos[1])]
            for ocupadas, bloqueo in pares:
                reglas[f"jugada_{idx}"] = {"ocupadas": ocupadas, "bloqueo": bloqueo, "tipo": "diagonal"}
                idx += 1

        return reglas
