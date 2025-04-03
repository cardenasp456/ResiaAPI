from database import db

class Chat(db.Model):
    __tablename__ = 'chats'

    chat_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con los mensajes (usando el nombre de la clase como cadena)
    messages = db.relationship('ChatMessage', backref='chat', cascade='all, delete-orphan')

    # Relación con el historial (usando el nombre de la clase como cadena)
    history = db.relationship('ChatHistory', backref='chat', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "title": self.title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }