from app import db

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    last_message_time = db.Column(db.DateTime, default=db.func.now())

    # Relaties met student en technieker
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=True)

    # Relaties definiëren
    student = db.relationship('Student', backref='conversations_as_student')
    technician = db.relationship('Technician', backref='conversations_as_technician')

    # Berichten in de conversatie
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True)
