from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)  # Verwijzing naar Student
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    technician_username = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaties
    technician = db.relationship('Technician', back_populates='transactions')
    listing = db.relationship('Listing', back_populates='transactions', lazy=True)
    student = db.relationship('Student', back_populates='transactions')  # Backref naar Student

    def __repr__(self):
        return f"<Transaction {self.id} | Listing {self.listing_id} | Status {self.status}>"
