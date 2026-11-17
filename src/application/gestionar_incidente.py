from src.domain.repositorios import IIncidenteRepository

class GestionarIncidenteUseCase:
    def __init__(self, repositorio: IIncidenteRepository):
        self.repositorio = repositorio
        
    def actualizar_incidente(self, incidente_id: str, nuevo_estado: str, responsable: str) -> bool:
        incidentes = self.repositorio.obtener_todos()
        for inc in incidentes:
            # Buscamos el incidente por su ID en el repositorio
            if inc.obtener_detalles()["id"] == incidente_id:
                if nuevo_estado:
                    inc.actualizar_estado(nuevo_estado)
                if responsable:
                    inc.asignar_responsable(responsable)
                return True
        return False