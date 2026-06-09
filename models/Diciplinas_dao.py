import sqlite3

class DisciplinasDAO:
    def __init__(self, db_name="concurso_dgti.db"):
        self.db_name = db_name

    def insertar_disciplina(self, disciplina):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO disciplinas (disciplina) VALUES (?)", (disciplina,))
            conexion.commit()
        
    def eliminar_disciplina(self, id_disciplina):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM disciplinas WHERE id_disciplina = ?", (id_disciplina,))
            conexion.commit()
    
    def modificar_disciplina(self, id_disciplina, nuevo_nombre):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            # usamos el id para saber exactamente cual fila actualizar
            cursor.execute("UPDATE disciplinas SET disciplina = ? WHERE id_disciplina = ?", (nuevo_nombre, id_disciplina))
            conexion.commit()  

    def listar_todas(self):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_disciplina, disciplina FROM disciplinas")
            return cursor.fetchall()