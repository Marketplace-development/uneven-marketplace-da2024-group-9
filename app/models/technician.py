from app import db
class Technician(db.Model):
    __tablename__ = 'technicians'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)

    # Relaties
    transactions = db.relationship('Transaction', back_populates='technician', lazy=True)
    conversations = db.relationship('Conversation', back_populates='technician', lazy=True)

