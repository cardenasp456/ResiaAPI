from database import db  # Importar la instancia de la base de datos

class Survey(db.Model):
    __tablename__ = 'Surveys'
    survey_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), name='class')
    difficulty = db.Column(db.String(50))
    enjoyment = db.Column(db.String(50))
    engagement = db.Column(db.String(50))
    topics_of_interest = db.Column(db.Text)  # Usamos Text para almacenar JSON
    comments = db.Column(db.Text)

    def to_dict(self):
        return {
            'survey_id': self.survey_id,
            'class_name': self.class_name,
            'difficulty': self.difficulty,
            'enjoyment': self.enjoyment,
            'engagement': self.engagement,
            'topics_of_interest': self.topics_of_interest,
            'comments': self.comments
        }