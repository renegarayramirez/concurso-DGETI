import sqlite3

def crear_tablas():
    with sqlite3.connect("concurso_dgti.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            create table if not exists disciplinas (
                id_disciplina integer primary key autoincrement,
                disciplina text not null
            )
        ''')
        cursor.execute('''
            create table if not exists alumnos (
                idAlumnos integer primary key autoincrement,
                nombre text not null,
                matricula text not null,
                nss text not null,
                calificacion real not null,
                plantel text not null,
                id_disciplina integer,
                foreign key (id_disciplina) references disciplinas(id_disciplina)
            )
        ''')
        conexion.commit()     