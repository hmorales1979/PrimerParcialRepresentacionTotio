# utils.py
# utilidades simples

import random

def sortear_quien_inicia():
    """devuelve 'humano' o 'bot' al azar."""
    return random.choice(["humano", "bot"])
