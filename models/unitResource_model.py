from database import db


class UnitResource(db.Model):
    __tablename__ = 'unit_resources'
    
    resource_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))
    resource_name = db.Column(db.String(255))

    unit = db.relationship('Unit', backref=db.backref('resources', lazy=True))

