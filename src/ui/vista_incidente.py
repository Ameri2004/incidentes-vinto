from nicegui import ui
from src.application.registrar_incidente import RegistrarIncidenteUseCase
from src.application.gestionar_incidente import GestionarIncidenteUseCase
from src.infrastructure.repositorio_mock import IncidenteRepositoryMock
from src.infrastructure.mapa_adapter import MapaAdapter

repositorio = IncidenteRepositoryMock()
caso_uso_registro = RegistrarIncidenteUseCase(repositorio)
caso_uso_gestion = GestionarIncidenteUseCase(repositorio)

def crear_interfaz():
    # Función de seguridad para cambiar la visibilidad de las pestañas
    def cambiar_rol(e):
        es_funcionario = (e.value == 'Funcionario')
        tab_listado.set_visibility(es_funcionario)
        tab_dashboard.set_visibility(es_funcionario)
        # Si el usuario vuelve a ser Ciudadano, lo forzamos a volver a la pestaña de registro
        if not es_funcionario:
            tabs.set_value(tab_registro)

    # --- ENCABEZADO Y CONTROL DE ROLES (RF-10) ---
    with ui.header().classes('bg-green-700 w-full p-4 flex justify-between items-center shadow-md'):
        ui.label('Municipio de Vinto - Sistema Medio Ambiental').classes('text-2xl font-bold text-white')
        
        with ui.row().classes('items-center gap-2'):
            ui.icon('person', color='white').classes('text-2xl')
            # Usamos on_change explícito para no romper el componente tabs
            rol_actual = ui.select(['Ciudadano', 'Funcionario'], value='Ciudadano', label='Simular Rol', on_change=cambiar_rol).classes('w-48 bg-white rounded px-2')
    
    # --- PESTAÑAS NAVEGABLES ---
    with ui.tabs().classes('w-full mt-4') as tabs:
        tab_registro = ui.tab('Registrar Incidente')
        tab_listado = ui.tab('Gestión de Incidentes')
        tab_dashboard = ui.tab('Dashboard y Estadísticas')
        
    # Estado inicial estricto: Ocultar todo lo de funcionario porque empieza en 'Ciudadano'
    tab_listado.set_visibility(False)
    tab_dashboard.set_visibility(False)
        
    with ui.tab_panels(tabs, value=tab_registro).classes('w-full bg-transparent'):
        
        # --- PESTAÑA 1: REGISTRO ---
        with ui.tab_panel(tab_registro):
            with ui.card().classes('w-full max-w-2xl p-4 bg-gray-50 mx-auto'):
                tipo = ui.select(['Basura', 'Agua'], label='Categoría del Incidente', value='Basura').classes('w-full')
                descripcion = ui.input(label='Descripción detallada').classes('w-full')
                
                mapa_adapter = MapaAdapter()
                with ui.row().classes('w-full gap-4 mt-2'):
                    latitud = ui.number(label='Latitud', value=-17.3935).classes('w-5/12').props('readonly')
                    longitud = ui.number(label='Longitud', value=-66.1570).classes('w-5/12').props('readonly')
                
                mapa_adapter.configurar_evento_click(lambda lat, lng: (latitud.set_value(round(lat, 6)), longitud.set_value(round(lng, 6))))
                
                extra = ui.input(label='Volumen (Basura) o Nivel (Agua)').classes('w-full mt-4')
                
                estado_imagen = {'subida': False} 
                upload = ui.upload(on_upload=lambda e: estado_imagen.update({'subida': True}), label="Subir foto de evidencia", auto_upload=True, max_files=1).classes('w-full mt-2')
                
                def enviar_reporte():
                    try:
                        if not descripcion.value or not estado_imagen['subida']:
                            ui.notify('La descripción y fotografía son obligatorias', color='warning')
                            return

                        caso_uso_registro.ejecutar(tipo.value, descripcion.value, latitud.value, longitud.value, volumen=extra.value, nivel=extra.value)
                        ui.notify('Reporte registrado con éxito.', color='positive', position='top')
                        
                        descripcion.value = ''
                        upload.reset()
                        estado_imagen['subida'] = False
                        actualizar_tabla()
                        actualizar_dashboard()
                    except Exception as e:
                        ui.notify(f'Error: {str(e)}', color='negative', position='top')

                ui.button('Registrar Incidente', on_click=enviar_reporte).classes('w-full mt-6 bg-green-600 text-white font-bold')

        # --- PESTAÑA 2: LISTADO Y GESTIÓN ---
        with ui.tab_panel(tab_listado):
            with ui.card().classes('w-full p-4 bg-gray-50 mx-auto'):
                filtro_categoria = ui.select(['Todos', 'Basura', 'Contaminación de Agua'], label='Filtrar por Categoría', value='Todos').classes('w-64 mb-4')
                
                columnas = [
                    {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
                    {'name': 'tipo', 'label': 'Tipo', 'field': 'tipo', 'align': 'left'},
                    {'name': 'descripcion', 'label': 'Descripción', 'field': 'descripcion', 'align': 'left'},
                    {'name': 'estado', 'label': 'Estado', 'field': 'estado', 'align': 'center'},
                    {'name': 'responsable', 'label': 'Responsable', 'field': 'responsable', 'align': 'center'},
                ]
                
                tabla = ui.table(columns=columnas, rows=[], row_key='id', selection='single').classes('w-full')
                
                def actualizar_tabla():
                    filas = []
                    for inc in repositorio.obtener_todos():
                        det = inc.obtener_detalles()
                        if filtro_categoria.value == 'Todos' or det['tipo'] == filtro_categoria.value:
                            filas.append(det)
                    tabla.rows = filas
                    tabla.update()

                filtro_categoria.on_value_change(actualizar_tabla)
                tabs.on_value_change(lambda e: (actualizar_tabla(), actualizar_dashboard()) if e.value in [tab_listado, tab_dashboard] else None)

            # Panel de Administración
            with ui.card().classes('w-full mt-4 bg-blue-50').bind_visibility_from(tabla, 'selected', backward=bool):
                ui.label('Administración de Incidente').classes('text-lg font-bold text-blue-800')
                
                with ui.row().classes('w-full gap-4'):
                    nuevo_estado = ui.select(['REPORTADO', 'EN REVISIÓN', 'EN ATENCIÓN', 'ATENDIDO', 'CERRADO'], label='Cambiar Estado', value='EN REVISIÓN').classes('w-5/12')
                    nuevo_responsable = ui.input(label='Asignar Cuadrilla').classes('w-5/12')
                
                def guardar_cambios():
                    if tabla.selected:
                        inc_id = tabla.selected[0]['id']
                        if caso_uso_gestion.actualizar_incidente(inc_id, nuevo_estado.value, nuevo_responsable.value):
                            ui.notify(f'Incidente {inc_id} actualizado.', color='positive')
                            tabla.selected.clear()
                            actualizar_tabla()
                            actualizar_dashboard()
                            
                ui.button('Guardar Cambios', on_click=guardar_cambios).classes('mt-4 bg-blue-600 text-white font-bold')

        # --- PESTAÑA 3: DASHBOARD ---
        with ui.tab_panel(tab_dashboard):
            with ui.card().classes('w-full max-w-4xl p-4 bg-gray-50 mx-auto'):
                ui.label('Panel de Control (Métricas en Tiempo Real)').classes('text-xl font-bold mb-4')
                
                with ui.row().classes('w-full gap-4 justify-between'):
                    tarjeta_total = ui.card().classes('w-1/4 bg-blue-100 text-center p-4')
                    with tarjeta_total:
                        ui.label('Total Incidentes').classes('text-sm font-semibold text-blue-800')
                        lbl_total = ui.label('0').classes('text-4xl font-bold text-blue-900 mt-2')
                        
                    tarjeta_basura = ui.card().classes('w-1/4 bg-orange-100 text-center p-4')
                    with tarjeta_basura:
                        ui.label('Reportes Basura').classes('text-sm font-semibold text-orange-800')
                        lbl_basura = ui.label('0').classes('text-4xl font-bold text-orange-900 mt-2')
                        
                    tarjeta_agua = ui.card().classes('w-1/4 bg-teal-100 text-center p-4')
                    with tarjeta_agua:
                        ui.label('Contaminación Agua').classes('text-sm font-semibold text-teal-800')
                        lbl_agua = ui.label('0').classes('text-4xl font-bold text-teal-900 mt-2')

                def actualizar_dashboard():
                    incidentes = repositorio.obtener_todos()
                    total = len(incidentes)
                    basura = sum(1 for inc in incidentes if inc.obtener_detalles()['tipo'] == 'Basura')
                    agua = sum(1 for inc in incidentes if inc.obtener_detalles()['tipo'] == 'Contaminación de Agua')
                    
                    lbl_total.set_text(str(total))
                    lbl_basura.set_text(str(basura))
                    lbl_agua.set_text(str(agua))