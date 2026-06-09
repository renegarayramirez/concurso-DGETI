import flet as ft

class PanelAdmin(ft.Column):
    def __init__(self, page):
        super().__init__(
            expand=True,                                       # 🛠️ Obliga a la columna a ocupar TODA la pantalla
            alignment=ft.MainAxisAlignment.CENTER,             # 🎯 Centrado Vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # 🎯 Centrado Horizontal de los componentes
            spacing=20
        )
        
        self.controls = [
            ft.Text(
                "Panel de Administración", 
                size=34, 
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER                 # Asegura el centrado del texto
            ),
            ft.Text(
                "Aquí puedes gestionar las disciplinas y calificaciones.",
                size=16,
                color="gray",
                text_align=ft.TextAlign.CENTER
            ),
            # Un contenedor transparente para dar un respiro visual antes de los botones
            ft.Container(height=10), 
            
            ft.ElevatedButton(
                "Gestionar Disciplinas",
                icon="list",  
                on_click=lambda _: page.go("/disciplinas"),
                width=260,                                     # Ancho fijo para que ambos botones midan lo mismo
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.ElevatedButton(
                "Gestionar Alumnos",
                icon="people", 
                on_click=lambda _: page.go("/alumnos"),
                width=260,                                     # Mismo ancho para mantener la simetría perfecta
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            )
        ]