from app import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_username = db.Column(db.String(50), nullable=False)
    receiver_username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ChatMessage {self.sender_username} -> {self.receiver_username}: {self.message}>"
