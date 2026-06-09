import sqlite3

class AlumnosDAO:
    def __init__(self, db_name="concurso_dgti.db"):
        self.db_name = db_name

    def insertar(self, alumno_objeto):
        """Recibe un objeto de la clase Alumno y lo guarda en la base de datos."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute('''
                    INSERT INTO alumnos (nombre, matricula, nss, plantel, calificacion, id_disciplina)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    alumno_objeto.nombre,
                    alumno_objeto.matricula,
                    alumno_objeto.nss,
                    alumno_objeto.plantel,
                    alumno_objeto.calificacion,
                    alumno_objeto.disciplina
                ))
                conexion.commit()
            except sqlite3.IntegrityError as e:
                raise ValueError("La matrícula ya existe") from e

    def modificar(self, alumno_objeto):
        """Recibe un objeto Alumno con datos actualizados y actualiza su fila."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                UPDATE alumnos
                SET nombre = ?, nss = ?, plantel = ?, calificacion = ?, id_disciplina = ?
                WHERE matricula = ?
            ''', (
                alumno_objeto.nombre,
                alumno_objeto.nss,
                alumno_objeto.plantel,
                alumno_objeto.calificacion,
                alumno_objeto.disciplina,
                alumno_objeto.matricula
            ))
            conexion.commit()

    def eliminar(self, matricula):
        """Elimina un alumno usando su matrícula como identificador único."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM alumnos WHERE matricula = ?', (matricula,))
            conexion.commit()

    def listar_todos(self):
        """Devuelve una lista de todos los alumnos registrados en la base de datos."""
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT nombre, matricula, nss, plantel, calificacion, id_disciplina FROM alumnos')
            return cursor.fetchall()