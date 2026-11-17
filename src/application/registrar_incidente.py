from src.domain.incidente import IncidenteFactory
from src.domain.repositorios import IIncidenteRepository

class RegistrarIncidenteUseCase:
    def __init__(self, repositorio: IIncidenteRepository):
        # Inyectamos el repositorio (Cumple el principio DIP de SOLID)
        self.repositorio = repositorio

    def ejecutar(self, tipo: str, descripcion: str, latitud: float, longitud: float, **kwargs) -> dict:
        # 1. Crear el incidente usando la fábrica
        incidente = IncidenteFactory.crear_incidente(tipo, descripcion, latitud, longitud, **kwargs)
        
        # 2. Guardar en el repositorio (Base de datos o memoria)
        self.repositorio.guardar(incidente)
        
        # 3. Retornar los detalles para mostrarlos en la UI
        return incidente.obtener_detalles()