from enum import Enum

class Horario(str, Enum):
    DIURNO = "diurno"
    NOCTURNO = "nocturno"