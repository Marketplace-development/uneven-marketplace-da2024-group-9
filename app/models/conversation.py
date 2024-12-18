from app import db
class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    last_message_time = db.Column(db.DateTime, default=db.func.now())

    student = db.relationship('Student', back_populates='conversations')
    technician = db.relationship('Technician', back_populates='conversations')
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True)

    def __repr__(self):
        return f"<Conversation {self.id}>"
