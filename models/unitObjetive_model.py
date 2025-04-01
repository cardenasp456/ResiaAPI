from database import db

class UnitObjective(db.Model):
    __tablename__ = 'unit_objectives'
    
    objective_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))
    objective_text = db.Column(db.Text)

    unit = db.relationship('Unit', backref=db.backref('objectives', lazy=True))

