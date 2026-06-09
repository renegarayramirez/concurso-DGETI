import flet as ft
from view.panel_admin import PanelAdmin
from view.diciplinas_view import DisciplinaView
from view.alumnos_view import AlumnosView
from models.database import crear_tablas  # 🛠️ Importamos la función constructora

def main(page: ft.Page):
    # 🛠️ Ejecutamos la creación de tablas al arrancar la app
    crear_tablas()

    page.title = "Concurso DGTI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 900
    page.window_height = 600
    page.scroll = "adaptive"

    # Diccionario de rutas
    rutas = {
        "/admin": lambda: PanelAdmin(page),
        "/disciplinas": lambda: DisciplinaView(page),
        "/alumnos": lambda: AlumnosView(page),
    }

    # Función para manejar navegación
    def route_change(e):
        page.views.clear()
        ruta = page.route
        if ruta in rutas:
            vista = rutas[ruta]()
            page.views.append(ft.View(route=ruta, controls=[vista]))
        else:
            # Ruta por defecto
            page.views.append(ft.View(route="/admin", controls=[PanelAdmin(page)]))
        page.update()

    # Función para manejar retroceso
    def view_pop(e):
        page.views.pop()
        if page.views:
            page.go(page.views[-1].route)

    # Eventos de navegación
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Iniciar en el panel de administración
    page.go("/admin")

ft.app(target=main)