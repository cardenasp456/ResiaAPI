from database import db  # Importar la instancia de la base de datos

class SurveySummary(db.Model):
    __tablename__ = 'SurveySummary'
    
    summary_id = db.Column(db.Integer, primary_key=True)  # Columna autoincrementable
    class_name = db.Column(db.String(50), name='class')  # Nombre de la clase
    most_interesting_topics = db.Column(db.Text)  # Almacenar los temas más interesantes en formato JSON (como texto)
    least_interesting_topics = db.Column(db.Text)  # Almacenar los temas menos interesantes en formato JSON (como texto)
    average_difficulty = db.Column(db.String(50))  # Dificultad promedio
    average_enjoyment = db.Column(db.String(50))  # Disfrute promedio
    average_engagement = db.Column(db.String(50))  # Participación promedio

    def to_dict(self):
        """
        Método para convertir el objeto del modelo a un diccionario.
        """
        return {
            'summary_id': self.summary_id,
            'class_name': self.class_name,
            'most_interesting_topics': self.most_interesting_topics,
            'least_interesting_topics': self.least_interesting_topics,
            'average_difficulty': self.average_difficulty,
            'average_enjoyment': self.average_enjoyment,
            'average_engagement': self.average_engagement
        }