from dataclasses import dataclass

@dataclass(frozen=True)
class Coordenadas:
    latitud: float
    longitud: float

    def es_valida(self) -> bool:
        return -90 <= self.latitud <= 90 and -180 <= self.longitud <= 180