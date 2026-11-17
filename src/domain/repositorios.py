from abc import ABC, abstractmethod
from src.domain.incidente import IIncidente

class IIncidenteRepository(ABC):
    @abstractmethod
    def guardar(self, incidente: IIncidente) -> None:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> list[IIncidente]:
        pass    