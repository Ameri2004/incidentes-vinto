from nicegui import ui
from src.ui.vista_incidente import crear_interfaz

# Renderizamos la interfaz que acabamos de crear
crear_interfaz()

# Iniciamos el servidor de NiceGUI
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Incidentes Vinto - MVP")