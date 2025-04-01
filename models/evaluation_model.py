from database import db

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    
    evaluation_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    exams = db.Column(db.String(50))
    projects = db.Column(db.String(50))
    classwork = db.Column(db.String(50))
    participation = db.Column(db.String(50))

    course = db.relationship('Course', backref=db.backref('evaluations', lazy=True))