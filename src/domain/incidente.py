import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from src.domain.coordenadas import Coordenadas

class IIncidente(ABC):
    @abstractmethod
    def obtener_detalles(self) -> dict: pass
    
    @abstractmethod
    def actualizar_estado(self, nuevo_estado: str) -> None: pass
    
    @abstractmethod
    def asignar_responsable(self, responsable: str) -> None: pass

class IncidenteBasura(IIncidente):
    def __init__(self, descripcion: str, ubicacion: Coordenadas, volumen_estimado: str):
        self.id = str(uuid.uuid4())[:8] # ID único corto
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.volumen_estimado = volumen_estimado
        self.fecha_reporte = datetime.now()
        self.estado = "REPORTADO"
        self.responsable = "Sin asignar"

    def actualizar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado
        
    def asignar_responsable(self, responsable: str) -> None:
        self.responsable = responsable

    def obtener_detalles(self) -> dict:
        return {"id": self.id, "tipo": "Basura", "descripcion": self.descripcion, "estado": self.estado, "responsable": self.responsable}

class IncidenteAgua(IIncidente):
    def __init__(self, descripcion: str, ubicacion: Coordenadas, nivel_contaminacion: str):
        self.id = str(uuid.uuid4())[:8]
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.nivel_contaminacion = nivel_contaminacion
        self.fecha_reporte = datetime.now()
        self.estado = "REPORTADO"
        self.responsable = "Sin asignar"
        
    def actualizar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado
        
    def asignar_responsable(self, responsable: str) -> None:
        self.responsable = responsable

    def obtener_detalles(self) -> dict:
        return {"id": self.id, "tipo": "Contaminación de Agua", "descripcion": self.descripcion, "estado": self.estado, "responsable": self.responsable}

class IncidenteFactory:
    @staticmethod
    def crear_incidente(tipo: str, descripcion: str, latitud: float, longitud: float, **kwargs) -> IIncidente:
        ubicacion = Coordenadas(latitud, longitud)
        if tipo.lower() == "basura": return IncidenteBasura(descripcion, ubicacion, kwargs.get("volumen", "N/A"))
        elif tipo.lower() == "agua": return IncidenteAgua(descripcion, ubicacion, kwargs.get("nivel", "N/A"))
        raise ValueError(f"Tipo '{tipo}' no soportado")