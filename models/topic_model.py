from database import db

class Topic(db.Model):
    __tablename__ = 'topics'
    
    topic_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))
    topic_name = db.Column(db.String(255))

    unit = db.relationship('Unit', backref=db.backref('topics', lazy=True))

