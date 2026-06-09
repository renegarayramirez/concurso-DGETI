class Disciplina:
    def __init__(self, id_disciplina, disciplina):
        self.id_disciplina = id_disciplina
        self.disciplina = disciplina

    def __str__(self):
        return f"{self.id_disciplina} - {self.disciplina}"