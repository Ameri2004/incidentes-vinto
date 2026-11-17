from src.domain.repositorios import IIncidenteRepository
from src.domain.incidente import IIncidente

class IncidenteRepositoryMock(IIncidenteRepository):
    def __init__(self):
        # Aquí guardaremos los incidentes en memoria (una lista)
        self._incidentes = []

    def guardar(self, incidente: IIncidente) -> None:
        self._incidentes.append(incidente)
        print(f"✅ Incidente guardado en Mock DB: {incidente.obtener_detalles()}")

    def obtener_todos(self) -> list[IIncidente]:
        return self._incidentes