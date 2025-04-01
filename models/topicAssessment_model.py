from database import db


class TopicAssessment(db.Model):
    __tablename__ = 'topic_assessments'
    
    assessment_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    assessment_method = db.Column(db.String(255))

    topic = db.relationship('Topic', backref=db.backref('assessments', lazy=True))
