import flet as ft
from controllers.diciplinas_controller import DisciplinasController

class DisciplinaView(ft.Column):
    def __init__(self, page: ft.Page):
        self.cargado = False  
        super().__init__(spacing=15, expand=True)
        self.main_page = page  
        self.controller = DisciplinasController(self)
        
        self.modo_edicion = False
        self.id_seleccionado = None

        self.lbl_form_titulo = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.txt_nombre = ft.TextField(label="Nombre de la disciplina")
        
        # Panel con fondo sólido en lugar de bordes
        self.form_container = ft.Container(
            content=ft.Column([
                self.lbl_form_titulo,
                self.txt_nombre,
                ft.Row([
                    ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_formulario),
                    ft.TextButton("Cancelar", on_click=self.ocultar_formulario)
                ], alignment=ft.MainAxisAlignment.END)
            ], tight=True, spacing=10),
            padding=15,
            bgcolor="black12",
            border_radius=10,
            visible=False
        )

        self.lbl_confirm_texto = ft.Text("", size=16, color="red")
        
        self.confirm_container = ft.Container(
            content=ft.Column([
                self.lbl_confirm_texto,
                ft.Row([
                    ft.ElevatedButton("Sí, Eliminar", bgcolor="red", color="white", on_click=self.ejecutar_eliminacion),
                    ft.TextButton("Cancelar", on_click=self.ocultar_confirmacion)
                ], alignment=ft.MainAxisAlignment.END)
            ], tight=True, spacing=10),
            padding=15,
            bgcolor="#15FF0000",
            border_radius=10,
            visible=False
        )

        self.lista_disciplinas = ft.ListView(expand=True, spacing=10, padding=10)

        header = ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.ARROW_BACK,  
                    on_click=lambda _: self.main_page.go("/admin"),
                    tooltip="Volver al Panel de Administración"
                ),
                ft.Text("Gestión de Disciplinas", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),  
                ft.IconButton(
                    ft.Icons.ADD,  
                    on_click=self.mostrar_formulario_agregar,
                    tooltip="Agregar Disciplina"
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.controls = [
            header,
            ft.Divider(),
            self.form_container,
            self.confirm_container,
            ft.Text("Disciplinas registradas", size=20, italic=True, color="gray"),  
            self.lista_disciplinas,
        ]

        self.actualizar_lista_disciplinas()
        self.cargado = True  

    def mostrar_mensaje(self, mensaje: str, es_error: bool = False):
        snack = ft.SnackBar(ft.Text(mensaje), bgcolor="red" if es_error else "green")
        self.main_page.snack_bar = snack
        snack.open = True
        self.main_page.update()

    def actualizar_lista_disciplinas(self):
        self.lista_disciplinas.controls.clear()
        try:
            disciplinas = self.controller.disciplinas_dao.listar_todas()
            for id_disciplina, nombre in disciplinas:
                fila = ft.Row(
                    controls=[
                        ft.Text(f"ID: {id_disciplina} — {nombre}", size=18),
                        ft.Row([
                            ft.IconButton(
                                ft.Icons.EDIT,  
                                tooltip="Editar Nombre",
                                on_click=lambda e, id=id_disciplina, nom=nombre: self.mostrar_formulario_editar(id, nom)
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,  
                                tooltip="Eliminar Disciplina",
                                on_click=lambda e, id=id_disciplina: self.mostrar_confirmacion_eliminar(id)
                            )
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                self.lista_disciplinas.controls.append(fila)
        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar disciplinas: {e}", es_error=True)
            
        if self.cargado:
            self.update()

    def mostrar_formulario_agregar(self, e):
        self.ocultar_confirmacion(None)
        self.modo_edicion = False
        self.lbl_form_titulo.value = "Agregar Nueva Disciplina"
        self.txt_nombre.value = ""
        self.form_container.visible = True
        self.update()

    def mostrar_formulario_editar(self, id_disciplina: int, nombre_actual: str):
        self.ocultar_confirmacion(None)
        self.modo_edicion = True
        self.id_seleccionado = id_disciplina
        self.lbl_form_titulo.value = f"Editar Disciplina (ID: {id_disciplina})"
        self.txt_nombre.value = nombre_actual
        self.form_container.visible = True
        self.update()

    def ocultar_formulario(self, e=None):
        self.form_container.visible = False
        self.update()

    def guardar_formulario(self, e):
        try:
            if self.modo_edicion:
                self.controller.modificar_disciplina(self.id_seleccionado, self.txt_nombre.value)
            else:
                self.controller.registrar_disciplina(self.txt_nombre.value)
            self.ocultar_formulario()
            self.actualizar_lista_disciplinas()
        except Exception as ex:
            self.mostrar_mensaje(str(ex), es_error=True)

    def mostrar_confirmacion_eliminar(self, id_disciplina: int):
        self.ocultar_formulario(None)
        self.id_seleccionado = id_disciplina
        self.lbl_confirm_texto.value = f"¿Estás completamente seguro de eliminar la disciplina con ID {id_disciplina}?"
        self.confirm_container.visible = True
        self.update()

    def ocultar_confirmacion(self, e=None):
        self.confirm_container.visible = False
        self.update()

    def ejecutar_eliminacion(self, e):
        try:
            self.controller.eliminar_disciplina(self.id_seleccionado)
            self.ocultar_confirmacion()
            self.actualizar_lista_disciplinas()
        except Exception as ex:
            self.mostrar_mensaje(str(ex), es_error=True)