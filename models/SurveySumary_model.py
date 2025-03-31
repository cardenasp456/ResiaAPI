from database import db  # Importar la instancia de la base de datos

class SurveySummary(db.Model):
    __tablename__ = 'SurveySummary'
    
    summary_id = db.Column(db.Integer, primary_key=True)  # Columna autoincrementable
    subject = db.Column(db.String(100))  # Materia
    answers = db.Column(db.Text)  # Respuestas en formato JSON (almacenadas como texto)

    def to_dict(self):
        """
        Método para convertir el objeto del modelo a un diccionario.
        """
        return {
            'summary_id': self.summary_id,
            'subject': self.subject,
            'answers': self.answers
        }