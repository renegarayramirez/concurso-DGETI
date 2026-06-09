from models.Alumnos_dao import AlumnosDAO
from models.Alumno import Alumno

class AlumnosController:
    def __init__(self, vista):
        self.vista = vista
        self.alumnos_dao = AlumnosDAO()

    def registrar_alumno(self, nombre, matricula, nss, disciplina, plantel, calificacion):
        if not nombre or not matricula or not nss or not plantel:
            self.vista.mostrar_mensaje("Error: Todos los campos son obligatorios.", es_error=True)
            return
        alumno_objeto = Alumno(
            nombre=nombre.strip(),
            matricula=matricula.strip(),
            nss=nss.strip(),
            plantel=plantel.strip(),
            calificacion=calificacion,
            disciplina=disciplina
        )
        try:
            self.alumnos_dao.insertar(alumno_objeto)
            self.vista.mostrar_mensaje(f"¡Alumno '{nombre}' registrado exitosamente!")
            self.vista.limpiar_formulario()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al guardar en la base de datos: {str(e)}", es_error=True)

    def modificar_alumno(self, nombre, matricula, nss, disciplina, plantel, calificacion):
        if not nombre or not matricula or not nss or not plantel:
            self.vista.mostrar_mensaje("Error: Todos los campos son obligatorios.", es_error=True)
            return
        alumno_objeto = Alumno(
            nombre=nombre.strip(),
            matricula=matricula.strip(),
            nss=nss.strip(),
            plantel=plantel.strip(),
            calificacion=calificacion,
            disciplina=disciplina
        )
        try:
            self.alumnos_dao.modificar(alumno_objeto)
            self.vista.mostrar_mensaje(f"¡Alumno '{nombre}' modificado exitosamente!")
            self.vista.limpiar_formulario()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al modificar en la base de datos: {str(e)}", es_error=True)

    def eliminar_alumno(self, matricula):
        if not matricula:
            self.vista.mostrar_mensaje("Error: La matrícula es obligatoria para eliminar.", es_error=True)
            return
        try:
            self.alumnos_dao.eliminar(matricula.strip())
            self.vista.mostrar_mensaje(f"¡Alumno con matrícula '{matricula}' eliminado exitosamente!")
            self.vista.limpiar_formulario()
        except Exception as e:
            self.vista.mostrar_mensaje(f"Error al eliminar en la base de datos: {str(e)}", es_error=True)  