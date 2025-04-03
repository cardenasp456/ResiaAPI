from database import db

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    history_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "history_id": self.history_id,
            "chat_id": self.chat_id,
            "saved_at": self.saved_at.strftime("%Y-%m-%d %H:%M:%S")
        }