from app import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)

    # Relaties
    listings = db.relationship('Listing', back_populates='student')
    conversations = db.relationship('Conversation', back_populates='student', lazy=True)
    transactions = db.relationship('Transaction', back_populates='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.username}>"
