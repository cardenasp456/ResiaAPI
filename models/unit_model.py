from database import db


class Unit(db.Model):
    __tablename__ = 'units'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    unit_name = db.Column(db.String(255))

    course = db.relationship('Course', backref=db.backref('units', lazy=True))
