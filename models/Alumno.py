class Alumno:
    def __init__(self, nombre, matricula, nss, calificacion, plantel, disciplina):
        self.nombre = nombre
        self.matricula = matricula
        self.nss = nss
        self.calificacion = calificacion
        self.plantel = plantel
        self.disciplina = disciplina
    #logica del negocio,verificamos que este dentro del reango permitido
        if self.calificacion < 5 or self.calificacion > 10:
            raise ValueError("La calificación debe estar entre 5 y 10")
        else: 
            self.calificacion = calificacion

        self.disciplina = disciplina
#devuelve una representacion legible del objeto Alumno,mosttrando sus atributos principales
    def mostrar_informacion(self):
        return f"Nombre: {self.nombre}, Disciplina: {self.disciplina}, Calificación: {self.calificacion}"