from database import db 

class Course(db.Model):
    __tablename__ = 'courses'
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255))
    grade_level = db.Column(db.String(50))
