# controller/disciplinas_controller.py
from models.Diciplinas_dao import DisciplinasDAO

class DisciplinasController:
    def __init__(self, vista):
        # Guardamos una referencia a la vista para poder enviarle respuestas
        self.vista = vista
        # Creamos una instancia de nuestro DAO para poder comunicarnos con la base de datos
        self.disciplinas_dao = DisciplinasDAO()

    def registrar_disciplina(self, nombre):
        """Lógica del negocio y control para dar de alta una nueva disciplina"""
        # 🛠️ Corregido: Validamos si está vacío correctamente
        if not nombre or nombre.strip() == "":
            self.vista.mostrar_mensaje("Error: El nombre de la disciplina no puede estar vacío.", es_error=True)
            return
        try:
            # Si todo está bien, llamamos al modelo para insertar
            self.disciplinas_dao.insertar_disciplina(nombre.strip())
            self.vista.mostrar_mensaje(f"¡Disciplina '{nombre}' registrada exitosamente!")
            self.vista.limpiar_formulario()  # Le pedimos que limpie su caja de texto
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al guardar en la base de datos: {str(e)}", es_error=True)

    def modificar_disciplina(self, id_disciplina, nuevo_nombre):
        """Lógica del negocio y control para modificar una disciplina existente"""
        # 🛠️ Corregido: Validamos si está vacío correctamente
        if not nuevo_nombre or nuevo_nombre.strip() == "":
            self.vista.mostrar_mensaje("Error: El nombre de la disciplina no puede estar vacío.", es_error=True)
            return
        try:
            self.disciplinas_dao.modificar_disciplina(id_disciplina, nuevo_nombre.strip())
            self.vista.mostrar_mensaje(f"¡Disciplina con ID '{id_disciplina}' modificada exitosamente!")
            self.vista.limpiar_formulario()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al modificar en la base de datos: {str(e)}", es_error=True)

    def eliminar_disciplina(self, id_disciplina):
        """Lógica del negocio y control para eliminar una disciplina existente"""
        if not id_disciplina:
            self.vista.mostrar_mensaje("Error: El ID de la disciplina es obligatorio para eliminar.", es_error=True)
            return
        try:
            self.disciplinas_dao.eliminar_disciplina(id_disciplina)
            self.vista.mostrar_mensaje(f"¡Disciplina con ID '{id_disciplina}' eliminada exitosamente!")
            self.vista.limpiar_formulario()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al eliminar en la base de datos: {str(e)}", es_error=True)