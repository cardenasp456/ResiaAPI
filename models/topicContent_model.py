from database import db

class TopicContent(db.Model):
    __tablename__ = 'topic_content'
    
    content_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    content_text = db.Column(db.Text)

    topic = db.relationship('Topic', backref=db.backref('contents', lazy=True))
