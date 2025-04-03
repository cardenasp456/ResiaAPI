from database import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    message_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "sender": self.sender,
            "message_text": self.message_text,
            "sent_at": self.sent_at.strftime("%Y-%m-%d %H:%M:%S")
        }