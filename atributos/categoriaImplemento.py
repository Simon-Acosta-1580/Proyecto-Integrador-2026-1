from enum import Enum

class Categoria(str, Enum):
    BALON = "balon"
    INSTRUMENTO = "instrumento"
    JUEGO = "juego"
    CANCHA = "cancha"