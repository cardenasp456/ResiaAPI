from database import db  # Importar la instancia de la base de datos

class Survey(db.Model):
    __tablename__ = 'Surveys'
     
    summary_id = db.Column(db.Integer, primary_key=True)  # Columna autoincrementable
    student_name = db.Column(db.String(100))  # Nombre del estudiante
    subject = db.Column(db.String(100))  # Materia
    answers = db.Column(db.Text)  # Respuestas en formato JSON (almacenadas como texto)

    def to_dict(self):
        """
        Método para convertir el objeto del modelo a un diccionario.
        """
        return {
            'summary_id': self.summary_id,
            'student_name': self.student_name,
            'subject': self.subject,
            'answers': self.answers
        }