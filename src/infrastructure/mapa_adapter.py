from nicegui import ui, events

class MapaAdapter:
    def __init__(self, lat_inicial: float = -17.3935, lon_inicial: float = -66.1570):
        # Inicializa el mapa centrado en la ubicación dada (Vinto, Cochabamba)
        self.mapa = ui.leaflet(center=(lat_inicial, lon_inicial), zoom=13).classes('w-full h-64 mt-2')
        self.marcador = self.mapa.marker(latlng=(lat_inicial, lon_inicial))
        
    def _on_map_click(self, e: events.GenericEventArguments, callback):
        # Extraer latitud y longitud del evento nativo de Leaflet
        lat = e.args['latlng']['lat']
        lng = e.args['latlng']['lng']
        
        # Mover el marcador al nuevo punto
        self.marcador.move(lat, lng)
        
        # Enviar los datos de vuelta a la interfaz
        callback(lat, lng)

    def configurar_evento_click(self, callback):
        # 'map-click' es el evento interno de NiceGUI para clics en el mapa
        self.mapa.on('map-click', lambda e: self._on_map_click(e, callback))