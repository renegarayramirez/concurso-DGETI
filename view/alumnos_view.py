import flet as ft
from controllers.alumnos_controller import AlumnosController
from controllers.diciplinas_controller import DisciplinasController # Importamos para leer las disciplinas

class AlumnosView(ft.Column):
    def __init__(self, page: ft.Page):
        self.cargado = False
        super().__init__(spacing=15, expand=True)
        self.main_page = page  
        self.controller = AlumnosController(self)
        # Instanciamos el controlador de disciplinas para llenar el dropdown
        self.disciplinas_controller = DisciplinasController(self)
        
        self.modo_edicion = False
        self.matricula_seleccionada = None

        self.lbl_form_titulo = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.txt_nombre = ft.TextField(label="Nombre Completo")
        self.txt_matricula = ft.TextField(label="Matrícula Única")
        self.txt_nss = ft.TextField(label="NSS")
        self.txt_plantel = ft.TextField(label="Plantel")
        self.txt_calificacion = ft.TextField(label="Calificación Inicial", keyboard_type=ft.KeyboardType.NUMBER)
        
        # 🔄 CAMBIO AQUÍ: Ahora es un Dropdown en lugar de un TextField
        self.dd_disciplina = ft.Dropdown(
            label="Selecciona la Disciplina",
            hint_text="Elige una opción de la lista..."
        )
        
        # Panel de formulario integrado
        self.form_container = ft.Container(
            content=ft.Column([
                self.lbl_form_titulo,
                self.txt_nombre,
                self.txt_matricula,
                self.txt_nss,
                self.txt_plantel,
                self.txt_calificacion,
                self.dd_disciplina, # Agregamos el dropdown al diseño
                ft.Row([
                    ft.ElevatedButton("Guardar Datos", icon=ft.Icons.SAVE, on_click=self.guardar_formulario),
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

        self.lista_alumnos = ft.ListView(expand=True, spacing=10, padding=10)

        header = ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    on_click=lambda _: self.main_page.go("/admin"),  
                    tooltip="Volver al Panel de Administración"
                ),
                ft.Text("Gestión de Alumnos", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),  
                ft.IconButton(
                    ft.Icons.ADD,
                    on_click=self.mostrar_formulario_agregar,
                    tooltip="Agregar Alumno"
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
            ft.Text("Alumnos registrados", size=20, italic=True, color="gray"),  
            self.lista_alumnos,
        ]

        self.actualizar_lista_alumnos()
        self.cargado = True

    def mostrar_mensaje(self, mensaje: str, es_error: bool = False):
        snack = ft.SnackBar(ft.Text(mensaje), bgcolor="red" if es_error else "green")
        self.main_page.snack_bar = snack  
        snack.open = True
        self.main_page.update()           

    def actualizar_lista_alumnos(self):
        self.lista_alumnos.controls.clear()
        try:
            alumnos = self.controller.alumnos_dao.listar_todos()
            for nombre, matricula, nss, plantel, calificacion, disciplina in alumnos:
                fila = ft.Row(
                    controls=[
                        ft.Text(f"{matricula} — {nombre} ({plantel})  Calif: {calificacion}", size=16),
                        ft.Row([
                            ft.IconButton(
                                ft.Icons.EDIT,
                                tooltip="Editar Alumno",
                                on_click=lambda e, m=matricula: self.mostrar_formulario_editar(m)
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                tooltip="Eliminar Alumno",
                                on_click=lambda e, m=matricula: self.mostrar_confirmacion_eliminar(m)
                            )
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                self.lista_alumnos.controls.append(fila)
        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar alumnos: {e}", es_error=True)
        
        if self.cargado:
            self.update()

    def _buscar_alumno_por_matricula(self, matricula: str):
        try:
            alumnos = self.controller.alumnos_dao.listar_todos()
            for nombre, mat, nss, plantel, calificacion, disciplina in alumnos:
                if mat == matricula:
                    return {
                        "nombre": nombre,
                        "matricula": mat,
                        "nss": nss,
                        "plantel": plantel,
                        "calificacion": calificacion,
                        "disciplina": disciplina
                    }
        except Exception:
            return None
        return None

    # 🛠️ Función auxiliar para recargar las opciones del Dropdown desde la BD
    def _cargar_opciones_disciplinas(self):
        self.dd_disciplina.options.clear()
        try:
            # Trae las disciplinas directamente usando el DAO asignado
            disciplinas = self.disciplinas_controller.disciplinas_dao.listar_todas()
            for id_disc, nombre_disc in disciplinas:
                # key es el valor interno (ID), text es lo que el usuario ve en pantalla
                self.dd_disciplina.options.append(
                    ft.dropdown.Option(key=str(id_disc), text=f"ID: {id_disc} — {nombre_disc}")
                )
        except Exception as e:
            self.mostrar_mensaje(f"No se pudieron cargar las disciplinas: {e}", es_error=True)

    def mostrar_formulario_agregar(self, e):
        self.ocultar_confirmacion(None)
        self.modo_edicion = False
        self.lbl_form_titulo.value = "Registrar Nuevo Alumno"
        self.txt_matricula.disabled = False
        
        # Recargar disciplinas para asegurar que aparezcan las más nuevas
        self._cargar_opciones_disciplinas()
        
        self.txt_nombre.value = ""
        self.txt_matricula.value = ""
        self.txt_nss.value = ""
        self.txt_plantel.value = ""
        self.txt_calificacion.value = ""
        self.dd_disciplina.value = None # Resetear selección
        
        self.form_container.visible = True
        self.update()

    def mostrar_formulario_editar(self, matricula: str):
        self.ocultar_confirmacion(None)
        alumno = self._buscar_alumno_por_matricula(matricula)
        if not alumno:
            self.mostrar_mensaje("No se encontraron los datos del alumno.", es_error=True)
            return
            
        self.modo_edicion = True
        self.matricula_seleccionada = matricula
        self.lbl_form_titulo.value = f"Modificar Alumno — Matrícula {matricula}"
        self.txt_matricula.disabled = True
        
        # Recargar disciplinas
        self._cargar_opciones_disciplinas()
        
        self.txt_nombre.value = alumno["nombre"]
        self.txt_matricula.value = alumno["matricula"]
        self.txt_nss.value = alumno["nss"]
        self.txt_plantel.value = alumno["plantel"]
        self.txt_calificacion.value = str(alumno["calificacion"])
        
        # Seleccionar automáticamente el ID correspondiente en el combo desplegable
        id_disc_alumno = alumno["disciplina"]
        self.dd_disciplina.value = str(id_disc_alumno) if id_disc_alumno is not None else None
        
        self.form_container.visible = True
        self.update()

    def ocultar_formulario(self, e=None):
        self.form_container.visible = False
        self.update()

    def guardar_formulario(self, e):
        try:
            # Capturamos el valor seleccionado del dropdown (será un string numérico o None)
            id_disciplina_seleccionado = int(self.dd_disciplina.value) if self.dd_disciplina.value else None

            if self.modo_edicion:
                self.controller.modificar_alumno(
                    self.txt_nombre.value,
                    self.matricula_seleccionada,
                    self.txt_nss.value,
                    id_disciplina_seleccionado,
                    self.txt_plantel.value,
                    float(self.txt_calificacion.value) if self.txt_calificacion.value else 0.0
                )
            else:
                self.controller.registrar_alumno(
                    self.txt_nombre.value,
                    self.txt_matricula.value,
                    self.txt_nss.value,
                    id_disciplina_seleccionado,
                    self.txt_plantel.value,
                    float(self.txt_calificacion.value) if self.txt_calificacion.value else 0.0
                )
            self.ocultar_formulario()
            self.actualizar_lista_alumnos()
        except Exception as ex:
            self.mostrar_mensaje(str(ex), es_error=True)

    def mostrar_confirmacion_eliminar(self, matricula: str):
        self.ocultar_formulario(None)
        self.matricula_seleccionada = matricula
        self.lbl_confirm_texto.value = f"¿Estás completamente seguro de eliminar permanentemente al alumno con matrícula: {matricula}?"
        self.confirm_container.visible = True
        self.update()

    def ocultar_confirmacion(self, e=None):
        self.confirm_container.visible = False
        self.update()

    def ejecutar_eliminacion(self, e):
        try:
            self.controller.eliminar_alumno(self.matricula_seleccionada)
            self.ocultar_confirmacion()
            self.actualizar_lista_alumnos()
        except Exception as ex:
            self.mostrar_mensaje(str(ex), es_error=True)